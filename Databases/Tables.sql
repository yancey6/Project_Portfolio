CREATE TABLE airline(
    airline_name varchar(50),
    PRIMARY KEY (airline_name)
);

CREATE TABLE staff(
    username varchar(50),
    password varchar(50),
    firstname varchar(50),
    lastname varchar(50),
    birthday DATE,
    airline_name varchar(50),
    PRIMARY KEY(username),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE airplane(
    airline_name varchar(50),
    airplane_id varchar(50),
    seats INT,
    PRIMARY KEY(airline_name, airplane_id),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE airport(
    airport_name varchar(50),
    city varchar(50),
    PRIMARY KEY(airport_name)
);

CREATE TABLE agent(
    email varchar(50),
    password varchar(50),
    booking_agent_id int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(booking_agent_id)
);

CREATE TABLE customer(
    email varchar(50),
    customer_name varchar(50),
    password varchar(50),
    birthday DATE,
    phone_nbr varchar(50),
    passport_nbr varchar(50),
    passport_expiration DATE,
    passport_country varchar(50),
    state varchar(50),
    city varchar(50),
    street varchar(50),
    building_nbr varchar(50),
    PRIMARY KEY(email)
);

CREATE TABLE flight(
    airline_name varchar(50),
    airplane_id varchar(50),
    flight_nbr varchar(50),
    t_depart TIMESTAMP,
    t_arrive TIMESTAMP,
    price FLOAT,
    status varchar(50),
    flight_id varchar(50),
    airport_depart varchar(50),
    airport_arrive varchar(50),
    PRIMARY KEY(airline_name, flight_nbr),
    FOREIGN KEY (airline_name, airplane_id) REFERENCES airplane(airline_name, airplane_id)
);

CREATE TABLE permission(
    username varchar(50),
    permission varchar(50),
    PRIMARY KEY(username),
    FOREIGN KEY (username) REFERENCES staff(username)
);

CREATE TABLE ticket(
    ticket_id int NOT NULL AUTO_INCREMENT,
    airline_name varchar(50),
    flight_nbr varchar(50),
    email varchar(50),
    booking_agent_id varchar(50),
    PRIMARY KEY(ticket_id),
    FOREIGN KEY (airline_name, flight_nbr) REFERENCES flight(airline_name, flight_nbr),
    FOREIGN KEY (email) REFERENCES customer(email)
);

CREATE TABLE workfor(
    airline_name varchar(50),
    booking_agent_id int NOT NULL,
    PRIMARY KEY(airline_name, booking_agent_id),
    FOREIGN KEY(airline_name) REFERENCES airline(airline_name),
    FOREIGN KEY(booking_agent_id) REFERENCES agent(booking_agent_id)
)
