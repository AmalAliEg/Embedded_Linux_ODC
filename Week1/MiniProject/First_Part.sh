#!/bin/bash 

 

# Database file 

DATABASE="bank_database.txt" 

 

# Function to initialize the database 

initialize_db() { 

    if [[ ! -f "$DATABASE" ]]; then 

        touch "$DATABASE" 

        echo "Database file created: $DATABASE" 

    fi 

} 

 
