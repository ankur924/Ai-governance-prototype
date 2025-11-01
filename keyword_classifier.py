import re
import string

class KeywordQueryClassifier:
    """
    A simple keyword-based classifier that can be used as a fallback
    when SBERT is not available
    """
    def __init__(self):
        self.categories = {
            "infrastructure": {
                "keywords": [
                    "infrastructure", "broken road", "pothole", "damaged footpath", "streetlight", 
                    "not working", "pwd", "public works department", "mcd", "municipal corporation", 
                    "road repair", "street maintenance", "construction", "pavement", "sidewalk"
                ],
                "examples": []
            },
            "water_sanitation": {
                "keywords": [
                    "water", "leakage", "dirty water", "sewer", "overflow", "garbage", "waste", 
                    "collection", "delhi jal board", "djb", "mcd sanitation", "drainage", "pipeline", 
                    "tap", "drinking", "sewage", "cleanliness", "trash", "dump"
                ],
                "examples": []
            },
            "electricity_power": {
                "keywords": [
                    "electricity", "power", "cut", "outage", "bill", "high bill", "meter", "faulty meter", 
                    "unsafe connection", "bses", "tpddl", "distribution company", "energy", "voltage", 
                    "connection", "transformer", "supply", "electric"
                ],
                "examples": []
            },
            "health_safety": {
                "keywords": [
                    "health", "safety", "sanitation", "hospital", "unhygienic", "stray dog", "medical", 
                    "clinic", "disease", "infection", "delhi health department", "mcd health", "public health", 
                    "cleanliness", "hygiene", "emergency", "ambulance", "doctor", "patient"
                ],
                "examples": []
            },
            "education_government": {
                "keywords": [
                    "education", "government service", "teacher", "certificate", "ration card", "school", 
                    "college", "university", "department of education", "food supply", "civil supplies", 
                    "revenue department", "admission", "scholarship", "student", "classroom", "study"
                ],
                "examples": []
            },
            "transport_traffic": {
                "keywords": [
                    "transport", "traffic", "congestion", "illegal parking", "traffic light", "signal", 
                    "delhi traffic police", "transport department", "gnctd", "vehicle", "road", "highway", 
                    "bus", "metro", "public transport", "jam", "accident", "driver", "commute"
                ],
                "examples": []
            },
            "law_order": {
                "keywords": [
                    "law", "order", "theft", "harassment", "nuisance", "illegal construction", "delhi police", 
                    "municipal enforcement", "crime", "security", "safety", "complaint", "fir", "police station", 
                    "investigation", "protection", "violation", "enforcement"
                ],
                "examples": []
            },
            "environmental": {
                "keywords": [
                    "environment", "pollution", "tree cutting", "illegal dumping", "noise pollution", 
                    "delhi pollution control", "dpcc", "forest department", "air quality", "water pollution", 
                    "waste management", "green", "conservation", "ecology", "climate", "sustainable"
                ],
                "examples": []
            },
            "corruption_delays": {
                "keywords": [
                    "corruption", "administrative delay", "bribe", "pending file", "misuse of power", 
                    "vigilance department", "anti-corruption branch", "acb", "bureaucracy", "red tape", 
                    "official", "government officer", "complaint", "transparency", "accountability"
                ],
                "examples": []
            },
            "digital_technical": {
                "keywords": [
                    "digital", "technical", "website", "website error", "not working", "online complaint", 
                    "portal", "it department", "nic", "national informatics centre", "software", "application", 
                    "login", "password", "account", "online service", "e-governance", "internet", "computer", 
                    "system", "website down", "online portal", "technical issue", "digital service"
                ],
                "examples": []
            }
        }
    
    def preprocess_text(self, text):
        """Preprocess the text by removing punctuation and converting to lowercase"""
        text = text.lower()
        text = re.sub(f'[{string.punctuation}]', ' ', text)
        return text
    
    def classify_query(self, query):
        """Classify a query into one of the predefined categories"""
        query = self.preprocess_text(query)
        
        scores = {}
        for category, data in self.categories.items():
            score = 0
            for keyword in data['keywords']:
                if keyword.lower() in query:
                    score += 1
            scores[category] = score
        
        if max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return "unknown"
    
    def get_confidence_scores(self, query):
        """Get confidence scores for each category"""
        query = self.preprocess_text(query)
        
        scores = {}
        total_keywords = 0
        for category, data in self.categories.items():
            score = 0
            for keyword in data['keywords']:
                if keyword.lower() in query:
                    score += 1
            scores[category] = score
            total_keywords += score
        
        confidence = {}
        if total_keywords > 0:
            for category, score in scores.items():
                confidence[category] = (score / total_keywords) * 100
        else:
            for category in scores.keys():
                confidence[category] = 25.0
        
        return confidence
    
    def train(self, save_path="model_data"):
        return "keyword_model"
    
    def load(self, model_path):
        pass