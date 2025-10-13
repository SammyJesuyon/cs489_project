# 🦷 ADS Dental Surgeries REST Web API (FastAPI)

Implements Lab 7 using Python, FastAPI, and SQLAlchemy ORM.

## 🚀 Setup & Run

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize and seed the database
python -m app.db.bootstrap

# 4. Run the FastAPI server
uvicorn app.main:app --reload