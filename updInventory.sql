CREATE OR REPLACE FUNCTION f_updInventory() RETURNS TRIGGER AS $$ 
	DECLARE
		subamt INTEGER;
		temp1 RECORD;
	BEGIN
		IF (TG_OP = 'UPDATE') THEN 
			OLD.orderdate = CURRENT_DATE;
			
			UPDATE inventory
			SET stock = stock - T1.quantity, sales = sales + T1.quantity
			FROM (
				SELECT prod_id, quantity 
				FROM orders NATURAL JOIN orderdetail AS T2
				WHERE OLD.orderid = T2.orderid
				GROUP BY prod_id, quantity
			) AS T1
			WHERE inventory.prod_id = T1.prod_id;

		--	FOR temp1 IN (SELECT * FROM inventory) LOOP
			--	IF (temp1.stock < 1) THEN
				--	INSERT INTO alerts (prod_id, stock) VALUES (temp1.prod_id, temp1.stock);
		--		END IF;
			--END LOOP;
		END IF;

		RETURN OLD;
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updInventory AFTER UPDATE ON orders 
	FOR EACH ROW EXECUTE PROCEDURE f_updInventory();


--insert into orders (orderid, orderdate, customerid) values (181791, current_date, 30);
--insert into orderdetail (orderid, prod_id, quantity) values (181791,7,9);
--select * from orderdetail natural join orders where orderid = 181791;

--select * from alerts

--insert into orderdetail (orderid, prod_id, quantity) values (181791,6,9);
--select * from orderdetail natural join orders where orderid = 181791;

--update orderdetail set quantity=quantity-8 where prod_id=6 and orderid=181791;
--select * from orderdetail natural join orders where orderid = 181791;

--delete from orderdetail where orderid=181791;
--select * from orderdetail natural join orders where orderid = 181791;
--delete from orders where orderid=181791;


--update orders set status = 'Paid' where orderid = 181791;
