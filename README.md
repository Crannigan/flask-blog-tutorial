### Install Instructions for Windows

Clone the repository then open a shell in the directory.

Run the following code.

Create the virtual environment:<br/>
`python -m venv venv`

Activate the virutal environment:<br/>
`venv\Scripts\activate`

Install Flask in the virtual environment:<br/>
`pip install Flask`

Set the location of the local app:<br/>
`set FLASK_APP=flaskr`

We are just running in a dev environment:<br/>
`set FLASK_ENV=development`

Install the project to the local environment:<br/>
`pip install -e .`

To start the flask server:<br/>
`flask run`

You should be able to go to `http://127.0.0.1:5000/` to see the front page of the blog.