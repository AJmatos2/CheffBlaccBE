from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)



class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
   
    
    def __init__ (self, name, price, course, description):
        self.course = course
        self.name = name
        # self.price = price
        self.description = description


class MenuItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "name",  "price","course", "description")

menuItem_schema = MenuItemSchema()
menuItems_schema = MenuItemSchema(many=True)


@app.route("/add-menu-item", methods=["POST"])
def add_item():
    course = request.json.get("course")
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")

    record = MenuItem(name, price, course, description)
    db.session.add(record)
    db.session.commit()

    return jsonify(menuItem_schema.dump(record))


@app.route("/get", methods=["GET"])
def get_items():
    all_menu_items = MenuItem.query.all()
    return jsonify(menuItems_schema.dump(all_menu_items))


@app.route("/menuItem/<id>", methods=["DELETE","GET","PUT"])
def menuItem_id(id):
    menuItem = MenuItem.query.get(id)
    if request.method == "DELETE":
        db.session.delete(menuItem)
        db.session.commit()
    
        return menuItem_schema.jsonify(menuItem)
        
    elif request.method == "PUT":
        name = request.json['name']
        course = request.json['course']
        price = request.json['price']
        description = request.json['description']

        menuItem.name = name
        menuItem.course = course
        menuItem.price = price
        menuItem.description = description

        db.session.commit()
        return menuItem_schema.jsonify(menuItem)
    elif request.method == "GET":
        return menuItem_schema.jsonify(menuItem)


if __name__ == "__main__":
    app.run(debug=True)