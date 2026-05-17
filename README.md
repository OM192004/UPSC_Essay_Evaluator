Developer Walkthrough: Running the UPSC Essay Evaluator
Welcome to the UPSC Essay Evaluator project! This guide will walk you through setting up and running the complete full-stack application (FastAPI backend + React frontend) on your local machine from scratch.

IMPORTANT

This project uses Git LFS (Large File Storage) to track the machine learning models (*.safetensors). Ensure you have Git LFS installed on your system before cloning the repository to avoid downloading pointer files instead of the actual models.

🛠 Prerequisites
Before you begin, ensure you have the following installed on your machine:

Python 3.8+ (for the FastAPI backend)
Node.js 18+ and npm (for the Vite/React frontend)
Git & Git LFS (git lfs install)
🚀 Step 1: Clone the Repository
Clone the repository and pull the large files (the DistilBert model):

bash
git clone https://github.com/OM192004/UPSC_Essay_Evaluator.git
cd UPSC_Essay_Evaluator
# Ensure you have the actual model files and not just pointers
git lfs pull
⚙️ Step 2: Set up the Backend (FastAPI)
The backend runs the machine learning pipeline and interacts with the Groq AI API for evaluation.

Navigate to the Backend directory:

bash
cd Backend
(Optional but Recommended) Create a Virtual Environment:

bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
Install Dependencies:

bash
pip install -r requirements.txt
Set up Environment Variables: The backend uses the Groq API. Set your API key as an environment variable (or let it fall back to the default one if applicable).

bash
# Windows (Command Prompt):
set GROK_API_KEY=your_api_key_here
# Mac/Linux:
export GROK_API_KEY="your_api_key_here"
Run the Backend Server:

bash
uvicorn app:app --reload
NOTE

The backend server should now be running at http://localhost:8000. You can test the API by visiting http://localhost:8000/docs to see the interactive Swagger UI.

🎨 Step 3: Set up the Frontend (React + Vite)
The frontend provides the UI for submitting essays and viewing detailed feedback.

Open a NEW terminal window (keep the backend running in the first one).

Navigate to the Frontend directory:

bash
cd Frontend
Install Dependencies:

bash
npm install
Run the Development Server:

bash
npm run dev
NOTE

The frontend should now be running (typically at http://localhost:5173/).

🎉 Step 4: Test the Application
Open your browser and navigate to the frontend URL (e.g., http://localhost:5173/).
Input a question/topic and paste a sample essay (must be at least 50 characters).
Click Evaluate Essay.
The application will route your essay to the FastAPI backend, where it will be processed by the local DistilBert ML model and the Groq LLM simultaneously, aggregating the result into a UPSC-style.
💡 Features to explore:
Theme Toggle: Use the ☀️/🌙 icon in the top right header to switch between Light and Dark mode.
