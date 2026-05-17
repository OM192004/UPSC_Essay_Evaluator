from llm_evaluator import evaluate_with_llm
from model_handler import get_ml_score

async def process_essay(essay_text: str, question: str) -> dict:
    """
    Orchestrates the evaluation pipeline:
    Preprocessing -> ML Models -> Score Aggregation -> LLM Evaluation -> Score Fusion
    """
    # 1. Preprocessing (Can be added here or inside model_handler)
    processed_text = essay_text.strip()
    
    # 2. ML Models & Score Aggregation
    # Call the ML model integration file provided by the user
    ml_score_data = get_ml_score(processed_text)
    
    # Extract the score (assuming get_ml_score returns a dict with 'score' or similar)
    # We will adjust this once the exact output format of the user's model is known
    ml_score = ml_score_data.get("score", 0.0)
    
    # 3. LLM Evaluation
    llm_evaluation = await evaluate_with_llm(processed_text, question)
    llm_score = llm_evaluation.get("score", 0.0)
    feedback = llm_evaluation.get("feedback", "No feedback available.")
    
    # 4. Score Fusion (Simple average for now, can be weighted)
    final_score = (ml_score * 0.1) + (llm_score * 0.9) # Giving slightly more weight to ML model
    
    return {
        "ml_score": round(ml_score, 2),
        "llm_score": round(llm_score, 2),
        "final_score": round(final_score, 2),
        "feedback": feedback,
        "breakdown": {
            "ml_components": ml_score_data,
            "llm_components": llm_evaluation.get("breakdown", {})
        }
    }
