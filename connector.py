#1.-pip install mysql-connector-python
#2.-sudo mysql -u root
#3.-USE mysql;
#4.-SELECT User, Host, plugin FROM mysql.user;
#5.-UPDATE user SET plugin='mysql_native_password' WHERE User='root';
#6.-FLUSH PRIVILEGES;
#7.-exit;
#8.-service mysql restart
#9.-sudo mysql -u root

import mysql.connector

linkedinDB = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='linkedin', port=3306)

print(linkedinDB)