from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from neo4j import GraphDatabase
from routes import router as book_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.neo4j_driver = GraphDatabase.driver(config["NEO4J_URI"], auth=(config["NEO4J_USER"], config["NEO4J_PASSWORD"]))

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()

app.include_router(book_router, tags=["movies"], prefix="/movie")