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
    except exc.SQLAlchemyError:
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

        db_conn.execute("select * from customers where username=%s", (username,))
        row = db_conn.fetchone()
        if row == None:
            if age == '':
                age=0

            else:
                int(age)
            id=1
            db_conn.execute("select max(customerid) from customers")
            id += db_conn.fetchone()[0]
            income = random.randint(0,100)
            db_conn.execute("INSERT INTO customers(customerid, firstname, lastname, age, address1, address2,city, state, country, region, zip, gender, email, phone, creditcard,creditcardtype, creditcardexpiration, username, password, income)VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, Fname, Lname, age,address1, address2, city, state, country, region, zip, gender, email, phone,creditcard, creditcardtype, creditcardexp, username, password,income,))
            db_engine.commit()
            print '***********Query register success***********'
            return True
        else:
            print '***********Query register failed, username already exists***********'
            return False


        db_conn.close()

    except exc.SQLAlchemyError:
        if db_conn is not None:
            db_conn.close()
        print '*******Something is broken on register**********'
        print (error)
        return None


    """
    cur = conn.cursor()
    try:
        cur.execute("select * from customers where username=%s", (username,))
        row = cur.fetchone()
        if row == None:
            if age == '':
                age=0
            #elif age not Integer:
            #    age = 0
            else:
                int(age)
            id=1
            cur.execute("select max(customerid) from customers")
            id += cur.fetchone()[0]
            income = random.randint(0,100)
            cur.execute("INSERT INTO customers(customerid, firstname, lastname, age, address1, address2,city, state, country, region, zip, gender, email, phone, creditcard,creditcardtype, creditcardexpiration, username, password, income)VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, Fname, Lname, age,address1, address2, city, state, country, region, zip, gender, email, phone,creditcard, creditcardtype, creditcardexp, username, password,income,))
            conn.commit()
            print '***********Query register success***********'
            return True
        else:
            print '***********Query register failed, username already exists***********'
            return False
    except(Exception, psycopg2.DatabaseError)as error:
        print '************Something is broken on register*****************'
        print(error)
        return False
    """

def db_login(username, password):
    """
    cur = conn.cursor()
    try:
        cur.execute("select password from customers where username=%s", (username,))
        row = cur.fetchone()[0]
        if row != None:
            print row
            print password
            print hashlib.md5(password).hexdigest()
            if row == hashlib.md5(password).hexdigest():
                print '***********Query login success***********'
                return True
            else:
                print '***********Query login failed, wrong password***********'
                return False
        else:
            print '***********Query login failed, username doesnt exist***********'
            return False
    except(Exception, psycopg2.DatabaseError)as error:
        print '************Something is broken on login*****************'
        print(error)
        return False

    """
