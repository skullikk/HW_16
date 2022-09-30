import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


def get_data_from_file(file):
    with open(file, encoding='utf-8') as file_data:
        return json.load(file_data)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(50))
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(50))
    role = db.Column(db.Text(50))
    phone = db.Column(db.Text(50))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(200))
    start_date = db.Column(db.Text(20))
    end_date = db.Column(db.Text(20))
    address = db.Column(db.Text(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer = relationship('User', foreign_keys='Order.customer_id')
    executor = relationship('User', foreign_keys='Order.executor_id')


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order = relationship('Order')
    executor = relationship('User')


db.drop_all()
db.create_all()

users_add = get_data_from_file('users.json')
for user in users_add:
    db.session.add(User(**user))

orders_add = get_data_from_file('orders.json')
for order in orders_add:
    db.session.add(Order(**order))

offers_add = get_data_from_file('offers.json')
for offer in offers_add:
    db.session.add(Offer(**offer))

db.session.commit()


@app.route('/')
def hello_my_home_work():  # put application's code here
    return 'Hello my Home Work №16!'


@app.get('/users')
def get_all_user():
    all_users = User.query.all()
    result = []
    for user in all_users:
        result.append(
            {
                'id':user.id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'age':user.age,
                'email':user.email,
                'role':user.role,
                'phone':user.phone
            }
        )
    return jsonify(result)

@app.get('/users/<int:id>')
def get_user_by_id(id):
    users_by_id = User.query.get(id)
    result = {
                'id':users_by_id.id,
                'first_name':users_by_id.first_name,
                'last_name':users_by_id.last_name,
                'age':users_by_id.age,
                'email':users_by_id.email,
                'role':users_by_id.role,
                'phone':users_by_id.phone
            }

    return jsonify(result)


if __name__ == '__main__':
    app.run()
