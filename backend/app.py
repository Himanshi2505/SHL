from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import SHLRecommender

app = FastAPI()
recommender = SHLRecommender()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/recommend")
def recommend(query: str = Query(..., description="Job description or natural language query")):
    results = recommender.recommend(query)
    return {"results": results}
