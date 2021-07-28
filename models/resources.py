from database import db


class Warehouse(db.Model):
    """Data model for inventory accounting of resources."""
    __tablename__ = 'wh'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    amount = db.Column(db.REAL)
    unit = db.Column(db.String)
    price = db.Column(db.REAL)
    cost = db.Column(db.REAL)
    date = db.Column(db.Date)

    def __init__(self, title, amount, unit, price, cost, date):
        self.title = title
        self.amount = amount
        self.unit = unit
        self.price = price
        self.cost = cost
        self.date = date

    def __repr__(self):
        return f"{self.id}: {self.title}"
