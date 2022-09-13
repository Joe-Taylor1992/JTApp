#Imports
from flask_user import UserManager, user_manager
from main_package.models import db, User, UserRoles, Tickets, Role
from flask import Flask
from config import ConfigClass

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

db.app = app
db.init_app(app)

user_manager = UserManager(app, db, User)

# Class defined to import into app.py
class dataload():
    # Add a user called 'member' with the role 'Agent'
    if not User.query.filter(User.username == 'member').first():
        user = User(
            username='member',
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()

    # Add a user called 'admin' with the role 'Admin'
    if not User.query.filter(User.username == 'admin').first():
        user = User(
            username='admin',
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Admin'))
        db.session.add(user)
        db.session.commit()

    # Add a ticket
    if not Tickets.query.filter(Tickets.ticket_id == '1').first():
        tickets = Tickets(
            uname='Joe Bloggs',
            contact='joe.bloggs@email.com',
            priority='1',
            description='This is test data for the description field.'
        )
        db.session.add(tickets)
        db.session.commit()

    # Add a ticket with a longer description to stress test the description field
    if not Tickets.query.filter(Tickets.ticket_id == '2').first():
        tickets = Tickets(
            uname='Ticket Tester',
            contact='ticket.tester@email.com',
            priority='10',
            description='This is longer test data for the description field. This is longer test data for the description field. This is longer test data for the description field.'
        )
        db.session.add(tickets)
        db.session.commit()
