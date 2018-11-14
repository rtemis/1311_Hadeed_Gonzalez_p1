create or replace function getTopMonths(integer, integer) returns table(
	anno integer,
	mes integer,
	importe float,
	productos bigint
) as $$
	declare
		numprod alias for $1;
		importe alias for $2;
		temp1 record;
	begin

	end;
$$ language 'plpgsql';

select * from getTopMonths(2012);
