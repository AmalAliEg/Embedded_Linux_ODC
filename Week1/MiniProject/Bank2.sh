#!/bin/bash 

 

DATABASE_FILE="bank_database.txt" 

 

# Check if database file exists, create if not 

if [ ! -f "$DATABASE_FILE" ]; then 

    touch "$DATABASE_FILE" 

fi 

 

# Function to add a new client 

add_client() { 

    echo "Enter client details:" 

    read -p "Name: " name 

    read -p "ID: " id 

     

    # Check if ID already exists 

    if grep -q "^ID: $id|" "$DATABASE_FILE"; then 

        echo "Error: Client with ID $id already exists!" 

        return 1 

    fi 

     

    read -p "Account Number: " account 

    read -p "Funds Amount: " funds 

    read -p "Phone Number: " phone 

     

    echo "ID: $id|Name: $name|Account: $account|Funds: $funds|Phone: $phone" >> "$DATABASE_FILE" 

    echo "Client added successfully!" 

} 

 

# Function to delete a client 

delete_client() { 

    read -p "Enter client ID to delete: " id 

    if grep -q "^ID: $id|" "$DATABASE_FILE"; then 

        sed -i "/^ID: $id|/d" "$DATABASE_FILE" 

        echo "Client deleted successfully!" 

    else 

        echo "Client not found!" 

    fi 

} 

 

# Function to update client information 

update_client() { 

    read -p "Enter client ID to update: " id 

    if grep -q "^ID: $id|" "$DATABASE_FILE"; then 

        echo "Enter new details (leave blank to keep current value):" 

        read -p "Name: " name 

        read -p "Account Number: " account 

        read -p "Funds Amount: " funds 

        read -p "Phone Number: " phone 

         

        # Get current values 

        current_line=$(grep "^ID: $id|" "$DATABASE_FILE") 

        current_name=$(echo $current_line | cut -d'|' -f2 | cut -d':' -f2 | tr -d ' ') 

        current_account=$(echo $current_line | cut -d'|' -f3 | cut -d':' -f2 | tr -d ' ') 

        current_funds=$(echo $current_line | cut -d'|' -f4 | cut -d':' -f2 | tr -d ' ') 

        current_phone=$(echo $current_line | cut -d'|' -f5 | cut -d':' -f2 | tr -d ' ') 

         

        # Use new values or keep current ones if blank 

        name=${name:-$current_name} 

        account=${account:-$current_account} 

        funds=${funds:-$current_funds} 

        phone=${phone:-$current_phone} 

         

        # Update the record 

        sed -i "/^ID: $id|/c\ID: $id|Name: $name|Account: $account|Funds: $funds|Phone: $phone" "$DATABASE_FILE" 

        echo "Client information updated successfully!" 

    else 

        echo "Client not found!" 

    fi 

} 

 

# Function to search for a client 

search_client() { 

    read -p "Enter client ID to search: " id 

    if grep -q "^ID: $id|" "$DATABASE_FILE"; then 

        grep "^ID: $id|" "$DATABASE_FILE" | tr '|' '\n' 

    else 

        echo "Client not found!" 

    fi 

} 

 

# Main menu 

while true; do 

    echo -e "\nBank Database Management System" 

    echo "1. Add Client" 

    echo "2. Delete Client" 

    echo "3. Update Client" 

    echo "4. Search Client" 

    echo "5. Exit" 

    read -p "Select an option (1-5): " choice 

     

    case $choice in 

        1) add_client ;; 

        2) delete_client ;; 

        3) update_client ;; 

        4) search_client ;; 

        5) echo "Exiting..."; exit 0 ;; 

        *) echo "Invalid option!" ;; 

    esac 

done 