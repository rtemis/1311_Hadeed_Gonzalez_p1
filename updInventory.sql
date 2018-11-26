CREATE OR REPLACE FUNCTION f_updInventory() RETURNS TRIGGER AS $$ 
	DECLARE
		temp1 RECORD;		-- For alerts table inserts
	BEGIN
		IF (TG_OP = 'UPDATE' AND NEW.status = 'Paid') THEN 
		-- Change to today's date
			OLD.orderdate = CURRENT_DATE;

		-- Updates the sales and stock fields of inventory on purchase
			UPDATE inventory
			SET stock = stock - T1.quantity, sales = sales + T1.quantity
			FROM (
				SELECT prod_id, quantity 
				FROM orders NATURAL JOIN orderdetail AS T2
				WHERE OLD.orderid = T2.orderid
				GROUP BY prod_id, quantity
			) AS T1
			WHERE inventory.prod_id = T1.prod_id;
			
		-- Inserts all elements with stock value less than 1 into alerts table 
			FOR temp1 IN (select prod_id from inventory where stock < 1) LOOP 
				INSERT INTO alerts (prod_id) VALUES (temp1.prod_id);
			END LOOP;
	--	ELSIF (TG_OP = 'UPDATE' AND NEW.status = 'Processed') THEN

	--	ELSIF (TG_OP = 'UPDATE' AND NEW.status = 'Shipped') THEN
		
		END IF;
		
		RETURN OLD;
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updInventory AFTER UPDATE ON orders 
	FOR EACH ROW EXECUTE PROCEDURE f_updInventory();