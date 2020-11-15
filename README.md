# Lesson Plan Repository

A not-for-profit organisation called TeachAll supports teachers in under-resourced countries by providing professional training programmes and teaching resources. They have called on me to help create a back-end application that allows their members to share their lesson plans. 

The application will:
1) Allow public to view lesson categories, lesson plans and lesson plans by category
1) Allow members to create a lesson plan and update a lesson plan in addition to those listed in the public access
2) Allow admin to create a category, create a lesson plan, update a lesson plan and delete a lesson plan in addition to those listed in the public access
3) Use Auth0 and JWT tokens to manage user authentication and access control for the application


## Backend

The `./backend` directory contains:
1) README.md
2) requirements.txt 
3) a Flask server
4) database models using SQLAlchemy module
5) API testing file
6) Basic Flask Auth file


### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)



##### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.



##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.



###### Running the server locally:

From within the `./backend` directory:

1) ensure you are working using your created virtual environment
2) create a database in your postgresql to point the app to. For example, mine is: postgresql://ira:ira@localhost:5432/lessonplan
3) update the DATABASE_URL variable in the ./setup.sh file
4) run the following commands on the terminal:

```bash
source ./setup.sh
gunicorn --bind 0.0.0.0:8080 app:app
```

5) Go to http://localhost:8080/categories to access the app.



###### Running the deployed server 

The app has been deployed on Heroku. Go to: https://lessonplanapp.herokuapp.com/categories to access the app.



###### Testing end points 

API endpoints can be tested with [Postman](https://getpostman.com). Samples of API testing and valid JWTs can be found in the postman collections below:

1) Local server: `./backend/Local lesson-plan.postman_collection.json` 
2) Deployed server: `./backend/Heroku lesson-plan.postman_collection.json` 
