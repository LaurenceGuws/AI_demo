#!/bin/bash

# Define a function to print a message within lines of '#' characters
print_message() {
    echo "################################################################################"
    echo " $1"
    echo "################################################################################"
}

print_message "Container starting..."

# Write environment variables to /etc/environment
printenv > /etc/environment

# Run the database initialization
if [ ! -f /app/instance/chat.db ]; then
    flask setup >> /proc/1/fd/1 2>> /proc/1/fd/2
    print_message "Starting database initialization..."
    print_message "Database initialization completed."

# Run the application
fi
print_message "Starting the application..."
flask run --debug --host=0.0.0.0 --port=5000 >> /proc/1/fd/1 2>> /proc/1/fd/2
print_message "Application has started."

