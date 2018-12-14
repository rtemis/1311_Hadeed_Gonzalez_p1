# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import *

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})
db_meta = MetaData(bind=db_engine)

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # Conexion a la base de datos
    db_conn = dbConnect()

    # Creacion de la consulta
    consulta = "SELECT COUNT(DISTINCT(customerid)) as cc \
    FROM orders WHERE date_part('year', orderdate)=%s \
    AND date_part('month',orderdate)=%s AND totalamount > %s"

    # Creacion del prepare
    db_conn.execute("PREPARE listaClientes (numeric,numeric,numeric) AS\
                SELECT COUNT(DISTINCT(customerid)) as cc \
                FROM orders WHERE date_part('year', orderdate)=$1\
                AND date_part('month',orderdate)=$2 AND totalamount > $3")

    # Creacion del indice
    db_conn.execute("CREATE INDEX anno ON orders(date_part('year',orderdate),date_part('month',orderdate))")

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    # Iterando sobre los clientes
    for ii in range(niter):
        # En caso de seleccionar 'usar prepare' en la pagina principal
        if use_prepare == True:
            result = db_conn.execute("EXECUTE listaClientes(%s,%s,%s)", anio, mes, iumbral)

        # En caso contrario
        else:
            # Ejecutamos directamente la consulta
            result = db_conn.execute(consulta,anio,mes,iumbral)

        # Recogemos los datos devueltos por la consulta
        res = result.fetchone()

        # Guardamos el resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})

        # Si se sale del bucle al no tener clientes
        if break0 == True:
            if res['cc'] == 0:
                break

        # Actualizacion de umbral
        iumbral = iumbral + iintervalo

    db_conn.close()

    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)

    resultproxy.close()

    db_conn.close()

    return a

def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()

    db_conn.close()

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}

def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    print "Enters here"
    # Array de trazas a mostrar en la página
    dbr=[]

    # Conexion a la base de datos
    db_conn = dbConnect()

    # Preparacion de las tablas para transacciones de SQLAlchemy
    customers = Table('customers',db_meta, autoload=True, autoload_with=db_engine)
    orders = Table('orders', db_meta, autoload=True, autoload_with=db_engine)

    try:
        print "ENTERS HERE "
        # En caso de querer usar sentencias SQL
        if bSQL == True:
            print "BSQL TRUE"

            # Iniciar la consulta
            db_conn.execute("BEGIN")

            # En caso de querer provocar un fallo, se hace el borrado fuera de orden
            if bFallo == True:
                print "BFALLO TRUE"
                # Ejecucion de la query
                results = db_conn.execute("DELETE FROM customers WHERE customerid=%s", customerid)
                # raise Exception
            else:
                print "BFALLO FALSE "
                result = db_conn.execute("SELECT orderid FROM orders WHERE customerid=%s", customerid)
                orderid = []
                for x in result:
                    orderid.append(x.encode('ascii','ignore'))
                print "RESSSSSS"
                for x in orderid:
                    print "NEXT"
                    results = db_conn.execute("DELETE FROM orderdetail WHERE orderid=%s", x)
                    # Anadir traza a dbr
                    traza = results.fetchone()[]
                    dbr.append(traza)
                print "REACGGG"
                # Borrado primero de las tablas donde se usa el customer id como clave foranea
                results = db_conn.execute("DELETE FROM orders WHERE customerid=%s", customerid)

            # Anadir traza a dbr
            traza = results.fetchone()
            dbr.append(traza)

            # Si el usuario ha seleccionado commits intermedios
            if bCommit == True:
                print "BCOMMIT"
                db_conn.execute("COMMIT")

            # Ejecucion de la query
            results = db_conn.execute("DELETE FROM customers WHERE customerid=%s", customerid)

        else:
            print "BSQL FASLE"
            # Comienzo de query
            trans = db_conn.begin()

            # Creacion de la query con sqlalchemy
            query1 = db.delete(orders)
            query1 = query1.where("%s.columns.customerid = %s", orders, customerid,)
            print "QUERY1"

            query = db
            # Creacion de la query con sqlalchemy
            query2 = db.delete(customers)
            query2 = query2.where("%s.columns.customerid = %s", customers, customerid,)
            print "QUERY2"

            if bFallo == True:
                print "FALLOOOO"
                # Ejecucion de la query fuera de orden
                results = trans.execute(query2)
                # raise Exception
            else:
                print " NOFALLO "
                # Ejecucion de la query en orden
                results = trans.execute(query1)

            # Anadir traza a dbr
            traza = results.fetchone()
            dbr.append(traza)

            # Si el usuario ha seleccionado commits intermedios
            if bCommit == True:
                trans.commit()

            # Ejecucion de la query con sqlalchemy
            results = trans.execute(query2)

        # En caso de querer provocar fallos
        if duerme != 0:
            time.sleep(duerme)

        # Anadir traza a dbr
        traza = results.fetchone()
        dbr.append(traza)

        # Si se produce un fallo, por ejemplo el deadlock
    except Exception as e:
        print "ENTERSSSSS HEREEEE"
        # Deshace en caso de error
        if bSQL == True:
            db_conn.execute("ROLLBACK")
        else:
            trans.rollback()
    else:
        # Confirma cambios si todo va bien
        if bSQL == True:
            db_conn.execute("COMMIT")
        else:
            trans.commit()

    dbCloseConnect(db_conn)
    return dbr
