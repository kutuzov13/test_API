from flask import Flask
from flask_restful import Api, reqparse
from flask import jsonify
import postgresql

app = Flask(__name__)
api = Api(app)

resources = [
    {
        "resources": [
            {
                "title": "res_1",
                "id": 0,
                "amount": 100,
                "unit": "kg",
                "price": 15,
                "cost": 1500,
                "date": "2022-02-12"
            },
            {
                "title": "res_2",
                "id": 1,
                "amount": 32,
                "unit": "liter",
                "price": 10,
                "cost": 320,
                "date": "2022-02-12"
            }
        ],
        "total_count": 2
    }
]


@app.route('/resources', methods=['GET'])
def get_all_resources():
    if resources:
        return jsonify(resources)
    return "Not Found"


@app.route('/resources', methods=['POST'])
def post(id_resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title")
    parser.add_argument("amount")
    parser.add_argument("unit")
    parser.add_argument("price")
    parser.add_argument("date")
    params = parser.parse_args()
    for res in resources:
        if id_resource == res["id"]:
            return f"Resource with id {id_resource} already exists", 400
    resource = {
        "author": params["title"],
        "id": int(id_resource),
        "amount": params["amount"],
        "unit": params["unit"],
        "price": params["price"],
        "date": params["date"]
    }
    resources.append(resource)
    return jsonify(resource)


@app.route('/resources', methods=['UPDATE'])
def update(id_resource):
    parser = reqparse.RequestParser()
    parser.add_argument("author")
    parser.add_argument("quote")
    params = parser.parse_args()
    for res in resources:
        if id_resource == res["id"]:
            res["author"] = params["author"]
            res["quote"] = params["quote"]
            return res, 200

    resource = {
        "author": params["title"],
        "id": int(id_resource),
        "amount": params["amount"],
        "unit": params["unit"],
        "price": params["price"],
        "date": params["date"]
    }

    resources.append(resource)
    return jsonify(resource)


@app.route('/resources', methods=['DELETE'])
def delete(id_resource):
    ai_quotes = [resource for resource in resources if resource["id"] == id_resource]
    return jsonify(f"Resource with id {id_resource} is deleted.")


@app.route('/total_cost', methods=['GET'])
def total():
    return jsonify(resources[0]['total_count'])


if __name__ == '__main__':
    api = Api(app)
    app.run(debug=True)