from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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


class ResourcesModel(db.Model):
    __tablename__ = 'test_api'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.REAL())
    unit = db.Column(db.String())
    cost = db.Column(db.REAL())
    date = db.Column(db.Date())

    def __init__(self, title, unit, cost, date):
        self.title = title
        self.unit = unit
        self.cost = cost
        self.date = date

    def __repr__(self):
        return "<Resource %s" % self.title


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post


class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            title=request.json['title'],
            content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(PostListResource, '/posts')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)