"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_the_member(member_id):
    the_member = jackson_family.get_member(member_id)
    if the_member:
       return jsonify(the_member), 200
    else:
       return jsonify({'msg': 'Member not found'}), 404



@app.route('/members/<int:member_id>', methods= ['DELETE'])
def delete_member(member_id):
   member_deleted = jackson_family.delete_member(member_id)
   if member_deleted:
       return jsonify({"done":True, 'Member deleted': member_deleted}),200
   else:
       return jsonify({'msg': 'Member not found'}), 404
   



@app.route('/members', methods= ['POST'])
def add_member():
    #pedir en el body "nombre", "edad" y "luky numbers"
    #si el usuario nos da el ID lo asignamos y sino lo generamos
    body = request.get_json(silent= True) #(silent= True) sirve para manejar errores 
                                          #si el usuario no envia el body

    if body is None:
        return jsonify({'msg':'Debe añadir un body'}),400
    if 'first_name' not in body:
        return jsonify({'msg':'El campo first_name es obligatorio!'}),400
    if 'age' not in body:
        return jsonify({'msg':'El campo age es obligatorio!'}),400
    if 'lucky_numbers' not in body:
        return jsonify({'msg':'El campo lucky_numbers es obligatorio!'}),400
    id = None
    if 'id' not in body:
        id = jackson_family._generate_id()
    else:
        id = body['id']
    new_member = {
        'id':id,
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }
    jackson_family.add_member(new_member)

    return jsonify({'msg':'OK', 'new_member': new_member}), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
