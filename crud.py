"""Create, read, update and delete"""

from model import *
from textblob import TextBlob, Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sqlalchemy import func

#Train NaiveBayesAnalyzer from Movie review lib to only have to train it once
Naive_Analysis = Blobber(analyzer=NaiveBayesAnalyzer())


#### USER CREDENTIAL FUNCTIONS ####
def create_user(user, pwd):
    """Create and return a new user.

    >>> create_user("flowers", "flowers")
    <Username:flowers>
    """

    user = User(username=user)
    #Using class fucntion to set password using hash
    user.set_password(pwd)

    db.session.add(user)
    db.session.commit()

    return user

def login_check(username, password):
    """Check if email matches password

    >>> login_check("test","test")
    <Username:test>
    >>> login_check("noone","noone")
    """
    try: 
        user = User.query.filter_by(username=username).first()

        if user.check_password(password):
            return user
    except:
        pass


def get_user_id(data):
    """Get the user_id from DB

    >>> get_user_id({"username":"test"})
    1
    """
    username = data['username']
    #return 404 if user is not found
    user_id = User.query.filter_by(username=username).first_or_404().id

    return user_id


#### SAVING INTO DB FUNCTIONs ####
def save_chat_message(data):
    """Saving chat message into DB and return the latest entry

    >>> save_chat_message({"username":"test", "message":"doctest", "timestamp":"2021-05-03T05:35:04Z"})
    <General_chat chatID:128 timestamp:2021-05-03 05:35:04 userID:1 message:doctest >
    """
    user_id = get_user_id(data)
    message = data['message'].replace("'", '"')
    timestamp = data['timestamp']

    db.session.add(General_chat(message=message, 
                                userID=user_id,
                                timestamp=timestamp))
    db.session.commit()

    return General_chat.query.order_by(General_chat.chatID.desc()).first()
    #get the latest input added 


def save_nlp(data, chatID):
    """Saving analysis to NLP Table and return if positive or negative

    >>> save_nlp({"username":"test", "message":"doctest", "timestamp":"2021-05-03T05:35:04Z"},10)
    'neutral'
    """
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


#### SENTIMENT ANALYSIS FUNCTIONS ####
def print_pos_neg(num):
    """Print if positive or negative in polarity level

    >>> print_pos_neg(0.8)
    'positive'
    >>> print_pos_neg(-0.5)
    'negative'

    """
    
    if num > 0:
        return "positive"
    elif num == 0: 
        return "neutral"
    else:
        return "negative"

def count_pos_neg():
    """Get a dictionary of positive to negative messages with count in nlp table"""
    pos_list= db.session.query(func.count(NLP.polarity)).filter(NLP.polarity>0).scalar()
    neg_list = db.session.query(func.count(NLP.polarity)).filter(NLP.polarity<0).scalar()
    total_messages = db.session.query(func.count(NLP.polarity)).scalar()

    count_dict = {}

    count_dict['positive'] = pos_list
    count_dict['negative'] = neg_list
    count_dict['total'] = total_messages

    return count_dict

def get_messages():
    """Get a list of messages by the chatID"""
    lst_messages = General_chat.query.order_by(General_chat.chatID.asc()).all()
    return lst_messages

#### CALCULATING FUNCTIONS FOR SENTIMENT POLARITY ####

def get_ratio(count_dict):
    """check if count_dict has total then Get ratio for all messages between pos and neg"""
    if count_dict['total'] != 0:
        pos_ratio = float(count_dict['positive'])/ float(count_dict.get('total',1))
        neg_ratio = float(count_dict['negative']) / float(count_dict.get('total',1))

        count_dict['pRatio'] = pos_ratio
        count_dict['nRatio'] = neg_ratio
    else: 
        count_dict['pRatio'] = 0
        count_dict['nRatio'] = 0
        
    return count_dict

    
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
    """Get the user's selection of sentiment analysis and return the polarity

    >>> print_polarity_from_input("pat", "testing this one out")
    0.0
    >>> print_polarity_from_input("pat", "I hate everyhting")
    -0.8
    >>> print_polarity_from_input("pat", "I love")
    0.5
    >>> print_polarity_from_input("naive", "I love")
    Sentiment(classification='pos', p_pos=0.5441400304414004, p_neg=0.45585996955859964)
    >>> print_polarity_from_input("naive", "I need this")
    Sentiment(classification='neg', p_pos=0.46209650208075576, p_neg=0.5379034979192443)
    >>> print_polarity_from_input("naive", "I hate everything")
    Sentiment(classification='pos', p_pos=0.5688745670970848, p_neg=0.431125432902915)

    """
    if quest == 'naive':
        blob = Naive_Analysis(text).sentiment
        return blob
        #this will be: Sentiment(classification='pos', p_pos=0.5702702702702702, p_neg=0.4297297297297299)
    else:
        blob = TextBlob(text).sentiment
        return blob.polarity

def break_down_naive(result):
    """return result into a dictionary

    >>> test = print_polarity_from_input("naive", "I hate everythin")
    >>> break_down_naive(test)
    {'class': 'Positive', 'polarity': '0.52'}
    
    """
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

def get_plant_health(count_dict):
    """With the ratio, return a number for the plant's pic to be added into hmtl"""
    #larger the num, the health level goes up/down
    pos_ratio = count_dict['pRatio']
    neg_ratio = count_dict['nRatio']
    
    if pos_ratio > neg_ratio:
        if pos_ratio < 0.3:
            num= 1
        elif pos_ratio < 0.5:
            num= 2
        elif pos_ratio < 0.8:
            num= 3
        else:
            num= 4
        return f"/static/images/happyplant{num}.PNG"
    else:
        if neg_ratio < 0.3:
            num= 1
        elif neg_ratio < 0.5:
            num= 2
        elif neg_ratio < 0.8:
            num= 3
        else:
            num= 4
        return f"/static/images/sadplant{num}.PNG"

if __name__ == '__main__':
    # from server import app
    # connect_to_db(app)

    pass

