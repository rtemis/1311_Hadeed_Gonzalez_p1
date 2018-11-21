CREATE OR REPLACE FUNCTION f_updOrders() RETURNS TRIGGER AS $$ 
	BEGIN
	
	-- If the trigger was caused by insert
		IF (TG_OP = 'INSERT') THEN
		-- Updating net amount

			NEW.price = (SELECT ROUND(price::NUMERIC,2)
			FROM products WHERE NEW.prod_id=prod_id);

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

		ELSIF (TG_OP = 'UPDATE') THEN
		
			UPDATE orders
			SET netamount = ROUND((OLD.price * NEW.quantity)::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;

			UPDATE orders
			SET totalamount = ROUND((netamount * (1 + tax/100.0))::NUMERIC,2)
			WHERE OLD.orderid = orders.orderid;	
			RETURN OLD;
		END IF; 
			
	END;
$$ LANGUAGE 'plpgsql';

--DROP TRIGGER updOrders on orderdetail
CREATE TRIGGER updOrders BEFORE INSERT OR DELETE OR UPDATE on orderdetail
	FOR EACH ROW EXECUTE PROCEDURE f_updOrders();

insert into orders (orderid, orderdate, customerid, status) values (181791, current_date, 30, NULL);

insert into orderdetail (orderid, prod_id, quantity) values (181791,1,9);
select * from orderdetail natural join orders where orderid = 181791;

update orderdetail set quantity=quantity-1 where prod_id=1 and orderid=181791;
select * from orderdetail natural join orders where orderid = 181791;

delete from orders where orderid=181791;

delete from orderdetail where orderid=181791;
select * from orderdetail natural join orders where orderid = 181791;