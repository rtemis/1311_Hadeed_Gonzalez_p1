update orderdetail 
set price = products.price 
from products where orderdetail.prod_id = products.prod_id;  