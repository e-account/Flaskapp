This is the readme.txt file for this flask app project:

This is a helpdesk ticketing application built using Python Flask and other related lightweight Python frameworks.
The application features the major CRUD operations for both user and admin accounts, allowing users to create new
accounts and tickets, view all current tickets and delete tickets, while admin accounts can view all users, update
user profiles, approve helpdesk request and delete both accounts and individual tickets.

There are some security features included within the code, whether that be objects that hold current logged in status
and username, validation checks to prevent breaching a page through its URL (as seen within OWASP as Broken Access
Control), and the ability only to create user accounts preventing security issues with non-trusted users gaining access
to administrator privileges.

For ease of access and for the purpose of the assignment, the database is a local lightweight SQLite database and is
accessed and interacted with, through the SQLAlchemy toolkit. The database has two tables with many relevant columns
with the two tables linked together through the Primary Key / Foreign Key pair being the username/userkey.

The application currently has three admin accounts available and seven user accounts, each user account has three
tickets on the system to meet the requirement of having at least ten records within the database. The accounts within
the current version of the database and an entity relationship diagram can be found below.

Basic readable naming conventions were used and help the code stay readable and followable, flask flash was used to
allow the application to notify the user of any major actions taking place and all major components of the program are
housed within its own section of the app.py file.

Heroku hosting has been set up using the Heroku CLI and gunicorn to help push the flaskapp through Github to Heroku.

Hosted website available here: https://flaskapp-deployment-084e8a3a3c3a.herokuapp.com/

extra notes:

The program was developed within PyCharm Community Edition 2025.2 x64

The requirements file was generated using the pip freeze command: (venv)... pip freeze

Within the terminal to set the main python application to run, execute the following code within the venv terminal:

set FLASK_APP=flaskapp.py
flask run

otherwise just run the program through the IDLE as it will execute through the code below found in the app.py file:

if __name__== '__main__'
app.run()



Accounts in database:
  Username   |    Password    |  Admin?  |
admin        |    password    |   Yes    |
newadx       |    pass123     |   Yes    |
testadmin    |    testpass    |   Yes    |
user1        |    passuser    |   No     |
user2        |    passuser    |   No     |
user3        |    passuser    |   No     |
user4        |    passuser    |   No     |
user5        |    passuser    |   No     |
user6        |    passuser    |   No     |
user7        |    passuser    |   No     |



Entity Relationship Diagram:

+-------------------------+             +-------------------------+
|           User          |             |         Ticket          |
+----------+--------------+             +----------+--------------+
|    id    |    int+*     |             |    id    |     int      |
+----------+--------------+             +----------+--------------+
| username | varchar(128) |+-----|      |   type   | varchar(128) |
+----------+--------------+      |      +----------+--------------+
| password | varchar(128) |      |      | tickname | varchar(128) |
+----------+--------------+      |      +----------+--------------+
| forename | varchar(128) |      |      |  reason  |    text      |
+----------+--------------+      |      +----------+--------------+
| surname  | varchar(128) |      |      | allowed  |   boolean    |
+----------+--------------+      |      +----------+--------------+
|  admin   |   boolean    |      |-----∞| userkey  | varchar(128) |
+-------------------------+             +-------------------------+

+ (one ) --- ∞ (many)

*int+ is just an incrementing int the size of python's 32 bit int variable
