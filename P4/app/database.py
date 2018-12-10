# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine, MetaData, Table

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

    # Array de trazas a mostrar en la página
    dbr=[]

    # Conexion a la base de datos
    db_conn = dbConnect()

    # Creacion del constraint
    constraint = "ALTER TABLE customers DROP CONSTRAINT customers_pkey, \
    ADD CONSTRAINT PRIMARY KEY (customerid) ON DELETE CASCADE"

    # Preparacion de la tabla customers
    customers = Table('customers',db_meta, autoload=True, autoload_with=db_engine)

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

    try:
        # En caso de querer usar sentencias SQL
        if bSQL == True:
            # Iniciar la consulta
            db_conn.execute("BEGIN")
            # Anadir el constraint ON DELETE CASCADE
            db_conn.execute(constraint)

            # Si el usuario ha seleccionado commits intermedios
            if bCommit == True:
                db_conn.execute("COMMIT")

            # Ejecucion de la query
            results = db_conn.execute("DELETE FROM customers WHERE customerid=%s", customerid)

        else:
            # Comienzo de query
            db_conn.begin()
            # Anadir el constraint ON DELETE CASCADE
            db_conn.execute(constraint)

            # Si el usuario ha seleccionado commits intermedios
            if bCommit == True:
                db_conn.commit()

            # Creacion de la query con sqlalchemy
            query = db.delete(customers)
            query = query.where((customers.columns.customerid = "%s"), customerid)

            # Ejecucion de la query con sqlalchemy
            results = connection.execute(query)

        # En caso de querer provocar fallos
        if bFallo == True:
            time.sleep(duerme)

        # Anadir traza a dbr
        traza = results.fetchone()
        dbr.append(traza)

        # Si se produce un fallo, por ejemplo el deadlock
    except Exception as e:
        # TODO: deshacer en caso de error
        if bSQL == True:
            db_conn.execute("ROLLBACK")
        else:
            db_conn.rollback()
    else:
        # TODO: confirmar cambios si todo va bien
        if bSQL == True:
            db_conn.execute("COMMIT")
        else:
            db_conn.commit()

    dbCloseConnect(db_conn)
    return dbr
