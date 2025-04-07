# SHL Assessment Recommender

A semantic search system that helps HR professionals find the right SHL assessments based on job descriptions.

![SHL Assessment Recommender](https://github.com/yourusername/shl-assessment-recommender/raw/main/docs/images/shl-demo-screenshot.png)

This tool helps you find the perfect SHL assessment for your hiring needs. Just paste a job description or type in what skills you're looking for, and it'll recommend the most relevant SHL assessments from their catalog.

## Features

- **Semantic Search**: Understands the meaning behind your job requirements, not just keywords
- **NLP-Powered**: Uses advanced language models to understand job requirements
- **Fast & Simple**: Get recommendations in seconds with an easy-to-use interface
- **Direct Links**: Jump straight to SHL's product pages for the recommended assessments

## Demo

When you search for "Java developers who can collaborate effectively with business teams," the system identifies relevant assessments that match both technical skills and collaboration abilities:

![Working Demo](https://github.com/yourusername/shl-assessment-recommender/raw/main/docs/images/shl-java-search-results.png)

As shown above, the system recommends assessments like "Apprentice 8.0 Job Focused Assessment" that evaluate both technical competency and behavioral traits - perfect for Java developer roles requiring collaboration skills.


## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/shl-assessment-recommender.git
cd shl-assessment-recommender

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Run the web app

```bash
# Start the backend API
cd backend
uvicorn app:app --reload

# In a new terminal, start the frontend
cd frontend
streamlit run app.py
```

Then open your browser to http://localhost:8501

### Option 2: Use the API directly

```python
import requests

query = "We need a customer service representative with strong problem-solving skills"
response = requests.get("http://localhost:8000/api/recommend", params={"query": query})
recommendations = response.json()["results"]

for rec in recommendations:
    print(f"{rec['name']} - Score: {rec['similarity_score']}")
```

## License

MIT

## Acknowledgements

- Built with [Sentence Transformers](https://www.sbert.net/)
- UI powered by [Streamlit](https://streamlit.io/)
- API built with [FastAPI](https://fastapi.tiangolo.com/)
