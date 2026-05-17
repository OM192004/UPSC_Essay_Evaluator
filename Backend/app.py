from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import process_essay

app = FastAPI(title="UPSC Essay Evaluator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EssayRequest(BaseModel):
    question: str
    text: str

class EvaluationResponse(BaseModel):
    ml_score: float
    llm_score: float
    final_score: float
    feedback: str
    breakdown: dict

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_essay(request: EssayRequest):
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Essay text is too short or empty.")
    
    try:
        # Run the evaluation pipeline
        result = await process_essay(request.text, request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
