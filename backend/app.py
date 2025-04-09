from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommender import SHLRecommender


class RecommendRequest(BaseModel):
    query: str


app = FastAPI()
recommender = SHLRecommender()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(request: RecommendRequest):
    results = recommender.recommend(request.query)
    return {"results": results}