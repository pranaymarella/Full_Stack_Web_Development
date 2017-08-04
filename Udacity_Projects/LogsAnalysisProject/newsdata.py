#! /usr/bin/env python
# lite version of MySQL database
import psycopg2


# Used for connect to database
def connect(database_name="news"):
    DB = psycopg2.connect("dbname={}".format(database_name))
    cursor = DB.cursor()
    return DB, cursor


def most_popular_articles():
    # making connection to database
    DB, c = connect()

    # the actual query to the database
    c.execute("SELECT title, COUNT (*) as views " +
              "FROM log JOIN articles " +
              "ON log.path = CONCAT('/article/', articles.slug) " +
              "GROUP BY title ORDER BY views DESC LIMIT 3;")

    # holds the results
    ans_one = c.fetchall()

    # close the connection to the database
    DB.close()

    # print answers to the console
    for i in ans_one:
        print ('\"' + i[0] + '\"' + " - " + str(i[1]) + " views")

    return


def most_popular_authors():
    # ESTABLISH CONNECTION TO DATABASE
    DB, c = connect()

    # SQL QUERY
    c.execute("SELECT name, views FROM (SELECT author, COUNT (*) as views " +
              "FROM log JOIN articles " +
              "ON log.path = CONCAT('/article/', articles.slug) " +
              "GROUP BY author ORDER BY views DESC) as auth " +
              "JOIN authors ON auth.author = authors.id ORDER BY views DESC;")

    ans_two = c.fetchall()

    # CLOSE DATABASE CONNECTION
    DB.close()

    for i in ans_two:
        print (i[0] + ' - ' + str(i[1]) + " views")

    return


def errors():
    DB, c = connect()

    c.execute("SELECT maxes.percent_errors, maxes.date " +
              "FROM (SELECT ROUND((100.0*error.count / ok_status.count), 1) " +
              "as percent_errors, to_char(error.time,'MonthDD,yyyy') " +
              "as date FROM error JOIN ok_status " +
              "ON error.time = ok_status.time) as maxes " +
              "WHERE maxes.percent_errors > 1.0;")

    ans_three = c.fetchall()

    DB.close()

    for i in ans_three:
        print(i[1].split()[0] + ' ' + i[1].split()[1] +
              ' - ' + str(i[0]) + "% errors")

if __name__ == '__main__':
    # Answer to: What are the most popular three articles of all time?
    print("What are the most popular three articles of all time?")
    most_popular_articles()
    print('\n')
    # Answer to: Who are the most popular article authors of all time?
    print("Who are the most popular article authors of all time?")
    most_popular_authors()
    print('\n')
    # Answer to: On which days did more than 1% of requests lead to errors?
    print("On which days did more than 1% of requests lead to errors?")
    errors()
    print('\n')
