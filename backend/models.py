"""
This module defines the Contact model using SQLAlchemy for a Flask application.

The Contact model represents contact information within the application, supporting
operations like creating, reading, updating, and deleting contacts. Each contact
includes a unique identifier, first name, last name, and an email address which is
enforced to be unique across all contacts.

Functions:
- to_json: Serializes the Contact object to a JSON-compatible dictionary for API responses.
"""

from config import db
# pylint: disable=R0903
class Contact(db.Model):
    """
    Contact model for storing contact information.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact, not required to be unique.
        last_name (str): Last name of the contact, not required to be unique.
        email (str): Email address of the contact, required to be unique.

    The Contact model uses SQLAlchemy's ORM features for database interactions.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_json(self):
        """
        Serializes the Contact object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary with the contact's id, first name, last name, and email.
        """
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
