from flask import Flask, request, render_template
import requests
import re

app = Flask(__name__)

# Função para extrair o código da questão do link do usuário
def extrair_codigo(link):
    match = re.search(r'exercicio/(.*?)\?', link)
    if match:
        return match.group(1)
    else:
        return None

# Função para fazer a solicitação GET e extrair a alternativa correta
def obter_alternativa_correta(url):
    try:
        response = requests.get(url)
        data = response.json()
        exercises = data.get('pageProps', {}).get('content', {}).get('children', [])

        for exercise in exercises:
            if 'list' in exercise:
                for item in exercise['list']:
                    if item.get('isCorrect'):
                        return item['letter']
    except Exception as e:
        print("Ocorreu um erro:", e)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    alternativa_correta = None
    if request.method == 'POST':
        link_usuario = request.form['link']
        codigo_questao = extrair_codigo(link_usuario)
        if codigo_questao:
            url = f"https://www.mesalva.com/app/_next/data/bm2l3_QV91OobhF5hOUQF/exercicio/{codigo_questao}.json"
            alternativa_correta = obter_alternativa_correta(url)
    
    return render_template('index.html', alternativa_correta=alternativa_correta)

if __name__ == '__main__':
    app.run(debug=True)
