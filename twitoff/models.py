from flask_sqlalchemy import SQLAlchemy

# Create a database object
DB = SQLAlchemy()

# Create a table with specific schema
# Create a python class


class User(DB.Model):
    # Two columns inside of user table
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Username column schema
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)


class Tweet(DB.Model):
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Text column schema
    text = DB.Column(DB.Unicode(300), nullable=False)
    # User column schema (secondary/foreign key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    # Establish relationship between tweets and users
    # Will automatically create one-to-many relationship
    # Will also add new attribute to User class "tweets"
    # Which will be list of all user tweets
    user = DB.relationship("User", backref=DB.backref('tweets'),
                           lazy=True)
    # Word embeddings vector storage (vect)
    vect = DB.Column(DB.PickleType, nullable=False)
