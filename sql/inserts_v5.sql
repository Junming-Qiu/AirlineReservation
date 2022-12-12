insert into airline values ('United');

`staff phone numbers? Email?`
insert into airline_staff values 
    ('admin', '8c02b3bfd0b00a36d01d16f0d108814e', 'Roe', 'Jones', '1978-05-25', 'United');

insert into airplane values
    ('1', 'United', 4, '2012-01-01', 'Boeing'),
    ('2', 'United', 4, '2010-01-01', 'Airbus'),
    ('3', 'United', 50, '2014-01-01', 'Boeing');

`Type can be both??`
insert into airport values
    ('JFK', 'NYC', 'USA', 'international'),
    ('BOS', 'Boston', 'USA', 'international'),
    ('PVG', 'Shanghai', 'China', 'international'),
    ('BEI', 'Beijing', 'China', 'international'),
    ('SFO', 'San Francisco', 'USA', 'international'),
    ('LAX', 'Los Angeles', 'USA', 'international'),
    ('HKA', 'Hong Kong', 'China', 'international'),
    ('SHEN', 'Shenzhen', 'China', 'international');

insert into customer values
    ('testcustomer@nyu.edu', 'Test Customer 1', '1f1c6dd651a798b959ffe15fe03e49ec', '1555', 'Brooklyn',
    'New York', 'Jay St', 'USA', '54321', '2025-12-24', '1999-12-19', '123-4321-4321'),
    ('user1@nyu.edu', 'User 1', '1f1c6dd651a798b959ffe15fe03e49ec', '5405', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54322', '2025-12-25', '1999-11-19', '123-4322-4322'),
    ('user2@nyu.edu', 'User 2', '1f1c6dd651a798b959ffe15fe03e49ec', '1702', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54323', '2025-10-24', '1999-10-19', '123-4323-4323'),
    ('user3@nyu.edu', 'User 3', '1f1c6dd651a798b959ffe15fe03e49ec', '1890', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54324', '2025-09-24', '1999-09-19', '123-4324-4324');

insert into flight values
    ('102', 'United', '3', '2022-09-12 16:50:25', 
    '2022-09-12 13:25:25', 300, 'LAX', 'SFO', 'on time'),
    ('104', 'United', '3', '2022-10-04 16:50:25', 
    '2022-10-04 13:25:25', 300, 'PVG', 'BEI', 'on time'),
    ('106', 'United', '3', '2022-08-04 16:50:25', 
    '2022-08-04 13:25:25', 350, 'SFO', 'LAX', 'delayed'),
    ('206', 'United', '2', '2023-02-04 16:50:25', 
    '2023-02-04 13:25:25', 400, 'SFO', 'LAX', 'on time'),
    ('207', 'United', '2', '2023-03-04 16:50:25', 
    '2023-03-04 13:25:25', 300, 'LAX', 'SFO', 'on time'),
    ('134', 'United', '3', '2022-07-12 16:50:25', 
    '2022-07-12 13:25:25', 300, 'JFK', 'BOS', 'delayed'),
    ('296', 'United', '1', '2022-12-30 16:50:25', 
    '2022-12-30 13:25:25', 3000, 'PVG', 'SFO', 'on time'),
    ('715', 'United', '1', '2022-09-30 16:50:25', 
    '2022-09-30 13:25:25', 500, 'PVG', 'BEI', 'delayed'),
    ('839', 'United', '3', '2021-12-26 16:50:25', 
    '2021-12-26 13:25:25', 300, 'SHEN', 'BEI', 'on time');

insert into ticket values 
    ()



