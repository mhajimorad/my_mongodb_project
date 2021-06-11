# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo

from model import get_channel_stats


# -- Initialization section --
app = Flask(__name__)

app.secret_key = '_5#yZL "F4Q8z\nxec]/'

# name of database
app.config['MONGO_DBNAME'] = 'database2'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://new-admin:QHeDa0xIHy13tVuY@cluster0.x71ub.mongodb.net/database2?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        #myCollectionNames = mongo.db.collection_names()
        #myCollectionNames.sort()
        myCollectionNames = ['Homework', 'Project', 'Off-Topic']
        return render_template("index.html", channels=myCollectionNames)
    else:
        selectedChannel = request.form['exampleFormControlSelect1']
        if selectedChannel[0] == "O":    # correcting for hyphen
            selectedChannel = "OffTopic"
        [theDocuments, channelTopics, nConvTopics, nComments] = get_channel_stats(selectedChannel, mongo.db)
        #print(theDocuments)
        return render_template("channelPage.html", docs=theDocuments, channelTopics=channelTopics, channel=selectedChannel, nConvTopics=nConvTopics, nComments=nComments)
    ## connect to the database
    #myCollection = mongo.db.events0
    ## find all data in the database
    ####myEvents = myCollection.find({"user":"Jeffrey"})   # if you only wanted to show database entries where "user" field is Jeffrey
    #myEvents = myCollection.find({})  # passing an empty argument yields all database entries
    ## return message to user
    #return render_template('index.html', channels=myCollectionNames)


@app.route('/addConvTopic/<name>', methods=['GET', 'POST'])   # here, <name> denotes a variable
def add_conv_topic(name):
    if request.method == 'GET':
        return render_template("addDocument.html", channel=name)
    else:
        [theDocuments, channelTopics, nConvTopics, nComments] = get_channel_stats(name, mongo.db)
        newConvTopic = request.form['exampleFormControlTextarea1']

        if name[0] == "H":
            theCollection = mongo.db.Homework
        elif name[0] == "P":
            theCollection = mongo.db.Project
        elif name[0] == "O":
            theCollection = mongo.db.OffTopic
        else:
            theCollection = mongo.db.Quiz

        #theCollection = mongo.db.Homework
        
        allCurrentConvTopics = list(theCollection.distinct("convTopic"))
        if allCurrentConvTopics.count(newConvTopic):   # do not add new topic if it already exists in collection database
            return redirect("/")
        else:
            #print(allCurrentConvTopics)
            newConvID = nConvTopics + 1
            theCollection.insert({"convID":newConvID, "convTopic":newConvTopic, "username":session['username']})
            return redirect("/")


@app.route('/addComment/<name1>/<name2>', methods=['GET', 'POST'])   # here, <name1> and <name2> denote variables
def add_comment(name1, name2):

    if name1[0] == "H":
        theCollection = mongo.db.Homework
    elif name1[0] == "P":
        theCollection = mongo.db.Project
    elif name1[0] == "O":
        theCollection = mongo.db.OffTopic
    else:
        theCollection = mongo.db.Quiz

    if request.method == 'GET':
        existingConv = theCollection.find_one({'convID':int(name2)})
        existingConvTopic = existingConv['convTopic']
        return render_template("addComment.html", channel=name1, topic=existingConvTopic, theID=name2)
    else:
        newComment = request.form['exampleFormControlTextarea2']  
        
        theCollection.insert({"convID":int(name2), "comment":newComment, "username":session['username']})
        return redirect("/")

    # connect to the database
    #myCollection = mongo.db.events0
    # find data in the database
    #myEvents = myCollection.find({"user":name})   # if you only wanted to show database entries where "user" is value of variable "name"
    #myEvents = myCollection.find({})  # passing an empty argument yields all database entries
    # return message to user
    #return render_template('person.html', events=myEvents)



# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database
    myEvents = mongo.db.events0   # connecting to the "events0" collection of "database0"
    # insert new data
    myEvents.insert({"event":"Birthday","data":"2019-09-10"})   # inserting an entry to the connected collection
    # return a message to the user
    return "Event has been added!"


# USER TO ADD A NEW EVENT
@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == 'GET':
        return render_template("new_event.html")
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']

        # Connect to DB
        myCollection = mongo.db.events0
        # Insert new data
        myCollection.insert({"event":event_name, "data":event_date, "user":user_name})
        # Return message to user (let's send them to a new page so that they can see addition to database)
        myEvents = myCollection.find({})
        return render_template('index.html', events=myEvents)
             


@app.route('/name/<name>')   # here, <name> denotes a variable
def name(name):
    # connect to the database
    myCollection = mongo.db.events0
    # find data in the database
    myEvents = myCollection.find({"user":name})   # if you only wanted to show database entries where "user" is value of variable "name"
    #myEvents = myCollection.find({})  # passing an empty argument yields all database entries
    # return message to user
    return render_template('person.html', events=myEvents)





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({'username':request.form['username']})

        if existing_user is None:
            users.insert({'username':request.form['username'], 'password':request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return "That username already exists!  Try logging in!"


    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({'username':request.form['username']})

        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    
        return "Invalid username/password combination!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
