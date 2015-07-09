# setup flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, g, session
app = Flask(__name__)
# we use githun flask to to the autorization
from flask.ext.github import GitHub

# you need to set client id and secret
app.config['GITHUB_CLIENT_ID'] = ''
app.config['GITHUB_CLIENT_SECRET'] = ''

# you need to specific the app secret
app_secret = ''
# call_cak function when successfully log in
github_callback_url = "http://localhost:5000/github-callback"
github = GitHub(app)

# setup sqlalchemy
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker,scoped_session
from database_setup import Base, Category, Item, User
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

# scope session is a global session object act as a singleton shared by multiple thread to ensure thread safe
db_session = scoped_session(sessionmaker(autocommit=False,
	autoflush=False,
	bind=engine))

Base.query = db_session.query_property()

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = db_session.query(Category).all()
    items = db_session.query(Item).order_by(Item.created.desc()).all()
    return render_template('catalog.html', categories = categories, items = items, user = g.user)

# show a category
@app.route('/catalog/<string:category_name>/')
def showCategory(category_name):
    categories = db_session.query(Category).all()
    category = db_session.query(Category).filter_by(name=category_name).one()
    items = db_session.query(Item).filter_by(category = category).all()
    return render_template('catalog.html', categories = categories, category = category, items = items, user = g.user)

#show a item
@app.route('/item/<int:item_id>/')
def showItem(item_id):
    item = db_session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', item = item, user = g.user)

#add item
@app.route('/catalog/<string:category_name>/add/', methods = ['GET', 'POST'])
def addItem(category_name):
    categories = db_session.query(Category).all()
    category = db_session.query(Category).filter_by(name = category_name).one()
    user = g.user
    if user is not None:
        if request.method == 'POST':
            if request.form['name'] != "":
                mycategory = db_session.query(Category).filter_by(name=request.form['category']).one()
                item = Item(name=request.form['name'],description=request.form['description'],category=mycategory,owner = user)
                db_session.add(item)
                db_session.commit()
                flash("Item " + item.name + " added ")
                return redirect(url_for('showCategory',category_name=mycategory.name))
            else:
                #categories = Category.query.all()
                return redirect(url_for('editItem',item_id=item.id))
        else:
        #categories = Category.query.all()
            return render_template('additem.html',category=category,categories=categories)
    else:
        flash("Unauthorized user")
        return redirect(url_for('showCatalog'))

#edit item
@app.route('/item/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(item_id):
    categories = db_session.query(Category).all()
    item = db_session.query(Item).filter_by(id = item_id).one()
    user = g.user
    if user == item.owner:
        if request.method == 'POST':
            if request.form['name'] != "":
                item.name = request.form['name']
                item.description = request.form['description']
                if request.form['category'] is not None:
                    mycategory = db_session.query(Category).filter_by(name=request.form['category']).one()
                    item.categoty = mycategory
                db_session.add(item)
                db_session.commit()
                flash("Item " + item.name + " edited ")
                return redirect(url_for('showItem',item_id=item.id))
            else:
            #categories = Category.query.all()
                return redirect(url_for('editItem',item_id=item.id))
        else:
            return render_template('editItem.html', item = item,categories=categories,user=user)
    else:
        flash("Unauthorized user")
        return redirect(url_for('showCatalog'))

#delete item
@app.route('/item/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(item_id):
    categories = db_session.query(Category).all()
    item = db_session.query(Item).filter_by(id = item_id).one()
    mycategory = item.category
    user = g.user
    if user == item.owner:
        if request.method == 'POST':
            db_session.delete(item)
            db_session.commit()
            flash("Item " + item.name + " deleted ")
            return redirect(url_for('showCategory',category_name=mycategory.name, user = user))
        else:
            #categories = Category.query.all()
            return render_template('deleteItem.html',item=item, user = user)
    else:
        flash("Unauthorized user")
        return redirect(url_for('showCatalog'))

@app.route('/login')

# login function
def loginUser():
	 if session.get('user_id', None) is None:
	 	return github.authorize()
	 else:
	 	flash('User is already logged in')
	 	return redirect(url_for('showCatalog'))

#logout function
@app.route('/logout')
def logoutUser():
    session.pop('user_id', None)
    flash('User logged out')
    return redirect(url_for('showCatalog'))

#call back for github log in
@app.route('/github-callback')
@github.authorized_handler

#function to add user to database and set the current user as the logged in one with a auth_token
def authorized(oauth_token):
	next_url = request.args.get('next') or url_for('showCatalog')
	if oauth_token is None:
		# something went wront
		flash("Authorization failed")
		flash(request.args.get('error'))
		flash(request.args.get('error_description'))
		flash(request.args.get('error_uri'))
		return redirect(next_url)
	user = User.query.filter_by(github_access_token=oauth_token).first()
	if user is None:
		# new user is not in database
		user = User(name="",github_access_token=oauth_token)
		db_session.add(user)
	# save oauth token in database
	user.github_access_token = oauth_token
	db_session.commit()
	session['user_id'] = user.id
	flash("User " + user.name + " logged in")
	return redirect(next_url)

#fuction for getting token
@github.access_token_getter

def token_getter():
	user = g.user
	if user is not None:
		return user.github_access_token

# Registers a function to run before each request.
@app.before_request

def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.get(session['user_id'])
		g.user.name = github.get('user')["name"]
		g.user.avatar = github.get('user')["avatar_url"]
		db_session.add(g.user)
		db_session.commit()

#remove the iser after resquest
@app.after_request

def after_request(response):
	db_session.remove()
	return response

# funtion for seding back api endpoint
@app.route('/catelog.json')

def catalogjson():
    result = []
    categories = db_session.query(Category).all()
    for category in categories:
        oneCategory = []
        oneCategory.append({"id" : category.id,
                           "name" : category.name})
        items = db_session.query(Item).filter_by(category = category)
        for item in items:
            list = []
            list.append({
                        "description" : item.description,
                        "id" : item.id,
                        "category" : item.category.name,
                        "name" : item.name
                    })
        oneCategory.append({"items" : list})
        result.append(oneCategory)
    return jsonify({"Category":result})

if __name__ == '__main__':
    app.debug = True
    app.secret_key = app_secret
    app.run(host='0.0.0.0', port=5000)

