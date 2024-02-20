"""
This module defines a Flask application for managing contact information via a REST API. It
supports operations to create, retrieve, update, and delete contacts. Each contact is
represented by a first name, last name, and email address, stored in a database.

Available endpoints:
- GET /contacts: Retrieves all contacts.
- POST /create_contact: Creates a new contact with provided details.
- PATCH /update_contact/<int:user_id>: Updates details for a specific contact.
- DELETE /delete_contact/<int:user_id>: Deletes a specific contact.

Dependencies:
- Flask for the web framework.
- SQLAlchemy for ORM.
- Assumes availability of `config` module and `models.Contact` for database schema.
"""

from flask import request, jsonify
from config import app, db
from models import Contact
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@app.route("/contacts", methods=["GET"])
def get_contacts():
    """
    Retrieve all contacts from the database.

    This function queries the database for all contacts, converts each contact into JSON format,
    and returns a JSON response containing a list of contacts.

    Returns:
        A JSON response object containing a list of contacts, each represented as a JSON object.
    """
    contacts = Contact.query.all()
    json_contacts = list(map (lambda x: x.to_json(), contacts))
    return jsonify({"contacts":json_contacts})

@app.route("/create_contact", methods = ["POST"])
def create_contact():
    """
    Create a new contact record in the database.

    This function extracts 'firstName', 'lastName', and 'email' from the JSON request body.
    It validates the presence of these fields and then creates a new Contact record in the database.
    If any of the fields are missing, it returns a 400 Bad Request response.
    If the contact is successfully created, it returns a 201 Created response.

    Returns:
        A JSON response object. If a field is missing, it returns a message indicating the error and
        a 400 status code.
        On successful creation, it returns a success message and a 201 status code.
    """
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message":"You must include a first name, lasat name and email"}),
            400,
        )
    new_contact = Contact(first_name = first_name, last_name = last_name, email = email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Rollback the session to a clean state
        app.logger.error("IntegrityError: %s", "A contact with similar details already exists.")
        return jsonify({
            "message": "Integrity error: a contact with similar details already exists."
        }), 400
    except SQLAlchemyError:
        db.session.rollback()  # Rollback the session to avoid leaving it in a broken state
        app.logger.error("SQLAlchemyError occurred", exc_info=True)
        return jsonify({"message": "Database error occurred."}), 500
    return jsonify({"message": "User Created"}), 201

@app.route("/update_contact/<int:user_id>", methods = ["PATCH"])
def updata_contact(user_id):
    """
    Update an existing contact record in the database.

    This function looks up a contact by its user ID. If the contact is found, it updates the
    contact's first name, last name, and email with the values provided in the request JSON,
    if they are provided. If a field is not provided in the request, the current value is kept.
    If the contact is not found, it returns a 400 Bad Request response.

    Parameters:
        user_id (int): The ID of the user to update.

    Returns:
        A JSON response object. If the user is not found, it returns a message indicating
        the error and a 400 status code. On successful update, it returns a success message
        and a 200 status code.
    """
    contact = Contact.query.get(user_id)
    if not contact:
        return (jsonify({"message": "User not found"}),400)
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify({"User updates!!!"}),200

@app.route("/delete_contact/<int:user_id>", methods = ["DELETE"])
def delete_contact(user_id):
    """
    Delete a contact record from the database.

    This function looks up a contact by its user ID and deletes it from the database.
    If the contact is not found, it returns a 400 Bad Request response.

    Parameters:
        user_id (int): The ID of the user to delete.

    Returns:
        A JSON response object. If the user is not found, it returns a message indicating
        the error and a 400 status code. On successful deletion, it returns a success message
        and a 200 status code.
    """
    contact = Contact.query.get(user_id)
    if not contact:
        return (jsonify({"message": "User not found"}),400)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"User deleted!!!"}),200



if __name__ == "__main__":
    with app.app_context():
        # Creates model if it hasn't been created already
        db.create_all()
    app.run(debug=True)
