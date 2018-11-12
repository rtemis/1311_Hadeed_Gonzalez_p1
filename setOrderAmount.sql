
drop function setOrderAmount();

create or replace function setOrderAmount() returns void as $$
	begin
		UPDATE orders
		SET netamount = t2.total
		FROM (
			SELECT orderid, SUM(price * quantity) AS total
			FROM orderdetail
			GROUP BY orderid
		) AS t2 where orders.orderid = t2.orderid;

		UPDATE orders 
		SET totalamount = t2.total
		FROM (
			SELECT orderid, sum(netamount + (netamount * (tax/100.0))) AS total
			FROM orders
			GROUP BY orderid
		) AS t2 where orders.orderid = t2.orderid; 
		
	end;
$$ language 'plpgsql';

select setOrderAmount();


