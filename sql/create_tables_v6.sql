create schema flight_app;

use flight_app;

create table airline(
    name            varchar(20) not null,
    primary key (name)
);
create table airline_staff(
    username        varchar(20) not null,
    password        varchar(40) not null,
    fname           varchar(20) not null,
    lname           varchar(20) not null,
    dob             timestamp not null,
    employer        varchar(20) not null,
    primary key (username),
    foreign key (employer) references airline(name)
);
create table staff_phone_num(
    username        varchar(20) not null,
    phone_number    varchar(20),
    primary key (username, phone_number),
    foreign key (username) references airline_staff(username)
);
create table staff_email(
    username        varchar(20) not null,
    email           varchar(20),
    primary key (username, email),
    foreign key (username) references airline_staff(username)
);
create table airport(
    name            varchar(20) not null,
    city            varchar(20) not null,
    country         varchar(20) not null,
    airport_type    varchar(20) not null,
    primary key (name),
    constraint valid_airport check (airport_type='international'
                                        or airport_type='domestic'
                                        or airport_type='hybrid')
);
create table airplane(
    id              varchar(20) not null,
    airline         varchar(20) not null,
    num_seats       int not null,
    age             timestamp not null,
    manufacturer    varchar(20) not null,
    primary key (id, airline),
    foreign  key (airline) references airline(name)
);

create table flight(
     flight_num         varchar(20) not null,
     airline            varchar(20) not null,
     airplane_id        varchar(20) not null,
     arrv_datetime   	timestamp not null,
     dept_datetime   	timestamp not null,
     base_price         float not null,
     origin             varchar(20) not null,
     destination        varchar(20) not null,
     flight_status      varchar(20) not null,
     primary key (flight_num, airline, dept_datetime),
     foreign  key (airplane_id, airline) references airplane(id, airline),
     foreign  key (origin) references airport(name),
     foreign  key (destination) references airport(name),
     constraint valid_baseprice check (base_price > 0),
     constraint valid_status check (flight_status='on time'
                                    or flight_status='delayed'
                                    or flight_status='canceled'
                                    or flight_status='complete')
);

create table ticket(
    id              varchar(20) not null,
    flight_num      varchar(20) not null,
    airline         varchar(20) not null,
    dept_datetime	timestamp not null,
    primary key (id),
    foreign key (flight_num, airline, dept_datetime)
		references flight(flight_num, airline, dept_datetime)
);
create table customer(
    email           varchar(20) not null,
    name            varchar(20) not null,
    password        varchar(40) not null,
    building_num    varchar(20) not null,
    city            varchar(20) not null,
    state           varchar(20) not null,
    street          varchar(20) not null,
    pp_country      varchar(20) not null,
    pp_num          varchar(20) not null,
    pp_exper        timestamp not null,
    dob             timestamp not null,
    phone_number    varchar(20) not null,
    primary key (email)
);

create table card_info(
    card_number     varchar(20) not null,
    card_exper      varchar(20) not null,
    name_on_card    varchar(20) not null,
    card_type       varchar(20) not null,
    primary key (card_number),
    constraint valid_card check (card_type='credit'
                                or card_type='debit')
);

create table purchase(
    customer_email      varchar(20) not null,
    ticket_id           varchar(20) not null,
    purchase_datetime   timestamp not null,
    sold_price          float not null,
    base_price          float not null references flight(base_price),
    card_number         varchar(20) not null,
    primary key (customer_email, ticket_id, card_number),
    foreign key (customer_email) references customer(email),
    foreign key (ticket_id) references ticket(id) ON DELETE CASCADE,
    foreign key (card_number) references card_info(card_number),
    constraint valid_price check (sold_price >= base_price)
);

create table flight_review(
    customer_email      varchar(20) not null,
    ticket_id           varchar(20) not null,
    rating           	int not null,
    comment	            varchar(400) not null,
    primary key (customer_email, ticket_id),
    foreign key (customer_email) references customer(email),
    foreign key (ticket_id) references ticket(id),
    constraint valid_rating check (rating between 0 and 5)
);

DELIMITER $$
CREATE FUNCTION customerTookFlight()
RETURNS int
AS BEGIN RETURN (
	SELECT COUNT(DISTINCT customer_email)
	FROM (purchase NATURAL JOIN flight_review) AS fr
      WHERE EXISTS (SELECT *
		   	  FROM ticket as t
			  WHERE fr.ticket_id = t.ticket_id AND t.dept_datetime < NOW())
) END
&&
ALTER TABLE flight_review ADD CONSTRAINT custCanReview
	CHECK (customerTookFlight() <> 0)
&&
DELIMITER ;




