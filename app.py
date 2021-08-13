# import library 
from flask import Flask,request,jsonify 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy 
import os 
# init your app 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# datbase 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db 
db = SQLAlchemy(app)
# init ma 
ma  = Marshmallow(app) 
# develop first api homepage
#@app.route('/', methods= ['GET']) 
#def home() : 
#    return  jsonify({'msg' : 'Hello World'})


# define model 
# product class 
class Product(db.Model) : 
    __tablename__= 'Product' 
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),unique = (True))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    # define __init__ method 

    def __init__(self,name,description,price,qty) : 
        self.name = name
        self.description = description 
        self.price = price
        self.qty = qty 
# Product schema 
class ProductSchema(ma.Schema) : 
    class Meta : 
        fields = ("id","name","description","price","qty")

        

# init schema 
# single product 
product_schema = ProductSchema()
# tacking with list of product   
products_schema = ProductSchema(many = True) 
# create our endpoints 
# output data in my views 
# create product 
@app.route('/product',methods= ['POST'])
def add_product() : 
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    # set a new variable 
    new_product = Product(name,description,price,qty)
# You can now use your schema to dump and load your ORM objects.
    db.session.add(new_product) 
    db.session.commit() 

    
    return product_schema.jsonify(new_product) 

# get all product 
# define the route url 
@app.route('/product',methods = ['GET'])
def get_products() : 
    all_products = Product.query.all() 
    result = products_schema.dump(all_products)
    return jsonify(result)
# execute the app

# get a single product 
@app.route('/product/<id>',methods = ['GET'])
def get_product(id) :
     product = Product.query.get(id)
     return product_schema.jsonify(product)

# update new product

@app.route('/product/<id>',methods = ['PUT'])
def update_product(id) : 
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    product.name = name 
    product.description = description 
    product.price = price 
    product.qty = qty 

    db.session.commit()

    return product_schema.jsonify(product) 

# delete product
@app.route('/product/id',methods = ['DELETE']) 
def delete_product(id) : 
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product) 
if __name__== '__main__' : 
    app.run(host='127.0.0.1', port=8080, debug=True)


