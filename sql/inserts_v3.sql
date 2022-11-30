insert into airline values ('JetBlue');

insert into airport values ('JFK','New York City','USA','international'),
    ('PVG', 'Shanghai', 'China', 'international');

insert into customer values 
    ('sharp242@gmail.com','Sol Sharp','7c6a180b36896a0a8c02787eeafb0e4c', '370', 'Brooklyn',
    'New York', 'Jay', 'USA', '12345678', "2027-07-23", "1994-07-23", '422-123-2522'),

    ('jj223@gmail.com','Jack Jones','6cb75f652a9b52798eb6cf2201057c73', '371', 'Brooklyn',
    'New York', 'Jay', 'USA', '11345678', "2027-07-23", "1994-07-23", '235-253-3519'),

    ('unhackable@gmail.com','Ava Knox','819b0643d6b89dc9b579fdfc9094f28e', '372', 'Brooklyn',
    'New York', 'Jay', 'USA', '11145678', "2027-07-23", "1994-07-23", '236-742-4915');


insert into airplane values
    ('Xqts-cOKP-BRGn-AXMn', "JetBlue", 150, "2013-08-21", 'Boeing'),

    ('APHQ-enfB-uRrT-lMzD', "JetBlue", 80, "2019-08-21", 'Airbus'),

    ('fXgM-uGTn-fUkL-VZQX', "JetBlue", 80, "2017-08-21", 'Airbus');

insert into airline_staff values
    ('kbennit283','305e4f55ce823e111a46a9d500bcb86c','kathrine','bennit','1983-03-24','JetBlue');

insert into staff_email values
    ('kbennit283','kben224@gmail.com');

insert into staff_phone_num values
    ('kbennit283','212-235-9924');

insert into flight values
    ('BA2491A', 'JetBlue', 'Xqts-cOKP-BRGn-AXMn', '2022-12-05',
        '2022-12-04', 934.63, 'JFK', 'PVG', 'on time'),

    ('BA6492B', 'JetBlue', 'APHQ-enfB-uRrT-lMzD', '2022-11-05',
    '2022-12-05', 765.35, 'JFK', 'PVG', 'delayed'),

    ('AA3181A', 'JetBlue', 'fXgM-uGTn-fUkL-VZQX', '2022-10-29',
    '2022-10-29', 334.33, 'JFK', 'PVG', 'on time'),

    ('AA4421A', 'JetBlue', 'APHQ-enfB-uRrT-lMzD', '2022-11-13',
    '2022-11-12', 484.20, 'PVG', 'JFK', 'delayed'),

    ('CA4441B', 'JetBlue', 'Xqts-cOKP-BRGn-AXMn', '2022-11-26',
    '2022-11-25', 1034.74,'PVG', 'JFK', 'on time');

insert into ticket values
('00001','AA3181A','JetBlue','2022-10-29'),
('00002','CA4441B','JetBlue','2022-11-25'),
('00003','AA3181A','JetBlue','2022-10-29'),
('00004','BA6492B','JetBlue','2022-12-05');

insert into card_info values
('4172926778282996','11/26','Sol Sharp','credit'),
('5344773531817134','2/24','Jack Jones','credit'),
('6011119001783002','5/25','Ava Knox','debit');

insert into purchase values
('sharp242@gmail.com', '00001', '2022-09-18', 520.34, 334.33,'4172926778282996'),
('jj223@gmail.com', '00002', '2022-09-13', 1052.59, 1034.74, '5344773531817134'),
('unhackable@gmail.com', '00003', '2022-09-29', 562.23, 334.33,'6011119001783002'),
('unhackable@gmail.com', '00004', '2022-10-03', 803.18, 765.35, '6011119001783002');







