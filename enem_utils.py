import random

def get_area(subject: str) -> str:
    match subject:
        case "Matemática":
            return "Matemática e suas tecnologias"
        
        case "Português" | "Inglês" | "Espanhol" | "Arte" | "Educação Física":
            return "Linguagens, códigos e suas tecnologias"
        
        case "Física" | "Química" | "Biologia":
            return "Ciências da Natureza e suas tecnologias"
        
        case "História" | "Geografia" | "Filosofia" | "Sociologia":
            return "Ciências Humanas e suas tecnologias"
        
    return "any"

def get_random_subject() -> str:
    subjects = ["Matemática", "Português", "Inglês", "Espanhol", "Arte", "Educação Física",
                "Física", "Química", "Biologia", "História", "Geografia", "Filosofia", "Sociologia"]
    
    return subjects[random.randint(0, len(subjects)-1)]
