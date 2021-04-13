from datetime import datetime, date

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


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    amount = db.Column(db.REAL())
    unit = db.Column(db.String(50))
    cost = db.Column(db.REAL())
    date = db.Column(db.String())

    def __repr__(self):
        return "<Resource %s" % self.title


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "amount", "unit", "cost", "date")
        model = Post


class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            title=request.json['title'],
            amount=request.json['amount'],
            unit=request.json['unit'],
            cost=request.json['cost'],
            date=request.json['date']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


api.add_resource(PostListResource, '/resources')
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)