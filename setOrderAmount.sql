create or replace function setOrderAmount() returns void as $$
	begin
		CREATE VIEW netamt AS
			SELECT orderid, SUM(price * quantity) AS total
			FROM orderdetail
			GROUP BY orderid;
			
		UPDATE orders
		SET netamount = netamt.total
		FROM netamt
		WHERE orders.orderid = netamt.orderid;

		DROP VIEW netamt;
		
		CREATE VIEW totals AS 
			select orderid, sum(netamount + (netamount * (tax/100.0))) as newtotal
			from orders 
			group by orderid;

		UPDATE orders
		SET totalamount = totals.newtotal
		FROM totals
		WHERE orders.orderid = totals.orderid;

		DROP VIEW totals;
	end;
$$ language 'plpgsql';

select setOrderAmount();