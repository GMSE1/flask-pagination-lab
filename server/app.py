#!/usr/bin/env python3
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
from config import create_app, db, api
from models import Book, BookSchema

class Books(Resource):
    def get(self):
        # Step 1: Accept query parameters (default per_page = 5)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        # Step 2: Use .paginate() with error_out=False
        pagination = Book.query.paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )
        
        # Step 3: Return structured response with metadata
        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': [BookSchema().dump(book) for book in pagination.items]
        }, 200

# Register resource BEFORE creating app
api.add_resource(Books, '/books', endpoint='books')

# NOW create the app
env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

if __name__ == '__main__':
    app.run(port=5555, debug=True)