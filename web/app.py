from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


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
        ret = (x*1.0 )/ y
        retMap = {
            "massage": ret,
            "Status_Code": 200
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Sub, "/sub")
api.add_resource(Multiply, "/multi")
api.add_resource(Divide, "/divide")

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
