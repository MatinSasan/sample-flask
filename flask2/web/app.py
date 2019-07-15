from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)


client = MongoClient(host="db", port=27017)
db = client.sentencesDatabase
users = db['users']


class Register(Resource):
    def post(self):
        postData = request.get_json()

        username = postData['username']
        password = postData['password']

        # hashpass + salt
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            'Username': username,
            'Password': hashed_pw,
            'Sentence': "",
            'Tokens': 3
        })

        ret_json = {
            'status': 200,
            'msg': 'You successfully signed up'
        }
        return jsonify(ret_json)


def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            ret_json = {
                "status": 302
            }
            return jsonify(ret_json)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            ret_json = {
                "status": 301
            }
            return jsonify(ret_json)

        users.update({"Username": username}, {
                     "$set": {"Sentence": sentence, "Tokens": num_tokens - 1}})

        ret_json = {
            "status": 200,
            "msg": 'Sentence saved successful'
        }
        return jsonify(ret_json)


class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['username']
        password = posted_data['password']

        corrected_pw = verifyPw(username, password)

        if not corrected_pw:
            ret_json = {"status": 302}
            return jsonify(ret_json)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            ret_json = {"status": 301}
            return jsonify(ret_json)

        users.update({"Username": username}, {
                     "$set": {"Tokens": num_tokens - 1}})

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        ret_json = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(ret_json)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
