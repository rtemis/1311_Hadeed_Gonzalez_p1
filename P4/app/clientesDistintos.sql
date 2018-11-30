-- ESTA CONSULTA COGE CADA PEDIDO POR SEPARADO DE UN CLIENTE EN UN MES DADO

EXPLAIN SELECT COUNT(DISTINCT(customerid)) as cc
FROM orders 
WHERE date_part('year', orderdate)=2015 AND date_part('month',orderdate)=04 AND totalamount > 100;

CREATE OR REPLACE INDEX anno ON orders(date_part('year',orderdate),date_part('month',orderdate));


-- ESTA CONSULTA COGE LA SUMA DE LOS PEDIDOS DE UN CLIENTE EN UN MES DADO

--SELECT COUNT(customerid) 
--FROM (
--	SELECT customerid, SUM(totalamount) as total
--	FROM orders 
--	WHERE date_part('year', orderdate)=2015 AND date_part('month',orderdate)=04
--	GROUP BY customerid
--) AS T1 
--WHERE total > 100;