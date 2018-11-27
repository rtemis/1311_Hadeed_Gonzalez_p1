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

            # inicializar el usuario
            db_conn.execute("INSERT INTO customers(firstname, lastname, age, address1, address2,city, state, country, region, zip, gender, email, phone, creditcard,creditcardtype, creditcardexpiration, username, password, income)VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (Fname, Lname, age,address1, address2, city, state, country, region, zip, gender, email, phone,creditcard, creditcardtype, creditcardexp, username, password,income,))

            # inicializar el carrito
            db_conn.execute("INSERT INTO orders(orderdate, customerid, status)VALUES(CURRENT_DATE, %s, NULL)",(id,))

            print '***********Query register success***********'
            db_conn.close()
            return True
        else:
            print '***********Query register failed, username already exists***********'
            db_conn.close()
            return False
        db_conn.close()

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
        print '************Something is broken on login*****************'
        print(error)
        return False

def db_catalogue():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        resul = db_conn.execute("select movietitle, year from imdb_movies")
        resul = resul.fetchall()

        return list(resul)

    except exc.SQLAlchemyError as error:
        print '************Something is broken on catalogue*****************'
        print(error)
        return None

#def db_addToCart(customerid):
#        try:
#            db_conn = None
#            db_conn = db_engine.connect()
#
#            result = db_conn.execute("SELECT orderid FROM orders WHERE customerid=%s AND status=NULL", (customerid,))
#            row = result.fetchone()[0]
#            if order == None:
