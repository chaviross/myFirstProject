""""
new project:

registration of user 0 tokens
Each user gets 10 tokens
Store a sentence on our database fot 1 token
Retrieve his stored sentence on our database for 1 token

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017/myDatabase")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        post_data = request.get_json()
        user_name = post_data["username"]
        password = post_data["password"]

        # TODO: check if the username and password are correct
        # TODO: check if the username singed up already

        hash_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert({
            "Username": user_name,
            "Password": hash_pw,
            "Sentence": "",
            "Tokens": 10
        })

        retJson = {
            "status": 200,
            "msg": "successfully signed up for the API"
        }
        return jsonify(retJson)


def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'),hashed_pw) == hashed_pw:
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
        post_data = request.get_json()
        user_name = post_data["username"]
        password = post_data["password"]
        sentence = post_data["sentence"]

        #verify that the username and password match
        correct_pw = verifyPw(user_name, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "username do not match to the password"
            }
            return jsonify(retJson)

        #verify user has enough tokens
        num_tokens = countTokens(user_name)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "your tokens are finished, please buy more"
            }
            return jsonify(retJson)

        #store the sentence and return 200 ok
        users.update({
            "Username": user_name
        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_tokens-1
                }
        })

        retJson = {
            "status": 200,
            "msg": "sentence saved successfully"
        }
        return jsonify(retJson)


class Get(Resource):

    def post(self):
        post_data = request.get_json()
        user_name = post_data["username"]
        password = post_data["password"]

        correct_pw = verifyPw(user_name, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "username do not match to the password"
            }
            return jsonify(retJson)

        num_tokens = countTokens(user_name)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "your tokens are finished, please buy extra more"
            }
            return jsonify(retJson)

        users.update({
            "Username": user_name
        }, {
            "$set": {
                "Tokens": num_tokens - 1
            }
        })

        sentence = users.find({
            "Username": user_name
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }

        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")


if __name__ == '__main__':

    app.run(host="0.0.0.0")


"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017/myDatabase")
db = client.aNewDB
UserName = db["UserName"]

UserName.insert_one({
    'num_of_users':0
})


class Visit(Resource):
    def get(self):
        prev_num = UserName.find({})[0]['num_of_users']
        new_num = prev_num+1
        UserName.update({},{"$set":{"num_of_users":new_num}})
        return str("Hello user "+ str(new_num))


def check_post_data(posted_data, function_name):
    if function_name == "add" or function_name =="sub" or function_name=="multi":
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        else:
            return 200
    elif function_name == "divide":
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        elif posted_data["y"]==0:
            return 302
        else:
            return 200


class Add (Resource):
    def post(self):

        post_data= request.get_json()

        status_code = check_post_data(post_data, "add")
        if status_code != 200:
            ret_json = {
                "message": "an error happened",
                "Status_Code": status_code
            }
            return jsonify(ret_json)

        x = post_data["x"]
        y = post_data["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        retMap = {
            "massage": ret,
            "Status_Code": 200
        }
        return jsonify(retMap)


class Sub (Resource):
    def post(self):
        post_data = request.get_json()

        status_code = check_post_data(post_data, "sub")

        if status_code != 200:
            ret_json = {
                "message": "an error happened",
                "Status_Code": status_code
            }
            return jsonify(ret_json)

        x = post_data["x"]
        y = post_data["y"]
        x = int(x)
        y = int(y)
        ret = x - y
        retMap = {
            "massage": ret,
            "Status_Code": 200
        }
        return jsonify(retMap)


class Multiply (Resource):
    def post(self):
        post_data = request.get_json()

        status_code = check_post_data(post_data, "multi")
        if status_code != 200:
            ret_json = {
                "message": "an error happened",
                "Status_Code": status_code
            }
            return jsonify(ret_json)

        x = post_data["x"]
        y = post_data["y"]
        x = int(x)
        y = int(y)
        ret = x * y
        retMap = {
            "massage": ret,
            "Status_Code": 200
        }
        return jsonify(retMap)


class Divide (Resource):
    def post(self):
        post_data = request.get_json()

        status_code = check_post_data(post_data, "divide")
        if status_code != 200:
            ret_json = {
                "message": "an error happened",
                "Status_Code": status_code
            }
            return jsonify(ret_json)

        x = post_data["x"]
        y = post_data["y"]
        x = int(x)
        y = int(y)
        ret = (x*1.0)/y
        retMap = {
            "massage": ret,
            "Status_Code": 200
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Sub, "/sub")
api.add_resource(Multiply, "/multi")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
"""