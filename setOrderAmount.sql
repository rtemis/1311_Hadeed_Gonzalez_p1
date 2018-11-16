--drop view totals;
--drop view netamt;
--drop function setOrderAmount();

create or replace function setOrderAmount() returns void as $$
	begin
		CREATE VIEW netamt AS
			SELECT orderid, SUM(price * quantity) AS total
			FROM orderdetail
			GROUP BY orderid;
			
		UPDATE orders
		SET netamount = ROUND(netamt.total::NUMERIC,2)
		FROM netamt
		WHERE orders.orderid = netamt.orderid;

		CREATE VIEW totals AS 
			select orderid, sum(netamount + (netamount * (tax/100.0))) as newtotal
			from orders 
			group by orderid;

		UPDATE orders
		SET totalamount = ROUND(totals.newtotal::NUMERIC,2) 
		FROM totals
		WHERE orders.orderid = totals.orderid;
	end;
$$ language 'plpgsql';

select setOrderAmount();

