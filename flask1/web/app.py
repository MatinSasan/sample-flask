from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient(host='db', port=27017)
db = client.newDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users': 0
})


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.update({}, {'$set': {"num_of_users": new_num}})
        return str(f"hello user {str(new_num)}")


def check_posted_data(posted_data, function_name):
    if isinstance(posted_data['x'], int) and isinstance(posted_data['y'], int):
        if (function_name == 'add' or function_name == 'subtract' or
                function_name == 'multiply'):
            if 'x' not in posted_data or 'y' not in posted_data:
                return 301
            else:
                return 200
        elif (function_name == 'division'):
            if 'x' not in posted_data or 'y' not in posted_data:
                return 301
            elif int(posted_data["y"]) == 0:
                return 302
            else:
                return 200
    else:
        return 302


class Add(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, 'add')

        if (status_code != 200):
            ret_json = {
                "Message": "an error occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = posted_data['x']
        y = posted_data['y']
        x = int(x)
        y = int(y)

        ret = x+y
        ret_map = {
            'Sum': ret,
            'Status Code': 200
        }
        return jsonify(ret_map)


class Subtract(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, 'subtract')

        if (status_code != 200):
            ret_json = {
                "Message": "an error occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = posted_data['x']
        y = posted_data['y']
        x = int(x)
        y = int(y)

        ret = x-y
        ret_map = {
            'Sum': ret,
            'Status Code': 200
        }
        return jsonify(ret_map)


class Multiply(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, 'multiply')

        if (status_code != 200):
            ret_json = {
                "Message": "an error occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = posted_data['x']
        y = posted_data['y']
        x = int(x)
        y = int(y)

        ret = x*y
        ret_map = {
            'Sum': ret,
            'Status Code': 200
        }
        return jsonify(ret_map)


class Divide(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, 'division')

        if (status_code != 200):
            ret_json = {
                "Message": "an error occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = posted_data['x']
        y = posted_data['y']
        x = int(x)
        y = int(y)

        ret = (x*1.0)/y
        ret_map = {
            'Sum': ret,
            'Status Code': 200
        }
        return jsonify(ret_map)


api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')
api.add_resource(Visit, '/hello')


@app.route('/')
def hello_world():
    some_json = {
        'hola': 'spanish',
        'field': 'def'
    }
    return jsonify(some_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
