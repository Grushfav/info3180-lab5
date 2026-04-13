from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired

class MovieForm(FlaskForm):
    title = StringField(
        'Movie Title',
        validators=[
            DataRequired(message="Please enter the movie title."),
            Length(min=1, max=100, message="Title must be between 1 and 100 characters.")
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message="Please provide a brief description of the movie."),
            Length(min=10, max=500, message="Description must be between 10 and 500 characters.")
        ]
    )

    poster = FileField(
        'Movie Poster',
        validators=[
            FileRequired(message="Please upload a movie poster."),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Images only! (jpg, jpeg, png, gif)")
        ]
    )
# Add any form classes for Flask-WTF here