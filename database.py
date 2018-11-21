
import psycopg2
import os



def db_register(name, username, password, email, creditcard, address, dob):
    try:
        conn = psycopg2.connect("dbname='si1' user='alumnodb' host='localhost' password='alumnodb'")
        print '---------CONEXION A LA BASE DE DATOS CON EXITO-----------'
    except:
        print "***********I am unable to connect to the database*************"

    cur = conn.cursor()
    try:

        query="""insert into customers(firstname, lastname,address1, email, creditcard, username, password, city, country, region, creditcardtype)values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(query, (name, name, address, email, creditcard, username, password, name, name, name, 'VISA'))
        conn.commit()
        print '=========query exitosa========='
    except:
        print '************Something is broken*****************'




def prueba():
    try:
        conn = psycopg2.connect("dbname='si1' user='alumnodb' host='localhost' password='alumnodb'")
        print '---------CONEXION A LA BASE DE DATOS CON EXITO-----------'
    except:
        print "***********I am unable to connect to the database*************"

    cur = conn.cursor()
    try:
        cur.execute("insert into imdb_languages (lang) values('españita')")
    except:
        print '$$$$$$$$$$$4tusmuertos------------------------------'
