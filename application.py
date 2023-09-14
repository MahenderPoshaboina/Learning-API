from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return "Hello World"

@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        output = []
        for data in drinks:
            drink_data = {'name': data.name, 'description': data.description}
            output.append(drink_data)
        return jsonify({"drinks": output})
    except Exception as e:
        return {"error": str(e)}, 500 

@app.route('/drinks/<id>')
def get_drink(id):
    drink=Drink.query.get_or_404(id)
    return {'name': drink.name, 'description': drink.description}
@app.route('/drinks', methods= ['POST'])
def add_drink():
    drink= Drink(name= request.json["name"], description= request.json["description"])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}
@app.route('/drinks/<id>', methods= ['DELETE'])
def del_drink(id):
    drink= Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()
    return {"Message": "deletion done"}
@app.route('/drinks/<id>', methods= ['PUT'])
def up_drink(id):
    drink= Drink.query.get_or_404(id)
    drink.name= request.json.get("name", drink.name)
    drink.description = request.json.get("description", drink.name)
    db.session.commit()
    return {"Message": "Updated Successfully"}
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')