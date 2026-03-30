import razorpay
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

razorpay_client = razorpay.Client(auth=("YOUR_KEY_ID","YOUR_KEY_SECRET"))

# ---------------- MODELS ----------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    brand = db.Column(db.String(120))
    description = db.Column(db.String(300))
    image = db.Column(db.String(200))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    status = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

# ---------------- CART COUNT ----------------

@app.context_processor
def inject_cart_count():

    if current_user.is_authenticated:
        count = Cart.query.filter_by(user_id=current_user.id).count()
    else:
        count = 0

    return dict(cart_count=count)

# ---------------- DATABASE INIT ----------------

def create_tables():
    db.drop_all()   # delete all existing tables
    db.create_all() # recreate tables with new columns

    if Product.query.count()==0:

        products=[

Product(
name="Laptop",
brand="HP",
description="HP Gaming Laptop with Intel i7 processor and 16GB RAM",
image="laptop.gif",
price=65000,
stock=5
),

Product(
name="Smartphone",
brand="Samsung",
description="Samsung Android Smartphone with AMOLED display",
image="samsung.gif",
price=22000,
stock=10
),

Product(
name="Headphones",
brand="Sony",
description="Sony Wireless Headphones with Noise Cancellation",
image="headphones.gif",
price=4000,
stock=15
),

Product(
name="Smart Watch",
brand="OnePlus",
description="OnePlus Fitness Smartwatch with heart rate monitor",
image="oneplus.gif",
price=5000,
stock=20
),

Product(
name="Running Shoes",
brand="Nike",
description="Nike Comfortable Running Shoes for daily training",
image="nike.gif",
price=3500,
stock=25
),

Product(
name="Backpack",
brand="Wildcraft",
description="Wildcraft Laptop Backpack with multiple compartments",
image="wildcraft.gif",
price=1500,
stock=30
),

Product(
name="Keyboard",
brand="Logitech",
description="Logitech Mechanical Keyboard with RGB lighting",
image="keyboard.gif",
price=4500,
stock=12
),

Product(
name="Mouse",
brand="Logitech",
description="Logitech Gaming Mouse with high precision sensor",
image="mouse.gif",
price=2000,
stock=20
),

Product(
name="Tablet",
brand="Samsung",
description="Samsung Android Tablet with 10 inch display",
image="tabelt.gif",
price=18000,
stock=8
),

Product(
name="Bluetooth Speaker",
brand="Boat",
description="Boat Portable Bluetooth Speaker with deep bass",
image="bluetooth.gif",
price=2500,
stock=14
)

]

        db.session.add_all(products)
        db.session.commit()

# ---------------- HOME ----------------

@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect("/products")

    return redirect("/login")

# ---------------- PRODUCTS ----------------

@app.route("/products")
@login_required
def products():

    products = Product.query.all()

    return render_template("index.html",products=products)

# ---------------- REGISTER ----------------

@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]

        hashed=generate_password_hash(password)

        user=User(username=username,email=email,password=hashed)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful")

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):

            login_user(user)

            return redirect("/products")

        flash("Invalid login")

    return render_template("login.html")

# ---------------- LOGOUT ----------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")

# ---------------- ADD TO CART ----------------

@app.route("/add/<int:id>")
@login_required
def add_to_cart(id):

    item=Cart.query.filter_by(user_id=current_user.id,product_id=id).first()

    if item:
        item.quantity+=1
    else:
        item=Cart(user_id=current_user.id,product_id=id,quantity=1)
        db.session.add(item)

    db.session.commit()

    return redirect("/products")

# ---------------- CART ----------------

@app.route("/cart")
@login_required
def cart():

    items=Cart.query.filter_by(user_id=current_user.id).all()

    cart_products=[]
    total=0

    for item in items:

        product=db.session.get(Product,item.product_id)

        subtotal=product.price*item.quantity

        total+=subtotal

        cart_products.append((product,item.quantity,subtotal))

    return render_template("cart.html",products=cart_products,total=total)

# ---------------- CHECKOUT ----------------

@app.route("/checkout")
@login_required
def checkout():

    items=Cart.query.filter_by(user_id=current_user.id).all()

    total=sum(db.session.get(Product,i.product_id).price*i.quantity for i in items)

    order=Order(user_id=current_user.id,amount=total,status="Placed")

    db.session.add(order)

    Cart.query.filter_by(user_id=current_user.id).delete()

    db.session.commit()

    return redirect("/orders")

# ---------------- ORDERS ----------------

@app.route("/orders")
@login_required
def orders():

    orders=Order.query.filter_by(user_id=current_user.id).all()

    return render_template("orders.html",orders=orders)

# ---------------- RUN ----------------

if __name__=="__main__":

    with app.app_context():
        create_tables()

    app.run(debug=True)