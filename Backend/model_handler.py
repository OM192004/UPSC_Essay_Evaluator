import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Get the absolute path to the model directory
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "model")

print(f"Loading ML model from {model_path}...")

try:
    # Load the tokenizer and the DistilBERT regression model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    
    # Set model to evaluation mode
    model.eval()
    
    # Use GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print("Model loaded successfully!")
    
except Exception as e:
    print(f"Failed to load the model: {e}")
    tokenizer = None
    model = None

def get_ml_score(essay_text: str) -> dict:
    """
    Runs the essay text through the DistilBERT regression model.
    """
    if model is None or tokenizer is None:
        return {
            "score": 0.0,
            "details": "Model failed to load. Check server logs."
        }
        
    try:
        # Preprocess and tokenize the text
        # Truncate to max length supported by DistilBERT (512 tokens)
        inputs = tokenizer(
            essay_text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512, 
            padding=True
        )
        
        # Move inputs to the correct device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        if "token_type_ids" in inputs:
            del inputs["token_type_ids"]
        
        # Run inference
        with torch.no_grad():
            outputs = model(**inputs)
            
        # The output is a regression score (logits of shape [1, 1])
        # We extract the scalar value
        prediction = outputs.logits.squeeze().item()
        
        # Note: If your model outputs a score from 0-1 (e.g. normalized), 
        # you might need to multiply by 100. If it directly outputs 0-100, leave it as is.
        # For now, we will assume it outputs a value out of 100, but cap it safely.
        # We will bound the score between 0 and 100.
        score = max(0.0, min(100.0, float(prediction)))
        score = score * 100
        
        return {
            "score": round(score, 2),
            "raw_prediction": prediction,
            "details": "Evaluated using DistilBERT regression model."
        }
        
    except Exception as e:
        print(f"Error during ML inference: {e}")
        return {
            "score": 0.0,
            "details": f"Inference error: {str(e)}"
        }
