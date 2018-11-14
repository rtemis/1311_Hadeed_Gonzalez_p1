update orderdetail
set price = products.price + (products.price * (0.02 * (date_part('year', CURRENT_DATE) - date_part('year', orders.orderdate)))) 
from products, orders 
where orderdetail.prod_id = products.prod_id and orders.orderid = orderdetail.orderid;
