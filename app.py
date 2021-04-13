from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# resources = [
#     {
#         "resources": [
#             {
#                 "title": "res_1",
#                 "id": 0,
#                 "amount": 100,
#                 "unit": "kg",
#                 "price": 15,
#                 "cost": 1500,
#                 "date": "2022-02-12"
#             },
#             {
#                 "title": "res_2",
#                 "id": 1,
#                 "amount": 32,
#                 "unit": "liter",
#                 "price": 10,
#                 "cost": 320,
#                 "date": "2022-02-12"
#             }
#         ],
#         "total_count": 2
#     }
# ]


class Warehouse(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    amount = db.Column(db.REAL())
    unit = db.Column(db.String(50))
    price = db.Column(db.REAL())
    date = db.Column(db.String(50))

    def __repr__(self):
        return "<Resource %s" % self.title


class WarehouseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'price', 'date', 'title', 'unit')
        model = Warehouse


class WarehouseListResource(Resource):
    def get(self):
        warehouse = Warehouse.query.all()
        return posts_schema.dump(warehouse)

    def post(self):
        new_resource = Warehouse(
            title=request.json['title'],
            amount=request.json['amount'],
            unit=request.json['unit'],
            price=request.json['price'],
            date=request.json['date']
        )
        db.session.add(new_resource)
        db.session.commit()
        return post_schema.dump(new_resource)


class WarehouseResource(Resource):
    def get(self):
        resources = Warehouse.query.all()
        return len(posts_schema.dump(resources))

    def update(self, post_id):
        resource = Warehouse.query.get_or_404(post_id)

        if 'title' in request.json:
            resource.title = request.json['title']
        if 'amount' in request.json:
            resource.content = request.json['amount']
        if 'unit' in request.json:
            resource.content = request.json['unit']
        if 'price' in request.json:
            resource.content = request.json['price']
        if 'date' in request.json:
            resource.content = request.json['date']

        db.session.commit()
        return post_schema.dump(resource)

    def delete(self, post_id):
        post = Warehouse.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(WarehouseResource, '/total_cost')
api.add_resource(WarehouseListResource, '/resources')
post_schema = WarehouseSchema()
posts_schema = WarehouseSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)