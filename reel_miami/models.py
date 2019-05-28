# models.py

from flask import abort, redirect, request, url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, RoleMixin, UserMixin
from wtforms import TextAreaField

from reel_miami import db
from config import Config

# Database models


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address1 = db.Column(db.String, nullable=False)
    address2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    venue_photo = db.Column(db.String(20), nullable=False,
                            default='default.jpg')
    web_url = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)

    films = db.relationship('Film', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue(name={self.name})>'

    def __str__(self):
        return f'{self.name}'


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    running_time = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))

    showtimes = db.relationship('Showtime', backref='film', lazy=True)

    def __repr__(self):
        return f'<Film(name={self.name})>'

    def __str__(self):
        return f'{self.name}'


class Showtime(db.Model):
    __tablename__ = 'showtimes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    ticketing_link = db.Column(db.String, nullable=False)

    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))

    def __repr__(self):
        return f'<Showtime(date={self.date}, time={self.time})>'

    def __str__(self):
        return f'{self.name}'


'''
The Flask-Security models that are stored in the database.
'''


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return f'{self.name}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return f'{self.email}'


"""
The following classes modify the primary Flask-Admin ModelView in order to
accomplish various tasks.
"""


class AdminVenueView(ModelView):

    column_labels = {'address1': 'Address', 'address2': 'Address 2',
                     'web_url': 'Website'}
    column_default_sort = 'name'
    column_exclude_list = ('description')
    form_excluded_columns = ['films']
    form_overrides = {'description': TextAreaField}
    form_widget_args = {'address1': {
                                     'placeholder': 'Primary address'},
                        'address2': {
                                     'placeholder': 'Suite/Bulding/Other'
                                    },
                        'description': {
                                        'rows': 10,
                                        'style': 'color: black',
                                        'maxlength': 1000,
                                        'placeholder': 'max 1000 characters',
                                        'spellcheck': 'true'
                                        },
                        'phone_number': {
                                        'placeholder': '123.456.7890'
                                        }
                        }
    form_extra_fields = {
            'venue_photo': form.ImageUploadField(
                'Venue Photo',
                base_path=Config.VENUE_PHOTOS_DIR,
                url_relative_path='images/venues/',
            )
        }

    def is_accessible(self):
        return (current_user.is_active
                and current_user.is_authenticated
                and (current_user.has_role('Superuser')
                     or current_user.has_role('User')))

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is
        not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminRoleView(ModelView):

    def is_accessible(self):
        return (current_user.is_active
                and current_user.is_authenticated
                and current_user.has_role('Superuser'))

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is
        not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminUserView(ModelView):

    column_exclude_list = 'password'

    def is_accessible(self):
        return (current_user.is_active
                and current_user.is_authenticated
                and current_user.has_role('Superuser'))

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is
        not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
