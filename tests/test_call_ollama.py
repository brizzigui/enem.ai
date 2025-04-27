import pytest
import json
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import call_ollama as enem_gen

@pytest.fixture
def sample_json_response():
    return json.dumps({
        "resumo": "Resumo da questão",
        "enunciado": "Enunciado da questão",
        "alternativas": ["A) alternativa 1", "B) alternativa 2", "C) alternativa 3", "D) alternativa 4", "E) alternativa 5"],
        "correta": "A",
        "justificativa": "Justificativa da resposta correta."
    })

def test_is_ollama_awake(monkeypatch):
    monkeypatch.setattr(enem_gen.ollama, "list", lambda: ["model1", "model2"])
    assert enem_gen.is_ollama_awake() is True

def test_is_ollama_awake_failure(monkeypatch):
    def raise_exception():
        raise Exception("Ollama not running")
    monkeypatch.setattr(enem_gen.ollama, "list", raise_exception)
    assert enem_gen.is_ollama_awake() is False

def test_get_random_difficulty():
    difficulties = set(enem_gen.get_random_difficulty() for _ in range(100))
    assert difficulties.issubset({"Fácil", "Média", "Difícil"})
    assert len(difficulties) >= 1

def test_create_prompt():
    area = "Linguagens"
    subject = "Literatura"
    difficulty = "Média"
    prompt = enem_gen.create_prompt(area, subject, difficulty)
    assert isinstance(prompt, str)
    assert area in prompt
    assert subject in prompt
    assert difficulty in prompt

def test_check_validity_valid(sample_json_response):
    assert enem_gen.check_validity(sample_json_response) is True

def test_check_validity_invalid():
    invalid_json = '{"resumo": "Resumo", "enunciado": "Enunciado"}'  # faltam campos
    assert enem_gen.check_validity(invalid_json) is False

def test_create_question(monkeypatch, sample_json_response):
    # mock dependencies
    monkeypatch.setattr(enem_gen, "get_response", lambda prompt: "```json" + sample_json_response + "```")
    monkeypatch.setattr(enem_gen, "check_validity", lambda response_text: True)
    
    area = "Ciências Humanas"
    subject = "História"
    difficulty = "Fácil"
    question_json = enem_gen.create_question(area, subject, difficulty)
    data = json.loads(question_json)
    
    assert "resumo" in data
    assert "enunciado" in data
    assert "alternativas" in data
    assert "correta" in data
    assert "justificativa" in data

def test_create_question_random(monkeypatch, sample_json_response):
    monkeypatch.setattr(enem_gen, "get_random_subject", lambda: "Química")
    monkeypatch.setattr(enem_gen, "get_area", lambda subject: "Ciências da Natureza")
    monkeypatch.setattr(enem_gen, "get_random_difficulty", lambda: "Média")
    monkeypatch.setattr(enem_gen, "get_response", lambda prompt: "```json" + sample_json_response + "```")
    monkeypatch.setattr(enem_gen, "check_validity", lambda response_text: True)

    question_json = enem_gen.create_question("any", "any", "any")
    data = json.loads(question_json)

    assert data["resumo"]
    assert data["enunciado"]
    assert data["alternativas"]
    assert data["correta"]
    assert data["justificativa"]