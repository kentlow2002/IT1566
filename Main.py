import User as u
import Order as o
import Report as r
import Product as p
import shelve
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signUp():
    return render_template('signup.html')

@app.route('/buyer/index')
def buyerIndex():
    return render_template('buyerIndex.html')


if __name__ == '__main__':
    app.run()
