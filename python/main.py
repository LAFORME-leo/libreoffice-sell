import sqlite3
import sys, os
from pathlib import Path
import pyperclip  # Ensure `pyperclip` is installed for clipboard handling

def get_db_data(query, output_dest="buffer"):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("C:\\Users\\Leo\\Downloads\\db.db")
        cursor = conn.cursor()
        
        # Parse query to check for special insert handling
        if query.strip().upper().startswith("INSERT INTO CLIENT"):
            # Extract first_name and last_name from query
            values_start = query.upper().find("VALUES") + len("VALUES")
            values = query[values_start:].strip(" ();")
            values_list = [v.strip(" '\"") for v in values.split(",")]
            first_name = values_list[1]
            last_name = values_list[0]
            
            # Check if the client already exists
            cursor.execute(
                "SELECT * FROM Client WHERE first_name = ? AND last_name = ?", 
                (first_name, last_name)
            )
            existing_client = cursor.fetchone()
            
            if existing_client:
                error_message = "Error: Client exists"
                handle_output(error_message, output_dest)
                return error_message
            
            # Proceed with the insert if no match is found
            cursor.execute(query)
            conn.commit()
            handle_output("ok", output_dest)
            return "ok"
        
        # Execute regular queries
        cursor.execute(query)
        
        # Fetch and handle SELECT results
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            formatted_result = '\n'.join([str(row) for row in result])
            handle_output(formatted_result, output_dest)
            return formatted_result
        
        # Commit changes for other write operations
        conn.commit()
        handle_output("ok", output_dest)
        return "ok"
    
    except sqlite3.Error as e:
        error_message = f"Error: {e}"
        handle_output(error_message, output_dest)
        return error_message
    
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

def handle_output(output, output_dest):
    """
    Handle output based on destination (buffer or file).
    """
    if output_dest == "buffer":
        # Write to clipboard
        pyperclip.copy(output)
        print("Output copied to clipboard.")
    elif output_dest == "file":
    # Define the folder and file name
     nameofFolder = "temp"
     folder_path = Path.home() / nameofFolder  # Create the path for the folder
     file_path = folder_path / "output.txt"    # Create the path for the file

    # Check if the folder exists, and create it if not
     if not folder_path.is_dir():
         folder_path.mkdir(parents=True, exist_ok=True)

    # Write to a text file in the folder
     with open(file_path, "w") as f:
         f.write(output)
    
     print(f"Output written to {file_path}.")

    else:
        print("Invalid output destination specified.")

if __name__ == '__main__':
    # Parse arguments
    func_name = sys.argv[1]
    func_arg = sys.argv[2]
    output_dest = sys.argv[3] if len(sys.argv) > 3 else "buffer"  # Default to buffer

    # Call the requested function with arguments
    # example: python main.py get_db_data "SELECT * FROM Client" file
    globals()[func_name](func_arg, output_dest)
