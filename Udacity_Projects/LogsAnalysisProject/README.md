# Project: Logs Analysis Project

Pranay Marella's submission for Udacity's Full-Stack Web Developer Nanodegree

##About

This project taught me the fundamentals of querying databases and working with multiple tables using JOIN and sub-queries. I also learned to work in virtual environments using Vagrant. I learned to use Vagrant with PostgreSQL. Check the output.txt file for an example of the programs output.

## What's Included

* newsdata.sql - Contains data required for this project and SQL instructions to setup the database
* newsdata.py - Code for querying the PostgreSQL database and results

## Requirements

* Vagrant
* Git Bash

## How to Run

* Clone or Download the file 'LogsAnalysisProject.zip'
* Extract it into the destination where you can share files with Vagrant (ex. if vagrant folder in desktop, extract to -> C:\Users\UserName\Desktop\vagrant\)
* Open GitBash and Change Directory to within Vagrant
* If Vagrant is not setup, run 'vagrant up'. After, run 'vagrant ssh' to get the virtual machine running
* Go into the LogsAnalysisProject folder in the virtual machine
* Run 'psql -d news -f newsdata.sql' to connec to database and set it up

# Setting up the Views within Database

* Run command "CREATE VIEW ok_status AS SELECT COUNT (status), time::timestamp::date FROM log WHERE status = '200 OK' GROUP BY time::timestamp::date;"
* Run command "CREATE VIEW error AS SELECT COUNT (status), time::timestamp::date FROM log WHERE status = '404 NOT FOUND' GROUP BY time::timestamp::date;"
* Run command "\d" and check to see that the views "ok_status" and "error" appear
* exit database using command "cntrl+D"

# Viewing Results

* Run 'python newsdata.py' to see results

# Author

Pranay Marella
