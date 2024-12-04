from flask import Flask, request, jsonify, redirect, url_for
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Função para calcular a distância entre dois pontos usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371.0
    return R * c  # Retorna a distância em quilômetros

@app.route('/validate-location')
def validate_location():
    # Pegando latitude e longitude da URL
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('long', 0))

    # Coordenadas da área permitida (exemplo: São Francisco)
    allowed_lat = 37.7749
    allowed_lon = -122.4194

    # Calculando a distância entre a localização e a área permitida
    distance = haversine(lat, lon, allowed_lat, allowed_lon)

    # Definindo um raio permitido (100 metros)
    if distance <= 0.1:
        # Redirecionar para o formulário se a localização for válida
        return redirect('/form.html')
    else:
        # Responder com um erro se a localização for inválida
        return jsonify({
            "latitude": lat,
            "longitude": lon,
            "distance_to_allowed_area": distance,
            "message": "Acesso negado: você está fora da área permitida."
        }), 403

@app.route('/form.html')
def form_page():
    # Página do formulário
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Formulário</title>
    </head>
    <body>
        <h1>Preencha o Formulário</h1>
        <form action="/submit-form" method="POST">
            Nome: <input type="text" name="nome" required><br>
            RGM: <input type="text" name="rgm" required><br>
            Turma: <input type="text" name="turma" required><br>
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    """

@app.route('/submit-form', methods=['POST'])
def submit_form():
    nome = request.form.get('nome')
    rgm = request.form.get('rgm')
    turma = request.form.get('turma')
    return jsonify({
        "message": "Formulário enviado com sucesso!",
        "dados": {"nome": nome, "rgm": rgm, "turma": turma}
    })

if __name__ == '__main__':
    app.run(debug=True)
