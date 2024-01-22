from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

API_KEY = os.getenv('API_KEY')  # Acessar a variável de ambiente

traducoes_clima = {
    'clear sky': 'céu limpo',
    'few clouds': 'algumas nuvens',
    'scattered clouds': 'nuvens dispersas',
    'broken clouds': 'nuvens quebradas',
    'shower rain': 'chuva',
    # Adicione outras traduções conforme necessário
}

def obter_previsao_tempo(cidade, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric'
    resposta = requests.get(url)
    dados = resposta.json()

    if resposta.status_code == 200:
        clima = dados['weather'][0]['description']
        if clima in traducoes_clima:
            clima_traduzido = traducoes_clima[clima]
        else:
            clima_traduzido = clima
        temperatura = dados['main']['temp']
        return f'O tempo em {cidade} está {clima_traduzido} com temperatura de {temperatura}°C.'
    else:
        return 'Não foi possível obter a previsão do tempo.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/previsao_tempo', methods=['POST'])
def previsao_tempo():
    cidade = request.form['cidade']

    resultado = obter_previsao_tempo(cidade, API_KEY)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
