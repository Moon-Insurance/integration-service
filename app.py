from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Migrations


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.String(50), unique=True, nullable=False)
    agent_id = db.Column(db.String(50), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            'sale_id': self.sale_id,
            'agent_id': self.agent_id,
            'product': self.product,
            'amount': self.amount
        }

@app.before_first_request
def create_tables():
    db.create_all()

# CREATE
@app.route('/', methods=['POST'])
def create_sale():
    data = request.json
    if not data or 'sale_id' not in data:
        abort(400, description="sale_id is required")
    sale = Sale(
        sale_id=data['sale_id'], 
        agent_id=data.get('agent_id', ''),
        product=data.get('product', ''),
        amount=data.get('amount', 0.0)
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify(sale.as_dict()), 201

# READ
@app.route('/<sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = Sale.query.filter_by(sale_id=sale_id).first()
    if not sale:
        abort(404)
    return jsonify(sale.as_dict())

# UPDATE
@app.route('/<sale_id>', methods=['PUT'])
def update_sale(sale_id):
    data = request.json
    sale = Sale.query.filter_by(sale_id=sale_id).first()
    if not sale:
        abort(404)
    sale.agent_id = data.get('agent_id', sale.agent_id)
    sale.product = data.get('product', sale.product)
    sale.amount = data.get('amount', sale.amount)
    db.session.commit()
    return jsonify(sale.as_dict())

# DELETE
@app.route('/<sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    sale = Sale.query.filter_by(sale_id=sale_id).first()
    if not sale:
        abort(404)
    db.session.delete(sale)
    db.session.commit()
    return jsonify({'message': 'Sale deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
