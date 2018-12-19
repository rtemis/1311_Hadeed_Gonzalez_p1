alter table customers add column promo numeric(7,2);

create or replace function f_updPromo() returns trigger as $$
	begin
		update orders
		set totalamount = orderamount * (100-NEW.promo);
	end;
$$ language 'plpgsql';


create trigger updPromo before update on customers
    FOR EACH ROW EXECUTE PROCEDURE f_updPromo();