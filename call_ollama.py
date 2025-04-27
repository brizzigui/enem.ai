from ollama import chat
from ollama import ChatResponse
import ollama

import random
import json

from enem_utils import get_random_subject, get_area

def is_ollama_awake() -> bool:
    try:
        models = ollama.list()
        print("Ollama is running and reachable. Starting server.")
        return True
    except Exception as e:
        print("Unable to connect to Ollama. Check if Ollama is running.")
        return False

def get_response(prompt: str) -> str:
    response: ChatResponse = chat(model='gemma3:12b', messages=[
    {
        'role': 'user',
        'content': prompt,
        'num_predict': 1000
    },
    ])

    return response['message']['content']

def get_random_difficulty() -> str:
    return ["Fácil", "Média", "Difícil"][random.randint(0, 2)]

def create_prompt(area, subject, difficulty) -> str:
    return f"""Escreva uma questão no *estilo da prova do ENEM*, com um grau adequado de dificuldade e contextualização para alunos de ensino médio sobre a matéria de {subject} - parte da prova de {area}.
    Siga os moldes do ENEM, mas inove no conteúdo. Se julgar necessário, traga textos e informações adicionais. Não traga de forma alguma imagens externas. A questão será apresentada igual foi escrita - então não deixe NENHUM placeholder.
    Forneça 5 alternativas, correspondentes aos itens a, b, c, d, e. Antes de começar a escrever a questão, *determine e escreva seu conteúdo específico* dentro da área. Após, determine se haverá texto adicional no enunciado e seu tamanho. Decida se a questão será mais conteudista ou interpretativa. 
    Diga qual a alternativa correta e apresente uma justificativa breve para ela. Seja criativo. Não invente informações. Seja verdadeiro. BASEIE-SE SEMPRE NA REALIDADE! NÃO SEJA ÓBVIO! NUNCA MINTA! MINIMIZE AMBIGUIDADES NAS ALTERNATIVAS!!! ATENHA-SE À MATÉRIA PEDIDA! Embaralhe as alternativas. Escreva da maneira que pedi, sem cometer erros. LEMBRE-SE: A RESPOSTA NÃO PODE SER ÓBVIA!!! VOCÊ DEVE TESTAR O CONHECIMENTO E INTERPRETAÇÃO DO ALUNO!!! DIFICULDADE ESCOLHIDA: {difficulty}.
    Não use caracteres especiais. TOME CUIDADO! A QUESTÃO DEVE TER UMA E APENAS UMA RESPOSTA CORRETA!!!!!
    
Após escrever, resolva sua questão como se fosse um aluno. Se verificar que há algum problema, que não há alternativa correta, ou que a lógica está errada, COMECE TUDO DE NOVO.

Após escrever, *formate a questão como um json* com os CONTENDO EXATAMENTE OS CAMPOS E NADA MAIS: 
    - ["resumo"]: resumo da questão (max 10 palavras), 
    - ["enunciado"]: o enunciado, 
    - ["alternativas"]: as alternativas, 
    - ["correta"]: a alternativa correta,
    - ["justificativa"]: texto de justificativa. 
    
    Use os nomes em colchetes para o json. Não use outros nomes em hipótese alguma. A resposta correta ["correta"] deve ser APENAS E EXCLUSIVAMENTE a letra da resposta (ex: 'A').

    Para indicar o começo do json escreva '```json' SIGA À RISCA AS INTRUÇÕES E MONTE A QUESTÃO DO ENEM CONFORME PEDIDO!"""

def check_validity(response_text: str) -> bool:
    try:
        data = json.loads(response_text)
        data["resumo"]
        data["enunciado"]
        data["alternativas"]
        data["correta"]
        data["justificativa"]

    except Exception as e:
        print(f"First parse error: {e}")
        return False
    
    return True

def create_question(area: str, subject: str, difficulty: str) -> str:
    if subject == "any":
        subject = get_random_subject()
        area = get_area(subject)
    if difficulty == "any":
        difficulty = get_random_difficulty()

    # will try to generate valid question for 'attemps'
    # else, fails
    attemps = 5
    for _ in range(attemps):
        prompt = create_prompt(area, subject, difficulty)
        response = get_response(prompt)
        index = response.find("```json")
        if index != -1 and check_validity(response[index+7:-3]):
            break
        else:
            print("Generation error: could not resolve json in model's response.")
    
    return response[index+7:-3]