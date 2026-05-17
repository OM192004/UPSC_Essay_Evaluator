import os
from openai import AsyncOpenAI
import json
from dotenv import load_dotenv

load_dotenv()

# The API key you provided starts with 'gsk_', which means it is a Groq API key!
# We will use the Groq OpenAI-compatible endpoint.
client = AsyncOpenAI(
    api_key=os.environ.get("GROK_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

async def evaluate_with_llm(essay_text: str, question: str) -> dict:
    """
    Evaluates the essay using Grok AI.
    Returns a dictionary with score, feedback, and breakdown.
    """
    prompt = f"""
    You are an expert UPSC (Union Public Service Commission) essay evaluator.
    Please evaluate the following essay based on UPSC standards:
    - Relevance to the topic (Question: {question})
    - Structure and Flow
    - Depth of knowledge and analysis
    - Vocabulary and Grammar

    Provide a final score out of 100, and a brief feedback summary.
    Return ONLY a JSON object with this exact structure:
    {{
        "score": <number between 0 and 100>,
        "feedback": "<your qualitative feedback>",
        "breakdown": {{
            "relevance": <score out of 25>,
            "structure": <score out of 25>,
            "depth": <score out of 25>,
            "language": <score out of 25>
        }}
    }}

    Question:
    {question}

    Essay:
    {essay_text}
    """

    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant", # Updated Groq model
            messages=[
                {"role": "system", "content": "You are a helpful UPSC evaluation assistant. You only output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Penalize score if relevance is below 8
        relevance_score = result.get("breakdown", {}).get("relevance", 25)
        if relevance_score < 8:
            result["score"] = min(result.get("score", 0) * 0.5, 30.0) # heavily penalize
            result["feedback"] = "The essay is largely off-topic. " + result.get("feedback", "")
            
        return result
        
    except Exception as e:
        print(f"Error calling Grok API: {e}")
        # Return fallback in case of API failure
        return {
            "score": 0.0,
            "feedback": "Failed to get evaluation from Grok AI.",
            "breakdown": {}
        }
