
# This is used to create the vector index on the database
# Create your index model, then create the search index
search_index_model = SearchIndexModel(
definition={
    "fields": [
    {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 1536,
        "similarity": "euclidean"
    },
    {
        "type": "filter",
        "path": "name",
    }
    ]
},

name="vector_index",
type="vectorSearch",
)
result = app.artists_collection.create_search_index(model=search_index_model)
print("New search index named " + result + " is building.")
# Wait for initial sync to complete
print("Polling to check if the index is ready. This may take up to a minute.")
predicate=None
if predicate is None:
    predicate = lambda index: index.get("queryable") is True