CREATE DATABASE holiday_clean;
USE holiday_clean;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(15) UNIQUE NOT NULL,
    postcode VARCHAR(8) NOT NULL,
    user_type ENUM('Owner', 'Cleaner') NOT NULL
) AUTO_INCREMENT = 10001;



INSERT INTO users (username, First_name, last_name, phone_no, postcode, user_type)
VALUES 	('Clean247', 'Kelly', 'Browne', '09803 856941', 'SK24 9PQ', 'Cleaner'),
		('Hol_Homes1', 'John', 'Wick', '09893 454721', 'SK24 7DC', 'Owner'),
        ('ChapLets', 'Ruth', 'Donald', '09634 499785', 'SK25 6SF', 'Owner'),
        ('DAWESClean7', 'Claire', 'Daweson', '09655 112854', 'SK24 6AQ', 'Cleaner'),
        ('SkyC0tt4ges', 'Amanda', 'Fox', '09234 787451', 'SK25 1PP', 'Owner'),
        ('L44tHaus', 'Mark', 'Rushton', '09115 235741', 'SK24 1LP', 'Owner'),
        ('CL£4NQU££N', 'Sarah', 'Lopez', '09875 464747', 'SK25 2LS', 'Cleaner'),
        ('AussieH0LS', 'Grayson', 'Waller', '09231 119876', 'SK24 5OZ', 'Owner'),
        ('HomeMaid_76', 'Daniel', 'Rogers', '09887 446217', 'SK25 1PP', 'Cleaner'),
        ('Cind£r£ll4$m!ce', 'Aurora', 'Wintergarten', '09663 778391', 'SK4 6FF', 'Cleaner'),
        ('QueenOfClean', 'Ana', 'Montez', '09321 115989', 'SK25 7DF', 'Cleaner'),
        ('The0ldFarm', 'Tracey', 'Shepard', '09887 118543', 'SK24 3VX', 'Owner'),
        ('HomeFromH0me45', 'Genieve', 'Pence', '09771 117119', 'SK25 3HJ', 'Owner'),
        ('ManAroundTheHOUSE', 'Sean', "O'Donaghue", '09877 164587', 'SK25 6WE', 'Cleaner'),
        ('ScottsFree', 'Scott', 'Bishop', '09631 911321', 'SK24 4TT', 'Cleaner'),
        ('PeakHolidayLets', 'Debbie', 'McQueen', '09781 135791', 'SK25 3GH', 'Owner');
    
CREATE TABLE properties (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    property_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    prop_postcode VARCHAR(8) NOT NULL,
    num_beds INT NOT NULL,
    num_baths INT NOT NULL,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id)
) AUTO_INCREMENT = 20001;

DELIMITER //
CREATE PROCEDURE insert_property (
IN own_id INT,
IN prop_name VARCHAR(100),
IN prop_address VARCHAR(255) ,
IN property_postcode VARCHAR(8),
IN prop_beds INT, 
IN prop_baths INT
) 
BEGIN 
DECLARE user_type VARCHAR(10);

SELECT 
    user_type
INTO user_type FROM
    Users
WHERE
    user_id = own_id; 
    IF user_type <> 'Owner' THEN -- brings up a specific error message

  SELECT 'Error: owner_id must belong to a user with UserType = Owner' AS MESSAGE; 
  ELSE -- inserts data INTo the table

INSERT INTO properties (owner_id, property_name, address, prop_postcode, num_beds, num_baths)
VALUES (own_id, prop_name, prop_address, property_postcode, prop_beds, prop_baths);
END IF; 

END//
DELIMITER ;


CALL insert_property(10002, 'The Hayloft', 'Danzig Hill, Combs', 'SK24 7EE', 2, 2);
CALL insert_property(10003, '1 Chapel Mews', 'High Street, Chapel-En-Le-Frith', 'SK24 8PO', 2, 1);
CALL insert_property(10003, '2 Chapel Mews', 'High Street, Chapel-En-Le-Frith', 'SK24 8PO', 3, 2);
CALL insert_property(10005, 'Sky Cottage', 'Mortimor Lane, Little Hayfield', 'SK25 9PL', 1, 1); -- Alreay ran this procedure to here
CALL insert_property(10005, 'Skylark House', 'Trustle Way, Hayfield', 'SK25 8OP', 4, 4);
CALL insert_property(10005, 'Skylark Barn', 'Trustle Way, Hayfield', 'SK25 8OP', 2, 2);
CALL insert_property(10006, 'The Old Vicarage', 'Church Lane, Chinley', 'SK24 9AW', 4, 3);
CALL insert_property(10008, "Shepherd's Watch", 'Old Bay Farm, Chapel Road, Buxworth', 'SK24 3GH', 1, 1);
CALL insert_property(10008, "Shepherd's Rest", 'Old Bay Farm, Chapel Road, Buxworth', 'SK24 3GH', 1, 1);
CALL insert_property(10008, "Shepherd's Retreat", 'Old Bay Farm, Chapel Road, Buxworth', 'SK24 3GH', 1, 1);
CALL insert_property(10012, "The Old Farm House", "Tom's Lane, Tunstead Milton", 'SK24 1HQ', 3, 1);
CALL insert_property(10013, 'The Stables', 'Reservoir Road, Kettleshulme', 'SK25 6HH', 2, 2);
CALL insert_property(10016, "Eccle's View", 'New Road, Whaley Bridge', 'SK24 5XN', 2, 1);












CREATE TABLE cleaning_job(
	job_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id int not null, 
    clean_date date not null,
    check_out_time time not null default '10:00:00',
    check_in_time time not null default '15:00:00',
    expected_clean_time int not null, 
    total_clean_time int generated always as (expected_clean_time + 1) stored,
    linens_provided enum ('Yes', 'No') not null,
    rate_per_hour decimal(10, 2) not null default 13.85,
    job_notes text,
    cleaner_id int null,
    start_time time null,
    end_time time null,
    job_status enum ('Pending', 'Accepted', 'Completed') default 'Pending',
    foreign key (property_id) references properties(property_id),
    foreign key (cleaner_id) references users(user_id)
    ) AUTO_INCREMENT = 101 ;
    

    
delimiter //

create procedure Accept_Cleaning_Job(
	in p_job_id int, 
    in p_cleaner_id int, 
    in p_start_time time,
    in p_end_time time
    )

begin
	declare job_exists int;
    
    select count(*) into job_exists
    from cleaning_job
    where job_id = p_job_id and job_status = 'Pending';
    
    if job_exsists = 1 then
		update cleaning_job
        set cleaner_id = p_cleaner_id,
			start_time = p_start_time,
            end_time = p_end_time, 
            job_status = 'Accepted'
		where job_id = p_job_id;
        
        select 'Job accepted successfully!' as message;
	else
		select 'Error: Job not found or already assigned' as message;
	end if;
    
end //

delimiter ;

INSERT INTO cleaning_job (property_id, clean_date, linens_provided, rate_per_hour, job_notes, expected_clean_time, job_status)
VALUES 
(20001, '2025-03-15', 'No', 13.85, 'Deep clean required.', 3, 'Pending'),
(20002, '2025-03-16', 'Yes', 13.85, 'Regular clean.', 2, 'Pending'),
(20003, '2025-03-17', 'Yes', 15.00, 'Post-stay cleanup.', 3, 'Pending');


CREATE TABLE linen_hire (
	linen_id INT AUTO_INCREMENT PRIMARY KEY,
    linen_type ENUM('Single', 'Double', 'King', 'Super King', 'Kitchen Towel', 'Bath Mat') NOT NULL,
    linen_price DECIMAL (5, 2) NOT NULL
    );
    
INSERT INTO linen_hire (linen_type, linen_price)
VALUES 
('Single', 13.29),
('Double', 17.69),
('King', 18.79), 
('Super King', 19.69),
('Kitchen Towel', 1.20),
('Bath Mat', 2.30);


CREATE TABLE linen_order (
    linen_order_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    linen_type ENUM('Single', 'Double', 'King', 'Super King', 'Kitchen Towel', 'Bath Mat') NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES cleaning_job(job_id)
) AUTO_INCREMENT=5001;


INSERT INTO linen_order(job_id, linen_type, quantity)
VALUES 	(102, 'Double', 1),
		(102, 'Single', 2), 
        (102, 'Bath Mat', 1),
        (102, 'Kitchen Towel', 2),
        (103, 'Double', 2),
        (103, 'Single', 2), 
        (103, 'Bath Mat', 2), 
        (103, 'Kitchen Towel', 2);
        

CREATE TABLE clocking_in_out (
	clock_id INT AUTO_INCREMENT PRIMARY KEY,
    cleaner_id INT, 
    job_id INT, 
    clock_in_time DATETIME NOT NULL,
    clock_out_time DATETIME,
    total_work_time INT, 
    FOREIGN KEY (cleaner_id) REFERENCES users(user_id),
    FOREIGN KEY (job_id) REFERENCES cleaning_job(job_id)
);





