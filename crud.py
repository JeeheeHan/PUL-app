"""Create, read, update and delete"""

from model import *
from textblob import TextBlob, Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sqlalchemy import func

#train NaiveBayesAnalyzer from Movie review lib to only have to train it once
Naive_Analysis = Blobber(analyzer=NaiveBayesAnalyzer())

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
    #return 404 if user is not found
    user_id = User.query.filter_by(username=username).first_or_404().id

    return user_id



def save_chat_message(data):
    """Saving chat message into DB and return chat ID"""
    user_id = get_user_id(data)
    message = data['message']
    timestamp = data['timestamp']

    db.session.add(General_chat(message=message, 
                                userID=user_id,
                                timestamp=timestamp))
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

    db.session.add(NLP(userID=user_id, 
                        word_count= word_count,
                        polarity=polarity,
                        filtered_words=list_of_word,
                        chatID=chatID))
    db.session.commit()

    return print_pos_neg(polarity)



def login_track(username):
    """Saving last logged into DB"""
    user = User.query.filter_by(username=username).first()
    user.last_login = datetime.utcnow()
    db.session.commit()


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

def count_pos_neg():
    """Get a dictionary of positive to negative messages with count in nlp table"""
    pos_list= db.session.query(func.count(NLP.polarity)).filter(NLP.polarity>0).scalar()
    neg_list = db.session.query(func.count(NLP.polarity)).filter(NLP.polarity<0).scalar()

    count_dict = {}

    count_dict['positive'] = pos_list
    count_dict['negative'] = neg_list

    return count_dict

def get_messages():
    """Get a list of messages by the chatID"""
    lst_messages = General_chat.query.order_by(General_chat.chatID.asc()).all()
    return lst_messages
####Just going to use these functions to decide on the overall polarity for the latest 50 messages when a user connects#######
def get_latest_messages():
    """Get the last 50 messages from message table"""
    list_inputs = General_chat.query.order_by(General_chat.chatID.desc()).limit(50).all()
    return ' '.join(item.message for item in list_inputs)
     #Get the last 50 messages and put it into one big string also make sure to seperate them out by spaces

def get_sentiment():
    """Get sentiment level from the last 50 messages"""
    text = get_latest_messages()
    status = TextBlob(text).sentiment.polarity
    return status
    
def get_plant_status(num):
    """"Return a number so that the appropriate image can be called"""
    if num < -0.5:
        return 1
    elif num < 0:
        return 2
    elif num < 0.5:
        return 3
    elif num < 1:
        return 4

def print_polarity_from_input(quest, text):
    """Get the user's selection of sentiment analysis and return the polarity"""
    if quest == 'naive':
        blob = Naive_Analysis(text).sentiment
        return blob
        #this will be: Sentiment(classification='pos', p_pos=0.5702702702702702, p_neg=0.4297297297297299)
    else:
        blob = TextBlob(text).sentiment
        return blob.polarity

def break_down_naive(result):
    """return result into a dictionary"""
    break_down = {}
    if result.p_pos > result.p_neg:
        break_down["class"] = "Positive"
        break_down["polarity"] = "{:.2f}".format(result.p_pos)
    elif result.p_pos < result.p_neg:
        break_down["class"] = "Negative"
        break_down["polarity"] = "{:.2f}".format(result.p_neg)
    else:#if the text is neutral the pos and neg is 0.5 exactly
        break_down["class"] = "Neutral"
        break_down["polarity"] = "0.5"

    return break_down

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

