#!/bin/bash
# Create database if it doesn't exist.

# https://serverfault.com/questions/173978
if ! mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "USE baseball;"
then
    echo "Baseball database does not exist."
    echo "/tCreating baseball database..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "CREATE DATABASE baseball;"
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/baseball.sql
    echo "/Adding data to database..."
    echo "/tBaseball database created."
else
    echo "Baseball database already exists."
    echo "/tRunning initial SQL queries..."
    echo "/tSQL queries ran."
fi

echo "Running main python script."
python /app/main.py