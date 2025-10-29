import re
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class GovQueryClassifier:
    def __init__(self):
        self.categories = {
            "education": {
                "keywords": [
                    "education", "school", "college", "university", "student", 
                    "teacher", "professor", "classroom", "curriculum", "degree",
                    "scholarship", "admission", "academic", "learning", "teaching",
                    "exam", "course", "study", "board", "ugc", "ncert", "cbse", "icse",
                    "sarva shiksha abhiyan", "mid-day meal", "right to education"
                ],
                "patterns": [
                    r"educat\w+", r"school\w*", r"colleg\w+", r"univers\w+", 
                    r"stud\w+", r"teach\w+", r"class\w+", r"learn\w+"
                ]
            },
            "highway": {
                "keywords": [
                    "highway", "road", "transport", "vehicle", "traffic", "bridge", 
                    "toll", "construction", "infrastructure", "expressway", "national highway",
                    "state highway", "nhai", "morth", "roadway", "corridor", "lane",
                    "bharatmala", "pradhan mantri gram sadak yojana", "pmgsy"
                ],
                "patterns": [
                    r"highway\w*", r"road\w*", r"transport\w+", r"vehic\w+", 
                    r"traffic\w*", r"bridge\w*", r"infrastruct\w+"
                ]
            },
            "electricity": {
                "keywords": [
                    "electricity", "power", "energy", "grid", "transmission", "distribution",
                    "generation", "solar", "wind", "hydro", "thermal", "renewable", "voltage",
                    "transformer", "substation", "billing", "meter", "connection", "outage",
                    "discom", "ntpc", "nhpc", "pgcil", "saubhagya", "ddugjy", "kusum"
                ],
                "patterns": [
                    r"electric\w+", r"power\w*", r"energ\w+", r"grid\w*", 
                    r"transmi\w+", r"distribut\w+", r"generat\w+"
                ]
            },
            "water": {
                "keywords": [
                    "water", "irrigation", "dam", "canal", "river", "lake", "reservoir",
                    "drinking water", "sanitation", "sewage", "drainage", "flood", "drought",
                    "watershed", "groundwater", "rainwater", "harvesting", "pipeline",
                    "jal jeevan mission", "namami gange", "swachh bharat", "amrut"
                ],
                "patterns": [
                    r"water\w*", r"irrigat\w+", r"dam\w*", r"canal\w*", 
                    r"river\w*", r"reservoir\w*", r"sanitat\w+"
                ]
            }
        }
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def preprocess_text(self, text):
        text = text.lower()
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        tokens = word_tokenize(text)
        
        processed_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words
        ]
        
        return processed_tokens
    
    def classify_query(self, query):
        processed_query = self.preprocess_text(query)
        query_text = ' '.join(processed_query)
        
        scores = {}
        
        for category, features in self.categories.items():
            score = 0
            
            for keyword in features["keywords"]:
                if keyword in processed_query or keyword in query_text:
                    score += 1
            
            for pattern in features["patterns"]:
                matches = re.findall(pattern, query_text)
                score += len(matches)
            
            scores[category] = score
        
        if all(score == 0 for score in scores.values()):
            return "unknown"
        
        max_category = max(scores, key=scores.get)
        return max_category
    
    def get_confidence_scores(self, query):
        processed_query = self.preprocess_text(query)
        query_text = ' '.join(processed_query)
        
        scores = {}
        
        for category, features in self.categories.items():
            score = 0
            
            for keyword in features["keywords"]:
                if keyword in processed_query or keyword in query_text:
                    score += 1
            
            for pattern in features["patterns"]:
                matches = re.findall(pattern, query_text)
                score += len(matches)
            
            scores[category] = score
        
        total_score = sum(scores.values())
        
        confidence = {}
        if total_score > 0:
            for category, score in scores.items():
                confidence[category] = (score / total_score) * 100
        else:
            for category in scores:
                confidence[category] = 0
        
        return confidence

if __name__ == "__main__":
    classifier = GovQueryClassifier()
    
    test_queries = [
        "How to apply for school admission?",
        "What are the toll rates on NH-8?",
        "Electricity bill payment options",
        "Water supply issues in my area",
        "What is the status of my passport application?"
    ]
    
    for query in test_queries:
        category = classifier.classify_query(query)
        confidence = classifier.get_confidence_scores(query)
        
        print(f"Query: {query}")
        print(f"Category: {category}")
        print(f"Confidence Scores: {json.dumps(confidence, indent=2)}")
        print("-" * 50)