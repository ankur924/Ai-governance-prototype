"""
Script to save and load the classifier model using pickle
"""
from sbert_classifier import SBERTQueryClassifier
import json

def main():
    print("Initializing classifier...")
    classifier = SBERTQueryClassifier()
    
    print("Loading training data...")
    with open('training_data.json', 'r') as f:
        training_data = json.load(f)
    
    print("Training model...")
    classifier.train(training_data)
    
    classifier.save_model('model.pkl')
    
    test_queries = [
        "Potholes on my street need repair",
        "Water supply issues in my area",
        "Electricity bill payment options"
    ]
    
    print("\nTesting classification before saving:")
    for query in test_queries:
        category = classifier.classify_query(query)
        confidence = classifier.get_confidence_scores(query).get(category, 0) * 100
        print(f"Query: {query}")
        print(f"Category: {category}")
        print(f"Confidence: {confidence:.2f}%")
        print("-" * 40)
    
    # Load the model
    print("\nLoading model from pickle file...")
    loaded_classifier = SBERTQueryClassifier.load_model('model.pkl')
    
    print("\nTesting classification after loading:")
    for query in test_queries:
        category = loaded_classifier.classify_query(query)
        confidence = loaded_classifier.get_confidence_scores(query).get(category, 0) * 100
        print(f"Query: {query}")
        print(f"Category: {category}")
        print(f"Confidence: {confidence:.2f}%")
        print("-" * 40)

if __name__ == "__main__":
    main()