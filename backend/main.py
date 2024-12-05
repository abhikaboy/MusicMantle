from fastapi import FastAPI
import csv
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from contextlib import asynccontextmanager
from pymongo import MongoClient
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

config = dotenv_values(".env")
load_dotenv()

KEY=""
client = OpenAI(api_key=KEY)

# headers in the csv file are  as follows: 
# mbid,artist_mb,artist_lastfm,country_mb,country_lastfm,tags_mb,tags_lastfm,listeners_lastfm,scrobbles_lastfm,ambiguous_artist

NAME_INDEX = 1
COUNTRY_INDEX = 3
TAGS = 6
LISTENERS_INDEX = 7
AMBIGUOUS = 9

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding


with open('artists.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    artists = [row for row in csv_reader]
    artists_slice = artists[1:1000]
    full_artist_list = []
    for row in artists_slice:
        # form a dictionary
        artist_dict = {}
        if row[AMBIGUOUS] == "FALSE":
            artist_dict['name'] = row[NAME_INDEX]
            artist_dict['country'] = row[COUNTRY_INDEX]
            artist_dict['tags'] = row[TAGS]
            artist_dict['listener_count'] = row[LISTENERS_INDEX]
            full_artist_list.append(artist_dict)


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
    count = 0
    # for artist in full_artist_list:
    #     insertEmbedding(artist, collection=app.artists_collection)
    #     print(f"Inserted {count} artists")
    #     count += 1
 
    print(f"Lifespan Startup Complete")
    yield

    print("Shutting down")
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)
router = APIRouter()

@app.get("/")
async def root():
    return {"message": "Welcome to the PyMongo tutorial!"}

# @app.post("/", response_description="Create a new Artist in Database", status_code=status.HTTP_201_CREATED)
# async def get_artists(request: Request, artists: List[dict] = Body(...)):
#     insertEmbedding(jsonable_encoder(full_artist_list[0]), collection=request.app.artists_collection)
#     return {"message": "Hello World"}


