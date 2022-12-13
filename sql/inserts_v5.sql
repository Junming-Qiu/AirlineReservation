insert into airline values ('Delta');

insert into airline_staff values 
    ('admin', '043160a4a5171670021f28f7d6a3f69b', 'Roe', 'Jones', '1978-05-25', 'Delta');

insert into staff_email values
    ('admin', 'staff@nyu.edu');

insert into staff_phone_num values
    ('admin', '111-222-3333'),
    ('admin', '444-555-6666');

insert into airplane values
    ('1', 'Delta', 4, '2012-01-01', 'Boeing'),
    ('2', 'Delta', 4, '2010-01-01', 'Airbus'),
    ('3', 'Delta', 50, '2014-01-01', 'Boeing');


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
    ('testcustomer@nyu.edu', 'Test Customer 1', '5df21263ad7262f11273a6e4339002e2', '1555', 'Brooklyn',
    'New York', 'Jay St', 'USA', '54321', '2025-12-24', '1999-12-19', '123-4321-4321'),
    ('user1@nyu.edu', 'User 1', '5df21263ad7262f11273a6e4339002e2', '5405', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54322', '2025-12-25', '1999-11-19', '123-4322-4322'),
    ('user2@nyu.edu', 'User 2', '5df21263ad7262f11273a6e4339002e2', '1702', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54323', '2025-10-24', '1999-10-19', '123-4323-4323'),
    ('user3@nyu.edu', 'User 3', '5df21263ad7262f11273a6e4339002e2', '1890', 'Brooklyn',
    'New York', 'Jay Street', 'USA', '54324', '2025-09-24', '1999-09-19', '123-4324-4324');

insert into flight values
    ('102', 'Delta', '3', '2022-09-12 16:50:25', 
    '2022-09-12 13:25:25', 300, 'LAX', 'SFO', 'on time'),
    ('104', 'Delta', '3', '2022-10-04 16:50:25', 
    '2022-10-04 13:25:25', 300, 'PVG', 'BEI', 'on time'),
    ('106', 'Delta', '3', '2022-08-04 16:50:25', 
    '2022-08-04 13:25:25', 350, 'SFO', 'LAX', 'delayed'),
    ('206', 'Delta', '2', '2023-02-04 16:50:25', 
    '2023-02-04 13:25:25', 400, 'SFO', 'LAX', 'on time'),
    ('207', 'Delta', '2', '2023-03-04 16:50:25', 
    '2023-03-04 13:25:25', 300, 'LAX', 'SFO', 'on time'),
    ('134', 'Delta', '3', '2022-07-12 16:50:25', 
    '2022-07-12 13:25:25', 300, 'JFK', 'BOS', 'delayed'),
    ('296', 'Delta', '1', '2022-12-30 16:50:25', 
    '2022-12-30 13:25:25', 3000, 'PVG', 'SFO', 'on time'),
    ('715', 'Delta', '1', '2022-09-28 16:50:25', 
    '2022-09-28 13:25:25', 500, 'PVG', 'BEI', 'delayed'),
    ('839', 'Delta', '3', '2021-12-26 16:50:25', 
    '2021-12-26 13:25:25', 300, 'SHEN', 'BEI', 'on time');

insert into ticket values 
    ('00001', '102', 'Delta', '2022-09-12 13:25:25'),
    ('00002', '102', 'Delta', '2022-09-12 13:25:25'),
    ('00003', '102', 'Delta', '2022-09-12 13:25:25'),
    ('00004', '104', 'Delta', '2022-10-04 13:25:25'),
    ('00005', '104', 'Delta', '2022-10-04 13:25:25'),
    ('00006', '106', 'Delta', '2022-08-04 13:25:25'),
    ('00007', '106', 'Delta', '2022-08-04 13:25:25'),
    ('00008', '839', 'Delta', '2021-12-26 13:25:25'),
    ('00009', '102', 'Delta', '2022-09-12 13:25:25'),
    ('00011', '134', 'Delta', '2022-07-12 13:25:25'),
    ('00012', '715', 'Delta', '2022-09-28 13:25:25'),
    ('00014', '206', 'Delta', '2023-02-04 13:25:25'),
    ('00015', '206', 'Delta', '2023-02-04 13:25:25'),
    ('00016', '206', 'Delta', '2023-02-04 13:25:25'),
    ('00017', '207', 'Delta', '2023-03-04 13:25:25'),
    ('00018', '207', 'Delta', '2023-03-04 13:25:25'),
    ('00019', '296', 'Delta', '2022-12-30 13:25:25'),
    ('00020', '296', 'Delta', '2022-12-30 13:25:25');

insert into card_info values
    ('1111222233334444', '3/23', 'Test Customer 1', 'credit'),
    ('1111222233335555', '3/23', 'User 1', 'credit');

insert into purchase values
    ('testcustomer@nyu.edu', '00001', '2022-08-04 11:55:55', 300, 300, '1111222233334444'),
    ('user1@nyu.edu', '00002', '2022-08-03 11:55:55', 300, 300, '1111222233335555'),
    ('user2@nyu.edu', '00003', '2022-09-04 11:55:55', 300, 300, '1111222233335555'),
    ('user1@nyu.edu', '00004', '2022-08-21 11:55:55', 300, 300, '1111222233335555'),
    ('testcustomer@nyu.edu', '00005', '2022-09-28 11:55:55', 300, 300, '1111222233334444'),
    ('testcustomer@nyu.edu', '00006', '2022-08-02 11:55:55', 350, 350, '1111222233334444'),
    ('user3@nyu.edu', '00007', '2022-07-03 11:55:55', 350, 350, '1111222233335555'),
    ('user3@nyu.edu', '00008', '2021-12-03 11:55:55', 300, 300, '1111222233335555'),
    ('user3@nyu.edu', '00009', '2022-07-04 11:55:55', 300, 300, '1111222233335555'),
    ('user3@nyu.edu', '00011', '2022-05-23 11:55:55', 300, 300, '1111222233335555'),
    ('testcustomer@nyu.edu', '00012', '2022-05-02 11:55:55', 500, 500, '1111222233334444'),
    ('user3@nyu.edu', '00014', '2022-11-20 11:55:55', 400, 400, '1111222233335555'),
    ('user1@nyu.edu', '00015', '2022-11-21 11:55:55', 400, 400, '1111222233335555'),
    ('user2@nyu.edu', '00016', '2022-09-19 11:55:55', 400, 400, '1111222233335555'),
    ('user1@nyu.edu', '00017', '2022-08-11 11:55:55', 300, 300, '1111222233335555'),
    ('testcustomer@nyu.edu', '00018', '2022-09-25 11:55:55', 300, 300, '1111222233334444'),
    ('user1@nyu.edu', '00019', '2022-11-12 11:55:55', 3000, 3000, '1111222233334444'),
    ('testcustomer@nyu.edu', '00020', '2022-07-12 11:55:55', 3000, 300, '1111222233334444');

insert into flight_review values 
    ('testcustomer@nyu.edu', '00001', '4', 'Very Comfortable'),
    ('user1@nyu.edu', '00002', '5', 'Relaxing, check-in and onboarding very professional'),
    ('user2@nyu.edu', '00003', '3', 'Satisfied and will use the same flight again'),
    ('testcustomer@nyu.edu', '00005', '1', 'Customer Care services are not good'),
    ('user1@nyu.edu', '00004', '5', 'Comfortable journey and Professional');




