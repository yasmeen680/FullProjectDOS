from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask,jsonify,json
import json
import requests

app = Flask(__name__)
api = Api(app)

divider = "\n-----------------------------------------------\n"

@app.route('/info/<id>', methods=['GET'])
def getBookById(id):
    r = requests.get('http://catalog-server:5050/books/{}'.format(id))
  
    if r.status_code == 404:
        return "invalid book number" 

    if r.status_code == 200:
        response = r.json()
        res = divider
        res +=  "id      : "+str(response["id"]) + "\n" 
        res +=  "title   : "+response["title"] + "\n" 
        res +=  "price   : "+str(response["price"])+ "\n" 
        res +=  "quantity: "+str(response["quantity"]) 
        res += divider        
        return res

    else : return "ERROR try again later"

@app.route('/search/<topic>', methods=['GET'])
def getBooksByTopic(topic):
    r = requests.get('http://catalog-server:5050/books?topic={}'.format(topic))
    if r.status_code == 404:
        return "  no books found with this topic" 
    if r.status_code == 200:
        response = r.json()
        print(r.text)
        res = divider
        for d in response:
            res += "id    : "+str(d["id"]) + "\n" 
            res += "title : "+d["title"] 
            res += divider
        return res

    else : return "ERROR try again later"

@app.route('/purchase/<id>', methods=['POST'])
def updateBookQuantity(id):
    body = request.get_json()
    name = body["name"]

    r = requests.post('http://orders-server:4040/orders',
                         json={"id":int(id), "name": name})
    if r.status_code == 404:
        return "No Book found, Invalid Id"
    if r.status_code == 400:
        return "Out of stock"
    if r.status_code == 200:
        response = r.json()
        return "Bought Book '" + response["title"]+"'"
    else : return "ERROR try again later"
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
