#!/bin/bash 

 
# Create the Database file to store clients info 
DATABASE="Clients_DataBase.txt" 


# Function to initialize the database  if doesn't exist
init_Database() { 

    # -f option indicate file. check if DATABASE not exist
    if [ ! -f "$DATABASE" ];                                                                                
    then 
        #touch to create the file
        touch "$DATABASE"                                                                                   

        #add header for first line in the database with alignment column
        printf "%-20s | %-15s | %-15s | %-15s | %s\n" "ID" "Client Name" "Account Number" "Phone Number" "Amount" >> "$DATABASE"             

        #massage appeared to the user after the creation of the file 
        echo "Database file created: $DATABASE"                                                             
    fi 

} 


#function to add the new clients to the database
Add_clients()
{   #take the info of the users 
    read -p "Enter client's name: " Client_Name
    read -p "Enter client's ID: " Client_ID
    read -p "Enter client's acount number: " Client_Account_NO
    read -p "Enter client's phone number : " Client_Phone_NO
    read -p "Enter the amount of the account : " Fund_Ammount

    #check if the user is exist or not 
    if grep -q "^$Client_ID" "$DATABASE" ;
    then
        #msg for the user 

        echo "the client with id: $Client_ID is exist"
    else
        #add values of the clients in the database with alignment column
        printf "%-20s | %-15s | %-15s | %-15s | %s\n" "$Client_ID" "$Client_Name" "$Client_Account_NO" "$Client_Phone_NO" "$Fund_Ammount" >> "$DATABASE"
        #msg for the user 
        echo "the client with id: $Client_ID added"
    fi

}


#function to Delete a client from the database 
Delete_Client(){
#ask the user for the id of the client to be deleted 
read -p "enter the id for the client to be deleted: " Client_ID
if  grep -q "^$Client_ID" "$DATABASE" ;
then 
    #this line insure to delete the entire row for the client according to its ID
    sed -i "/^$Client_ID/d" "$DATABASE"
    echo "client removed successfully!"
else
    echo "client Already not exsit or Removed!"
fi 

}

#function to save Database in backup file if lost
Save_Database(){
    #get the current directory 
    current_dir=$(pwd)

    BackUp_DIR="$current_dir/BACKUP_FILES_DATABASE_AM"

    #if the folder not exist create one
    if [  ! -d $BackUp_DIR ]
    #create the backup directory 
    then 
        mkdir -p "$BackUp_DIR"
        echo "Backup Directory created successfully!"
    fi 

    #count the creation number of the backup files
    count=$(ls "$BackUp_DIR" | grep -c "^backup_" )

    #check over the condition and delete the oldest five files to save the memory
    if [ "$count" -gt 10 ];
    then 
        ls -1t "$BackUp_DIR"/backup_* | tail -n 5 | xargs rm -f
        echo "the oldest 5 backup files deleted successfully!"

    fi

    #create a backup file using the current date and hour for naming it
    cp "$DATABASE" "$BackUp_DIR/backup_$(date +%Y%m%d_%H%M%S).txt"
    echo "backup file created successfully!"

}


#Call the init function
#init_Database          

#Call the Add function                                
#Add_clients      

#Call the Delete function                                
#Delete_Client

#Call the copying function                                
#Save_Database
