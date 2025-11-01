import os
import json
from sbert_classifier import SBERTQueryClassifier

def main():
    print("Training SBERT Query Classifier for Indian Government Categories")
    print("-" * 60)
    

    os.makedirs("model_data", exist_ok=True)
    

    classifier = SBERTQueryClassifier()
    

    model_path = classifier.train()
    print(f"Model trained and saved to {model_path}")
    
    test_queries = [
        "How to apply for school admission?",
        "What are the toll rates on NH-8?",
        "Electricity bill payment options",
        "Water supply issues in my area",
        "What is the status of my passport application?",
        "How to get birth certificate?",
        "What are the documents required for voter ID?",
        "How to apply for scholarship for SC/ST students?",
        "When will the new flyover construction be completed?",
        "How to report power theft in my neighborhood?"
    ]
    
    print("\nTesting the trained model with example queries:")
    print("-" * 60)
    
    for query in test_queries:
        category = classifier.classify_query(query)
        confidence = classifier.get_confidence_scores(query)
        
        print(f"Query: {query}")
        print(f"Predicted Category: {category}")
        

        print("Confidence Scores:")
        for cat, score in confidence.items():
            print(f"  - {cat}: {score:.2f}%")
        
        print("-" * 60)
    
    print("Model training and testing completed successfully!")

if __name__ == "__main__":
    main()