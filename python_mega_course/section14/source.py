#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : source.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 11/2/2020
# =============================================================================
"""
This is an script made by Ardit and given to students. It is made to access
his online database. This was extracted from the video
    107. Making the App
I might it into a function to import it on myApp1 (v2)
"""
# =============================================================================


import mysql.connector


def get_mysql_con():
    con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
    )

    return con

