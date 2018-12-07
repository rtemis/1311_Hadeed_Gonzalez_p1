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

    # Creacion del indice
    db_conn.execute("CREATE INDEX anno ON orders(date_part('year',orderdate),date_part('month',orderdate))")

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    # Iterando sobre los clientes
    for ii in range(niter):
        # En caso de seleccionar 'usar prepare' en la pagina principal
        if use_prepare == True:

            # Inicializamos la transaccion
            twoPhase = db_conn.begin_twophase()
            # Preparamos la transaccion
            twoPhase.prepare()
            # Recogemos el resultado de la query para uso futuro
            result = twoPhase.execute(consulta,anio,mes,iumbral)
            # Hacemos el commit para guardar los cambios en la base de datos
            twoPhase.commit()
            # Liberamos memoria de la transaccion
            twoPhase.DEALLOCATE

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

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

#    try:
        # TODO: ejecutar consultas

#    except Exception as e:
        # TODO: deshacer en caso de error

#    else:
        # TODO: confirmar cambios si todo va bien


    return dbr
