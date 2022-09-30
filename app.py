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
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            }
        )
    return jsonify(result)


@app.get('/users/<int:id>')
def get_user_by_id(id):
    user_by_id = User.query.get(id)
    result = {
        'id': user_by_id.id,
        'first_name': user_by_id.first_name,
        'last_name': user_by_id.last_name,
        'age': user_by_id.age,
        'email': user_by_id.email,
        'role': user_by_id.role,
        'phone': user_by_id.phone
    }
    return jsonify(result)


@app.get('/orders')
def get_all_orders():
    all_orders = db.session.query(Order, User.first_name, User.last_name).join(User, Order.customer_id==User.id, isouter=True).all()
    result = []
    for order in all_orders:
        result.append(
            {
                'id': order[0].id,
                'name': order[0].name,
                'description': order[0].description,
                'start_date': order[0].start_date,
                'end_date': order[0].end_date,
                'address': order[0].address,
                'price': order[0].price,
                'customer_id': order[0].customer_id,
                'executor_id': order[0].executor_id,
                'first_name': order[1],
                'last_name': order[2]
            }
        )
    return jsonify(result)

@app.get('/orders/<int:id>')
def get_order_by_id(id):
    order_by_id = Order.query.get(id)
    result = {
                'id': order_by_id.id,
                'name': order_by_id.name,
                'description': order_by_id.description,
                'start_date': order_by_id.start_date,
                'end_date': order_by_id.end_date,
                'address': order_by_id.address,
                'price': order_by_id.price,
                'customer_id': order_by_id.customer_id,
                'executor_id': order_by_id.executor_id
            }
    return jsonify(result)


if __name__ == '__main__':
    app.run()
