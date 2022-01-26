from flask import Flask, render_template, request
from .models import DB, User
from os import getenv
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():
    app = Flask(__name__)

    # Configuration variables
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect database to app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # Query all users in database
        return render_template('base.html', title='Home',
                               users=User.query.all())

    # @app.route('/populate')
    # # Test database functionality
    # def populate():
    #     add_or_update_user('austen')
    #     add_or_update_user('antoniogm')
    #     add_or_update_user('balajis')
        # DB.drop_all()
        # DB.create_all()
        # # Make two new users
        # ryan = User(id=1, username='ryanallred')
        # julian = User(id=2, username='julian')

        # # Make two tweets and attach to new users
        # tweet1 = Tweet(id=1, text="This is Ryan's tweet",
        #                user=ryan)
        # tweet2 = Tweet(id=2, text="This is Julian's tweet",
        #                user=julian)
        # tweet3 = Tweet(id=3, text="My first name is Ryan",
        #                user=ryan)
        # tweet4 = Tweet(id=4, text="My first name is Julian",
        #                user=julian)
        # tweet5 = Tweet(id=5, text="My surname is Allred",
        #                user=ryan)
        # tweet6 = Tweet(id=6, text="My surname is Edelman",
        #                user=julian)
        # tweet7 = Tweet(
        #     id=7, text="A pleasure to meet you, Mr. Edelman",
        #     user=ryan)
        # tweet8 = Tweet(id=8, text="Likewise, Mr. Allred",
        #                user=julian)

        # # Insert into database
        # DB.session.add(ryan)
        # DB.session.add(julian)
        # DB.session.add(tweet1)
        # DB.session.add(tweet2)
        # DB.session.add(tweet3)
        # DB.session.add(tweet4)
        # DB.session.add(tweet5)
        # DB.session.add(tweet6)
        # DB.session.add(tweet7)
        # DB.session.add(tweet8)

        # # Commit database changes
        # DB.session.commit()
        # return render_template('base.html', title='Populate')

    @app.route('/update')
    def update():
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html',
                               title='All users have been updated')

    @app.route('/reset')
    def reset():
        # Drop old database tables
        # Remake new database tables
        DB.drop_all()
        DB.create_all()
        return render_template('base.html',
                               title='Database has been reset')

    # User route is a more traditional API endpoint
    # Endpoint can only accept certain kinds of http requests
    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = f'User {username} successfully added!'
            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []
        return render_template('user.html', title=username,
                               tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'],
                              request.values['user1']])
        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user0, user1,
                                      request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}".format(
                request.values['tweet_text'],
                user1 if prediction else user0,
                user0 if prediction else user1)
        return render_template('/prediction.html', title='Prediction',
                               message=message)

    return app


def get_usernames():
    # Get all the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames
