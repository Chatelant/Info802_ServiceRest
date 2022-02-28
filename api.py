from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('km', int)
parser.add_argument('autonomy', int)
parser.add_argument('reload_time', int)
parser.add_argument('travel_time', int)


# fetch("http://127.0.0.1:5000/travelTime?autonomy=100&reload_time=600&km=220&travel_time=600").then(r => r.json()).then(r => console.log(r))


# Pour le moment on part du principe que l'ont roule a une vitesse moyenne de 100km/h
class TravelTime(Resource):
    def get(self):
        # nb arret , temps rechargement + temps de route estimé
        # Args
        args = parser.parse_args()
        km = int(args['km'])  # km à parcourir
        autonomy = int(args['autonomy'])  # km / charge
        reload = int(args['reload_time'])  # temps de chargement optimal en minutes
        travel_time = int(args['travel_time'])  # temps de trajet en minutes

        total_time = travel_time + (km // autonomy) * reload

        return jsonify({'minutes': total_time})

    def post(self):
        return "km - autonomy - reload_time"


api.add_resource(TravelTime, '/travelTime')

if __name__ == '__main__':
    app.run(debug=True)
