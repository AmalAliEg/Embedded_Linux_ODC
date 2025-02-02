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

 

# Function to add a new client 

add_client() { 

    echo "Enter client details:" 

    echo "Name:" 

    read name 

    echo "ID:" 

    read id 

    echo "Account number:" 

    read account 

    echo "Funds amount:" 

    read funds 

    echo "Phone number:" 

    read phone 

 

    # Check if client ID already exists 

    if grep -q "^$id," "$DATABASE"; then 

        echo "Client with ID $id already exists." 

    else 

        echo "$id,$name,$account,$funds,$phone" >> "$DATABASE" 

        echo "Client added successfully." 

    fi 

} 

 

# Function to delete a client 

delete_client() { 

    echo "Enter client ID to delete:" 

    read id 
 # Check if client exists 

    if grep -q "^$id," "$DATABASE"; then 

        grep -v "^$id," "$DATABASE" > temp.txt && mv temp.txt "$DATABASE" 

        echo "Client with ID $id deleted successfully." 

    else 

        echo "Client with ID $id not found." 

    fi 

} 

 

# Function to update client details 

update_client() { 

    echo "Enter client ID to update:" 

    read id 

 

    # Check if client exists 

    if grep -q "^$id," "$DATABASE"; then 

        echo "Enter new details:" 

        echo "Name:" 

        read name 

        echo "Account number:" 

        read account 

        echo "Funds amount:" 

        read funds 

        echo "Phone number:" 

        read phone 

 

        # Update the client record 

        awk -v id="$id" -v name="$name" -v account="$account" -v funds="$funds" -v phone="$phone" -F, '{ 

            if ($1 == id) { 

                $2 = name 

                $3 = account 

                $4 = funds 

                $5 = phone 

            } 

            print $0 

        }' OFS=, "$DATABASE" > temp.txt && mv temp.txt "$DATABASE" 

        echo "Client with ID $id updated successfully." 

    else 

        echo "Client with ID $id not found." 

    fi 

} 

 

# Function to search for a client 

search_client() { 

    echo "Enter client ID to search:" 

    read id 

 

    # Search for the client 
  if grep -q "^$id," "$DATABASE"; then 

        echo "Client details:" 

        grep "^$id," "$DATABASE" 

    else 

        echo "Client with ID $id not found." 

    fi 

} 

 

# Function to save the database to a file 

save_database() { 

    cp "$DATABASE" "backup_$(date +%Y%m%d_%H%M%S).txt" 

    echo "Database saved to backup file." 

} 

 

# Function to display all clients 

list_clients() { 

    echo "Listing all clients:" 

    cat "$DATABASE" 

} 

 

# Main menu 

main_menu() { 

    while true; do 

        echo "Bank Database System" 

        echo "1. Add Client" 

        echo "2. Delete Client" 

        echo "3. Update Client" 

        echo "4. Search Client" 

        echo "5. Save Database" 

        echo "6. List All Clients" 

        echo "7. Exit" 

        echo "Enter your choice:" 

        read choice 

 

        case $choice in 

            1) add_client ;; 

            2) delete_client ;; 

            3) update_client ;; 

            4) search_client ;; 

            5) save_database ;; 

            6) list_clients ;; 

            7) echo "Exiting..."; break ;; 

            *) echo "Invalid choice. Please try again." ;; 

        esac 

    done 

} 

 

# Initialize the database and start the main menu 

initialize_db 

main_menu 