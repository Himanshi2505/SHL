from dotenv import load_dotenv
import os
import json
import numpy as np
from tqdm import tqdm
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class SHLRecommender:
    def __init__(self, data_path="shl_assessments.json", model="models/embedding-001"):
        self.test_type_mapping = {
            'A': 'Ability & Aptitude',
            'B': 'Behavior & Situational Judgement',
            'C': 'Competencies',
            'D': 'Development & 360',
            'E': 'Assessment Exercises',
            'K': 'Knowledge & Skills',
            'P': 'Personality & Behavior',
            'S': 'Simulations'
        }

        self.model = model

        with open(data_path, "r") as f:
            self.data = json.load(f)

        self.corpus = []
        for item in self.data:
            test_types = item['test_type'].strip().split('\n')
            expanded_test_types = [self.test_type_mapping.get(t, t) for t in test_types]
            description = f"{item['name']} - {', '.join(expanded_test_types)}"
            self.corpus.append(description)

        self.corpus_embeddings = self.compute_embeddings(self.corpus)

    def compute_embeddings(self, texts):
        embeddings = []
        for text in tqdm(texts, desc="Embedding corpus"):
            try:
                response = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(response['embedding'])
            except Exception as e:
                print(f"Error embedding '{text[:30]}...': {e}")
                embeddings.append(np.zeros(768))  # or 512 depending on model
        return np.array(embeddings)

    def get_embedding(self, text):
        try:
            response = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_query"
            )
            return np.array(response['embedding'])
        except Exception as e:
            print(f"Error getting query embedding: {e}")
            return np.zeros(768)

    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def get_expanded_test_types(self, test_type_str):
        test_types = test_type_str.strip().split('\n')
        return [self.test_type_mapping.get(t, t) for t in test_types]

    def recommend(self, query, top_k=10):
        query_embedding = self.get_embedding(query)
        scores = [self.cosine_similarity(query_embedding, emb) for emb in self.corpus_embeddings]
        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            item = self.data[idx]
            expanded_item = item.copy()
            expanded_item['test_type_expanded'] = self.get_expanded_test_types(item['test_type'])
            expanded_item['similarity_score'] = float(scores[idx])
            results.append(expanded_item)

        return results

    def display_recommendations(self, recommendations):
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['name']} (Score: {rec['similarity_score']:.4f})")
            print(f"   URL: {rec['url']}")
            print(f"   Remote Testing: {rec['remote_testing_support']}")
            print(f"   Adaptive IRT: {rec['adaptive_irt_support']}")
            print(f"   Duration: {rec['duration']}")
            print(f"   Test Types: {', '.join(rec['test_type_expanded'])}")


if __name__ == "__main__":
    recommender = SHLRecommender()
    query = "I need aptitude tests for bank administrators"
    recommendations = recommender.recommend(query, top_k=5)
    recommender.display_recommendations(recommendations)
