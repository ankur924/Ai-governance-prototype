from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

try:
    from sbert_classifier import SBERTQueryClassifier as Classifier
except Exception:
    from keyword_classifier import KeywordQueryClassifier as Classifier

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

MODEL_PICKLE = "model.pkl"
TRAINING_JSON = "training_data.json"

classifier = None

def load_or_init_classifier():
    global classifier
    if classifier is not None:
        return classifier

    if os.path.exists(MODEL_PICKLE):
        try:
            from sbert_classifier import SBERTQueryClassifier
            classifier = SBERTQueryClassifier.load_model(MODEL_PICKLE)
            print("✅ Loaded SBERT model")
            return classifier
        except Exception as e:
            print(f"⚠️ Could not load model.pkl: {e}")

    classifier = Classifier()
    if os.path.exists(TRAINING_JSON):
        with open(TRAINING_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            if hasattr(classifier, "categories"):
                for cat, examples in data.items():
                    if cat in classifier.categories:
                        for ex in examples:
                            classifier.categories[cat]["examples"].append(ex)
        if hasattr(classifier, "train"):
            classifier.train()
    return classifier


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query'"}), 400

    clf = load_or_init_classifier()
    query = data["query"]
    try:
        category = clf.classify_query(query)
        confidence = clf.get_confidence_scores(query)
        return jsonify({
            "query": query,
            "category": category,
            "confidence_scores": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Server starting...")
    load_or_init_classifier()
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)
