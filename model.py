from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model_path = "fine-tuned-distilbert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def predict(input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    # Process the outputs
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)

    return predictions.item()


def predict_classes(input_dict):
    output_dict = {
        "Positive" : 0,
        "Neutral" : 0,
        "Sarcastic" : 0,
        "Negative" : 0,
    }
    
    for text in input_dict:
        
        predicted_class = predict(text)
        if(predicted_class==0):
            output_dict["Neutral"] = output_dict["Neutral"] + 1
        elif(predicted_class==1):
            output_dict["Positive"] = output_dict["Positive"] + 1
        elif(predicted_class==2):
            output_dict["Negative"] = output_dict["Negative"] + 1
        elif(predicted_class==3):
            output_dict["Sarcastic"] = output_dict["Sarcastic"] + 1
        elif(predicted_class==4):
            output_dict["Sarcastic"] = output_dict["Sarcastic"] + 1

    return output_dict

# Example usage
input_dict = {
    "This movie never ends",
    "I love this book!",
    "The weather is terrible today."
}

# Get predictions
# predictions = predict_classes(input_dict)
# print(predictions)
# print(predict("I love this book!"))
