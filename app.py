from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


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
    @staticmethod
    def get():
        warehouse = Warehouse.query.all()
        return {'resources': posts_schema.dump(warehouse), 'total_count': len(posts_schema.dump(warehouse))}

    @staticmethod
    def post():
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

    @staticmethod
    def patch(resource_id):
        resource = Warehouse.query.get_or_404(resource_id)

        if 'title' in request.json:
            resource.title = request.json['title']
        if 'amount' in request.json:
            resource.amount = request.json['amount']
        if 'unit' in request.json:
            resource.unit = request.json['unit']
        if 'price' in request.json:
            resource.price = request.json['price']
        if 'date' in request.json:
            resource.date = request.json['date']

        db.session.commit()
        return post_schema.dump(resource)

    @staticmethod
    def delete(resource_id):
        post = Warehouse.query.get_or_404(resource_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


class WarehouseTotalResource(Resource):
    @staticmethod
    def get():
        resources = Warehouse.query.all()
        return {'total_cost': len(posts_schema.dump(resources))}


api.add_resource(WarehouseListResource, '/resources', '/resources/<int:resource_id>')
api.add_resource(WarehouseTotalResource, '/total_cost')
post_schema = WarehouseSchema()
posts_schema = WarehouseSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
