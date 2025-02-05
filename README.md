# Dolibarr Python API 
by Nizo Priskorn 2020-2024

## Background
This API has been written and rewritten over a 
number of years based on the business requirements of 
the author.

It uses classes and MVC to handle the complexity of 
different suppliers and Dolibarr.

At ~12k lines it is currently the largest and 
most advanced API written for Dolibarr 
and can be used to automate almost 
all actions in Dolibarr v14 to 
avoid tedious and time consuming manual entry. 
E.g. entring the payment data for an invoice and mark it as paid.

The hundred of hours invested in the writing of this API 
has paid back itself multiple times by 
delivering business value. 
It is battle tested and gets the job done.

## Features

* Login and scraping of data from supplies semi-automatically and automatically.
* Scraping of Shimano PDF invoices is supported to better handle their order/shipment 
complexity compared to scraping the orders from their website.  
* Semi-automatic order import from Sello AB which links to Tradera and other marketplaces.
* Product import based on scraped supplier data.
* Custom accounting report generation using Pandas. 
* Generation of tax and report data for Skatteverket.
* Scripts to handle prices and products in bulk to avoid tedious manual work.

Not included
* Custom SQL scripts that are useful to track sales and orders, 
list inventory that has not moved for a specific time period, etc.

## Classes
A total of 119 classes have been written to support the import of orders, 
products and provide accounting reports in a swedish context.

### Examples:
src/controllers/dolibarr/customer/invoice.py
src/controllers/dolibarr/customer/order.py
src/controllers/dolibarr/customer/payment.py
src/controllers/dolibarr/product.py
src/controllers/dolibarr/supplier/invoice.py
src/controllers/dolibarr/supplier/order.py
src/controllers/dolibarr/supplier/payment.py
src/controllers/marketplaces/sello/order.py
src/controllers/marketplaces/sello/orders.py
src/models/supplier/order/eu_order.py
src/models/suppliers/shimano/login.py
src/my_base_class.py
src/views/dolibarr/customer/invoice.py
src/views/dolibarr/entities.py
src/views/dolibarr/product.py
src/views/dolibarr/supplier/invoice.py
src/views/dolibarr/supplier/order.py
src/views/marketplaces/sello/order.py
src/views/marketplaces/sello/order_row.py
src/views/my_base_view.py

## Tests
105 manual tests written so far which cover 69% of the code.

## SCC Statistics
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                      96      8694      487      1997     6210        229
───────────────────────────────────────────────────────────────────────────────
Total                       96      8694      487      1997     6210        229
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $183,798
Estimated Schedule Effort (organic) 7.23 months
Estimated People Required (organic) 2.26
───────────────────────────────────────────────────────────────────────────────
Processed 340544 bytes, 0.341 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
src/views:
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                      14       923       56       175      692        120
───────────────────────────────────────────────────────────────────────────────
Total                       14       923       56       175      692        120
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $18,352
Estimated Schedule Effort (organic) 3.01 months
Estimated People Required (organic) 0.54
───────────────────────────────────────────────────────────────────────────────
Processed 38509 bytes, 0.039 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
src/controllers:
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                      26      1891       88       276     1527         57
───────────────────────────────────────────────────────────────────────────────
Total                       26      1891       88       276     1527         57
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $42,133
Estimated Schedule Effort (organic) 4.13 months
Estimated People Required (organic) 0.91
───────────────────────────────────────────────────────────────────────────────
Processed 80914 bytes, 0.081 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
tests:
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                      75      2441      229      1125     1087         41
───────────────────────────────────────────────────────────────────────────────
Total                       75      2441      229      1125     1087         41
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $29,487
Estimated Schedule Effort (organic) 3.60 months
Estimated People Required (organic) 0.73
───────────────────────────────────────────────────────────────────────────────
Processed 84573 bytes, 0.085 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
Total:
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                     203     15187      971      5233     8983        511
JSON                         5      2587        0         0     2587          0
Shell                        4        21        0         5       16          0
INI                          2         8        1         1        6          0
Plain Text                   2       185        0         0      185          0
YAML                         2        80        4        30       46          0
Markdown                     1        15        3         0       12          0
TOML                         1       169        7        20      142          0
───────────────────────────────────────────────────────────────────────────────
Total                      220     18252      986      5289    11977        511
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $366,320
Estimated Schedule Effort (organic) 9.39 months
Estimated People Required (organic) 3.47
───────────────────────────────────────────────────────────────────────────────
Processed 680417 bytes, 0.680 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────

## Abstract classes
All supplier classes which should never be instantiated are abstract.

## MVC
Separated into model, view and controller in june 2024.
The view handles all questions and similar.
The controller handles all CUD operations.
The model handles all read operations.

## Obstacles

* Unreliable data from suppliers
* Bugs in Dolibarr (file upload does not seem to work via API in v14 no matter what I tried resulting 
no photos could be added to the products during import) - the bug was reported and is allegedly fixed in newer version of Dolibarr.
* Missing API actions for certain operations, like linking order to invoice, etc.
* Missing knowledge as a solo developer. This has been a real learning experience!

## Thanks
I want to thank all the people at the Dolibarr forum who helped me with understanding 
the inner workings of the API when I failed.
