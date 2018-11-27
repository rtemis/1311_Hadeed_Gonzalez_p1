from sqlalchemy import create_engine, func, exc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
import os
import hashlib
import random

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)


def db_getTopVentas(anno):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()


        db_resul = db_conn.execute("select * from getTopVentas(%s)", (anno,))
        db_resul = db_resul.fetchall()
        db_conn.close()

        return  list(db_resul)
    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '*******Something is broken on getTopVentas**********'
        print (error)
        return None

def db_register(Fname, Lname, age, address1,address2, city, state, country, region, zip, gender, email, phone, creditcard, creditcardtype, creditcardexp, username, password):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select * from customers where username=%s", (username,))
        row = resul.fetchone()
        if row == None:
            if age == '':
                age=0

            else:
                int(age)
            id=1
            resul = db_conn.execute("select max(customerid) from customers")
            id += resul.fetchone()[0]
            income = random.randint(0,100)
            db_conn.execute("INSERT INTO customers(customerid, firstname, lastname, age, address1, address2,city, state, country, region, zip, gender, email, phone, creditcard,creditcardtype, creditcardexpiration, username, password, income)VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, Fname, Lname, age,address1, address2, city, state, country, region, zip, gender, email, phone,creditcard, creditcardtype, creditcardexp, username, password,income,))
            print '***********Query register success***********'
            db_conn.close()
            return True
        else:
            print '***********Query register failed, username already exists***********'
            db_conn.close()
            return False

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '*******Something is broken on register**********'
        print (error)
        return False


def db_login(username, password):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select password from customers where username=%s", (username,))
        row = resul.fetchone()[0]
        if row != None:
            if row == hashlib.md5(password).hexdigest():
                print '***********Query login success***********'
                db_conn.close()
                return True
            else:
                print '***********Query login failed, wrong password***********'
                db_conn.close()
                return False
        else:
            print '***********Query login failed, username doesnt exist***********'
            db_conn.close()
            return False
    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on login*****************'
        print (error)
        return False


def db_getDetails(movieid):
    try:

        moviedict = {}

        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select price, description from imdb_movies natural join products where movieid=%s", (movieid,))
        movies = resul.fetchall()
        
        resul = db_conn.execute("select actorname, movieid from (imdb_movies natural join imdb_actormovies) natural join imdb_actors where movieid=%s", (movieid,))
        actors = resul.fetchall()

        resul = db_conn.execute("select directorname, movieid from (imdb_movies natural join imdb_directormovies) natural join imdb_directors where movieid=%s", (movieid,))
        directors = resul.fetchall()

        resul = db_conn.execute("select genre, movieid from (imdb_movies natural join imdb_moviegenres) natural join imdb_genres where movieid=%s", (movieid,))
        genres = resul.fetchall()

        resul = db_conn.execute("select lang, movieid from (imdb_movies natural join imdb_movielanguages) natural join imdb_languages where movieid=%s", (movieid,))
        languages = resul.fetchall()

        db_conn.close()

        moviedict = {'movies': list(movies), 'actors': list(actors), 'directors': list(directors), 'genres': list(genres), 'languages': list(languages)}

        return moviedict

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on catalogue*****************'
        print (error)
        return None


def db_catalogue():
    try:

        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select movieid, movietitle from imdb_movies  LIMIT 50")
        resul = resul.fetchall()
        db_conn.close()

        return list(resul)

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on catalogue*****************'
        print (error)
        return None
"""
def db_search(title, genre):
    try:

        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        print "*************"
        print title
        print "************"

        if title == "":
            if genre != "#":
                resul = db_conn.execute("select movieid, movietitle, genre, price from ((imdb_movies natural join imdb_moviegenres) natural join imdb_genres)natural join products LIMIT 50 where genre = %s", (genre,))
                resul = resul.fetchall()
            else:
                resul = db_catalogue()
        else:
            if genre != "#":
                resul = db_conn.execute("select movieid, movietitle, genre, price from ((imdb_movies natural join imdb_moviegenres) natural join imdb_genres)natural join products LIMIT 50 where genre = %s and movietitle= %s", (genre,title,))
                resul = resul.fetchall()
            else:
                resul = db_conn.execute("select movieid, movietitle, genre, price from ((imdb_movies natural join imdb_moviegenres) natural join imdb_genres)natural join products LIMIT 50 where movietitle = %s", (title,))
                resul = resul.fetchall()



        db_conn.close()

        return list(resul)

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on catalogue*****************'
        print (error)
        return None

"""
def db_description(movieid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select movieid, movietitle, directorname, country, actorname, price, description from (((((((imdb_movies natural join imdb_directormovies) natural join imdb_directors) natural join imdb_moviecountries)natural join imdb_countries) natural join imdb_actormovies) natural join imdb_actors) natural join products) where movieid=%s", (movieid,))
        resul = resul.fetchone()
        db_conn.close()
        return resul

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on description*****************'
        print (error)
        return None

def db_genres():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select * from imdb_genres")
        resul = resul.fetchall()
        db_conn.close()
        return list(resul)

    except exc.SQLAlchemyError as error:
        if db_conn is not None:
            db_conn.close()
        print '************Something is broken on genres*****************'
        print (error)
        return None

""""def db_addToCart(customerid):
        try:
            db_conn = None
            db_conn = db_engine.connect()

            result = db_conn.execute("SELECT orderid FROM orders WHERE customerid=%s AND status=NULL", (customerid,))
            row = result.fetchone()[0]
"""
