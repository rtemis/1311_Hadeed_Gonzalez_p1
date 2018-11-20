CREATE OR REPLACE FUNCTION f_updOrders() RETURNS TRIGGER AS $$ 
	BEGIN
	
	-- If the trigger was caused by insert
		IF (TG_OP = 'INSERT') THEN
		-- Updating net amount
			
			SELECT ROUND(price::NUMERIC,2) INTO NEW.price
			from products where NEW.prod_id=prod_id;

			UPDATE orders
			SET netamount = ROUND((netamount + (NEW.price * NEW.quantity))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;
			RETURN NEW;
			
	-- If the trigger was caused by delete
		ELSIF (TG_OP = 'DELETE') THEN
		-- Updating net amount
			UPDATE orders
			SET netamount = ROUND((netamount - (OLD.price * OLD.quantity))::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;	
			RETURN OLD;		
		END IF; 
			
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updOrders BEFORE INSERT OR DELETE on orderdetail
	FOR EACH ROW EXECUTE PROCEDURE f_updOrders();

--insert into orderdetail (orderid, prod_id, quantity) values (140320,1,9);
--select * from orderdetail natural join orders where orderid = 140320;
--delete from orderdetail where orderid=140320 and prod_id=1;
--select * from orderdetail natural join orders where orderid = 140320;