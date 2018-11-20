CREATE OR REPLACE FUNCTION f_updOrders() RETURNS TRIGGER AS $$ 
	BEGIN
	-- If the trigger was caused by insert
		IF (TG_OP = 'INSERT') THEN
		-- Updating net amount
			UPDATE orders
			SET netamount = ROUND((netamount + (NEW.price * NEW.quantity))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;
			
	-- If the trigger was caused by delete
		ELSIF (TG_OP = 'DELETE') THEN
		-- Updating net amount
			UPDATE orders
			SET netamount = ROUND((netamount - (NEW.price * NEW.quantity))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;
		-- Updating total amount
			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE NEW.orderid = orders.orderid;

		END IF; 
			
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updOrders() BEFORE INSERT, DELETE on orderdetail
	FOR EACH ROW EXECUTE PROCEDURE updOrders();

insert into orderdetail VALUES (1)

