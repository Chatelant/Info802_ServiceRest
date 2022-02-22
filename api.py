from _datetime import time

from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

# Faire l'equivalent pour notre class
# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('km', int)
parser.add_argument('autonomy', int)
parser.add_argument('reload_time', int)


# Pour le moment on part du principe que l'ont roule a une vitesse moyenne de 100km/h
class TravelTime(Resource):
    def get(self):
        # Args
        args = parser.parse_args()
        km: int = int(args['km'])  # Km to parcours
        autonomy: int = int(args['autonomy'])  # KM / charge
        reload: int = int(args['reload_time'])  # temps de chargement optimal
        vit_kmh = 100
        vit_kmm = vit_kmh / 24
        print(vit_kmm)

        nb_reload: int = int(km / autonomy) - 1
        hours = int(int(nb_reload * reload // 60) + (int(km / 100)))
        mints = int((nb_reload * reload % 60) + int((km % 100) / vit_kmm))
        res: time = time(hour=hours, minute=mints, second=int((km % 100) % vit_kmm))
        return res.strftime("%H:%M:%S")

    def post(self):
        return "km - autonomy - reload_time"


##
## Actually setup the Api resource routing here
##
api.add_resource(TravelTime, '/travelTime')

if __name__ == '__main__':
    # app.run(debug=True)  # Local server
    app.run(host='info802-service-rest.herokuapp.com', debug=True)  # Heroku server
