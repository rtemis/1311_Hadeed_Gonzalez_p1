﻿CREATE OR REPLACE FUNCTION f_updOrders() RETURNS TRIGGER AS $$ 
	DECLARE 
		subtotal NUMERIC(7,2);

	BEGIN

	-- If the trigger was caused by insert
		IF (TG_OP = 'INSERT') THEN
		
		-- Setting price for inserted item
			NEW.price = (SELECT ROUND(price::NUMERIC,2)
			FROM products WHERE NEW.prod_id=prod_id);
			
		-- Updating net amount
			UPDATE orders
			SET netamount = ROUND((netamount + (NEW.price * NEW.quantity))::NUMERIC,2), orderdate = CURRENT_DATE
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
			SET netamount = ROUND((netamount - (OLD.price * OLD.quantity))::NUMERIC,2), orderdate = CURRENT_DATE
			WHERE OLD.orderid = orders.orderid;
			
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;	
			
			RETURN OLD;

	-- If the trigger was caused by update
		ELSIF (TG_OP = 'UPDATE') THEN

		-- Creating a subtotal to manage the new price of the product order  
			subtotal =  ROUND((OLD.price * (NEW.quantity - OLD.quantity))::NUMERIC,2); 
			
		-- Updating net amount
			UPDATE orders
			SET netamount = netamount + subtotal, orderdate = CURRENT_DATE
			WHERE OLD.orderid = orders.orderid;	
			
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;	
			
		-- Setting the new quantity
			OLD.quantity = NEW.quantity;

			RETURN OLD;
		END IF; 
			
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updOrders BEFORE INSERT OR DELETE OR UPDATE on orderdetail
	FOR EACH ROW EXECUTE PROCEDURE f_updOrders();
