#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : flask_basics.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 11/17/2020
# =============================================================================
"""
This contains some pieces of code shown on section 18, which is an introduction
to flask
"""
# =============================================================================

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
