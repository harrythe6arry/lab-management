import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request, jsonify
from psycopg2 import sql

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

