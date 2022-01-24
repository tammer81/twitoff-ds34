from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():
    app = Flask(__name__)

    # Configuration variables
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect database to app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        users = User.query.all()
        print(users)
        return render_template('base.html', title='Home', users=users)

    @app.route('/populate')
    # Test database functionality
    def populate():
        DB.drop_all()
        DB.create_all()
        # Make two new users
        ryan = User(id=1, username='ryanallred')
        julian = User(id=2, username='julian')

        tweet1 = Tweet(id=1, text="This is Ryan's tweet", user=ryan)
        tweet2 = Tweet(id=2, text="This is Julian's tweet", user=julian)

        # Insert into database
        DB.session.add(ryan)
        DB.session.add(julian)
        DB.session.add(tweet1)
        DB.session.add(tweet2)

        DB.session.commit()
        return render_template('base.html', title='Populate')

        # Make two tweets and attach to new users

    @app.route('/reset')
    def reset():
        # Drop old database tables
        # Remake new database tables

        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    return app
