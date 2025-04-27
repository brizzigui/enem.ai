import pytest
from enem_utils import get_area, get_random_subject

def test_get_area():
    assert get_area("Matemática") == "Matemática e suas tecnologias"
    assert get_area("Português") == "Linguagens, códigos e suas tecnologias"
    assert get_area("Física") == "Ciências da Natureza e suas tecnologias"
    assert get_area("História") == "Ciências Humanas e suas tecnologias"

    assert get_area("Geografia") == "Ciências Humanas e suas tecnologias"
    assert get_area("Arte") == "Linguagens, códigos e suas tecnologias"
    assert get_area("Filosofia") == "Ciências Humanas e suas tecnologias"
    assert get_area("Sociologia") == "Ciências Humanas e suas tecnologias"
    assert get_area("Química") == "Ciências da Natureza e suas tecnologias"
    assert get_area("Inglês") == "Linguagens, códigos e suas tecnologias"
    # casos não contemplados devem retornar "any"
    assert get_area("any_subject") == "any"

def test_get_random_subject():
    subjects = ["Matemática", "Português", "Inglês", "Espanhol", "Arte", "Educação Física",
                "Física", "Química", "Biologia", "História", "Geografia", "Filosofia", "Sociologia"]
    
    for _ in range(100):  # roda 100 vezes para garantir que sempre retorna algo válido
        subject = get_random_subject()
        assert subject in subjects
