from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Função para calcular a distância entre dois pontos usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    # Converte as coordenadas de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Raio da Terra em quilômetros
    R = 6371.0
    return R * c  # Retorna a distância em quilômetros

@app.route('/validate-location')
def validate_location():
    # Pegando latitude e longitude da URL
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('long'))

    # Coordenadas da área permitida (exemplo, São Francisco)
    allowed_lat = 37.7749
    allowed_lon = -122.4194

    # Calculando a distância entre a localização e a área permitida
    distance = haversine(lat, lon, allowed_lat, allowed_lon)

    # Exibindo a localização atual
    response = {
        "latitude": lat,
        "longitude": lon,
        "distance_to_allowed_area": distance,
        "message": "Acesso permitido" if distance <= 0.1 else "Acesso negado"
    }

    # Retornando a resposta JSON com a localização e a validação
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
