import sqlite3

def setup_database():
    """Initializes an in-memory database with mock enterprise records."""
    # Connect to an isolated, temporary in-memory database instance
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    
    # Create a mock internal corporate accounts matrix
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            clearance_level TEXT NOT NULL
        )
    """)
    
    # Seed the tables with enterprise data profiles
    mock_accounts = [
        ('admin', 'SuperSecretVaultKey2026', 'Level-5-Top-Secret'),
        ('jane_dev', 'password556', 'Level-2-Engineering'),
        ('bob_hr', 'securehr99', 'Level-3-Human-Resources')
    ]
    cursor.executemany("INSERT INTO users (username, password, clearance_level) VALUES (?, ?, ?)", mock_accounts)
    connection.commit()
    return connection, cursor


def vulnerable_login(cursor, input_username):
    """
    DANGEROUS: Demonstrates a SQL Injection vulnerability 
    caused by raw string concatenation.
    """
    print(f"\n[ATTEMPTING VULNERABLE LOGIN] Input: {input_username}")
    
    # The Vulnerable Construct: Directly stitching strings together
    malicious_query = "SELECT username, clearance_level FROM users WHERE username = '" + input_username + "'"
    
    try:
        # The database engine compiles and runs the raw, unvalidated combined string
        cursor.execute(malicious_query)
        records = cursor.fetchall()
        
        if records:
            print("STATUS: Access Granted! Leaked User Records:")
            for row in records:
                print(f" -> User: {row[0]} | Access Cleared: {row[1]}")
        else:
            print("STATUS: Access Denied. No matching user found.")
            
    except sqlite3.Error as err:
        print(f"DATABASE CRASHED SYSTEM ERROR: {err}")


def secure_login(cursor, input_username):
    """
    SECURE: Neutralizes SQL Injection completely 
    using a Parameterized Query (Prepared Statement).
    """
    print(f"\n[ATTEMPTING SECURE PARAMETERIZED LOGIN] Input: {input_username}")
    
    # The Secure Construct: Using a designated placeholder '?'
    secure_query = "SELECT username, clearance_level FROM users WHERE username = ?"
    
    try:
        # Pass the user input explicitly inside an isolated tuple array wrapper
        cursor.execute(secure_query, (input_username,))
        records = cursor.fetchall()
        
        if records:
            print("STATUS: Access Granted! User Records:")
            for row in records:
                print(f" -> User: {row[0]} | Access Cleared: {row[1]}")
        else:
            print("STATUS: Access Denied. No matching records located.")
            
    except sqlite3.Error as err:
        print(f"DATABASE ERROR: {err}")


# ==========================================
# MAIN EXECUTION CORE
# ==========================================
if __name__ == "__main__":
    print("=== Step 1: Spinning Up Mock Secure Database Context ===")
    db_conn, db_cursor = setup_database()
    
    # Case A: Standard behavior works fine
    vulnerable_login(db_cursor, "jane_dev")
    
    # Case B: The Exploitation Phase
    # The hacker injects a payload that manipulates the SQL logic to always evaluate to true.
    # The syntax closes the string query early via "'" and comments out any trailing code via "--"
    sqli_attack_payload = "attacker_flag' OR '1'='1"
    
    print("\n=== Step 2: Launching Cyber Exploitation Payload ===")
    vulnerable_login(db_cursor, sqli_attack_payload)
    
    # Case C: The Production Mitigation Phase
    print("\n=== Step 3: Deploying Parameterized Remediation Protection ===")
    secure_login(db_cursor, sqli_attack_payload)
    
    # Cleanup database connection
    db_conn.close()
    print("\nSandbox Environment Cleanly Demolished.")