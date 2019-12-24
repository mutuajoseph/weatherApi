from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
import requests

DB_URL = 'postgresql://postgres:wamzy@127.0.0.1:5432/weatherApi'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='some-secret-string'

db =SQLAlchemy(app)

class City(db.Model):
     __tablename__ = 'city'
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(45), nullable=False)

     # Create 
     def create_city(self):
        db.session.add(self)
        db.session.commit()


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = []

    for city in cities: 

        r = requests.get(url.format(city.name)).json()

        weather  = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }

        weather_data.append(weather)

    return render_template('weather.html' , weather_data=weather_data)



if __name__ == "__main__":
    app.run(debug=True)