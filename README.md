# raspberry-pi 4, temperature sensor, mariaDB, MySQL
Reading temperature data from DS18B20 sensor using raspberry pi GPIO port and storing it in a CSV file 'temperature_log.csv' along with timeseries data.
First to create a MariaDB Server and a database named 'temperature_data'. Second, to create a table 'temperature_log' that matches the columns of the CSV file 'temperature_log.csv' created.
Creating a virtual environment to overcome #error: externally-managed-environment and to access the DB using a newuser because Debian based systems does not allow the 'root' user to authenticate using a password when accessed through programming interfaces.
Then load the data from CSV to the TABLE while avoiding duplicate entries.
Finally automating the execution of the python code using 'cron job'
