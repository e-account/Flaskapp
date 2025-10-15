# importing an instance of os
import os
# creates an instance of the classes listed below:
# flask is the main web interface building extension that includes myriad functions with other py extensions
from flask import Flask, redirect, flash, render_template, redirect, url_for, request
# a flask extension that helps with html
from flask_bootstrap import Bootstrap
# flask wtf and wtforms act as a more efficient way of producing flask forms with better functioning validations
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
# sqlalchemy is a lightweight sqlite database that skips the difficulties of hosting a database via the web
from flask_sqlalchemy import SQLAlchemy
# dotenv is a library used to help remove sensitive variables from the main code and place them inside a .env file
from dotenv import load_dotenv
# loading environment variables from the .env file
load_dotenv()
# main flask app constructors
app = Flask(__name__)
bootstrap = Bootstrap(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# CSRF secret key of random characters for security purposes
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
# sqlalchemy database pathway configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, os.getenv('DATABASE'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQL-TRACK-MOD')
# debug variable held within .env file
Debug = os.getenv('DEBUG')
# database object constructor
db = SQLAlchemy(app)
# Object to hold the current logged in user and checks whether the user is actively logged on
log = False
adlog = False
current = ''


# constructor class to create Menu class
class MainMenu(FlaskForm):
    signup = SubmitField('signup')
    login = SubmitField('login')


# constructor class to create Signup class
class Signup(FlaskForm):
    # each object has the validator that requires all user inputs for the form to be submitted, with an updated regexp to prevent specific character inputs
    username = StringField('Input Username:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    password = StringField('Input Password:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    forename = StringField('Input Forename:', validators=[DataRequired(), Length(min=2, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    surname = StringField('Input Surname:', validators=[DataRequired(), Length(min=2, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    submit = SubmitField('Submit')


# constructor class to create Signup class
class Login(FlaskForm):
    # each object has the validator that requires all user inputs for the form to be submitted, with an updated regexp to prevent specific character inputs
    username = StringField('Input Username:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    password = StringField('Input Password:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    submit = SubmitField('Submit')


# constructor class to create UserMenu class
class UserMenu(FlaskForm):
    newticket = SubmitField('New Ticket')
    viewticket = SubmitField('View Tickets')
    logout = SubmitField('Log Out')


# constructor class to create AdminMenu class
class AdminMenu(FlaskForm):
    viewticket = SubmitField('View Tickets')
    viewusers = SubmitField('View Users')
    logout = SubmitField('Log Out')


# constructor class to create Ticket Creation class, with an updated regexp to prevent specific character inputs
class HelpTicket(FlaskForm):
    type = SelectField('Vendor Selection:', choices=[('software', 'software'),
                                                     ('hardware', 'hardware'), ('error', 'error')], default='software')
    tickname = StringField('Title of Request:', validators=[DataRequired(), Length(min=2, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    reason = TextAreaField('Explanation of Request:', validators=[DataRequired()])
    submit = SubmitField('Submit')


# constructor class to create Ticket Approval class
class ApproveTicket(FlaskForm):
    approve = SubmitField('approve')


# constructor class to create Ticket Deletion class
class DeleteTicket(FlaskForm):
    delete = SubmitField('Submit')


# constructor class to create User Edit class, with an updated regexp to prevent specific character inputs
class EditUser(FlaskForm):
    username = StringField('Change Username:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    password = StringField('Change Password:', validators=[DataRequired(), Length(min=5, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    forename = StringField('Change Forename:', validators=[DataRequired(), Length(min=2, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    surname = StringField('Change Surname:', validators=[DataRequired(), Length(min=2, max=128),
        Regexp('^[a-zA-Z0-9 -_]+$', message='Input field can only contain alphanumeric characters, dashes and underscores')])
    submit = SubmitField('Submit')


# constructor class to create Delete User class
class DeleteUser(FlaskForm):
    delete = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    # a unique auto-incrementing value that acts as primary identification
    id = db.Column(db.Integer, primary_key=True)
    # user data will not all for empty data inputs and has to be unique, characteristics important to usernames
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    forename = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    # back-referenced link between User and Tickets to allow for easier object references
    tickets = db.relationship('Ticket', backref='user')

    # __repr__ returns a string of the accessed object which helps when viewing the database
    def __repr__(self):
        return f'<User: {self.username}, Is Admin: {self.admin}>'


class Ticket(db.Model):
    __tablename__ = 'tickets'
    # a unique auto-incrementing value that acts as primary identification
    id = db.Column(db.Integer, primary_key=True)
    # Help desk data fields that will be found within the tickets
    type = db.Column(db.String(128), nullable=False)
    tickname = db.Column(db.String(128), nullable=False)
    reason = db.Column(db.Text)
    # the ticket will be set to False on creation and then will be able to be allowed by admin users later on
    allowed = db.Column(db.Boolean, default=False, nullable=False)

    # linking two of the classes together with users.usernames as the primary key
    userkey = db.Column(db.String(128), db.ForeignKey('users.username'))

    # __repr__ returns a string of the accessed object which helps when viewing the database
    def __repr__(self):
        return f'<User: {self.userkey}, Ticket No. {self.id}, Type: {self.type}, Reason: {self.reason}>'


# Shell integration for database instances that makes it easier to recall the objects and debug the database
@app.shell_context_processor
def make_shell_context():
    # dictionary key terms for shell interfacing with the database
    return dict(db=db, User=User, Ticket=Ticket)

# creates application instance for '/'
@app.route('/', methods=['GET', 'POST'])
def main():
    # using global variables that are reset when accessing main, this is the ensure logged out users can't log back in
    global log, adlog, current
    log = False
    adlog = False
    current = ''
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: Main Menu'
    form = MainMenu()
    if form.validate_on_submit():  # menu to allow users to signup or login to the system
        if request.method == 'POST':
            if 'signup' in request.form:
                return redirect('/signup')
            if 'login' in request.form:
                return redirect('/login')
    return render_template('menu.html', form=form, title=title)


# creates application instance for '/signup'
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: Signup'
    form = Signup()
    if form.validate_on_submit():
        # user search query for checking against a new user creation form input
        user_search = User.query.filter_by(username=form.username.data).first()
        # user role is creating a constructor to pass User from the Roles table
        if user_search is None:
            # if the query doesn't return a match the user input in the field will create a new user account
            a_user = User(username=form.username.data, password=form.password.data,
                          forename=form.forename.data, surname=form.surname.data,
                          admin=False)  # admin can only be set to false in signup to avoid unwanted admin privileges
            db.session.add(a_user)
            db.session.commit()
            flash("New account created")
            return redirect('/login')
        else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
            flash("Incorrect signup details")
            return redirect('/signup')
    return render_template('menu.html', form=form, title=title)


# creates application instance for '/login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    # using global variable to check whether user has logged on to prevent faulty access
    global log, adlog, current
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: Login'
    form = Login()
    # queries to check whether a user exists and whether a user is an admin
    login_query = User.query.filter(User.username.in_([form.username.data]),
                                    User.password.in_([form.password.data])).first()
    admin_query = User.query.filter(User.username.in_([form.username.data]),
                                    User.password.in_([form.password.data]), User.admin == True).first()
    if form.validate_on_submit():  # validation of login menu
        if login_query is not None:
            current = form.username.data
            if admin_query is not None:
                adlog = True
                return redirect(url_for('admin', users=form.username.data))
            else:
                log = True
                return redirect(url_for('user', users=form.username.data))
        else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
            flash("Incorrect login details provided")
            return redirect('/login')
    return render_template('menu.html', form=form, title=title)


# creates application instance for the navbar menu interaction
@app.route('/rerouting', methods=['GET', 'POST'])
def reroute():
    global log, adlog, current
    # rerouting webpage that will send the user to the correct home page depending on their logged in status
    if log:
        # if user then go to the user homepage
        return redirect(url_for('user', users=current))
    elif adlog:
        # if admin then go to the user homepage
        return redirect(url_for('admin', users=current))
    else:
        # if the user of the webpage tries to type in the url to this page it will send them back to the main page
        flash("You are currently not logged in")
        current = ''
        return redirect(url_for('main'))


# creates application instance for '/users/username'
@app.route('/user/<string:users>', methods=['GET', 'POST'])
def user(users):
    # using global variable to check whether user has logged on to prevent faulty access
    global log, current
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: User'
    form = UserMenu()
    # querying the sqlalchemy database whether the passed username exists, so only logged in users can access
    user_query = User.query.filter(User.username.in_([users])).first()
    if user_query is not None:
        if log:
            if form.validate_on_submit():  # validation of user homepage
                if 'newticket' in request.form:
                    return redirect(url_for('create', users=users))
                elif 'viewticket' in request.form:
                    return redirect(url_for('view', users=users))
                elif 'logout' in request.form:
                    log = False
                    flash("You've logged out successfully")
                    return redirect(url_for('main'))
            # render template won't run if the global log variable hasn't been activated
            return render_template('menu.html', form=form, title=title)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        current = ''
        return redirect(url_for('main'))


# creates application instance for 'admin/username' separating admin and user profiles to protect from bad actors
@app.route('/admin/<string:users>', methods=['GET', 'POST'])
def admin(users):
    # using global variable to check whether user has logged on to prevent faulty access
    global adlog, current
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: Admin'
    form = AdminMenu()
    # querying the sqlalchemy database whether the passed username exists, so only logged in admins can access
    admin_query = User.query.filter(User.username.in_([users]), User.admin == True).first()
    if admin_query is not None:
        if adlog:
            if form.validate_on_submit():  # validation of admin homepage
                if 'viewticket' in request.form:
                    return redirect(url_for('view', users=users))
                elif 'viewusers' in request.form:
                    return redirect(url_for('viewuser', users=users))
                elif 'logout' in request.form:
                    adlog = False
                    flash("You've logged out successfully")
                    return redirect(url_for('main'))
            # render template won't run if the global adlog variable hasn't been activated
            return render_template('menu.html', form=form, title=title)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        current = ''
        return redirect(url_for('main'))


# creates application instance for '/user/username/create_ticket' allowing for new tickets to be made
@app.route('/user/<string:users>/create_ticket', methods=['GET', 'POST'])
def create(users):
    # using global variable to check whether user has logged on to prevent faulty access
    global log
    # title object will allow to reuse the menu.html to be more efficient rather than have myriad menu pages
    title = 'Helpdesk: New Ticket'
    form = HelpTicket()
    if log:
        if form.validate_on_submit():
            a_ticket = Ticket(type=form.type.data, tickname=form.tickname.data,
                              reason=form.reason.data, userkey=current, allowed=False)
            db.session.add(a_ticket)
            db.session.commit()
            # ticket userkey was set to the current logged in user which will store all tickets under same account
            flash('New ticket created')
            return redirect(url_for('reroute'))
        return render_template('menu.html', form=form, title=title, current=current)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        return redirect(url_for('main'))


# creates application instance for '/tickets/username' where tickets assigned to each user will be shown
@app.route('/tickets/<string:users>')
def view(users):
    # using the global variables adlog and log to check whether the user is an admin or not
    global log, adlog, current
    title = 'Helpdesk: View Tickets'
    if adlog:
        tickets = Ticket.query.filter(Ticket.id).all()  # database query to show all tickets in the database (admin)
        return render_template('viewticket.html', tickets=tickets, users=users, title=title)
    if log:
        tickets = Ticket.query.filter(Ticket.userkey == current)  # database query to show user's current tickets
        return render_template('viewticket.html', tickets=tickets, users=users, title=title)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        return redirect(url_for('main'))


# creates and application instance for '/tickets/<string:users>/<string:id>' where admins and users can view tickets
@app.route('/tickets/<string:users>/<string:id>', methods=['GET', 'POST'])
def viewtickets(users, id):
    global log, adlog, current
    form1 = ApproveTicket()
    form2 = DeleteTicket()
    ticketed = Ticket.query.filter_by(id=id).first()
    title = 'Helpdesk: Ticket No.' + id
    if log or adlog:
        if form1.validate_on_submit():
            if 'approve' in request.form:
                ticketed.allowed = True
                db.session.add(ticketed)
                db.session.commit()
                flash("Ticket approved")
        if form2.validate_on_submit():
            if 'delete' in request.form:
                db.session.delete(ticketed)
                db.session.commit()
                return redirect(url_for("reroute"))  # reroutes to main menu once ticket is deleted
        return render_template('viewtickets.html', ticketed=ticketed, title=title, log=log, adlog=adlog,
                               form1=form1, form2=form2)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        return redirect(url_for('main'))


# creates application instance for '/admin/<string:users>/viewuser' where admins will be able to view all user accounts
@app.route('/admin/<string:users>/viewuser')
def viewuser(users):
    # using global variable to check whether user has logged on to prevent faulty access
    global adlog, current
    title = 'Helpdesk: View User'
    used = User.query.filter(User.admin == False)
    if adlog:
        return render_template('viewuser.html', used=used, users=users, title=title)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        return redirect(url_for('main'))


# creates application instance for '/admin/<string:users>/viewuser/<string:id>'where admins can view a single account
@app.route('/admin/<string:users>/viewuser/<string:id>', methods=['GET', 'POST'])
def viewusers(users, id):
    # using global variable to check whether user has logged on to prevent faulty access
    global adlog
    form1 = EditUser()
    form2 = DeleteUser()
    used = User.query.filter_by(id=id, admin=False).first()
    user_search = User.query.filter_by(username=form1.username.data).first()
    username = used.username
    title = 'Helpdesk: View ' + username
    if adlog:
        if used:
            if form1.validate_on_submit():  # validation of editing account
                if user_search is None:  # updates each input with the new information inputted by admin
                    used.username = form1.username.data
                    used.password = form1.password.data
                    used.forename = form1.forename.data
                    used.surname = form1.surname.data
                    db.session.add(used)
                    db.session.commit()
                    flash("User updated")
                else:
                    flash("Invalid or pre-existing username")
            if form2.validate_on_submit():  # validation of deleting account
                if 'delete' in request.form:
                    delete_user = User.query.filter_by(id=id, admin=False).first()
                    db.session.delete(delete_user)  # deletes the selected user
                    db.session.commit()
                    delete_tickets = Ticket.query.filter(Ticket.userkey == username).all()
                    for x in delete_tickets:
                        # deletes each ticket in the delete_tickets query so no unlinked tickets are left in db
                        db.session.delete(x)
                        db.session.commit()
                    flash("User account and related tickets deleted")
                    return redirect(url_for("reroute"))  # reroutes to main menu once account is deleted
            return render_template('viewusers.html', used=used, title=title, form1=form1, form2=form2)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        flash("You are currently not logged in")
        return redirect(url_for('main'))


# creates a route to the about page for the
@app.route('/about')
def about():
    return render_template('about.html')


# command that runs application in debug mode
if __name__ == '__main__':
    app.run(debug=Debug)
