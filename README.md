# Trabalho 1 de Qualidade de Software

## Programa

O programa desenvolvido se trata de uma aplicação de estudos que gera questões inéditas no estilo ENEM com auxílio de Inteligência Artificial.
Trata-se de uma aplicação web com interface pensada para dispositivos móveis. Pode ser acessada em [enemai.brizzigui.com](http://enemai.brizzigui.com). 

> [!WARNING]  
> Para evitar uso desnecessário de recursos, o servidor está sendo deixado desligado. Para restaurar o serviço, envie um email para [brizzigui@gmail.com](mailto:brizzigui@gmail.com). Alternativamente, você pode usar seu próprio servidor local.

## Testes

A pasta `tests` contém os arquivos relacionados aos testes de unidade relativos ao Trabalho. Os testes foram implementados usando a biblioteca `pytest`.

Para executar os testes, basta dar o comando:
```bash
pytest
```

## Servidor Local

Para hostear localmente, é necessário:

- Python
- Ollama
- Dependências:
    ```bash
    pip install ollama flask
    ```
- Baixe o modelo de IA desejado por meio da Ollama. Veja os disponíveis em [ollama.com](http://ollama.com). Por default, está sendo usado o `gemma3:12b`. Para instalar, rode:

    ```bash
    ollama run gemma3:12b
    ```