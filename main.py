from flask import Flask, request, jsonify, render_template
import json
import call_ollama
from enem_utils import get_area

app = Flask(__name__, static_folder='./assets', template_folder='./assets')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next', methods=['POST'])
def next():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid format"}), 400
    
    subject = data.get('subject')
    difficulty = data.get('difficulty')
    area = get_area(subject)

    question = call_ollama.create_question(area, subject, difficulty)
    return json.dumps(question), 200, {"Content-Type": "application/json"}

def main() -> None:
    assert call_ollama.is_ollama_awake() == True
    app.run(debug=True, port=5001)

if __name__ == "__main__":
    main()