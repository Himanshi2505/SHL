import json
from sentence_transformers import SentenceTransformer, util

class SHLRecommender:
    def __init__(self, data_path="shl_assessments.json"):
        # Define the test type mapping
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
        
        # Load the data
        with open(data_path, "r") as f:
            self.data = json.load(f)
        
        # Initialize the model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Preprocess the corpus with expanded test type descriptions
        self.corpus = []
        for item in self.data:
            # Convert test_type from alphabet codes to full descriptions
            test_types = item['test_type'].strip().split('\n')
            expanded_test_types = [self.test_type_mapping.get(t, t) for t in test_types]
            
            # Create a rich description for embedding
            description = f"{item['name']} - {', '.join(expanded_test_types)}"
            self.corpus.append(description)
        
        # Generate embeddings for the corpus
        self.corpus_embeddings = self.model.encode(self.corpus, convert_to_tensor=True)
    
    def get_expanded_test_types(self, test_type_str):
        """Convert test type codes to their full descriptions"""
        test_types = test_type_str.strip().split('\n')
        return [self.test_type_mapping.get(t, t) for t in test_types]
    
    def recommend(self, query, top_k=10):
        # Generate embedding for the query
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Find similar items
        hits = util.semantic_search(query_embedding, self.corpus_embeddings, top_k=top_k)[0]
        
        results = []
        for hit in hits:
            item = self.data[hit['corpus_id']]
            # Include expanded test types in the result
            expanded_item = item.copy()
            expanded_item['test_type_expanded'] = self.get_expanded_test_types(item['test_type'])
            expanded_item['similarity_score'] = hit['score']
            results.append(expanded_item)
            
        return results
    
    def display_recommendations(self, recommendations):
        """Format and display recommendations nicely"""
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['name']} (Score: {rec['similarity_score']:.4f})")
            print(f"   URL: {rec['url']}")
            print(f"   Remote Testing: {rec['remote_testing_support']}")
            print(f"   Adaptive IRT: {rec['adaptive_irt_support']}")
            print(f"   Duration: {rec['duration']}")
            print(f"   Test Types: {', '.join(rec['test_type_expanded'])}")


# Example usage:
if __name__ == "__main__":
    recommender = SHLRecommender()
    
    # Example query
    query = "I need aptitude tests for bank administrators"
    recommendations = recommender.recommend(query, top_k=5)
    
    # Display results
    recommender.display_recommendations(recommendations)