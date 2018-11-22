
import psycopg2
import os
import hashlib

try:
    conn = psycopg2.connect("dbname='si1' user='alumnodb' host='localhost' password='alumnodb'")
    print '---------CONEXION A LA BASE DE DATOS CON EXITO-----------'
except:
    print "***********I am unable to connect to the database*************"



def db_getTopVentas(anno):
    cur = conn.cursor()

    cur.callproc("getTopVentas", (anno,))
    resul = cur.fetchall()
    return resul


def db_register(Fname, Lname, address1,address2, city, state, country, region, zip, email, phone, creditcard, creditcardtype, creditcardexp, username, password):
    #NO ESTAN TODOS LOS CAMPOS PERO INSERTA

    cur = conn.cursor()
    try:
        cur.execute("select * from customers where username=%s", (username,))
        row = cur.fetchone()
        if row == None:
            id=1
            cur.execute("select max(customerid) from customers")
            id += cur.fetchone()[0]

            cur.execute("INSERT INTO customers(customerid, firstname, lastname,address1, address2,city, state, country, region, zip, email, phone, creditcard,creditcardtype, creditcardexpiration, username, password )VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, Fname, Lname, address1, address2, city, state, country, region, zip, email, phone,creditcard, creditcardtype, creditcardexp, username, password,))
            conn.commit()
            print '***********Query register success***********'
            return True
        else:
            return False
    except(Exception, psycopg2.DatabaseError)as error:
        print '************Something is broken on register*****************'
        print(error)


def db_login(username, password):
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
