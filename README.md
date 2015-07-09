# udacity_fullstack_project3

##Files
* project3.py -- python script with flask main application
* catalog.db -- sqlite database for item catalog
* database_setup.py -- pathon script for sqlalchemy database schema
* addData.py -- python script to polulate database with sample data
* static/styles.css -- css style for all views
* templates/additem.html -- template for item add view
* templates/catalog.html -- template for catalog and category overview
* templates/deleteitem.html -- template for item delete view
* templates/edititem.html -- template for item edit view
* templates/item.html -- template for item view
* templates/header.html -- header for all views
* templates/footer.html -- footer for all views

## Requirements

* python
* [flask](http://flask.pocoo.org)
* [sqlalchemy](http://www.sqlalchemy.org)
* [GitHub-Flask](https://github-flask.readthedocs.org/en/latest/)(We use is to do githup authorization: https://github.com/cenkalti/github-flask/blob/master/example.py)

##Setup
for GitHub OAuth the Client ID and Client Secret have to be changed in application.py: 

```python
app.config['GITHUB_CLIENT_ID'] = ''
app.config['GITHUB_CLIENT_SECRET'] = ''
```

for session managment you should change the secret key of the app:
```python
app_secret = ''
```

the callback url should be something like https://dev.danielburkard.de/github-callback and can be configured in the head of application.py:
```python
github_callback_url = "http://localhost:5000/github-callback"
```

reset database:
```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/catalog$ rm catalog.db 
vagrant@vagrant-ubuntu-trusty-32:/vagrant/catalog$ python addData.py 
```

##Usage
start application
```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/catalog$ python project3.py 
```
