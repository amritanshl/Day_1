import os
from flask import Flask, render_template_string
from jinja2 import Environment, select_autoescape

app = Flask(__name__)

# Mock enterprise database record containing a malicious XSS payload injected by an attacker
DB_MOCK_ATTACK_COMMENT = """
<script>
    console.warn("[EXPLOIT ALIVE] Capturing Document Cookie Data...");
    alert("XSS Vulnerability Executed! Session hijacked.");
</script>
"""

@app.route("/")
def home_dashboard():
    # Simple, safe landing navigation page
    return """
    <h1>Cybersecurity Lab: XSS Sandbox</h1>
    <p>Select an architectural path to evaluate:</p>
    <ul>
        <li><a href="/vulnerable"><b>/vulnerable</b></a> - Raw Rendering (High Risk)</li>
        <li><a href="/secure"><b>/secure</b></a> - Auto-Escaped Rendering (Production Ready)</li>
    </ul>
    """


@app.route("/vulnerable")
def vulnerable_endpoint():
    """
    DANGEROUS: Renders data without auto-escaping, allowing the browser 
    to interpret user data as executable JavaScript code.
    """
    print("\n[ALERT] Serving Vulnerable Pipeline Route...")
    
    # We explicitly turn off auto-escaping to simulate a vulnerable template configuration
    vulnerable_template = """
    <html>
    <head><title>Vulnerable Portal</title></head>
    <body>
        <h1>Corporate Feed (Vulnerable)</h1>
        <p>Latest Comment from Database:</p>
        <div style='border: 1px solid red; padding: 10px;'>
            """ + DB_MOCK_ATTACK_COMMENT + """
        </div>
    </body>
    </html>
    """
    return render_template_string(vulnerable_template)


@app.route("/secure")
def secure_endpoint():
    """
    SECURE: Uses Jinja2's native context-aware Auto-Escaping engine 
    to convert script tags into harmless literal HTML entities.
    """
    print("\n[SECURITY] Serving Secure Auto-Escaped Route...")
    
    # Standard Jinja2 template layout string
    secure_template = """
    <html>
    <head><title>Secure Portal</title></head>
    <body>
        <h1>Corporate Feed (Secure)</h1>
        <p>Latest Comment from Database:</p>
        <div style='border: 1px solid green; padding: 10px;'>
            {{ user_comment }}
        </div>
    </body>
    </html>
    """
    
    # Passing the variable cleanly to the template context model engine
    return render_template_string(secure_template, user_comment=DB_MOCK_ATTACK_COMMENT)


# ==========================================
# MAIN EXECUTION CORE
# ==========================================
if __name__ == "__main__":
    print("=== Launching Secure Coding Local Server ===")
    print("Open your web browser and navigate to: http://127.0.0.1:5000")
    
    # Start local server loop
    app.run(debug=True, port=5000)