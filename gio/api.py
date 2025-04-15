from flask_restful import Resource, Api, fields, marshal_with
from flask_login import login_required
from models import Article, User, db

api = Api()

article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'author': fields.String(attribute=lambda x: x.author.email)
}

class ArticleAPI(Resource):
    @marshal_with(article_fields)
    def get(self):
        return Article.query.all()

    @login_required
    def post(self):
        # Реализация добавления статьи через API
        pass

api.add_resource(ArticleAPI, '/api/articles')