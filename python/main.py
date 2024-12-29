import sqlite3
import sys

def get_db_data(query):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("C:\\Users\\Leo\\Downloads\\db.db")
        cursor = conn.cursor()
        
        # Parse query to check for special insert handling
        if query.strip().upper().startswith("INSERT INTO CLIENT"):
            # Extract first_name and last_name from query
            # NOTE: This assumes a specific query format, e.g.,
            # INSERT CLIENT (first_name, last_name, ...) VALUES ('John', 'Smith', ...)
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
                print(error_message)
                return error_message
            
            # Proceed with the insert if no match is found
            cursor.execute(query)
            conn.commit()
            print("ok")  # Indicate success
            return "ok"
        
        # Execute regular queries
        cursor.execute(query)
        
        # Fetch and handle SELECT results
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            formatted_result = '\n'.join([str(row) for row in result])
            print(formatted_result)
            return formatted_result
        
        # Commit changes for other write operations
        conn.commit()
        print("ok")
        return "ok"
    
    except sqlite3.Error as e:
        error_message = f"Error: {e}"
        print(error_message)
        return error_message
    
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

if __name__ == '__main__':
    # Execute the requested function with provided argument
    func_name = sys.argv[1]
    func_arg = sys.argv[2]
    globals()[func_name](func_arg)
