from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from database import db
from flasgger import Swagger
from config import Config
from models.resources import Warehouse
from schema.resource import WarehouseSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = Config.DEBUG
ma = Marshmallow(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
warehouse_schema = WarehouseSchema()
warehouse_schemas = WarehouseSchema(many=True)


# Get all resources
@app.route('/resources', methods=['GET'])
def get_all_resources():
    all_resources = Warehouse.query.all()
    result = warehouse_schemas.dump(all_resources)

    return jsonify({'resources': result,
                    'total_count': len(result)}), 200


# Add resources
@app.route('/resources', methods=['POST'])
def add_resource():
    title = request.json['title']
    amount = request.json['amount']
    unit = request.json['unit']
    price = request.json['price']
    cost = request.json['cost']
    date = request.json['date']

    new_product = Warehouse(title, amount, unit, price, cost, date)

    db.session.add(new_product)
    db.session.commit()

    return warehouse_schema.jsonify(new_product), 201


# Update resource
@app.route('/resources/<id>', methods=['PUT'])
def update_resources(id):
    resource = Warehouse.query.get_or_404(id)

    title = request.json['title']
    amount = request.json['amount']
    unit = request.json['unit']
    price = request.json['price']
    cost = request.json['cost']
    date = request.json['date']

    resource.title = title
    resource.amount = amount
    resource.unit = unit
    resource.price = price
    resource.cost = cost
    resource.date = date

    db.session.commit()

    return warehouse_schema.jsonify(resource), 201


# Delete resource
@app.route('/resources/<id>', methods=['DELETE'])
def delete_resource(id):
    resource = Warehouse.query.get(id)
    db.session.delete(resource)
    db.session.commit()

    return warehouse_schema.jsonify(resource), 201


# total cost of orders on the warehouse
@app.route('/total_cost', methods=['GET'])
def get_total_cost():
    resources = Warehouse.query.all()
    total_cost = int(sum([cost.cost for cost in resources]))

    return jsonify({'total_cost': total_cost}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
