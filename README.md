***This is now archived since I have closed my business and do not intend to support or develop this further.***
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
- src/
 - controllers/
   - dolibarr/
     - customer/
       - invoice.py
       - order.py 
       - payment.py
     - product.py
     - supplier/
       - invoice.py
       - order.py
       - payment.py
   - marketplaces/
     - sello/
       - order.py
       - orders.py
 - models/
   - supplier/
     - order/
       - eu_order.py
   - suppliers/
     - shimano/
       - login.py
 - my_base_class.py
 - views/
   - dolibarr/
     - customer/
       - invoice.py
     - entities.py
     - product.py
     - supplier/
       - invoice.py
       - order.py
   - marketplaces/
     - sello/
       - order.py
       - order_row.py
   - my_base_view.py
## Tests
105 manual tests written so far which cover 69% of the code.

## SCC Statistics
```
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
```
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

## Assessment by Claude based on SCC
Looking at the code metrics provided, I notice a few potential areas for improvement:

1. Unbalanced Code-to-Test Ratio
- There are 96 Python files with 6,210 lines of code
- But only 75 test files with 1,087 lines of test code
- This suggests test coverage may be insufficient
- Aim for at least 1:1 ratio of test code to production code

2. High Cyclomatic Complexity
- Controllers have 57 complexity points across 26 files
- Views have 120 complexity points across 14 files
- Consider refactoring complex views to reduce cognitive load
- Break down complex methods into smaller, more focused ones

3. Comments-to-Code Distribution
- 1,997 comments for 6,210 lines of code (about 32% comment ratio)
- Comments seem concentrated in tests (1,125 comments) rather than main code
- Consider adding more documentation in the main codebase, especially for complex logic

4. Structural Improvements
- Consider splitting larger files (some views/controllers may be too large)
- Look for opportunities to extract common functionality into base classes
- Could potentially reorganize code to improve the module structure
