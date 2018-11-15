update orderdetail
set price = (products.price * (0.98 ^ (date_part('year', CURRENT_DATE) - date_part('year', orders.orderdate)))) 
from products, orders
where orderdetail.prod_id = products.prod_id and orders.orderid = orderdetail.orderid;
