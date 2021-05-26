## Plants Utilize Language
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)]()
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)  


## Table of Contents
1. [Overview](#overview)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Roadmap](#roadmap)
5. [FAQs](#faqs)

### Overview
<a name="Overview"></a>
PUL allows users to interactively insult or compliment the virtual plant via live chat. In this virtual stimulation, the comments are categorized by positive or negative sentiment using NLP. Every message is analyzed then tokenized which allows users to see their contribution’s sentiment polarity and directly impact the plant’s health. As for the virtual plant, just like a real plant, it has the capability to withstand positivity or negativity depending on the conversation’s flow. The more messages the plant receives, the plant’s health tolerates more one way or the other depending on the total sentiment polarity.
Check out the live app here (TBD on getting a custom domain name)
https://plants-utilize-language.herokuapp.com/


***Any users can see the live chat but not able to send a message unless logging in***
![](/demo/PUL-app1.gif)

***Users can log in/log out/edit password***

![](/demo/PUL-app2.gif)

***This form allows users to play around sentiment polarity scores for 2 different libraries***

![](/demo/form1.png)

***Logged in users can see their own messages and the polarity as well***

![](/demo/analyze.png)

***And there we have it!***

![](/demo/PUL-app4.gif)


***Here is the plant at its happiest***

![](/demo/PUL-app5.gif)


### Technologies
<a name="Technologies"></a>
- Python, SQLAlchemy, PostgreSQL, Flask, FlaskSocketIO, eventlet, Flask-Login, WTForms, TextBlob
- Javascript, jQuery(AJAX), Jinja2, Bootstrap, Google Fonts, HTML5, CSS3
- APIs: Socket.IO, Complimentr 


### Installation
<a name="installation"></a>
Tip: Create your own secrets.sh for the secret key
***
A little intro about the installation. 
```
$ git clone https://github.com/JeeheeHan/PUL-app.git
$ pip3 install -r requirements.txt
$ source secrets.sh
$ python3 server.py
```

### Roadmap
<a name="Roadmap"></a>
Feature releases coming up:
- Regex implementation for sanitizing messages
- Visualization of top words
- More plants!

### FAQs
<a name="faqs"></a>
Jenny was a revenue manager specializing in hospitality management which included data modeling, forecasting, and channel optimizing. As the POS expert, she got involved in a new website launch to test the direct booking integration. Through this involvement, she got inspired to transition into SWE to create cost effective infrastructure that can improve operations and system reliability with numerous distributions. From the holistic perspective of CRM and profit driving strategies, Jenny is eager to apply her coding skills to enhance such tech. Aside from programming, she is also passionate about keeping up with the latest technologies for best performance with new game launches. Find her on [LinkedIn](https://www.linkedin.com/in/jihee-jenny/) and on [Github](https://github.com/JeeheeHan).