from .models import User
from sklearn.linear_model import LogisticRegression
import numpy as np
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):
    # Query for two users
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get word embeddings of tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine word embeddings into Numpy array (X matrix)
    vects = np.vstack([user0_vects, user1_vects])

    # Create Numpy array to represent y vector
    # (identifies word embedding author)
    labels = np.concatenate([np.zeros(len(user0.tweets)),
                            np.ones(len(user1.tweets))])

    # Import and train logistic regression
    log_reg = LogisticRegression()

    # Train logistic regression
    log_reg.fit(vects, labels)

    # Get word embedding for hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # Generate prediction
    prediction = log_reg.predict([hypo_tweet_vect])

    return prediction[0]
