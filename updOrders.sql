CREATE OR REPLACE FUNCTION updOrders(integer) RETURNS TRIGGER AS $$ 
	DECLARE 
		customer ALIAS FOR $1;
		tmp record;
	BEGIN
		IF TG_OP = INSERT THEN 
			NEW.orderdate := CURRENT_DATE;
			NEW.customerid := customer;
			NEW.status := "Pending";
			NEW.tax := 15;
			RETURN NEW;
			SELECT setOrderAmount();
		ELSIF TG_OP = DELETE THEN
			OLD.
			RETURN 
			
	END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_updOrders(integer) BEFORE INSERT, DELETE on orders
	FOR EACH ROW EXECUTE PROCEDURE updOrders(integer);

INSERT into orders VALUES (693); 