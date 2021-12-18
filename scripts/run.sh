#!/bin/bash
# Create database if it doesn't exist.
# https://serverfault.com/questions/173978
if ! mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "USE baseball;"
then
    echo "Baseball database does not exist..."
    echo "...creating baseball database..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP -e "CREATE DATABASE baseball;"
    # https://dba.stackexchange.com/questions/17367
    # https://stackoverflow.com/questions/36138219
    echo "...adding data to database..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/baseball.sql
    echo "...baseball database created."

    echo "Adding tables..."
    echo "...creating table mlb_game..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/mlb_game.sql
    echo "...creating table prior_game..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/prior_game.sql
    echo "...creating 'window' tables..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/window.sql
    echo "...creating team performance table..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/team_performance.sql
    echo "...creating pythagorean expectation tables..."
    mysql -uroot -ppassword --host="mariadb" -P3306 --protocol=TCP baseball < /scripts/sql/pythagorean_expectation.sql

    echo "Database setup complete"

else
    echo "Baseball database already exists."
fi



echo "Running main python script."
python /app/main.py