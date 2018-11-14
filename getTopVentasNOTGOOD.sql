drop function getTopVentas(integer) cascade;

drop view sales cascade ;
drop view movies cascade ;
drop view orderyears cascade ;

create or replace function getTopVentas(integer) returns table(
	anno integer,
	pelicula varchar,
	ventas bigint
) as $$
	declare 
		maximum bigint := 0;
		selyear alias for $1;
		temp1 record;
		temp2 record;
	begin 
		create view sales as 
			select prod_id, count(quantity) as sale
			from orderdetail
			group by prod_id;
			
		create view movies as
			select prod_id, movietitle
			from products natural join imdb_movies
			where products.movieid=imdb_movies.movieid;

		create view moviesales as 
			select * 
			from movies natural join sales;

		create view orderyears as 
			select prod_id, date_part('year',orderdate) as yr
			from orders natural join orderdetail
			order by yr desc;

		create view results as 
			select yr, movietitle, max(sale) as ventas
			from moviesales natural join orderyears
			group by yr, movietitle
			order by yr desc;

		loop
		exit when selyear > date_part('year', current_date);
			for temp1 in( select * from results )loop
				if temp1.yr = selyear then
					if temp1.ventas > maximum then
						maximum := temp1.ventas;
						temp2 := temp1;
					end if;
				end if;
			end loop;
			anno := selyear;
			pelicula := temp2.movietitle;
			ventas := temp2.ventas;
			return next;
			selyear := selyear + 1;
			maximum := 0;
		end loop;
		
		
	end;
$$ language 'plpgsql';

select getTopVentas(2014);



select max(ventas), movietitle, prod_id, yr 
from ( 
	select count(quantity) as ventas, prod_id, yr
	from (
		select prod_id, orderid, quantity, date_part('year', orderdate) as yr 
		from orders natural join orderdetail
		where date_part('year',orderdate) = 2015
		group by prod_id, orderid, quantity
		)as x 
	group by prod_id, yr
	order by prod_id, yr
) as y natural join (products natural join imdb_movies)
group by ventas, prod_id, movietitle, yr
order by ventas desc
limit 1;



