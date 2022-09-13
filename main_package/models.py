# Imports
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin



# Initialize SQLAlchemy
db = SQLAlchemy()

# Define User data model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Define username and password for authentication purposes. Username must be unique.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information for profile purposes, not used in app logic.
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'),default=1)

# Define Tickets table for core application function
class Tickets(db.Model):
    __tablename__ = 'tickets'
    ticket_id = db.Column(db.Integer(), primary_key=True)
    uname = db.Column(db.String())
    contact = db.Column(db.String(50))
    priority = db.Column(db.Integer())
    description = db.Column(db.String())

