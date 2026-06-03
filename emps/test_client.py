import requests
import time

BASE_URL = "http://localhost:8000/api/v1/employees"

def execute_automated_crud_test():
    print("=== STARTING PROGRAMMATIC CLIENT TEST VIA REQUESTS ===")
    
    # 1. TEST POST (CREATE)
    new_emp_payload = {
        "name": "Jane Doe",
        "department": "Engineering",
        "salary": 115000.00
    }
    print("\n[Action] Sending POST request to create employee...")
    post_response = requests.post(BASE_URL, json=new_emp_payload)
    print(f"Server Response Code: {post_response.status_code}")
    print(f"Payload Response: {post_response.json()}")
    
    # Extract the dynamic ID assigned to Jane by the server handler
    assigned_id = post_response.json()["id"]
    time.sleep(1)

    # 2. TEST GET (READ ALL + QUERY FILTERING)
    print(f"\n[Action] Sending GET request with department filter query parameter...")
    get_filtered_response = requests.get(f"{BASE_URL}?department=Engineering")
    print(f"Server Response Code: {get_filtered_response.status_code}")
    print(f"Filtered Results: {get_filtered_response.json()}")
    time.sleep(1)

    # 3. TEST PUT (UPDATE SPECIFIC RESOURCE)
    update_payload = {
        "name": "Jane Doe-Smith",
        "department": "Engineering",
        "salary": 125000.00  # Give her a promotion salary raise
    }
    print(f"\n[Action] Sending PUT request to path ID parameter: /api/v1/employees/{assigned_id}")
    put_response = requests.put(f"{BASE_URL}/{assigned_id}", json=update_payload)
    print(f"Server Response Code: {put_response.status_code}")
    print(f"Updated Payload: {put_response.json()}")
    time.sleep(1)

    # 4. TEST DELETE (DESTROY RESOURCE)
    print(f"\n[Action] Sending DELETE execution request to path parameter: /api/v1/employees/{assigned_id}")
    delete_response = requests.delete(f"{BASE_URL}/{assigned_id}")
    print(f"Server Response Code: {delete_response.status_code}")
    print(f"Server Message: {delete_response.json()}")

if __name__ == "__main__":
    execute_automated_crud_test()