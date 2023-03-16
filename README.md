# Airport Management System

This project is about developing an Airport Management system using Python. The application will help in managing the operations of an airport, such as booking and tracking flights, managing passengers, and keeping track of the resources available at the airport.

## Requirements

* Python 3.x
* MySQL

## Installation

1. Clone the repository
2. Install all the dependencies by executing the command `pip install -r requirements.txt`
3. Create the database with the command `python manage.py migrate`
4. Create a user with the command `python manage.py createsuperuser`
5. Update the database configuration in the file `connect.py`

## Usage

1. Start the server by executing `python manage.py runserver`
2. Open the browser and go to `http://localhost:8000`
3. Login with the credentials created in installation
4. You are now ready to use the application

## Database Configuration

You can set up the database configuration in the file `connect.py`

**Database Configuration Parameters**
* DBUSER = "root" #PUT YOUR MySQL username here - usually admin
* DBPASS = "" #PUT YOUR PASSWORD HERE
* DBHOST = "localhost" #PUT YOUR AWS Connect String here
* DBPORT = "3306"
* DBNAME = "airline" #PUT YOUR Database Name
 
## Contribute

If you want to contribute to this project, feel free to fork the repository and make pull requests.

## License

This project is released under the MIT License.
