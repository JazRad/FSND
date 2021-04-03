import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(token):
    drink_detail = Drink.query.all()
    formatted_drink_detail = [drink.long() for drink in drink_detail]

    return jsonify({
        "success": True,
        "drinks": formatted_drink_detail
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    body = request.get_json()

    drink_title = body.get('title')
    drink_recipe = body.get('recipe', [])

    if (drink_title is None
            or drink_recipe is None):

        abort(422)

    else:
        if type(drink_recipe) != list:
            drink_recipe = [drink_recipe]

        try:
            drink = Drink(title=drink_title,
                          recipe=json.dumps(drink_recipe))

            drink.insert()

            return jsonify({
                "success": True,
                "drinks": drink.long()
            }), 200

        except NoResultFound:
            abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(token, drink_id):
    body = request.get_json()

    response_drink_id = body.get('id')
    drink_title = body.get('title', None)
    drink_recipe = body.get('recipe', None)

    drink = Drink.query.get(drink_id)

    if 'title' in body:
        drink.title = body.get('title', None)

    if 'recipe' in body:
        drink.recipe = json.dumps(drink_recipe)

    try:
        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200

    except NoResultFound:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, drink_id):
    body = request.get_json()

    drink = Drink.query.get(drink_id)

    try:
        drink.delete()
        return jsonify({
            "success": True,
            "delete": drink_id
        }), 200

    except NoResultFound:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''


@app.errorhandler(400)
def method_error(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Unprocessable entity'
    }), 400


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'A bad request made. Resource not found'
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def not_authorised(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
