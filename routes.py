from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Dict
from dotenv import dotenv_values

from models import Movie, MovieUpdate

config = dotenv_values(".env")

router = APIRouter()

@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    try:
        # Assuming the collection name is 'movies'
        movies = list(request.app.database["movies"].find().limit(100))
        return movies
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/specific", response_model=List[Movie])
async def list_specific_movie(request: Request, title: Optional[str] = None, actor: Optional[str] = None):
    query = {}
    if title:
        query["title"] = title
    if actor:
        query["cast"] = actor

    if not query:
        raise HTTPException(status_code=400, detail="Either title or actor must be provided")

    movies = list(request.app.database["movies"].find(query)) 
    return movies

@router.put("/{title}", response_description="Update a movie")
async def update_movie(request: Request, title: str, movie_update: MovieUpdate):
    update_result = request.app.database["movies"].update_one({"title": title}, {"$set": movie_update.dict(exclude_unset=True)})

    if update_result.matched_count == 0:
        print(f"Movie with title '{title}' not found")
        raise HTTPException(status_code=404, detail=f"Movie with title '{title}' not found")

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No update performed. Perhaps the new data is the same as existing data.")

    return {"message": "Movie updated successfully"}


@router.get("/common", response_description="get the movies in common between MongoDB and Neo4J databases", response_model=int)
async def get_common_movies(request: Request):
    with request.app.neo4j_driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m.title")
        neo4j_movies = [record["m.title"] for record in result]
    mongo_movies = list(request.app.database["movies"].find({}, {"title": 1, "_id": 0}))
    mongo_movies = [movie["title"] for movie in mongo_movies]
    common_movies = set(neo4j_movies).intersection(set(mongo_movies))
    return len(common_movies)


@router.get("/{movie_name}/rated-users", response_model=List[str])
async def list_users_who_rated_movie(request: Request, movie_name: str):
    query = """
    MATCH (p:Person)-[:REVIEWED]->(m:Movie {title: $movie_name})
    RETURN p.name AS personName
    """
    try:
        with request.app.neo4j_driver.session() as session:
            result = session.run(query, parameters={"movie_name": movie_name})
            names = [record["personName"] for record in result]
            return names
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{user_name}/ratings", response_model=Dict[str, object])
async def list_user_ratings(request: Request, user_name: str):
    query = """
    MATCH (p:Person {name: $user_name})-[t:REVIEWED]->(m:Movie) RETURN m
    """
    try:
        with request.app.neo4j_driver.session() as session:
            result = session.run(query, parameters={"user_name": user_name})
            movies = [record["m"] for record in result]
            return {"user": user_name, "movies_rated": len(movies), "rated_movies": movies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))