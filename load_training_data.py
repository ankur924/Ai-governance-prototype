import json
import os

try:
    from sbert_classifier import SBERTQueryClassifier
    Classifier = SBERTQueryClassifier
    print("Using SBERT classifier")
except ImportError:
    from keyword_classifier import KeywordQueryClassifier
    Classifier = KeywordQueryClassifier
    print("Using fallback keyword classifier")

def load_training_data():
    """Load training data from JSON file and train the model"""
    print("Loading training data and training model...")
    
    # Check if training data exists
    if not os.path.exists('training_data.json'):
        print("Error: training_data.json not found!")
        return False
    
    with open('training_data.json', 'r') as f:
        training_data = json.load(f)
    
    classifier = Classifier()
    
    for category, examples in training_data.items():
        if category in classifier.categories:
            for example in examples:
                classifier.categories[category]['examples'].append(example)
    
    # Train the model
    model_path = classifier.train()
    print(f"Model trained successfully and saved to {model_path}")
    
    test_queries = [
        "Potholes on my street need repair",
        "Sewer overflow in my neighborhood",
        "Frequent power cuts in my area",
        "Unhygienic conditions in local hospital",
        "Need help with ration card application",
        "Traffic signal not working at junction",
        "How to report theft in my locality",
        "Air pollution levels are very high",
        "Bribery demand for processing my file",
        "Website of government portal is not loading"
    ]
    
    print("\nTesting the trained model:")
    for query in test_queries:
        category = classifier.classify_query(query)
        confidence = classifier.get_confidence_scores(query)
        
        print(f"Query: {query}")
        print(f"Category: {category}")
        if category in confidence:
            print(f"Confidence: {confidence[category]:.2f}%")
        else:
            print(f"Confidence: N/A")
        print("-" * 40)
    
    return True

if __name__ == "__main__":
    load_training_data()