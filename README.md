
# SHL Assessment Recommender

A semantic search system that helps HR professionals find the right SHL assessments based on job descriptions.

This tool helps you find the perfect SHL assessment for your hiring needs. Just paste a job description or type in what skills you're looking for, and it'll recommend the most relevant SHL assessments from their catalog.

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

### Run the web app

```bash
# Start the backend API
cd backend
uvicorn app:app --reload

# In a new terminal, start the frontend
cd frontend
streamlit run app.py
```

## License

MIT
