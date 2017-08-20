import json
import string
import random
import os
import httplib2
import requests


# Flask Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import abort, g, flash, Response, make_response
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth

# SQLAlchemy imports
from models import Category, Items, Users, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc

# OAuth imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db = DBSession()
app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item_Catalog_Application"


def redirect_url(default='/'):
    return request.args.get('next') or request.referrer or url_for(default)


################################
# USER LOGIN AND REGISTRATION #
##############################
@auth.verify_password
def verify_password(username, password):
    user = db.query(Users).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


# Create a state token to prevent request forgery
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Helper Functions for creating users
def createUser(login_session):
    newUser = Users(username=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    db.add(newUser)
    db.commit()
    user = db.query(Users).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = db.query(Users).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = db.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


@app.route('/simplelogin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if verify_password(username, password):
            user = db.query(Users).filter_by(username=username).first()
            login_session['username'] = user.username
            login_session['user_id'] = user.id
            login_session['picture'] = user.picture
            login_session['email'] = user.email
            flash("You have been logged in as: %s" % user.username)
            g.user = user
            return redirect(url_for('index'))
        else:
            return render_template('login.html',
                                   error="Wrong Username or Password!")
    else:
        return redirect(url_for('index'))


@app.route('/simplelogout')
def logout():
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    flash("You have been logged out")
    return redirect(url_for('index'))


@app.route('/simplesignup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        verify_password = request.form.get('verifypassword')

        if username is None or password is None or password != verify_password:
            return render_template('signup.html',
                                   error="You must give a valid username" +
                                   " and password")

        # check if user already in database
        user = db.query(Users).filter_by(username=username).first()
        if user:
            return render_template('signup.html',
                                   error="You already have a" +
                                   " registered account!")
        else:
            user = Users(username=username)
            user.hash_password(password)
            db.add(user)
            db.commit()
            flash("You have been registered, now log in to continue.")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# used to confrim that the token that the client sends to the server matches
# the token that the server sends to the client
# this round trip verification helps ensure that the user is making the request
# and not a malicious script
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # examines the state token passed in and compares to state of login session
    if (request.args.get('state') != login_session['state']):
        # if these two do not match then i creates
        # a response of an invalid state token
        response = make_response(json.dumps('Invalid state parameter', 401))
        response.headers['Content-Type'] = 'application/json'
        return response
    # if above statment not true then proceed
    # and collect one-time code from server
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the' +
                                            ' authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that that access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?' +
           'access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't" +
                                            "match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client" +
                                            " ID does not match "), 401)
        print "Token's client ID does not match app's."
        resposne.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is' +
                                            ' already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the access token in the session for later use
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get User Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += 'class="login_image">'

    flash("you are now logged in as %s" % login_session['username'])
    return output


# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        flash("Current user not connected.")
        return redirect(url_for('index'))

    # Execute HTTP GET request to revoke current token
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        flash("Unable to logout current user")
    else:
        del login_session['gplus_id']
        del login_session['credentials']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have been logged out")
    return redirect(url_for('index'))


###################
# VIEW FUNCTIONS
#################
@app.route('/')
def index():
    categories = db.query(Category).all()
    latest_items = db.query(Items).order_by(desc('created_date')).limit(10)
    return render_template('home.html',
                           categories=categories,
                           latest_items=latest_items,
                           login_session=login_session)


# SHOWS ALL ITEMS WITHIN A CATEGORY
@app.route('/catalog/<catalog_name>/items')
def show_catalog(catalog_name):
    all_categories = db.query(Category).all()
    category = db.query(Category).filter_by(name=catalog_name).first()
    catalog_items = db.query(Items).filter_by(category=category).all()
    return render_template('category.html',
                           categories=all_categories,
                           catalog_name=catalog_name,
                           catalog_items=catalog_items,
                           login_session=login_session)


# SHOWS SPECIFIC ITEM WITHIN A CATEGORY
@app.route('/catalog/<catalog_name>/<item_name>/<item_id>')
def show_item(catalog_name, item_name, item_id):
    category = db.query(Category).filter_by(name=catalog_name).first()
    item = db.query(Items).filter_by(name=item_name,
                                     category=category,
                                     id=item_id).first()
    return render_template('item.html', item=item, login_session=login_session)


# JSON ENDPOINT SHOWS ALL CATEGORIES WITH RESPECTIVE ITEMS
@app.route('/catalog.json')
def catalog_json():
    categories = db.query(Category).all()
    c = [i.serialize for i in categories]

    for j in c:
        items = db.query(Items).filter_by(category_id=j['id']).all()
        if items:
            x = [i.serialize for i in items]
            j['Items'] = x
    return jsonify(c)


######################################
# ADDING, EDITING, AND DELETING ITEMS
######################################
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        if (login_session['username'] is not None):
            categories = db.query(Category).all()
            return render_template('add_item.html',
                                   login_session=login_session,
                                   categories=categories)
        else:
            return render_template('login.html',
                                   error="You must be logged in to do that!")
    elif request.method == 'POST':
        categories = db.query(Category).all()
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        new_category = request.form.get('new_category')

        if item_name is not None and item_name != '':
            item = Items(name=item_name)
            if price is not None and item.price != '':
                item.price = price
            if description is not None and description != '':
                item.description = description
            item.author = getUserInfo(login_session['user_id'])
        else:
            flash("You need to give an item!")
            return redirect(url_for('add_item'))

        if category is not None and category != '':
            c = db.query(Category).filter_by(name=category).first()
            item.category = c
        elif new_category is not None and new_category != '':
            c = db.query(Category).filter_by(name=new_category).first()
            if (c):
                flash("You cannot add a category that already exists!")
                return redirect(url_for('add_item'))
            new_category = Category(name=new_category)
            item.category = new_category
            db.add(new_category)
        else:
            flash("You need to provide a category!")
            return redirect(url_for('add_item'))

        db.add(item)
        db.commit()
        return redirect(url_for('index'))


@app.route('/catalog/<catalog_name>/<item_name>/edit', methods=['GET', 'POST'])
def edit_item(catalog_name, item_name):
    if request.method == 'GET':
        category = db.query(Category).filter_by(name=catalog_name).first()
        item = db.query(Items).filter_by(name=item_name,
                                         category=category).first()
        if (item.author.username == login_session['username']):
            categories = db.query(Category).all()
            return render_template('edit_item.html',
                                   item=item,
                                   category=category,
                                   categories=categories,
                                   login_session=login_session)
        else:
            flash("You do not have permission to edit that item!")
            return redirect(url_for('index'))
    if request.method == 'POST':
        category = db.query(Category).filter_by(name=catalog_name).first()
        item = db.query(Items).filter_by(name=item_name,
                                         category=category).first()
        item_n = request.form.get('item_name')
        item_p = request.form.get('price')
        item_d = request.form.get('description')
        item_c = request.form.get('category')
        item_n_c = request.form.get('new_category')

        if item_n != '' and item_n != item.name:
            item.name = item_n
        if item_p != '' and item_p != item.price:
            item.price = item_p
        if item_d != '' and item_d != item.description:
            item.description = item_d
        if item_c != '':
            c = db.query(Category).filter_by(name=item_c).first()
            if c != item.category:
                item.category = c
        elif item_n_c != '':
            c = db.query(Category).filter_by(name=item_n_c).first()
            if not c:
                cat = Category(name=c)
                item.category = cat
                db.add(cat)

        db.add(item)
        db.commit()
        flash("Item has been modified")
        return redirect(url_for('index'))


@app.route('/catalog/<catalog_name>/<item_name>/delete', methods=['GET',
                                                                  'POST'])
def delete_item(catalog_name, item_name):
    if request.method == 'GET':
        category = db.query(Category).filter_by(name=catalog_name).first()
        item = db.query(Items).filter_by(name=item_name,
                                         category=category).first()
        if login_session['username'] == item.author.username:
            return render_template('delete.html',
                                   item=item,
                                   login_session=login_session)
        else:
            flash("you do not have permission to delete that!")
            return redirect(url_for('index'))
    elif request.method == 'POST':
        item = db.query(Items).filter_by(name=item_name).first()
        if login_session['username'] == item.author.username:
            db.delete(item)
            db.commit()
            flash("Item has been deleted")
            return redirect(url_for('index'))
        else:
            flash("you do not have permission to delete that!")
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
