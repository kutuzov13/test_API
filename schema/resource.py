from flask_marshmallow import Schema
from models.resources import Warehouse


class WarehouseSchema(Schema):
    class Meta:
        fields = ('title', 'id', 'amount', 'unit', 'price', 'cost', 'date')
        model = Warehouse

