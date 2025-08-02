from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')

@app.route("/")
def index():
    return "Hello, Hexlet!"