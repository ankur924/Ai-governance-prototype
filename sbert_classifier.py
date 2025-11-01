import os
import json
import torch
import numpy as np
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    print("Using fallback classifier without sentence_transformers")
    SentenceTransformer = None
    util = None
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class SBERTQueryClassifier:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        Initialize the SBERT Query Classifier
        
        Args:
            model_name (str): Name of the pre-trained SBERT model to use
        """
        self.model_name = model_name
        self.use_fallback = SentenceTransformer is None
        
        if not self.use_fallback:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                print(f"Error loading SBERT model: {e}")
                print("Using fallback keyword-based classifier")
                self.use_fallback = True
        self.categories = {
            "infrastructure": {
                "keywords": [
                    "infrastructure", "broken road", "pothole", "damaged footpath", "streetlight", 
                    "not working", "pwd", "public works department", "mcd", "municipal corporation", 
                    "road repair", "street maintenance", "construction", "pavement", "sidewalk"
                ],
                "examples": [
                    "How to report potholes in my area?",
                    "When will the broken streetlights be fixed?",
                    "Who is responsible for repairing damaged footpaths?",
                    "How to file a complaint about road conditions?",
                    "What department handles street maintenance issues?"
                ]
            },
            "water_sanitation": {
                "keywords": [
                    "water", "leakage", "dirty water", "sewer", "overflow", "garbage", "waste", 
                    "collection", "delhi jal board", "djb", "mcd sanitation", "drainage", "pipeline", 
                    "tap", "drinking", "sewage", "cleanliness", "trash", "dump"
                ],
                "examples": [
                    "How to report water leakage in my area?",
                    "Who to contact for sewer overflow problems?",
                    "When will garbage collection resume in my locality?",
                    "How to file a complaint about dirty water supply?",
                    "What department handles sanitation issues?"
                ]
            },
            "electricity_power": {
                "keywords": [
                    "electricity", "power", "cut", "outage", "bill", "high bill", "meter", "faulty meter", 
                    "unsafe connection", "bses", "tpddl", "distribution company", "energy", "voltage", 
                    "connection", "transformer", "supply", "electric"
                ],
                "examples": [
                    "How to report frequent power cuts?",
                    "Who to contact about high electricity bills?",
                    "How to get a faulty meter replaced?",
                    "When will power be restored in my area?",
                    "How to report unsafe electrical connections?"
                ]
            },
            "health_safety": {
                "keywords": [
                    "health", "safety", "sanitation", "hospital", "unhygienic", "stray dog", "medical", 
                    "clinic", "disease", "infection", "delhi health department", "mcd health", "public health", 
                    "cleanliness", "hygiene", "emergency", "ambulance", "doctor", "patient"
                ],
                "examples": [
                    "How to report unhygienic conditions in hospitals?",
                    "Who handles stray dog issues in residential areas?",
                    "How to file a complaint about poor sanitation?",
                    "What department is responsible for public health?",
                    "How to request emergency medical services?"
                ]
            },
            "education_government": {
                "keywords": [
                    "education", "government service", "teacher", "certificate", "ration card", "school", 
                    "college", "university", "department of education", "food supply", "civil supplies", 
                    "revenue department", "admission", "scholarship", "student", "classroom", "study"
                ],
                "examples": [
                    "How to apply for school admission?",
                    "What are the best colleges for engineering?",
                    "How to get a ration card issued?",
                    "When will certificates be issued by the revenue department?",
                    "How to report shortage of teachers in schools?"
                ]
            },
            "transport_traffic": {
                "keywords": [
                    "transport", "traffic", "congestion", "illegal parking", "traffic light", "signal", 
                    "delhi traffic police", "transport department", "gnctd", "vehicle", "road", "highway", 
                    "bus", "metro", "public transport", "jam", "accident", "driver", "commute"
                ],
                "examples": [
                    "How to report traffic congestion issues?",
                    "Who to contact about illegal parking?",
                    "How to report broken traffic signals?",
                    "What department handles public transport problems?",
                    "How to file a complaint about reckless driving?"
                ]
            },
            "law_order": {
                "keywords": [
                    "law", "order", "theft", "harassment", "nuisance", "illegal construction", "delhi police", 
                    "municipal enforcement", "crime", "security", "safety", "complaint", "fir", "police station", 
                    "investigation", "protection", "violation", "enforcement"
                ],
                "examples": [
                    "How to report theft in my neighborhood?",
                    "Who to contact about harassment issues?",
                    "How to file a complaint about illegal construction?",
                    "What department handles public nuisance complaints?",
                    "How to register an FIR at the police station?"
                ]
            },
            "environmental": {
                "keywords": [
                    "environment", "pollution", "tree cutting", "illegal dumping", "noise pollution", 
                    "delhi pollution control", "dpcc", "forest department", "air quality", "water pollution", 
                    "waste management", "green", "conservation", "ecology", "climate", "sustainable"
                ],
                "examples": [
                    "How to report air pollution in my area?",
                    "Who to contact about illegal tree cutting?",
                    "How to file a complaint about waste dumping?",
                    "What department handles noise pollution issues?",
                    "How to report water pollution in local water bodies?"
                ]
            },
            "corruption_delays": {
                "keywords": [
                    "corruption", "administrative delay", "bribe", "pending file", "misuse of power", 
                    "vigilance department", "anti-corruption branch", "acb", "bureaucracy", "red tape", 
                    "official", "government officer", "complaint", "transparency", "accountability"
                ],
                "examples": [
                    "How to report corruption in government offices?",
                    "Who to contact about administrative delays?",
                    "How to file a complaint about bribery demands?",
                    "What department handles misuse of power by officials?",
                    "How to track status of pending files in government departments?"
                ]
            },
            "digital_technical": {
                "keywords": [
                    "digital", "technical", "website error", "online complaint", "portal", "it department", 
                    "nic", "national informatics centre", "software", "application", "login", "password", 
                    "account", "online service", "e-governance", "internet", "computer", "system"
                ],
                "examples": [
                    "How to report government website errors?",
                    "Who to contact when online complaint portal is not working?",
                    "How to resolve login issues with government portals?",
                    "What department handles e-governance technical problems?",
                    "How to get help with online service applications?"
                ]
            }
        }
        
        self.embeddings = {}
        
        self.category_embeddings = {}
        self.keyword_embeddings = {}
        self.example_embeddings = {}
        
    def train(self, save_path="model_data"):
        """
        Train the SBERT model by encoding category keywords and examples
        
        Args:
            save_path (str): Path to save the trained model data
        """
        if self.use_fallback:
            print("Using fallback mode - no actual training performed")
            return "fallback_model"
            

        os.makedirs(save_path, exist_ok=True)
        
        try:
            for category, data in self.categories.items():
                keywords = data['keywords']
                keyword_embeddings = self.model.encode(keywords, convert_to_tensor=True)
                self.keyword_embeddings[category] = keyword_embeddings
                
                examples = data['examples']
                if examples:  # Only encode if there are examples
                    example_embeddings = self.model.encode(examples, convert_to_tensor=True)
                    self.example_embeddings[category] = example_embeddings
                    
                    all_embeddings = torch.cat([keyword_embeddings, example_embeddings], dim=0)
                    category_embedding = torch.mean(all_embeddings, dim=0)
                else:
                    category_embedding = torch.mean(keyword_embeddings, dim=0)
                    
                self.category_embeddings[category] = category_embedding
            
            model_data = {
                'model_name': self.model_name,
                'categories': self.categories,
                'category_embeddings': {k: v.cpu().numpy() for k, v in self.category_embeddings.items()},
                'keyword_embeddings': {k: v.cpu().numpy() for k, v in self.keyword_embeddings.items()},
                'example_embeddings': {k: v.cpu().numpy() for k, v in self.example_embeddings.items()}
            }
            
            with open(os.path.join(save_path, 'model_data.pkl'), 'wb') as f:
                pickle.dump(model_data, f)
                
            return os.path.join(save_path, 'model_data.pkl')
        except Exception as e:
            print(f"Error during training: {e}")
            print("Falling back to keyword-based classification")
            self.use_fallback = True
            return "fallback_model"
    
    def load(self, model_path):
        """
        Load a trained model from disk
        
        Args:
            model_path (str): Path to the saved model data
        """
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model_name = model_data['model_name']
        self.categories = model_data['categories']
        
        self.category_embeddings = {k: torch.tensor(v) for k, v in model_data['category_embeddings'].items()}
        self.keyword_embeddings = {k: torch.tensor(v) for k, v in model_data['keyword_embeddings'].items()}
        self.example_embeddings = {k: torch.tensor(v) for k, v in model_data['example_embeddings'].items()}
    
    def classify_query(self, query):
        """
        Classify a query using SBERT embeddings
        
        Args:
            query (str): The query to classify
            
        Returns:
            str: The predicted category
        """
        if self.use_fallback:
            query_lower = query.lower()
            scores = {}
            
            for category, data in self.categories.items():
                score = 0
                for keyword in data['keywords']:
                    if keyword.lower() in query_lower:
                        score += 1
                scores[category] = score
            
            if max(scores.values()) > 0:
                return max(scores.items(), key=lambda x: x[1])[0]
            else:
                return "unknown"
        
        try:
            query_embedding = self.model.encode(query, convert_to_tensor=True)
            
            similarities = {}
            for category, embedding in self.category_embeddings.items():
                similarity = util.pytorch_cos_sim(query_embedding, embedding).item()
                similarities[category] = similarity
            
            if all(sim == 0 for sim in similarities.values()):
                return "unknown"
            
            max_category = max(similarities, key=similarities.get)
            return max_category
        except Exception as e:
            print(f"Error during classification: {e}")
            print("Falling back to keyword-based classification")
            self.use_fallback = True
            return self.classify_query(query)  
    
    def get_confidence_scores(self, query):
        """
        Get confidence scores for each category
        
        Args:
            query (str): The query to classify
            
        Returns:
            dict: Dictionary with confidence scores for each category
        """
        if self.use_fallback:
            query_lower = query.lower()
            scores = {}
            total_keywords = 0
            
            for category, data in self.categories.items():
                score = 0
                for keyword in data['keywords']:
                    if keyword.lower() in query_lower:
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
        
        try:
            query_embedding = self.model.encode(query, convert_to_tensor=True)
            
            similarities = {}
            for category, embedding in self.category_embeddings.items():
                similarity = util.pytorch_cos_sim(query_embedding, embedding).item()
                similarities[category] = similarity
            
            total = sum(max(0, sim) for sim in similarities.values())
            
            confidence = {}
            if total > 0:
                for category, similarity in similarities.items():
                    confidence[category] = (max(0, similarity) / total) * 100
            else:
                for category in similarities:
                    confidence[category] = 0
            
            return confidence
        except Exception as e:
            print(f"Error during confidence calculation: {e}")
            print("Falling back to keyword-based confidence scores")
            self.use_fallback = True
            return self.get_confidence_scores(query) 
    
    def save_model(self, file_path='model.pkl'):
        """
        Save the classifier model using pickle for deployment
        
        Args:
            file_path (str): Path to save the pickled model
        """
        print(f"Saving model to {file_path}...")
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"Model saved successfully to {file_path}")
        
    @classmethod
    def load_model(cls, file_path='model.pkl'):
        """
        Load a saved classifier model from pickle file
        
        Args:
            file_path (str): Path to the pickled model file
            
        Returns:
            SBERTQueryClassifier: Loaded classifier instance
        """
        print(f"Loading model from {file_path}...")
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded successfully from {file_path}")
        return model 
    
    def add_training_example(self, query, category):
        """
        Add a new training example to a category
        
        Args:
            query (str): The query to add as an example
            category (str): The category to add the example to
        """
        if category in self.categories:
            self.categories[category]['examples'].append(query)
            self.train()
        else:
            raise ValueError(f"Category '{category}' not found")

if __name__ == "__main__":
    classifier = SBERTQueryClassifier()
    
    model_path = classifier.train()
    print(f"Model trained and saved to {model_path}")
    
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