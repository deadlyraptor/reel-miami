# models.py

from reel_miami import db


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
