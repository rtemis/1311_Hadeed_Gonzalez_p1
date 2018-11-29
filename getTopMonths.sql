create or replace function getTopMonths(integer, integer) returns table(
	anno integer,
	mes integer,
	importe float,
	productos bigint
) as $$
	declare
		numprod alias for $1;
		imp alias for $2;
		temp1 record;
	begin
		for temp1 in (
			select yrs, mnth, sum(x) as ipte, sum(quantity) as total
			from (
				select sum(totalamount) as x, date_part('month',orderdate) as mnth, date_part('year',orderdate) as yrs, orderid
				from orders
				group by yrs, mnth, orderid
				order by yrs, mnth
			) as t1 join orderdetail on t1.orderid = orderdetail.orderid
			group by yrs, mnth
		) loop
			if temp1.ipte > imp then
		 		if temp1.total > numprod then 
					anno := temp1.yrs;
					mes := temp1.mnth;
					importe := temp1.ipte;
					productos := temp1.total;
					return next;
				end if;
			end if;
		end loop;
	end;
$$ language 'plpgsql';

select * from getTopMonths(19000,320000);
