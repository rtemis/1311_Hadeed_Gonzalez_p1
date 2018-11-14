--drop function getTopVentas(integer) cascade;

create or replace function getTopVentas(integer) returns table(
	anno integer,
	pelicula varchar,
	ventas bigint
) as $$
	declare 
		selyear alias for $1;
		temp1 record;
	begin 
		loop
		exit when selyear > date_part('year', current_date);

			for temp1 in (
				select max(sales), movietitle, prod_id, yr 
				from ( 
					select sum(quantity) as sales, prod_id, yr
					from (
						select prod_id, orderid, quantity, date_part('year', orderdate) as yr 
						from orders natural join orderdetail
						where date_part('year',orderdate) = selyear
						group by prod_id, orderid, quantity
					) as x 
					group by prod_id, yr
					order by prod_id, yr
				) as y natural join (products natural join imdb_movies)
				group by sales, prod_id, movietitle, yr
				order by sales desc
				limit 1
			) loop
				anno := temp1.yr;
				pelicula := temp1.movietitle;
				ventas := temp1.max;
				return next;
			end loop;
			selyear := selyear + 1;
		end loop;
	end;
$$ language 'plpgsql';

select * from getTopVentas(2012);







