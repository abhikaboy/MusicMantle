from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from contextlib import asynccontextmanager
from pymongo import MongoClient
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from pymongo.errors import DuplicateKeyError
from pymongo.operations import SearchIndexModel 

config = dotenv_values(".env")
load_dotenv()

KEY="" # Removed for security reasons
client = OpenAI(api_key=KEY)

# headers in the csv file are  as follows: 
# mbid,artist_mb,artist_lastfm,country_mb,country_lastfm,tags_mb,tags_lastfm,listeners_lastfm,scrobbles_lastfm,ambiguous_artist

NAME_INDEX = 1
COUNTRY_INDEX = 3
TAGS = 6
LISTENERS_INDEX = 7
AMBIGUOUS = 9

# This function is used to get the embeddings of the text
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

# Given a text and a secret, this function will tell us how similar the text is to the secret
def vectorQuery(text, secret, collection):
    # define pipeline
    pipeline = [
    {
        '$vectorSearch': {
        'index': 'vector_index', 
        'filter': {
            'name': {
                '$eq': secret
            }
        },
        'path': 'embedding', 
        'queryVector': get_embedding(text),
        'numCandidates': 150, 
        'limit': 10
        } 
    }, {
        '$project': {
        '_id': 0, 
        'name': 1,
        'score': {
                '$meta': 'vectorSearchScore'
            }
        }
    }
    ]
    print("Querying the database for term: " + text)
    return collection.aggregate(pipeline)

# This function is used to read the artists from the csv file
def readArtists():
    with open('artists.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        artists = [row for row in csv_reader]
        artists_slice = artists[1:1000]
        full_artist_list = []
        for row in artists_slice:
            # Filter out Artists that are ambiguous meaning that they have multiple entries
            artist_dict = {}
            if row[AMBIGUOUS] == "FALSE":
                artist_dict['name'] = row[NAME_INDEX]
                # Allow for the country to be in the prompt so that the model can be more accurate
                artist_dict['country'] = row[COUNTRY_INDEX]
                # Using tags from lastfm which have a higher coverage within the dataset
                artist_dict['tags'] = row[TAGS]
                # Utilize the listeners from lastfm to get a better estimate of the popularity of the artist
                artist_dict['listener_count'] = row[LISTENERS_INDEX]
                full_artist_list.append(artist_dict)

# This will take the artist dictionary and insert it into the database
def insertEmbedding(artist_dict, collection):
    prompt = f"The artist is {artist_dict['name']} from {artist_dict['country']} with {artist_dict['tags']} and {artist_dict['listener_count']} listeners"
    embedding = get_embedding(prompt)
    artist_dict['embedding'] = embedding
    artist_dict['prompt'] = prompt
    collection.insert_one(artist_dict)
    print(f"Prompt: {prompt}")
    print(f"Inserted embedding for {artist_dict['name']}") 
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.artists_collection = app.database["artists"]
    print("Connected to the MongoDB database!")

    # for artist in full_artist_list:
    #     insertEmbedding(artist, collection=app.artists_collection)
    #     print(f"Inserted {count} artists")
    #     count += 1
 
    print(f"Lifespan Startup Complete")
    yield

    print("Shutting down")
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, replace with specific methods if needed
    allow_headers=["*"],  # Allows all headers, replace with specific headers if needed
)
router = APIRouter()

@app.get("/")
async def root():
    return {"message": "Welcome to Music Mantle!"}

@app.get("/random", response_description="Create a new Artist in Database", status_code=status.HTTP_200_OK)
async def get_random_artist(request: Request):
    random_pick = request.app.artists_collection.aggregate([
        {
            '$sample': {
                'size': 1
            }
        }
    ])
    for artist in random_pick:
        return {
            "name": artist['name'],
            "prompt": artist['prompt']
        }

@app.get("/check", response_description="Given a query, return the artists that match the query", status_code=status.HTTP_200_OK)
async def query_artists(term, secret, request: Request):
    print("Secret is: " + secret)
    return list(vectorQuery(term, secret, request.app.artists_collection))