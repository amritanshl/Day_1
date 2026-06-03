import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Our in-memory database simulating enterprise storage
EMPLOYEE_DB = {
    1: {"id": 1, "name": "Alex Russo", "department": "Engineering", "salary": 95000.0},
    2: {"id": 2, "name": "Sam Wilson", "department": "Marketing", "salary": 72000.0}
}
next_id = 3

class RESTAPIHandler(BaseHTTPRequestHandler):
    
    # Global CORS Headers allowing our webpage and Postman to talk to the server safely
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, status_code: int, payload: dict):
        """Helper method to format and send standard JSON responses."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        """Handles browser pre-flight security checks."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    # ==========================================
    # 1. READ OPERATIONS (GET)
    # ==========================================
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Endpoint Matrix 1: GET /api/v1/employees (With Query Param Filtering)
        if path == "/api/v1/employees":
            employee_list = list(EMPLOYEE_DB.values())
            
            # Implementation of Query Parameters: ?department=Engineering
            if "department" in query_params:
                target_dept = query_params["department"][0]
                employee_list = [emp for emp in employee_list if emp["department"].lower() == target_dept.lower()]
                
            return self._respond(200, employee_list)

        # Endpoint Matrix 2: GET /api/v1/employees/{id} (Path Parameter)
        elif path.startswith("/api/v1/employees/"):
            try:
                emp_id = int(path.split("/")[-1])
                if emp_id in EMPLOYEE_DB:
                    return self._respond(200, EMPLOYEE_DB[emp_id])
                return self._respond(404, {"error": f"Employee ID {emp_id} not found."})
            except ValueError:
                return self._respond(400, {"error": "Invalid Path Parameter ID format."})

        # Fallback 404
        return self._respond(404, {"error": "Endpoint mapping not found."})

    # ==========================================
    # 2. CREATE OPERATIONS (POST)
    # ==========================================
    def do_POST(self):
        global next_id
        path = urlparse(self.path).path

        if path == "/api/v1/employees":
            # Extract and parse the Request Payload Body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode('utf-8'))
                
                # Validation Gate Check
                if "name" not in data or "department" not in data or "salary" not in data:
                    return self._respond(400, {"error": "Payload missing required parameters."})

                new_employee = {
                    "id": next_id,
                    "name": data["name"],
                    "department": data["department"],
                    "salary": float(data["salary"])
                }
                
                EMPLOYEE_DB[next_id] = new_employee
                next_id += 1
                return self._respond(201, new_employee) # 201 Created Status Code
                
            except Exception as e:
                return self._respond(400, {"error": f"Malformed payload JSON: {str(e)}"})

        return self._respond(404, {"error": "Endpoint mapping not found."})

    # ==========================================
    # 3. UPDATE OPERATIONS (PUT)
    # ==========================================
    def do_PUT(self):
        path = urlparse(self.path).path

        if path.startswith("/api/v1/employees/"):
            try:
                emp_id = int(path.split("/")[-1])
                if emp_id not in EMPLOYEE_DB:
                    return self._respond(404, {"error": f"Employee with ID {emp_id} does not exist."})

                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                # Complete Resource Replacement Manipulation
                EMPLOYEE_DB[emp_id]["name"] = data.get("name", EMPLOYEE_DB[emp_id]["name"])
                EMPLOYEE_DB[emp_id]["department"] = data.get("department", EMPLOYEE_DB[emp_id]["department"])
                EMPLOYEE_DB[emp_id]["salary"] = float(data.get("salary", EMPLOYEE_DB[emp_id]["salary"]))

                return self._respond(200, EMPLOYEE_DB[emp_id])
            except Exception as e:
                return self._respond(400, {"error": str(e)})

        return self._respond(404, {"error": "Endpoint mapping not found."})

    # ==========================================
    # 4. DELETE OPERATIONS (DELETE)
    # ==========================================
    def do_DELETE(self):
        path = urlparse(self.path).path

        if path.startswith("/api/v1/employees/"):
            try:
                emp_id = int(path.split("/")[-1])
                if emp_id in EMPLOYEE_DB:
                    deleted_resource = EMPLOYEE_DB.pop(emp_id)
                    return self._respond(200, {"message": "Resource successfully expunged.", "deleted": deleted_resource})
                return self._respond(404, {"error": f"Employee ID {emp_id} not found."})
            except ValueError:
                return self._respond(400, {"error": "Invalid Path Parameter structure."})

        return self._respond(404, {"error": "Endpoint mapping not found."})

# Initialize and lock the server on port 8000
def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RESTAPIHandler)
    print("🚀 Enterprise Mock HTTP Server running natively on http://localhost:8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()