CREATE INDEX IF NOT EXISTS estado ON orders(status); 

EXPLAIN select count(*) 
from orders 
where status is null;

EXPLAIN select count(*) 
from orders 
where status ='Shipped';

select count(*) 
from orders 
where status ='Paid';

select count(*) 
from orders 
where status ='Processed';
