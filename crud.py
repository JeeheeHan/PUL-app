"""Create, read, update and delete"""

from model import *
from textblob import TextBlob

def create_user(user, pwd):
    """Create and return a new user."""

    user = User(username=user)
    #Using class fucntion to set password using hash
    user.set_password(pwd)

    db.session.add(user)
    db.session.commit()

    return user

def login_check(username, password):
    """Check if email matches password"""

    #https://wtforms.readthedocs.io/en/2.3.x/fields/
    try: 
        user = User.query.filter_by(username=username).first()
        # password_by_username = user.password

        if user.check_password(password):
            return user
    except:
        pass


def get_user_id(data):
    """Get the user_id from DB"""
    username = data['username']
    user_id = User.query.filter_by(username=username).first().id

    return user_id



def save_chat_message(data):
    """Saving chat message into DB and return chat ID"""
    user_id = get_user_id(data)
    message = data['message']
    timestamp = data['timestamp']

    db.session.add(General_chat(message=message, userID=user_id, timestamp=timestamp))
    db.session.commit()

    return General_chat.query.order_by(General_chat.chatID.desc()).first().chatID
    #get the latest input added 

def print_pos_neg(num):
    """Print if positive or negative in polarity level"""
    
    if num > 0:
        return "positive"
    elif num == 0: 
        return "neutral"
    else:
        return "negative"



def save_nlp(data, chatID):
    """Saving analysis to NLP Table and return if positive or negative"""
    user_id = get_user_id(data)
    message = data['message']
    blob = TextBlob(message).correct()
    #This is to run the correction function to get the right spelling of vocabs

    list_of_word = blob.words
    polarity = blob.sentiment.polarity

    words = " ".join(list_of_word)
    #string the list of tokenized words to save into DB
    word_count = len(list_of_word)

    db.session.add(NLP(userID=user_id, word_count= word_count, polarity=polarity, filtered_words=list_of_word, chatID=chatID))
    db.session.commit()

    return print_pos_neg(polarity)



def login_track(username):
    """Saving last logged into DB"""
    user = User.query.filter_by(username=username).first()
    user.last_login = datetime.utcnow

def create_adjectives(word_type, word):
    """Put each word in text file into adjectives table"""
    adj = Adjectives(word_type= word_type,
                        word = word)
    db.session.add(adj)
    db.session.commit()
    
    return adj

def get_words():
    """This gets all the words"""
    return Adjectives.query.all()


#need a function to get the top 30 words used..
#https://textblob.readthedocs.io/en/dev/quickstart.html#quickstart
#The sentiment property returns a namedtuple of the form Sentiment(polarity,
#subjectivity). The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a
#float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

# def get_latest_messages():
#     """Get the last 50 messages from message table"""
#     list_inputs = General_chat.query.order_by(General_chat.chatID.desc()).limit(50).all()
#     return ''.join(item.message for item in list_inputs)
#      #Get the last 50 messages and put it into one big string

# def get_sentiment():
#     """Get sentiment level from the last 50 messages"""
#     text = get_latest_messages()
#     status = TextBlob(text).sentiment.polarity
#     return status

def get_messages():
    """Get a list of messages by the chatID"""
    lst_messages = General_chat.query.order_by(General_chat.chatID.asc()).all()
    return lst_messages
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
