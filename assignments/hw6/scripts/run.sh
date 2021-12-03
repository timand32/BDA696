#!/bin/bash
# Create database if it doesn't exist.

# https://serverfault.com/questions/173978
if mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "USE baseball;"
then 
    echo "Baseball database already exists."
else
    echo "Baseball database does not exist, creating it..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "CREATE DATABASE baseball;"
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /data/baseball.sql
    echo "Running pitcher stat queries..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/pitcher.sql
fi

python /hw5/hw5.py