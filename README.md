# AirlineReservation

Airline reservation system for Database Class

### FILE DESCRIPTIONS ###

CSS
index.css - global stylesheet

HTML
base.html - global html base which allows css to more easily be passed through
customer_delete_flight.html - form to allow customer to delete a flight
customer_purchase_flight.html - form to allow customer to purchase a flight
customer_rate_and_comment.html - form to let customer rate and comment on their flights
customer_spending.html - form which displays customer spending + bar chart
customer_stage_delete.html - confirmation to delete ticket
customer_stage_purchase.html - confirmation to make a purchase
customer_stage_rate_and_comment.html - form for customer to rate and comment on a flight
customer_view_flights.html - allow customer to view all their purchased flights
customer.html - customer home menu
index.html - home page for not logged customers
login_customer.html - login screen for customer
login_staff.html - login screen for staff
public_info.html - form to search for flight info
public_status.html - form to search for flight status
register customer.html - form to make a new customer account
register staff.html - form to make a new staff account
staff_add_new_airplane.html - form for staff to add a new airplane for their company
staff_add_new_airport.html - form for staff to add a new airport
staff_change_flight_status.html - form to let staff change status of existing flights
staff_chart.html - displays bar graph for staff for past year of tickets sales
staff_create_flight.html - form to let staff make a new flight
staff_view_flight_ratings.html - form to let staff view average ratings of their flights
staff_view_flights_customers.html - form to let staff view customers of their flights
staff_view_flights.html - form to let staff view their airline’s flights
staff_view_frequent_customer.html - form to allow for staff to view their airline’s most frequent customer
staff_view_ratings_and_comments.html - form to allow staff to view specific ratings and commends for each flight
staff_view_report_form.html - form which chooses a date range to create a report form
staff_view_report.html - shows earnings report for a period of time
staff_view_revenue.html - shows revenue for airline in a period of time
staff.html - home page for staff
success.html - displays success message after successful form
table_template.html - template for tables

Python
tests.py - testing various datetime configurations
customer.py - all customer queries
general.py - general functions for SQL, authentication, and date checking
login.py - functions related to session management and verifying credentials
public_info.py - queries for all use cases for public group
register.py - queries for all use cases for register group
staff.py - queries for all use cases for staff group
__init__.py - all views for every page in web app

Config
db_info.yaml - DB login configuration (info to establish DB connection)

SQL
create_tables.sql - create schema and all SQL tables
inserts.sql - add dummy data to database


### USE CASES ###

Public Use Cases:

1. Search for flight information

Files
Public_info.html - web page for public flight information
Public_info.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Public_view_twoway_flights - builds and executes SQL query on two way flights
Public_view_oneway_flights - builds and executes SQL query on one way flights
Public_info - renders public_info.html
Public_view_flights - gets user input, displays result of query

2. View flight status

Files
Public_status.html - web page for public flight status
Public_info.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Public_view_flight_status - executes SQL query on one way flights
Public_status - renders public_status.html
Public_check_status - gets user input, displays result of query

Staff Use Cases:

1. View flights

Files
Staff_view_flights.html - shows form and query results
Staff_view_flights_customers.html - shows customers on a flight
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_view_flights - gets flight info and displays all flights matching query
Staff_view_flights_customer - shows customers on a flight

2. Create new flights

Files
Staff_create_flight.html - shows form for creating flight
Success.html - shows success message
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_create_flight_view - renders create flight page
Staff_create_flight_submit - runs query to add flight

3. Change status of flights

Files
Staff_change_flight_status.html - form to change flight status
Success.html - shows success message
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_change_flights - renders form for changing flight status
Staff_change_flights_submit - runs query to change flight status

4. Add an airplane in the system

Files
Staff_add_new_airplane.html - form to add new airplane
Success.html - shows success message
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_add_new_airplane - renders add new airplane form
Staff_add_new_airplane_submit - runs query for adding new airplane

5. Add new airport in the system

Files
Staff_add_new_airport.html
Success.html - shows success message
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_add_new_airport - renders form to add new airport
Staff_add_new_airport_submit - runs query to add new airport
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

6. View flight ratings

Files
Staff_view_flight_ratings.html - search form and shows list of flights and ratings
Staff_view_ratings_and_comments.html - shows comments and ratings for a single flight
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_view_flight_ratings - runs query to filter for flights, and allows flights to be selected to see ratings and comments
Staff_view_ratings_and_comments_view - gives comments and rating  for individual flights

7. View frequent customers

Files
Staff_view_frequent_customer.html - shows the most frequent customer
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_view_frequent_customer - runs query to get most frequent customer

8. View reports

Files
Staff_view_report_form.html - shows form to select range which to generate form
Staff_view_report.html - shows report
Staff_chart.html - shows bar chart on sales by month
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_view_tickets_sold - render form to get range to generate report
Staff_view_tickets_sold_view - run queries to get report data
Staff_view_monthly_sales - run queries to generate bar chart data

9. View earned revenue

Files
Staff_view_revenue.html - show revenue and form to select range
Staff.py - contains helper functions, prepared statements
General.py - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Staff_view_revenue - runs queries to get revenue data
	
Customer Use Cases:

1. View my flights

Files
Customer_view_flights.html - web page for customer’s flights information
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_view_flight - gets user input, displays results of query

2. Search for flights

Files
Public_info.html - web page for public flight information
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_search_flight - gets user input, displays results of query

3. Purchase ticket

Files
Customer_stage_purchse.html - web page with selectable flights for purchase
Customer_purchase_flight.html - web page to enter card information and make purchase
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_init_purchase - loads customer_purchase_flight.html with default query results
Customer_purchase_search_flight - loads customer_purchase_flight.html with user specified query results
Customer_stage_purchase - loads customer_stage_purchase.html with user selected flight information
Customer_confirm_purchase - gets user input card information, makes ticket purchase

4. Cancel ticket

Files
Customer_delete_flight.html -  web page to select flight to delete
Customer_stage_delete.html - web page to delete selected flight
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_init_delete - loads customer_delete_flight.html with default query results
Customer_search_delete - loads customer_delete_flight.html with user specified query results
Customer_confirm_delete - cancels the selected flight

5. Give rating and comment

Files
Customer_stage_rate_and_comment.html - web page to make comment and rating
Customer_rate_and_comment.html - web page to view comments, rating, and select flights
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_rate_and_comment - loads customer_rate_and_comment.html with default data
Customer_stage_rate_and_comment - loads customer_create_rate_and_comment.html with user selected ticket information
Customer_create_rate_and_comment - gets user input and creates a flight review

6. Track Spending

Files
Customer_spending.html - web page to view customer’s spending + bar chart
Customer.py - contains helper functions, prepared statements
General.py  - contains helper functions, prepared statements
__init__.py - contains app functions

Functions
Customer_spending - loads customer_spending.html with default data
Customer_spending_search - loads customer_spending.html with user specified data
Customer_spending_past6months - loads customer_spending.html in the past 6 months
Customer_spending_pastyear - loads customer_spending.html in the past year

7. Logout

Files
__init__.py - contains app functions

Functions
Logout - resets session metadata and redirects to homepage 


### TEAM SUMMARY ###

Sanjana Gupta
Helped create + correct ER diagram and relational diagram for parts 1 and 2. Also helped write some sql for part 2. Assisted with part 3 use cases for staff and customer on front + back end.

Junming Qiu
I worked on frontend and backend in login session persistence, staff use cases, styling, creating framework for HTML templates, creating variable SQL statements, and testing.

Harry Rios
Worked on schema design and sql queries in parts 1 and 2. Wrote prepared sql statements in part 3. Helped develop customer and public use cases, front and back end. 


