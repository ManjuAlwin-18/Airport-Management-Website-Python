from flask import Flask

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for,g,session
import mysql.connector
import connect
import uuid

#connection = None
dbconn = None

app=Flask(__name__)
app.secret_key = "secret_key"

def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, \
        password=connect.dbpass, host=connect.dbhost, \
        database=connect.dbname, autocommit=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        return dbconn

def genID():
    return uuid.uuid4().fields[1]




@app.route('/')
def home():
   
    return redirect(url_for('arrivals_departures'))


@app.route('/arrivals_departures', methods=['GET','POST'])
def arrivals_departures():

    
    if request.method == 'POST':

         print(request.form)
         select_airport = request.form.get('select_airport')
         print(select_airport)
         cur = getCursor()
         cur.execute("select DISTINCT FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                FlightDate AS Flight_Date,\
                DepTime AS Scheduled_Departure_Time,DepEstAct AS Estimated_Or_Actual_Depature_Time,\
                FlightStatus AS Flight_Status from flight f \
                join route r on f.FlightNum=r.FlightNum\
                join airport a on a.AirportCode=r.ArrCode where DepCode=%s and (FlightDate BETWEEN '2022-10-26' AND '2022-11-02')",(select_airport,))
         select_result = cur.fetchall()
         column_names = [desc[0] for desc in cur.description]
         
         print(request.form)
         select_airport = request.form.get('select_airport')
         print(select_airport)
         cur = getCursor()
         cur.execute("select DISTINCT FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',DepCode,']') AS Source_Airport_Name_And_Code,\
                FlightDate AS Flight_Date,\
                DepTime AS Scheduled_Arrival_Time,DepEstAct AS Estimated_Or_Actual_Arrival_Time,\
                FlightStatus AS Flight_Status from flight f \
                join route r on f.FlightNum=r.FlightNum \
                join airport a on a.AirportCode=r.DepCode where ArrCode=%s and (FlightDate BETWEEN '2022-10-26' AND '2022-11-02')",(select_airport,))
         select_result_arrival = cur.fetchall()
         column_names_arrivals = [desc[0] for desc in cur.description]
         return render_template('arrivals_departures.html',dbresult_arrivals=select_result_arrival,dbcols_arrivals=column_names_arrivals,dbresult=select_result,dbcols=column_names)
    
    else:
         cur = getCursor()
         cur.execute("select DISTINCT FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                FlightDate AS Flight_Date,\
                DepTime AS Scheduled_Departure_Time,DepEstAct AS Estimated_Or_Actual_Depature_Time,\
                FlightStatus AS Flight_Status from flight f \
                join route r on f.FlightNum=r.FlightNum\
                join airport a on a.AirportCode=r.ArrCode where DepCode=%s and (FlightDate BETWEEN '2022-10-26' AND '2022-11-02')",('NSN',))
         select_result = cur.fetchall()
         column_names = [desc[0] for desc in cur.description]
         
         
       
         cur = getCursor()
         cur.execute("select DISTINCT FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',DepCode,']') AS Source_Airport_Name_And_Code,\
                FlightDate AS Flight_Date,\
                DepTime AS Scheduled_Arrival_Time,DepEstAct AS Estimated_Or_Actual_Arrival_Time,\
                FlightStatus AS Flight_Status from flight f \
                join route r on f.FlightNum=r.FlightNum \
                join airport a on a.AirportCode=r.DepCode where ArrCode=%s and (FlightDate BETWEEN '2022-10-26' AND '2022-11-02')",('NSN',))
         select_result_arrival = cur.fetchall()
         column_names_arrivals = [desc[0] for desc in cur.description]
         return render_template('arrivals_departures.html',dbresult_arrivals=select_result_arrival,dbcols_arrivals=column_names_arrivals,dbresult=select_result,dbcols=column_names)
    
        

   
@app.route('/passenger_login', methods=['GET','POST'])
def passenger_login():
    
    if request.method == 'POST':

        login_email = request.form.get('loginemail') 
        
        print(login_email)

        cur = getCursor()
        cur.execute('SELECT * FROM passenger WHERE EmailAddress = %s',(login_email,))
       
        
        dbOutput = cur.fetchall()
        dblogin = list(dbOutput)  
        for row in dblogin:
            passenger_id=row[0]
            FirstName=row[1]
            LastName=row[2]

        if passenger_id == '':
            print(LastName)
            msg =" Sorry,This Email ID Does Not Exist."
            return render_template('passenger_login.html',msg = msg)

        else:
            print(FirstName)
            session['login_email'] = login_email   
            return redirect(url_for('passenger_page'))

           
    return render_template('passenger_login.html') 



@app.route('/passenger_register', methods=['GET','POST'])
def passenger_register():
    if request.method == 'POST':
        
        print(request.form)
        firstname = request.form.get('userfirstname')
        lastname = request.form.get('userlastname')
        email = request.form.get('useremail')
        userphone = request.form.get('userphone')
        passportnumber = request.form.get('userpassportnumber')
        dateofbirth = request.form.get('userdateofbirth')
        print(firstname,lastname,email,userphone,passportnumber,dateofbirth)
        cur = getCursor()
        cur.execute("INSERT INTO passenger(FirstName, LastName, EmailAddress,PhoneNumber,PassportNumber,DateOfBirth) VALUES (%s,%s,%s,%s,%s,%s);",(firstname,lastname,email,userphone,passportnumber,dateofbirth))

        return redirect(request.url)

    return render_template('passenger_register.html')


    
@app.route('/passenger_page', methods=['GET','POST'])
def passenger_page():
    if request.method == 'POST':
        
        print(request.form)
        firstname = request.form.get('userfirstname')
        lastname = request.form.get('userlastname')
        email = request.form.get('useremail')
        userphone = request.form.get('userphone')
        passportnumber = request.form.get('userpassportnumber')
        dateofbirth = request.form.get('userdateofbirth')
        cur = getCursor()
        cur.execute("UPDATE passenger SET FirstName=%s, LastName=%s,EmailAddress=%s, PhoneNumber=%s,\
                    PassportNumber=%s, DateOfBirth=%s\
                    where PassengerID=%s",(firstname,lastname,email,userphone,passportnumber,dateofbirth,"1657"))
        cur = getCursor()
        cur.execute("SELECT * FROM passenger where PassengerID=%s",("1657",))
        select_result = cur.fetchall()


        cur = getCursor()
        cur.execute("select f.FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                 concat(AirportName,' ','[',DepCode,']') AS Source_Airport_Name_And_Code,\
                     f.FlightDate AS Flight_Date,\
                DepTime AS Departure_Time,ArrTime AS Arrival_Time,\
                FlightStatus AS Flight_Status,f.Aircraft AS Aircraft from flight f\
                join route r on f.FlightNum=r.FlightNum\
                join passengerflight p on p.FlightID=f.FlightID\
                join airport a on a.AirportCode=r.ArrCode where PassengerID=%s",("1657",))
        existing_result = cur.fetchall()
        existing_column_names = [desc[0] for desc in cur.description]



        return render_template('passenger_page.html',dbresult=select_result,dbexist=existing_result,existing_col_names=existing_column_names)
        
        if request.form['submit_button'] == 'Add_new_flight':
             return redirect(url_for('passenger_add_flight'))

            
        elif request.form['submit_button'] == 'logout_page':
            return redirect(url_for('logout'))

 
    else:
        cur = getCursor()
        cur.execute("SELECT * FROM passenger where PassengerID=%s",('1657',))
        select_result = cur.fetchall()
        print(select_result)    

        cur = getCursor()
        cur.execute("select f.FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                    concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                    concat(AirportName,' ','[',DepCode,']') AS Source_Airport_Name_And_Code,\
                    f.FlightDate AS Flight_Date,\
                    DepTime AS Departure_Time,ArrTime AS Arrival_Time,\
                    FlightStatus AS Flight_Status,f.Aircraft AS Aircraft from flight f\
                    join route r on f.FlightNum=r.FlightNum\
                    join passengerflight p on p.FlightID=f.FlightID\
                    join airport a on a.AirportCode=r.ArrCode where PassengerID=%s ORDER BY FlightDate ASC, DepTime ASC",('1657',))
        existing_result = cur.fetchall()
        existing_column_names = [desc[0] for desc in cur.description]
        return render_template('passenger_page.html',dbresult=select_result,dbexist=existing_result,existing_col_names=existing_column_names)

        if request.form['submit_button'] == 'Add_new_flight':
             return redirect(url_for('passenger_add_flight'))

            
        elif request.form['submit_button'] == 'logout_page':
            return redirect(url_for('logout'))


@app.before_request
def before_request():
    g.login_email=None

    if 'login_email' in session:
        g.login_email=session['login_email']



 
@app.route('/passenger_page/update', methods=['GET','POST'])
def passenger_page_update():
    if request.method == 'POST':
        
        print(request.form)
        firstname = request.form.get('userfirstname')
        lastname = request.form.get('userlastname')
        email = request.form.get('useremail')
        userphone = request.form.get('userphone')
        passportnumber = request.form.get('userpassportnumber')
        dateofbirth = request.form.get('userdateofbirth')
        cur = getCursor()
        cur.execute("UPDATE passenger SET FirstName=%s, LastName=%s,EmailAddress=%s, PhoneNumber=%s,\
                    PassportNumber=%s, DateOfBirth=%s\
                    where PassengerID=%s",(firstname,lastname,email,userphone,passportnumber,dateofbirth,"1657"))
        cur = getCursor()
        cur.execute("SELECT * FROM passenger where PassengerID=%s",("1657",))
        select_result = cur.fetchall()


        cur = getCursor()
        cur.execute("select f.FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                 concat(AirportName,' ','[',DepCode,']') AS Source_Airport_Name_And_Code,\
                     f.FlightDate AS Flight_Date,\
                DepTime AS Departure_Time,ArrTime AS Arrival_Time,\
                FlightStatus AS Flight_Status,f.Aircraft AS Aircraft from flight f\
                join route r on f.FlightNum=r.FlightNum\
                join passengerflight p on p.FlightID=f.FlightID\
                join airport a on a.AirportCode=r.ArrCode where PassengerID=%s",("1657",))
        existing_result = cur.fetchall()
        existing_column_names = [desc[0] for desc in cur.description]



        return render_template('passenger_page.html',dbresult=select_result,dbexist=existing_result,existing_col_names=existing_column_names)
        
        if request.form['submit_button'] == 'Add_new_flight':
             return redirect(url_for('passenger_add_flight'))

            
        elif request.form['submit_button'] == 'logout_page':
            return redirect(url_for('logout'))




@app.route('/passenger_add_flight', methods=['GET','POST'])
def passenger_add_flight():
    if request.method == 'POST':

         print(request.form)
         Depatureairport = request.form.get('DepatureAirport')
         print(Depatureairport)
         cur = getCursor()
         cur.execute("select FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(AirportName,' ','[',ArrCode,']') AS Destination_Airport_Name_And_Code,\
                DepTime AS Scheduled_Departure_Time,DepEstAct AS Estimated_Or_Actual_Depature_Time,\
                FlightStatus AS Flight_Status from flight f \
                join route r on f.FlightNum=r.FlightNum\
                join airport a on a.AirportCode=r.ArrCode where DepCode=%s",(Depatureairport,))
         select_result = cur.fetchall()
         column_names = [desc[0] for desc in cur.description]

         return render_template('passenger_add_flight.html',dbresult=select_result,dbcols=column_names)
        
    return render_template('passenger_add_flight.html')



@app.route('/admin/', methods=['GET','POST'])
def admin_home():
    if request.method == 'POST':

        print(request.form)
        staff_login_id = request.form.get('staff_login') 
        print(staff_login_id)

        cur = getCursor()
        cur.execute('SELECT * FROM staff WHERE StaffID = %s',(staff_login_id,))
        select_result_staff = cur.fetchall()
        print(select_result_staff)

        list_select_result_staff = list(select_result_staff)  
        for row_staff in list_select_result_staff:
            select_result_s_login =row_staff[0]
            print(select_result_s_login)
            if select_result_s_login !=0:
                print(select_result_s_login)
                msg = "Logged in Successfully"
                return redirect(url_for('admin_passenger_list'))
           
        
    return render_template('admin/staff_login.html')





@app.route('/admin/passenger_list')
def admin_passenger_list():
    
    
    cur = getCursor()
    cur.execute("select p.PassengerID AS Passenger_ID,p.FirstName AS Flight_Name,\
                p.LastName AS Last_Name,p.EmailAddress AS Email,\
                 p.PhoneNumber AS Phone_Number,\
                p.PassportNumber AS Passport_Number,p.DateOfBirth AS Date_Of_Birth,\
                f.FlightNum AS Flight_Numbers,f.Aircraft AS Aircraft from passenger p\
                join passengerflight pf on p.PassengerID=pf.PassengerID\
                join flight f on pf.FlightID=f.FlightID ORDER BY LastName ASC, FirstName ASC")
    passenger_list = cur.fetchall()
    passenger_list_names = [desc[0] for desc in cur.description]
    return render_template('admin/passenger_list.html',dbresult=passenger_list,dbcol_passenger=passenger_list_names)

    


@app.route('/admin/flight_lists')
def admin_flight_lists():
   
    cur = getCursor()
    cur.execute("select DISTINCT f.FlightID AS Flight_ID,f.FlightNum AS Flight_Number,\
                concat(ap.AirportName,' ','[',r.DepCode,']') AS Departure__Airport, \
                f.FlightDate AS Flight_Date,\
                DepTime AS Departure_Time,ArrTime AS Arrival_Time,\
                f.Aircraft AS Aircraft,ar.Seating AS Total_Seats from flight f \
                join passengerflight pf on pf.FlightID=f.FlightID\
                join passenger p on p.PassengerID=pf.PassengerID\
                join aircraft ar on f.Aircraft=ar.RegMark\
                join route r on r.FlightNum=f.FlightNum\
				join airport ap on ap.AirportCode=r.DepCode ORDER BY FlightDate ASC, DepTime ASC, DepTime ASC")
    flight_list = cur.fetchall()
    flight_list_names = [desc[0] for desc in cur.description]
    return render_template('admin/flight_lists.html',dbresult=flight_list,dbcol_flight=flight_list_names)
    


@app.route('/admin/passenger_List_edit',methods=['GET','POST'])
def admin_passenger_List_edit():
    if request.method == 'POST':

        print(request.form)
        passenger_id = request.form.get('passenger_id')
        firstname = request.form.get('userfirstname')
        lastname = request.form.get('userlastname')
        email = request.form.get('useremail')
        userphone = request.form.get('userphone')
        passportnumber = request.form.get('userpassportnumber')
        dateofbirth = request.form.get('userdateofbirth')
        cur = getCursor()
        cur.execute("UPDATE passenger SET FirstName=%s, LastName=%s,EmailAddress=%s, PhoneNumber=%s,\
                    PassportNumber=%s, DateOfBirth=%s\
                    where PassengerID=%s",(firstname,lastname,email,userphone,passportnumber,dateofbirth,passenger_id))

        
        cur = getCursor()
        cur.execute("SELECT * FROM passenger where PassengerID=%s",(passenger_id,))
        select_passenger = cur.fetchall()

        cur.execute("select DISTINCT p.PassengerID AS Passenger_ID,p.FirstName AS Flight_Name,\
                    p.LastName AS Last_Name,p.EmailAddress AS Email,\
                    p.PhoneNumber AS Phone_Number,\
                    p.PassportNumber AS Passport_Number,p.DateOfBirth AS Date_Of_Birth,\
                    f.FlightNum AS Flight_Numbers,f.Aircraft AS Aircraft from passenger p\
                    join passengerflight pf on p.PassengerID=pf.PassengerID\
                    join flight f on pf.FlightID=f.FlightID where p.PassengerID=%s\
                     ORDER BY LastName ASC, FirstName ASC ",(passenger_id,))
        passenger_details= cur.fetchall()
        passenger_details_cols= [desc[0] for desc in cur.description]

        
        return render_template('admin/passenger_List_edit.html',dbresult=select_passenger,dbpassenger=passenger_details,dbcol_passenger=passenger_details_cols)

    else:
        passenger_id = request.args.get('passenger_id')
        print(passenger_id)
        if id == '':
            return redirect("/")
        else:
            print(passenger_id)
            cur = getCursor()

            cur.execute("SELECT * FROM passenger where PassengerID=%s",(passenger_id,))
            select_passenger= cur.fetchall()

            cur.execute("select DISTINCT p.PassengerID AS Passenger_ID,p.FirstName AS Flight_Name,\
                    p.LastName AS Last_Name,p.EmailAddress AS Email,\
                    p.PhoneNumber AS Phone_Number,\
                    p.PassportNumber AS Passport_Number,p.DateOfBirth AS Date_Of_Birth,\
                    f.FlightNum AS Flight_Numbers,f.Aircraft AS Aircraft from passenger p\
                    join passengerflight pf on p.PassengerID=pf.PassengerID\
                    join flight f on pf.FlightID=f.FlightID where p.PassengerID=%s\
                     ORDER BY LastName ASC, FirstName ASC ",(passenger_id,))
            passenger_details= cur.fetchall()
            passenger_details_cols= [desc[0] for desc in cur.description]

            return render_template('admin/passenger_List_edit.html',dbresult=select_passenger,dbpassenger=passenger_details,dbcol_passenger=passenger_details_cols)
           


@app.route('/admin/flight_List_edit',methods=['GET','POST'])
def admin_flight_List_edit():
    
    if request.method == 'POST':

        print(request.form)
        flight_id = request.form.get('flight_id')
        flight_NUm = request.form.get('flight_NUm')
        aircraft_name = request.form.get('aircraft_name')
        flight_date = request.form.get('flight_date')
        dep_time = request.form.get('dep_time')
        arr_time = request.form.get('arr_time')
        flight_status = request.form.get('flight_status')
        dep_est_time = request.form.get('dep_est_time')
        esti_arr_time = request.form.get('esti_arr_time')

        cur = getCursor()
        cur.execute("UPDATE flight SET FlightNum=%s,FlightDate=%s, DepTime=%s,\
                    ArrTime=%s, FlightStatus=%s,DepEstAct=%s,ArrEstAct=%s\
                    where FlightID=%s",(flight_NUm,flight_date,dep_time,arr_time,flight_status,dep_est_time,esti_arr_time,flight_id))
        cur = getCursor()
        cur.execute("SELECT * FROM flight where FlightID=%s",(flight_id,))
        select_flight = cur.fetchall()
        
        cur = getCursor()
        cur.execute("select p.PassengerID AS Passenger_ID,p.FirstName AS Flight_Name,\
                    p.LastName AS Last_Name,p.EmailAddress AS Email,\
                    p.PhoneNumber AS Phone_Number,\
                    p.PassportNumber AS Passport_Number,p.DateOfBirth AS Date_Of_Birth from passenger p\
                    join passengerflight pf on p.PassengerID=pf.PassengerID\
                    join flight f on pf.FlightID=f.FlightID where f.FlightID=%s ORDER BY LastName ASC, FirstName ASC",(flight_id,))
        passenger_lists= cur.fetchall()
        passenger_lists_cols = [desc[0] for desc in cur.description]


        return render_template('admin/flight_List_edit.html',dbresult=select_flight,dbcol_passenger=passenger_lists_cols,dbpassengerresult=passenger_lists)
    else:

        flight_id = request.args.get('flight_id')
        print(flight_id)
        if id == '':
            return redirect("/")
        else:
            print(flight_id)
            cur = getCursor()

            cur.execute("select * from flight where FlightID=%s",(flight_id,))
            select_flight= cur.fetchall()
            
            cur = getCursor()
            cur.execute("select p.PassengerID AS Passenger_ID,p.FirstName AS Flight_Name,\
                        p.LastName AS Last_Name,p.EmailAddress AS Email,\
                        p.PhoneNumber AS Phone_Number,\
                        p.PassportNumber AS Passport_Number,p.DateOfBirth AS Date_Of_Birth from passenger p\
                        join passengerflight pf on p.PassengerID=pf.PassengerID\
                        join flight f on pf.FlightID=f.FlightID where f.FlightID=%s ORDER BY LastName ASC, FirstName ASC",(flight_id,))
            passenger_lists= cur.fetchall()
            passenger_lists_cols = [desc[0] for desc in cur.description]

            return render_template('admin/flight_List_edit.html',dbresult=select_flight,dbcol_passenger=passenger_lists_cols,dbpassengerresult=passenger_lists)
        return render_template('admin/flight_List_edit.html')



@app.route('/admin/manager_add_flights',methods=['GET','POST'])
def admin_manager_add_flights():
    if request.method == 'POST':

        if request.form['submit_button'] == 'Add_previous_week':
            print("add email")
            cur = getCursor()
            cur.execute("SELECT FlightNum,WeekNum+1,DATE_ADD(FlightDate,INTERVAL 7 DAY),DepTime,ArrTime,Duration,DepTime,ArrTime,\
                        FlightStatus,Aircraft FROM flight where WeekNum=(select max(WeekNum) from flight);") 
            dbOutput = cur.fetchall()

            ## Insert multiple rows  into Flights table
            sql_insert = "INSERT INTO flight (FlightNum, WeekNum, FlightDate, DepTime,ArrTime,Duration,DepEstAct,ArrEstAct,FlightStatus,Aircraft) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s);"
            cur.executemany(sql_insert,dbOutput)

            
        elif request.form['submit_button'] == 'add_new':
                
                print(request.form)
                flight_NUm = request.form.get('flight_NUm')
                aircraft_name = request.form.get('aircraft_name')
                flight_date = request.form.get('flight_date')
                dep_time = request.form.get('dep_time')
                arr_time = request.form.get('arr_time')
                
               

                Duration=arr_time-dep_time
                cur.execute("SELECT DISTINCT WeekNum+1 FROM flight where WeekNum=(select max(WeekNum) from flight);") 
                dbOutput = cur.fetchall()

                cur = getCursor()
                cur.execute("INSERT INTO flight(FlightNum, Aircraft, FlightDate,DepTime,\
                                ArrTime,DepEstAct,ArrEstAct,Duration,FlightStatus,WeekNum) VALUES (%s,%s,%s,%s,%s,%s,\
                                    %s,%s,%s,%s);",(flight_NUm,aircraft_name,flight_date,dep_time,arr_time,dep_time,arr_time,Duration,"On time",dbOutput))

                return redirect(request.url)
   
    return render_template('admin/manager_add_flights.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('passenger_login'))


if __name__=='__main__':
    app.run(debug=True)