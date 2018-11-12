drop function getTopVentas() cascade;

create or replace function getTopVentas(integer anno) returns setof record as $$
	declare 
		temp1 record;
	begin 
		for select * in 
	end;
$$ language 'plpgsql';