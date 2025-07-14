import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, create_staff, create_student, log_review, create_upvote, create_downvote, get_all_users_json, get_all_users )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff('Nicholas Mendez', 'mendezpass', 'nicholasmendez@gmail.com')
    create_staff('Kwasi Edwards', 'kwasipass', 'kwasiedwards@gmail.com')
    create_staff('Amit Ramkissoon', 'amitpass', 'amitramkissoon@gmail.com')
    create_staff('Daniel Rasheed', 'danpass', 'danielrasheed@gmail.com')
    create_staff('Joshua Mathura', 'joshpass', 'joshuamathura@gmail.com')

    create_student('Nicholas Pariag', 'nickpass', 'nicholaspariag@gmail.com')
    create_student('Jason Balroop', 'jasonpass', 'jasonbalroop@gmail.com')
    create_student('Chris Hemsworth', 'chrispass', 'chrishemsworth@gmail.com')
    create_student('Kyle Samlal', 'kylepass', 'kylesamlal@gmail.com')
    create_student('Jardel Mitchell', 'jardelpass', 'jardelmitchell@gmail.com')
    create_student('Caleb Ramdath', 'calebpass', 'calebramdath@gmail.com')

    log_review(2, 7, 'Always attentive in class and willing to help peers.')
    log_review(2, 8, 'Shows great leadership during group assignments.')

    log_review(3, 7, 'Submits assignments early and with excellent quality.')
    log_review(3, 9, 'Very respectful and professional in all interactions.')

    log_review(4, 8, 'A consistent top performer who takes feedback seriously.')
    log_review(4, 9, 'Average performance, but potential to improve.')
    log_review(4, 10, "Often misses deadlines and ignores instructions.")
    
    log_review(5, 10, 'Usually quiet in class — hard to evaluate participation.')
    log_review(5, 11, 'Work is inconsistent: sometimes great, other times rushed.')
    log_review(5, 12, "Shows little interest in collaborating during group work.")

    log_review(6, 11, 'Tries hard but needs more confidence and clarity.')
    log_review(6, 12, "Follows instructions but doesn't go beyond the basics.")
    
    create_upvote(2, 1)
    create_upvote(2, 2)
    create_upvote(2, 3)
    create_upvote(2, 6)
    create_downvote(2, 4)

    create_upvote(3, 1)
    create_upvote(3, 2)
    create_upvote(3, 5)
    create_upvote(3, 3)
    create_upvote(3, 8)
    create_downvote(3, 4)

    create_upvote(4, 2)
    create_upvote(4, 3)
    create_upvote(4, 5)
    create_upvote(4, 6)
    create_upvote(4, 7)
    create_upvote(4, 9)
    create_downvote(4, 1)
    
    create_upvote(5, 2)
    create_upvote(5, 5)
    create_upvote(5, 7)
    create_upvote(5, 8)
    create_upvote(5, 10)
    create_downvote(5, 6)

    create_upvote(6, 3)
    create_upvote(6, 5)
    create_upvote(6, 11)
    create_upvote(6, 12)
    create_downvote(6, 2)

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)