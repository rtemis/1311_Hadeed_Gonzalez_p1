drop function getTopVentas() cascade;

drop view sales cascade ;
drop view movies cascade ;
drop view orderyears cascade ;
drop view results cascade ;
create or replace function getTopVentas(integer anno) returns setof record as $$
	declare 
		maximum bigint := 0;
		temp1 record;
		temp2 record;
	begin 
		create view sales as 
			select prod_id, count(quantity) as ventas
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
			select yr, movietitle, max(ventas)
			from moviesales natural join orderyears
			group by yr, movietitle, ventas
			order by yr desc;

		select * from results;
		
		
		
	end;
$$ language 'plpgsql';

select getTopVentas(1970);
