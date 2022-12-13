from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector
import json
import numpy as np
import hashlib

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='Airline_Ticket')

#Define a route to hello function
@app.route('/')
def index():
    return render_template('Index.html')

#Define a route to public information
@app.route('/publicinfo')
def publicinfo():
    return render_template('publicinfo.html')

@app.route('/pi1', methods=['GET', 'POST'])
def pi1():
    source_airport = request.form['source_airport']
    destination_airport = request.form['destination_airport']
    date = request.form['date']
    cursor = conn.cursor()
    query = "SELECT * FROM flight WHERE airport_depart = '{}' AND airport_arrive = '{}' AND CAST(t_depart AS DATE) = CAST('{}' AS DATE)"
    cursor.execute(query.format(source_airport, destination_airport, date))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('publicinfo.html', pi1=data1)

@app.route('/pi2', methods=['GET', 'POST'])
def pi2():
    flight_nbr = request.form['flight_nbr']
    departure_date = request.form['departure_date']
    cursor = conn.cursor()
    query = "SELECT flight_nbr, t_depart, status FROM flight WHERE flight_nbr = '{}' AND CAST(t_depart AS DATE) = CAST('{}' AS DATE)"
    cursor.execute(query.format(flight_nbr, departure_date))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('publicinfo.html', pi2=data2)

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/customer')
def register_customer():
    return render_template('register_customer.html')
#Authenticates the register
@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():
    username = request.form['username']
    customer_name = request.form['customer_name']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    birthday = request.form['birthday']
    phone_nbr = request.form['phone_nbr']
    passport_nbr = request.form['passport_nbr']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    state = request.form['state']
    city = request.form['city']
    street = request.form['street']
    building_nbr = request.form['building_nbr']
    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE email = '{}'"
    cursor.execute(query.format(username))
    data = cursor.fetchone()
    error = None
    if(data):
        error = "This user already exists"
        return render_template('register_customer.html', error = error)
    else:
        ins = "INSERT INTO customer VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        cursor.execute(ins.format(username, customer_name, password, birthday, phone_nbr, passport_nbr, passport_expiration, passport_country, state, city, street, building_nbr))
        conn.commit()
        cursor.close()
        return render_template('Index.html')

@app.route('/register/agent')
def register_agent():
    return render_template('register_agent.html')

@app.route('/registerAuth_agent', methods=['GET', 'POST'])
def registerAuth_agent():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    cursor = conn.cursor()
    query = "SELECT * FROM agent WHERE email = '{}'"
    cursor.execute(query.format(username))
    data = cursor.fetchone()
    error = None
    if(data):
        error = "This user already exists"
        return render_template('register_agent.html', error = error)
    else:
        ins = "INSERT INTO agent(email, password) VALUES('{}', '{}')"
        cursor.execute(ins.format(username, password))
        conn.commit()
        cursor.close()
        return render_template('Index.html')

@app.route('/register/staff')
def register_staff():
    return render_template('register_staff.html')

@app.route('/registerAuth_staff', methods=['GET', 'POST'])
def registerAuth_staff():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    birthday = request.form['birthday']
    airline_name = request.form['airline_name']
    cursor = conn.cursor()
    query = "SELECT * FROM staff WHERE username = '{}'"
    cursor.execute(query.format(username))
    data = cursor.fetchone()
    error = None
    if(data):
        error = "This user already exists"
        return render_template('register_staff.html', error = error)
    else:
        ins = "INSERT INTO staff VALUES('{}', '{}', '{}', '{}', '{}', '{}')"
        cursor.execute(ins.format(username, password, firstname, lastname, birthday, airline_name))
        conn.commit()
        cursor.close()
        return render_template('Index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/customer')
def login_customer():
    return render_template('login_customer.html')
#Authenticates the login
@app.route('/loginAuth_customer', methods=['GET', 'POST'])
def loginAuth_customer():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE email = '{}' and password = '{}'"
    cursor.execute(query.format(username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['username'] = username
        session['role'] = 'customer'
        return redirect(url_for('home_customer'))
    else:
        error = 'Invalid login or username'
        return render_template('login_customer.html', error=error)

@app.route('/login/agent')
def login_agent():
    return render_template('login_agent.html')
#Authenticates the login
@app.route('/loginAuth_agent', methods=['GET', 'POST'])
def loginAuth_agent():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    cursor = conn.cursor()
    query = "SELECT * FROM agent WHERE email = '{}' and password = '{}'"
    cursor.execute(query.format(username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['username'] = username
        session['role'] = 'agent'
        return redirect(url_for('home_agent'))
    else:
        error = 'Invalid login or username'
        return render_template('login_agent.html', error=error)

@app.route('/login/staff')
def login_staff():
    return render_template('login_staff.html')
#Authenticates the login
@app.route('/loginAuth_staff', methods=['GET', 'POST'])
def loginAuth_staff():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    cursor = conn.cursor()
    query = "SELECT * FROM staff WHERE username = '{}' and password = '{}'"
    cursor.execute(query.format(username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['username'] = username
        session['role'] = 'staff'
        return redirect(url_for('home_staff'))
    else:
        error = 'Invalid login or username'
        return render_template('login_staff.html', error=error)

@app.route('/home_customer')
def home_customer():
    if session['role'] != 'customer':
        return render_template('Index.html')
    username = session['username']
    cursor = conn.cursor();
    query = "SELECT airline_name, airplane_id, flight_nbr, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket NATURAL JOIN flight WHERE email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT SUM(price) FROM `ticket` NATURAL JOIN flight WHERE status = 'completed' AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE AND email = '{}'"
    cursor.execute(query.format(username))
    Total_Exp_Past_Year = cursor.fetchall()
    query = "SELECT month(t_depart), SUM(price) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND email = '{}' GROUP BY month(t_depart)"
    cursor.execute(query.format(username))
    six_months_expenditure = cursor.fetchall()
    cursor.close()
    return render_template('home_customer.html', username=username, view_my_flights = view_my_flights,
                               Total_Exp_Past_Year = Total_Exp_Past_Year, six_months_expenditure = six_months_expenditure)

@app.route('/purchase_tickets', methods=['GET', 'POST'])
def purchase_tickets():
    if session['role'] != 'customer':
        return render_template('Index.html')
    airline_name = request.form['airline_name']
    flight_nbr = request.form['flight_nbr']
    username = session['username']
    booking_agent_id = None
    cursor = conn.cursor()
    query = "SELECT seats FROM `flight` NATURAL JOIN airplane WHERE airline_name = '{}' AND flight_nbr = '{}'"
    cursor.execute(query.format(airline_name, flight_nbr))
    seats = cursor.fetchall()[0][0]
    query = "SELECT COUNT(ticket_id) FROM `ticket` WHERE airline_name = '{}' AND flight_nbr = '{}'"
    cursor.execute(query.format(airline_name, flight_nbr))
    tickets_sold = cursor.fetchall()[0][0]
    if int(tickets_sold) > int(seats)-1:
        error = 'Sorry, the flight is full.'
        return render_template('error_customer.html', error=error)
    else:
        query = "INSERT INTO ticket(airline_name, flight_nbr, email, booking_agent_id) VALUES('{}', '{}', '{}', '{}')"
        cursor.execute(query.format(airline_name, flight_nbr, username, booking_agent_id))
        conn.commit()
        cursor.close()
        return redirect(url_for('home_customer'))

@app.route('/search_for_flights', methods=['GET', 'POST'])
def search_for_flights():
    if session['role'] != 'customer':
        return render_template('Index.html')
    username = session['username']
    source_airport = request.form['source_airport']
    destination_airport = request.form['destination_airport']
    date = request.form['date']
    cursor = conn.cursor()
    query = "SELECT airline_name, airplane_id, flight_nbr, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket NATURAL JOIN flight WHERE email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT * FROM flight WHERE airport_depart = '{}' AND airport_arrive = '{}' AND CAST(t_depart AS DATE) = CAST('{}' AS DATE)"
    cursor.execute(query.format(source_airport, destination_airport, date))
    search_for_flights = cursor.fetchall()
    query = "SELECT SUM(price) FROM `ticket` NATURAL JOIN flight WHERE status = 'completed' AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE AND email = '{}'"
    cursor.execute(query.format(username))
    Total_Exp_Past_Year = cursor.fetchall()
    query = "SELECT month(t_depart), SUM(price) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND email = '{}' GROUP BY month(t_depart)"
    cursor.execute(query.format(username))
    six_months_expenditure = cursor.fetchall()
    cursor.close()
    return render_template('home_customer.html', username=username, view_my_flights = view_my_flights,
                           search_for_flights = search_for_flights, Total_Exp_Past_Year = Total_Exp_Past_Year, six_months_expenditure = six_months_expenditure)

@app.route('/range_month_expenditure', methods=['GET', 'POST'])
def range_month_expenditure():
    if session['role'] != 'customer':
        return render_template('Index.html')
    username = session['username']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor()
    query = "SELECT airline_name, airplane_id, flight_nbr, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket NATURAL JOIN flight WHERE email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT SUM(price) FROM `ticket` NATURAL JOIN flight WHERE status = 'completed' AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE AND email = '{}'"
    cursor.execute(query.format(username))
    Total_Exp_Past_Year = cursor.fetchall()
    query = "SELECT month(t_depart), SUM(price) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND email = '{}' GROUP BY month(t_depart)"
    cursor.execute(query.format(username))
    six_months_expenditure = cursor.fetchall()
    query = "SELECT month(t_depart), SUM(price) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN '{}' AND '{}') AND email = '{}' GROUP BY month(t_depart)"
    cursor.execute(query.format(start_date, end_date, username))
    range_month_expenditure = cursor.fetchall()
    cursor.close()
    return render_template('home_customer.html', username=username, view_my_flights = view_my_flights,
                         Total_Exp_Past_Year = Total_Exp_Past_Year, six_months_expenditure = six_months_expenditure, range_month_expenditure = range_month_expenditure)


@app.route('/home_agent')
def home_agent():
    if session['role'] != 'agent':
        return render_template('Index.html')
    username = session['username']
    cursor = conn.cursor();
    query = "SELECT T.email, airline_name, flight_nbr, ticket_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT SUM(price)*0.1, AVG(price)*0.1, COUNT(ticket_id) FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND (t_depart BETWEEN CURRENT_DATE-INTERVAL 30 day AND CURRENT_DATE) AND status = 'completed'"
    cursor.execute(query.format(username))
    view_my_commission = cursor.fetchall()
    query = "SELECT T.email, COUNT(ticket_id) N FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY N DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_ticket = cursor.fetchall()
    query = "SELECT T.email, 0.1*SUM(price) P FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY P DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_commission = cursor.fetchall()
    cursor.close()
    return render_template('home_agent.html', username=username, view_my_flights=view_my_flights, view_my_commission=view_my_commission, top_cus_ticket=top_cus_ticket, top_cus_commission=top_cus_commission)

@app.route('/purchase_tickets_agent', methods=['GET', 'POST'])
def purchase_tickets_agent():
    if session['role'] != 'agent':
        return render_template('Index.html')
    username = session['username']
    airline_name = request.form['airline_name']
    flight_nbr = request.form['flight_nbr']
    customer_email = request.form['customer_email']
    cursor = conn.cursor()
    query = "SELECT seats FROM `flight` NATURAL JOIN airplane WHERE airline_name = '{}' AND flight_nbr = '{}'"
    cursor.execute(query.format(airline_name, flight_nbr))
    seats = cursor.fetchall()[0][0]
    query = "SELECT COUNT(ticket_id) FROM `ticket` WHERE airline_name = '{}' AND flight_nbr = '{}'"
    cursor.execute(query.format(airline_name, flight_nbr))
    tickets_sold = cursor.fetchall()[0][0]
    query = "SELECT booking_agent_id FROM agent WHERE email = '{}'"
    cursor.execute(query.format(username))
    booking_agent_id = cursor.fetchall()[0][0]
    query = "SELECT airline_name FROM workfor WHERE booking_agent_id = '{}'"
    cursor.execute(query.format(booking_agent_id))
    airline_constraint = cursor.fetchall()
    airline_constraint = np.array(airline_constraint.copy())
    if airline_name not in airline_constraint:
        error = 'You are not Allowed to Purchase Ticket of Airlines that You do not Work for'
        return render_template('error_agent.html', error=error)
    else:
        if int(tickets_sold) > int(seats) - 1:
            error = 'Sorry, the flight is full.'
            return render_template('error_agent.html', error=error)
        else:
            query = "INSERT INTO ticket(airline_name, flight_nbr, email, booking_agent_id) VALUES('{}', '{}', '{}', '{}')"
            cursor.execute(query.format(airline_name, flight_nbr, customer_email, booking_agent_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('home_agent'))

@app.route('/search_for_flights_agent', methods=['GET', 'POST'])
def search_for_flights_agent():
    if session['role'] != 'agent':
        return render_template('Index.html')
    username = session['username']
    source_airport = request.form['source_airport']
    destination_airport = request.form['destination_airport']
    date = request.form['date']
    cursor = conn.cursor()
    query = "SELECT T.email, airline_name, flight_nbr, ticket_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT * FROM flight WHERE airport_depart = '{}' AND airport_arrive = '{}' AND CAST(t_depart AS DATE) = CAST('{}' AS DATE)"
    cursor.execute(query.format(source_airport, destination_airport, date))
    search_for_flights = cursor.fetchall()
    query = "SELECT SUM(price)*0.1, AVG(price)*0.1, COUNT(ticket_id) FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND (t_depart BETWEEN CURRENT_DATE-INTERVAL 30 day AND CURRENT_DATE) AND status = 'completed'"
    cursor.execute(query.format(username))
    view_my_commission = cursor.fetchall()
    query = "SELECT T.email, COUNT(ticket_id) N FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY N DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_ticket = cursor.fetchall()
    query = "SELECT T.email, 0.1*SUM(price) P FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY P DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_commission = cursor.fetchall()
    cursor.close()
    return render_template('home_agent.html', username=username, view_my_flights = view_my_flights,
                           search_for_flights = search_for_flights, view_my_commission = view_my_commission, top_cus_ticket=top_cus_ticket, top_cus_commission=top_cus_commission)

@app.route('/range_commission', methods=['GET', 'POST'])
def range_commission():
    if session['role'] != 'agent':
        return render_template('Index.html')
    username = session['username']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor()
    query = "SELECT T.email, airline_name, flight_nbr, ticket_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND  status != 'completed'"
    cursor.execute(query.format(username))
    view_my_flights = cursor.fetchall()
    query = "SELECT SUM(price)*0.1, AVG(price)*0.1, COUNT(ticket_id) FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE A.email = '{}' AND (t_depart BETWEEN CURRENT_DATE-INTERVAL 30 day AND CURRENT_DATE) AND status = 'completed'"
    cursor.execute(query.format(username))
    view_my_commission = cursor.fetchall()
    query = "SELECT SUM(price)*0.1, COUNT(ticket_id) FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN '{}' AND '{}') AND A.email = '{}' AND status = 'completed'"
    cursor.execute(query.format(start_date, end_date, username))
    range_commission = cursor.fetchall()
    query = "SELECT T.email, COUNT(ticket_id) N FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 6 month AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY N DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_ticket = cursor.fetchall()
    query = "SELECT T.email, 0.1*SUM(price) P FROM ticket T NATURAL JOIN flight LEFT JOIN agent A USING (booking_agent_id) WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE) AND status = 'completed' AND A.email = '{}' GROUP BY T.email ORDER BY P DESC LIMIT 5"
    cursor.execute(query.format(username))
    top_cus_commission = cursor.fetchall()
    cursor.close()
    return render_template('home_agent.html', username=username, view_my_flights=view_my_flights,
                           range_commission=range_commission, view_my_commission=view_my_commission, top_cus_ticket=top_cus_ticket, top_cus_commission=top_cus_commission)

@app.route('/home_staff')
def home_staff():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    cursor = conn.cursor()
    query = "SELECT airline_name, flight_nbr, airplane_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM `flight` LEFT JOIN staff USING (airline_name) WHERE t_depart BETWEEN CURRENT_DATE AND CURRENT_DATE+INTERVAL 30 day AND username = '{}'"
    cursor.execute(query.format(username))
    upcoming_flights = cursor.fetchall()
    cursor.close()
    return render_template('home_staff.html', username=username, upcoming_flights=upcoming_flights)

@app.route('/search_flights_staff', methods=['GET', 'POST'])
def search_flights_staff():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    source_airport = request.form['source_airport']
    destination_airport = request.form['destination_airport']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor()
    query = "SELECT airline_name, flight_nbr, airplane_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM `flight` LEFT JOIN staff USING (airline_name) WHERE t_depart BETWEEN CURRENT_DATE AND CURRENT_DATE+INTERVAL 30 day AND username = '{}'"
    cursor.execute(query.format(username))
    upcoming_flights = cursor.fetchall()
    query = "SELECT airline_name, flight_nbr, airplane_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM `flight` LEFT JOIN staff USING (airline_name) WHERE t_depart BETWEEN '{}' AND '{}' AND airport_depart = '{}' AND airport_arrive = '{}' AND username = '{}'"
    cursor.execute(query.format(start_date, end_date, source_airport, destination_airport, username))
    search_flights_staff = cursor.fetchall()
    cursor.close()
    return render_template('home_staff.html', username=username, upcoming_flights=upcoming_flights, search_flights_staff=search_flights_staff)


@app.route('/customer_flight', methods=['GET', 'POST'])
def customer_flight():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    flight_nbr = request.form['flight_nbr']
    cursor = conn.cursor()
    query = "SELECT airline_name, flight_nbr, airplane_id, t_depart, t_arrive, price, status, airport_depart, airport_arrive FROM `flight` LEFT JOIN staff USING (airline_name) WHERE t_depart BETWEEN CURRENT_DATE AND CURRENT_DATE+INTERVAL 30 day AND username = '{}'"
    cursor.execute(query.format(username))
    upcoming_flights = cursor.fetchall()
    query = "SELECT T.airline_name, flight_nbr, email FROM `ticket` T LEFT JOIN staff USING (airline_name) WHERE flight_nbr = '{}' AND username = '{}';"
    cursor.execute(query.format(flight_nbr, username))
    customer_flight = cursor.fetchall()
    cursor.close()
    return render_template('home_staff.html', username=username, upcoming_flights=upcoming_flights, customer_flight=customer_flight)

@app.route('/create_flights', methods=['GET', 'POST'])
def create_flights():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    airplane_id = request.form['airplane_id']
    flight_nbr = request.form['flight_nbr']
    t_depart = request.form['t_depart']
    t_arrive = request.form['t_arrive']
    price = request.form['price']
    airport_depart = request.form['airport_depart']
    airport_arrive = request.form['airport_arrive']
    cursor = conn.cursor()
    query = "SELECT airline_name FROM `staff` WHERE username = '{}'"
    cursor.execute(query.format(username))
    airline_name = cursor.fetchall()
    airline_name = np.array(airline_name.copy())[0][0]
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if 'Admin' not in permi_lst:
        error = 'Sorry, You are not Allowed to Create Flights'
        return render_template('error_staff.html', error=error)
    else:
        query = "INSERT INTO flight VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        cursor.execute(query.format(airline_name, airplane_id, flight_nbr, t_depart, t_arrive, price, 'upcoming', airport_depart, airport_arrive))
        conn.commit()
    cursor.close()
    return redirect(url_for('home_staff'))

@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    flight_nbr = request.form['flight_nbr']
    new_status = request.form['new_status']
    cursor = conn.cursor()
    query = "SELECT airline_name FROM `staff` WHERE username = '{}'"
    cursor.execute(query.format(username))
    airline_name = cursor.fetchall()
    airline_name = np.array(airline_name.copy())[0][0]
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if 'Operator' not in permi_lst:
        error = 'Sorry, You are not Allowed to Create Flights'
        return render_template('error_staff.html', error=error)
    else:
        query = "UPDATE flight SET status = '{}' WHERE airline_name = '{}' AND flight_nbr = '{}'"
        cursor.execute(query.format(new_status, airline_name, flight_nbr))
        conn.commit()
    cursor.close()
    return redirect(url_for('home_staff'))

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    airplane_id = request.form['airplane_id']
    seats = request.form['seats']
    cursor = conn.cursor()
    query = "SELECT airline_name FROM `staff` WHERE username = '{}'"
    cursor.execute(query.format(username))
    airline_name = cursor.fetchall()
    airline_name = np.array(airline_name.copy())[0][0]
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if 'Admin' not in permi_lst:
        error = 'Sorry, You are not Allowed to Add Airplanes'
        return render_template('error_staff.html', error=error)
    else:
        query = "INSERT INTO airplane VALUES('{}', '{}', '{}')"
        cursor.execute(query.format(airline_name, airplane_id, seats))
        conn.commit()
        query = "SELECT airplane_id FROM airplane WHERE airline_name = '{}'"
        cursor.execute(query.format(airline_name))
        airplane = cursor.fetchall()
        cursor.close()
        return render_template('confirmation_airplane.html', airplane=airplane)

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    airport_name = request.form['airport_name']
    city = request.form['city']
    cursor = conn.cursor()
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if 'Admin' not in permi_lst:
        error = 'Sorry, You are not Allowed to Add Airports'
        return render_template('error_staff.html', error=error)
    else:
        query = "INSERT INTO airport VALUES('{}', '{}')"
        cursor.execute(query.format(airport_name, city))
        conn.commit()
        cursor.close()
        return redirect(url_for('home_staff'))

@app.route('/view_agents')
def view_agents():
    if session['role'] != 'staff':
        return render_template('Index.html')
    cursor = conn.cursor()
    query = "SELECT A.email, COUNT(ticket_id) N FROM `ticket` NATURAL JOIN flight LEFT JOIN agent A USING(booking_agent_id) " \
            "WHERE A.email IS NOT NULL AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE GROUP BY A.email ORDER BY N DESC LIMIT 5"
    cursor.execute(query)
    agent_ticket_month = cursor.fetchall()
    query = "SELECT A.email, COUNT(ticket_id) N FROM `ticket` NATURAL JOIN flight LEFT JOIN agent A USING(booking_agent_id) " \
            "WHERE A.email IS NOT NULL AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE GROUP BY A.email ORDER BY N DESC LIMIT 5"
    cursor.execute(query)
    agent_ticket_year = cursor.fetchall()
    query = "SELECT A.email, 0.1*SUM(price) P FROM `ticket` NATURAL JOIN flight LEFT JOIN agent A USING(booking_agent_id) " \
            "WHERE A.email IS NOT NULL AND t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE GROUP BY A.email ORDER BY P DESC LIMIT 5"
    cursor.execute(query)
    agent_commission = cursor.fetchall()
    cursor.close()
    return render_template('view_agents.html', agent_ticket_month=agent_ticket_month, agent_ticket_year=agent_ticket_year, agent_commission=agent_commission)

@app.route('/view_customers')
def view_customers():
    if session['role'] != 'staff':
        return render_template('Index.html')
    cursor = conn.cursor()
    query = "SELECT email, COUNT(ticket_id) N FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE GROUP BY email ORDER BY N DESC LIMIT 1"
    cursor.execute(query)
    most_frequent = cursor.fetchall()
    query = "SELECT email FROM `ticket` GROUP BY email HAVING COUNT(airline_name) = 1"
    cursor.execute(query)
    loyal_customer = cursor.fetchall()
    cursor.close()
    return render_template('view_customers.html', most_frequent=most_frequent, loyal_customer=loyal_customer)

@app.route('/view_reports')
def view_reports():
    if session['role'] != 'staff':
        return render_template('Index.html')
    cursor = conn.cursor()
    query = "SELECT month(t_depart), COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE GROUP BY month(t_depart)"
    cursor.execute(query)
    total_ticket_year = cursor.fetchall()
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE"
    cursor.execute(query)
    total_ticket_month = cursor.fetchall()
    cursor.close()
    return render_template('view_reports.html', total_ticket_year=total_ticket_year, total_ticket_month=total_ticket_month)

@app.route('/total_ticket', methods=['GET', 'POST'])
def total_ticket():
    if session['role'] != 'staff':
        return render_template('Index.html')
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor()
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN '{}' AND '{}';"
    cursor.execute(query.format(start_date,end_date))
    total_ticket = cursor.fetchall()
    query = "SELECT month(t_depart), COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE GROUP BY month(t_depart)"
    cursor.execute(query)
    total_ticket_year = cursor.fetchall()
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE"
    cursor.execute(query)
    total_ticket_month = cursor.fetchall()
    cursor.close()
    return render_template('view_reports.html', total_ticket=total_ticket, total_ticket_year=total_ticket_year, total_ticket_month=total_ticket_month)

@app.route('/revenue_pie')
def revenue_pie():
    if session['role'] != 'staff':
        return render_template('Index.html')
    cursor = conn.cursor()
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE) AND booking_agent_id = 'None';"
    cursor.execute(query)
    direct_year = cursor.fetchall()[0][0]
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE) AND booking_agent_id != 'None';"
    cursor.execute(query)
    indirect_year = cursor.fetchall()[0][0]
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE) AND booking_agent_id = 'None';"
    cursor.execute(query)
    direct_month = cursor.fetchall()[0][0]
    query = "SELECT COUNT(ticket_id) FROM `ticket` NATURAL JOIN flight WHERE (t_depart BETWEEN CURRENT_DATE-INTERVAL 1 month AND CURRENT_DATE) AND booking_agent_id != 'None';"
    cursor.execute(query)
    indirect_month = cursor.fetchall()[0][0]
    cursor.close()
    return render_template('revenue_pie.html', direct_year=direct_year, indirect_year=indirect_year, direct_month=direct_month, indirect_month=indirect_month)

@app.route('/top_destination')
def top_destination():
    if session['role'] != 'staff':
        return render_template('Index.html')
    cursor = conn.cursor()
    query = "SELECT airport_arrive, COUNT(*) N FROM `flight` WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 3 month AND CURRENT_DATE GROUP BY airport_arrive ORDER BY N DESC LIMIT 3"
    cursor.execute(query)
    destination_month = cursor.fetchall()
    query = "SELECT airport_arrive, COUNT(*) N FROM `flight` WHERE t_depart BETWEEN CURRENT_DATE-INTERVAL 1 year AND CURRENT_DATE GROUP BY airport_arrive ORDER BY N DESC LIMIT 3"
    cursor.execute(query)
    destination_year = cursor.fetchall()
    cursor.close()
    return render_template('top_destination.html', destination_month=destination_month, destination_year=destination_year)

@app.route('/grant_permission', methods=['GET', 'POST'])
def grant_permission():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    staff_username = request.form['staff_username']
    new_permission = request.form['new_permission']
    cursor = conn.cursor()
    query = "SELECT airline_name FROM `staff` WHERE username = '{}'"
    cursor.execute(query.format(username))
    airline_user = cursor.fetchall()
    airline_user = np.array(airline_user.copy())[0][0]
    cursor.execute(query.format(staff_username))
    airline_staff = cursor.fetchall()
    airline_staff = np.array(airline_staff.copy())[0][0]
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if ('Admin' not in permi_lst) or (airline_user != airline_staff):
        error = 'Sorry, You are not Allowed to Grant Permissions'
        return render_template('error_staff.html', error=error)
    else:
        query = "SELECT permission FROM `permission` WHERE username = '{}'"
        cursor.execute(query.format(staff_username))
        permi = cursor.fetchall()
        permi = np.array(permi.copy())[0][0]
        permi_lst = json.loads(permi)
        if new_permission not in permi_lst:
            permi_lst.append(new_permission)
            permi = json.dumps(permi_lst)
            query = "UPDATE permission SET permission = '{}' WHERE username = '{}'"
            cursor.execute(query.format(permi,staff_username))
            conn.commit()
            cursor.close()
        return redirect(url_for('home_staff'))

@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
    if session['role'] != 'staff':
        return render_template('Index.html')
    username = session['username']
    agent_username = request.form['agent_username']
    cursor = conn.cursor()
    query = "SELECT airline_name FROM `staff` WHERE username = '{}'"
    cursor.execute(query.format(username))
    airline_user = cursor.fetchall()
    airline_user = np.array(airline_user.copy())[0][0]
    query = "SELECT booking_agent_id FROM `agent` WHERE email = '{}'"
    cursor.execute(query.format(agent_username))
    id = cursor.fetchall()
    id = np.array(id.copy())[0][0]
    query = "SELECT permission FROM `permission` WHERE username = '{}'"
    cursor.execute(query.format(username))
    permi = cursor.fetchall()
    permi = np.array(permi.copy())[0][0]
    permi_lst = json.loads(permi)
    if 'Admin' not in permi_lst:
        error = 'Sorry, You are not Allowed to Add Agents'
        return render_template('error_staff.html', error=error)
    else:
        query = "INSERT INTO workfor VALUES('{}',{})"
        cursor.execute(query.format(airline_user,id))
        conn.commit()
        cursor.close()
        return redirect(url_for('home_staff'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)



