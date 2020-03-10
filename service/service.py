# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pet API Controller

This modules provides a REST API for the Pet Model

Paths:
------
GET /pets - Lists all of the Pets
GET /pets/{id} - Retrieves a single Pet with the specified id
POST /pets - Creates a new Pet
PUT /pets/{id} - Updates a single Pet with the specified id
DELETE /pets/{id} - Deletes a single Pet with the specified id
POST /pets/{id}/purchase - Action to purchase a Pet
"""

import os
import sys
import logging
from functools import wraps
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from service.models import Pet, DataValidationError
from service import app

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# DECORATORS
######################################################################
def requires_content_type(*content_types):
    """ Use this decorator to check content type """
    def decorator(func):
        """ Inner decorator """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """ Checks that the content type is correct """
            if not 'Content-Type' in request.headers:
                abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                      'Content-Type must be set')

            for content_type in content_types:
                if request.headers['Content-Type'] == content_type:
                    return func(*args, **kwargs)

            app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
            abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                  'Content-Type must be {}'.format(content_types))
        return wrapper
    return decorator

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Send back the home page """
    app.logger.info('Request for home page')
    return app.send_static_file('index.html')

######################################################################
# LIST ALL PETS
######################################################################
@app.route('/pets', methods=['GET'])
def list_pets():
    """ Returns all of the Pets """
    app.logger.info('Request for List Pets')
    pets = []
    category = request.args.get('category')
    name = request.args.get('name')
    available = request.args.get('available')
    if category:
        pets = Pet.find_by_category(category)
    elif name:
        pets = Pet.find_by_name(name)
    elif available:
        pets = Pet.find_by_availability(available)
    else:
        pets = Pet.all()

    results = [pet.serialize() for pet in pets]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A PET
######################################################################
@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pets(pet_id):
    """
    Retrieve a single Pet

    This endpoint will return a Pet based on it's id
    """
    app.logger.info('Request to get Pet with id %s', pet_id)
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, "Pet with id '{}' was not found.".format(pet_id))
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW PET
######################################################################
@app.route('/pets', methods=['POST'])
@requires_content_type('application/json', 'application/x-www-form-urlencoded')
def create_pets():
    """
    Creates a Pet

    This endpoint will create a Pet based the data in the body that is posted
    or data that is sent via an html form post.
    """
    app.logger.info('Request to create a Pet')
    data = {}
    # Check for form submission data
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        app.logger.info('Processing FORM data')
        data = {
            'name': request.form['name'],
            'category': request.form['category'],
            'available': request.form['available'].lower() in ['true', '1', 't']
        }
    else:
        app.logger.info('Processing JSON data')
        data = request.get_json()
    pet = Pet()
    pet.deserialize(data)
    pet.save()
    message = pet.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {'Location': url_for('get_pets', pet_id=pet.id, _external=True)})

######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route('/pets/<int:pet_id>', methods=['PUT'])
@requires_content_type('application/json')
def update_pets(pet_id):
    """
    Update a Pet

    This endpoint will update a Pet based the body that is posted
    """
    app.logger.info('Request to update Pet with id %s', pet_id)
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, "Pet with id '{}' was not found.".format(pet_id))
    pet.deserialize(request.get_json())
    pet.id = pet_id
    pet.save()
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PET
######################################################################
@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pets(pet_id):
    """
    Delete a Pet

    This endpoint will delete a Pet based the id specified in the path
    """
    app.logger.info('Request to delete Pet with id %s', pet_id)
    pet = Pet.find(pet_id)
    if pet:
        pet.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# PURCHASE A PET
######################################################################
@app.route('/pets/<int:pet_id>/purchase', methods=['PUT'])
def purchase_pets(pet_id):
    """ Purchase a Pet """
    app.logger.info('Request to purchase Pet with id %s', pet_id)
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, "Pet with id '{}' was not found.".format(pet_id))
    if not pet.available:
        abort(status.HTTP_400_BAD_REQUEST, "Pet with id '{}' is not available.".format(pet_id))
    pet.available = False
    pet.save()
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db(redis=None):
    """ Initlaize the model """
    Pet.init_db(redis)

# load sample data
def data_load(payload):
    """ Loads a Pet into the database """
    pet = Pet(0, payload['name'], payload['category'])
    pet.save()

def data_reset():
    """ Removes all Pets from the database """
    Pet.remove_all()

# def check_content_type(content_type):
#     """ Checks that the media type is correct """
#     if request.headers['Content-Type'] == content_type:
#         return
#     app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
#     abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))

# @app.before_first_request
def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print("************************************************************")
    print("        P E T   R E S T   A P I   S E R V I C E ")
    print("************************************************************")
    initialize_logging(app.config['LOGGING_LEVEL'])
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
