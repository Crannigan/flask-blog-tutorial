### Install Instructions for Windows

Clone the repository then open a shell in the directory.

Run the following code.

Create the virtual environment:<br/>
`python -m venv venv`<br/>

Activate the virutal environment:<br/>
`venv\Scripts\activate`<br/>

Install Flask in the virtual environment:<br/>
`pip install Flask`<br/>

Set the location of the local app:<br/>
`set FLASK_APP=flaskr`<br/>

We are just running in a dev environment:<br/>
`set FLASK_ENV=development`<br/>

Install the project to the local environment:<br/>
`pip install -e .`<br/>

Initialize the databases:<br/>
`flask init-db`<br/>

To start the flask server:<br/>
`flask run`<br/>

You should be able to go to `http://127.0.0.1:5000/` to see the front page of the blog.


To run tests you need to install pytest and coverage within the venv:<br/>
`pip install pytest coverage`
`pytest`