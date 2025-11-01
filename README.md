# Indian Government Query Classifier

This application classifies user queries into different Indian government departments/categories:
- Education
- Highway
- Electricity
- Water

## Features

- Natural Language Processing (NLP) based query classification
- Confidence scores for each category
- Simple web interface for testing
- RESTful API endpoint for integration

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Application

1. Start the Flask application:
   ```
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`
3. Enter your query in the text box and click "Classify Query"

### Using the Classifier in Your Code

```python
from query_classifier import GovQueryClassifier

# Initialize the classifier
classifier = GovQueryClassifier()

# Classify a query
query = "How to apply for school admission?"
category = classifier.classify_query(query)
confidence = classifier.get_confidence_scores(query)

print(f"Category: {category}")
print(f"Confidence Scores: {confidence}")
```

## How It Works

The classifier uses a keyword and pattern-based approach with NLP techniques:

1. Text preprocessing (tokenization, stopword removal, lemmatization)
2. Matching against predefined keywords and regex patterns for each category
3. Scoring based on matches
4. Determining the most likely category

## Customization

You can customize the categories and their associated keywords/patterns in the `query_classifier.py` file.

## License

This project is open source and available under the MIT License.