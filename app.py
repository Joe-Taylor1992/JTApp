#       DWP - PBMIS Application Fault Logging System 
#
# Application is designed to log information surrounding issues with
# the DWP application 'PBMIS'. Features include CRUD operations to
# log tickets, and a user structure with 'Admin' and 'Agent' roles.
#
# 






# Imports
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_user import login_required, roles_required, UserManager
from flask_user.signals import user_registered
import sqlite3 as sql
from config import ConfigClass




def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Import database models from models.py
    from main_package.models import db, User, UserRoles, Tickets, Role

    db.app = app
    db.init_app(app)

    # Define user_manager
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    # Import test data if necessary
    from dataload import dataload



    # Upon registration assigns Agent role as default
    @user_registered.connect_via(app)
    def _after_reg_hook(sender, user, **extra):
        role = Role.query.filter_by(name='Agent').one()
        user.roles.append(role)
        db.session.commit()
        return

    # Home page
    @app.route('/')
    def home_page():
        return render_template("home.html")

    # Ticket index route
    @app.route("/index")
    @login_required
    def index():
        con=sql.connect("pbmisdata.sqlite")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from tickets")
        data=cur.fetchall()
        return render_template("index.html",datas=data)

    # User index route
    @app.route("/userindex")
    @login_required
    def userindex():
        con=sql.connect("pbmisdata.sqlite")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from users LEFT JOIN user_roles on user_roles.user_id = users.id LEFT JOIN roles on user_roles.role_id = roles.id;")
        data=cur.fetchall()
        return render_template("userindex.html",datas=data)


    # Route accessed to add ticket to database
    @app.route("/add_ticket",methods=['POST','GET'])
    @login_required
    def add_ticket():
        if request.method=='POST':
            uname=request.form['uname']
            contact=request.form['contact']
            priority=request.form['priority']
            description=request.form['description']
            con=sql.connect("pbmisdata.sqlite")
            cur=con.cursor()
            cur.execute("insert into tickets(UNAME,CONTACT,PRIORITY,DESCRIPTION) values (?,?,?,?)",(uname,contact,priority,description))
            con.commit()
            flash('Ticket Added','success')
            return redirect(url_for("index"))
        return render_template("add_ticket.html")


    # Route accessed to delete ticket from database    
    @app.route("/delete_ticket/<string:ticket_id>",methods=['GET'])
    @roles_required('Admin')
    def delete_ticket(ticket_id):
        con=sql.connect("pbmisdata.sqlite")
        cur=con.cursor()
        cur.execute("delete from tickets where TICKET_ID=?",(ticket_id))
        con.commit()
        flash('Ticket Deleted','warning')
        return redirect(url_for("index"))


    # Route accessed to delete a user from the database
    @app.route("/delete_user/<string:id>",methods=['GET'])
    @roles_required('Admin')
    def delete_user(id):
        con=sql.connect("pbmisdata.sqlite")
        cur=con.cursor()
        cur.execute("delete from USERS where ID=?",(id,))
        con.commit()
        flash('User Deleted','warning')
        return redirect(url_for("userindex"))


    # Route accessed to edit an already existing ticket
    @app.route("/edit_ticket/<string:ticket_id>",methods=['POST','GET'])
    @login_required
    def edit_ticket(ticket_id):
        if request.method=='POST':
            uname=request.form['uname']
            contact=request.form['contact']
            priority=request.form['priority']
            description=request.form['description']
            con=sql.connect("pbmisdata.sqlite")
            cur=con.cursor()
            cur.execute("update tickets set UNAME=?,CONTACT=?,PRIORITY=?,DESCRIPTION=? where TICKET_ID=?",(uname,contact,priority,description,ticket_id))
            con.commit()
            flash('Ticket Updated','success')
            return redirect(url_for("index"))
        con=sql.connect("pbmisdata.sqlite")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from tickets where TICKET_ID=?",(ticket_id,))
        data=cur.fetchone()
        return render_template("edit_ticket.html",datas=data)


    # Route accessed to edit an already existing user
    @app.route("/edit_user/<string:id>",methods=['POST','GET'])
    @login_required
    def edit_user(id):
        if request.method=='POST':
            username=request.form['username']
            con=sql.connect("pbmisdata.sqlite")
            cur=con.cursor()
            cur.execute("update users set USERNAME=? where ID=?",(username,id))
            con.commit()
            flash('User Updated','success')
            return redirect(url_for("userindex"))
        con=sql.connect("pbmisdata.sqlite")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from users where ID=?",(id,))
        data=cur.fetchone()
        return render_template("edit_user.html",datas=data)


    # Route accessed to edit the role for an existing user
    @app.route("/edit_role/<string:user_id>",methods=['POST','GET'])
    @roles_required('Admin')
    def edit_role(user_id):
        if request.method=='POST':
            role_id=request.form['role_id']
            con=sql.connect("pbmisdata.sqlite")
            cur=con.cursor()
            cur.execute("update user_roles set ROLE_ID=? where USER_ID=?",(role_id,user_id))
            con.commit()
            flash('Role Updated','success')
            return redirect(url_for("userindex"))
        con=sql.connect("pbmisdata.sqlite")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from user_roles where USER_ID=?",(user_id,))
        data=cur.fetchone()
        return render_template("edit_role.html",datas=data)

    return app


# Start web server
if __name__=='__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=True)