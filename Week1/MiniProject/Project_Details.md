# Bank Database System - Bash Script

This project is a Bash shell script designed to manage client data for a bank database system. It allows users to add, delete, update, search, and list client records, as well as save backups of the database. The script is a great way to practice Bash scripting and collaboration.

---

## Features

- **Database File:**  
  The database is stored in a text file (`bank_database.txt`), where each line represents a client with fields separated by commas (`,`).  
  Format: `ID,Name,Account,Funds,Phone`.

- **Functions:**
  - **Add Client:** Add a new client to the database.
  - **Delete Client:** Remove a client by their ID.
  - **Update Client:** Modify client details by their ID.
  - **Search Client:** Find a client by their ID.
  - **Save Database:** Create a backup of the database.
  - **List Clients:** Display all clients in the database.

- **Main Menu:**  
  Provides a user-friendly interface to interact with the database.

---

## Task Division

### Core Functionality (Person 1)
1. **Database Initialization:**  
   Implement the `initialize_db` function to create the database file if it doesn’t exist.
2. **Add Client:**  
   Implement the `add_client` function to add a new client to the database.
3. **Delete Client:**  
   Implement the `delete_client` function to remove a client by their ID.
4. **Save Database:**  
   Implement the `save_database` function to create a backup of the database.

### Advanced Functionality (Person 2)
1. **Update Client:**  
   Implement the `update_client` function to modify client details by their ID.
2. **Search Client:**  
   Implement the `search_client` function to find a client by their ID.
3. **List Clients:**  
   Implement the `list_clients` function to display all clients in the database.
4. **Main Menu:**  
   Implement the `main_menu` function to provide a user interface for interacting with the database.

---

## Collaboration Tips

1. **Version Control:**  
   Use Git to collaborate on the script. Create a repository and push changes regularly.
2. **Testing:**  
   Test each function independently before integrating them into the main script.
3. **Documentation:**  
   Add comments to the code to explain how each function works.
4. **Communication:**  
   Regularly communicate to ensure both team members are on the same page.

---

## How to Run the Script

1. Save the script to a file, e.g., `bank_system.sh`.
2. Make it executable:
   ```bash
   chmod +x bank_system.sh
