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
		SET netamount = t2.total
		FROM (
			SELECT orderid, round(avg(total)::NUMERIC,2) as total
			FROM netamt
			GROUP BY netamt.orderid
		) AS t2 WHERE orders.orderid = t2.orderid;

		CREATE VIEW totals AS 
			select orderid, sum(netamount + (netamount * (tax/100.0))) as newtotal
			from orders 
			group by orderid;

		UPDATE orders
		SET totalamount = t2.newtotal 
		FROM (
			SELECT orderid, round(avg(newtotal)::NUMERIC,2) as newtotal
			FROM totals
			GROUP BY totals.orderid
		) AS t2 WHERE orders.orderid = t2.orderid;
	end;
$$ language 'plpgsql';

select setOrderAmount();

