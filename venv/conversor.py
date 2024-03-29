from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '24d97746da0f44a4feca49d2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converter', methods=['POST'])
def converter():
    moeda_de = request.form['moeda_de']
    moeda_para = request.form['moeda_para']
    quantidade = float(request.form['quantidade'])

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{moeda_de}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        taxa = data['conversion_rates'][moeda_para]
        resultado = quantidade * taxa
        return render_template('index.html', resultado=resultado)
    else:
        return render_template('index.html', erro="Erro ao converter moeda.")

if __name__ == '__main__':
    app.run(debug=True)