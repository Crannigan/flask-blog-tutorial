### Install Instructions for Windows

Clone the repository then open a shell in the directory.

Run the following code.

Create the virtual environment:
`python -m venv venv`

Activate the virutal environment:
`venv\Scripts\activate`

Install Flask in the virtual environment:
`pip install Flask`

Set the location of the local app:
`set FLASK_APP=flaskr`

We are just running in a dev environment:
`set FLASK_ENV=development`

To start the flask server:
`flask run`

You should be able to go to `http://127.0.0.1:5000/` to see the front page of the blog.