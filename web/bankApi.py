from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017")
db = client.BankAPI
users = db["Users"]


def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Username already exist"
            }
            return jsonify(retJson)
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Own": 0,
            "Debt": 0
        })

        retJson = {
            "status": 200,
            "msg": "you've successfully signed up to your bank count"
        }
        return jsonify(retJson)


def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def cashWithUser(username):
    cash = users.find({
        "Username": username
    })[0]["Own"]
    return cash


def debtWithUser(username):
    debt = users.find({
        "Username": username
    })[0]["Debt"]
    return debt


def generetReturnDictionatry(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson


def verifyCredentials(username, password):
    if not UserExist(username):
        return generetReturnDictionatry(301, "Invalid Username"), True
    correct_pw = verifyPw(username, password)
    if not correct_pw:
        return generetReturnDictionatry(302, "Incorrect Password"), True
    return None, False


def updateAccount(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Own": balance
        }
    })


def updateDebt(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Debt": balance
    }
    })


class Add(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        if money<=0:
            return jsonify(generetReturnDictionatry(304, "The money amount must be > 0"))

        cash = cashWithUser(username)
        money -=1
        bank_cash = cashWithUser("BANK")
        updateAccount("BANK", bank_cash+1)
        updateAccount(username, cash+money)

        return jsonify(generetReturnDictionatry(200, "Amount added successfully"))


class Transfer(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)
        if cash<=money:
            return jsonify(generetReturnDictionatry(304, "you are out of money, please add or take a lone"))

        if not UserExist(to):
            return jsonify(generetReturnDictionatry(301, "receiver user not exist"))

        cash_from = cashWithUser(username)
        cash_to = cashWithUser(to)
        bank_cash = cashWithUser("BANK")

        updateAccount("BANK", bank_cash+1)
        updateAccount(username, cash_from-money)
        updateAccount(to, cash_to+money-1)

        return jsonify(generetReturnDictionatry(200, "amount transferred successfully"))


class Balance(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        retJson = users.find({
            "Username": username
        },{
            "Password": 0,
            "_id": 0
        })[0]

        return jsonify(retJson)


class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)
        debt = debtWithUser(username)

        updateAccount(username, cash+money)
        updateDebt(username, debt+money)

        return jsonify(generetReturnDictionatry(200, "Loan added to your account"))


class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)

        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)

        if cash < money:
            return jsonify(generetReturnDictionatry(303, "Not enough cash in your account"))

        debt = debtWithUser(username)

        if money > debt:
            return jsonify(generetReturnDictionatry(305, "You are trying to pay load much more money than your debt"))

        updateAccount(username, cash - money)
        updateDebt(username, debt - money)

        return jsonify(generetReturnDictionatry(200, "Loan removed from your account"))


api.add_resource(Register,'/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

