from flask import Flask, jsonify, request, render_template
import datetime
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, or specify origins if needed

# Store client data.  Using a dictionary for simplicity,
# but in a real application, this would be a database.
clients = {}

# Store enrollment data.
enrollments = []

client_id_counter = 0  # Initialize counter outside the function

def generate_client_id():
    """
    Generates a unique client ID.  For simplicity, this uses a counter,
    but in a real application, you'd want a more robust method
    (e.g., UUIDs) to avoid collisions.
    """
    global client_id_counter
    client_id_counter += 1
    return f"CLIENT-{client_id_counter:04d}"  # Ensure 4 digits with leading zeros



def register_client(name, dob, contact_info):
    """
    Registers a new client.

    Args:
        name (str): The client's full name.
        dob (str): The client's date of birth (YYYY-MM-DD).
        contact_info (str): The client's contact information.

    Returns:
        dict: The newly registered client's data, including the generated ID.
        str:  Error message, None if no error.
    """
    try:
        # Basic input validation
        if not name or not dob or not contact_info:
            return None, "Name, date of birth, and contact information are required."

        datetime.datetime.strptime(dob, "%Y-%m-%d")  # Check DOB format

        client_id = generate_client_id()
        client = {
            "id": client_id,  # Changed from "client_id" to "id" to match frontend
            "name": name,
            "dob": dob,
            "contact": contact_info, # Changed from "contact_info" to "contact"
        }
        clients[client_id] = client
        return client, None
    except ValueError:
        return None, "Invalid date format. Please use %Y-%m-%d."
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"



def enroll_client_in_program(client_id, program):
    """
    Enrolls an existing client in a health program.

    Args:
        client_id (str): The ID of the client to enroll.
        program (str): The name of the health program.

    Returns:
        dict: Returns the enrollment data if successful, None otherwise
        str: Error message, None if no error.
    """
    if not client_id or not program:
        return None, "Client ID and program name are required."

    if client_id not in clients:
        return None, f"Client with ID {client_id} not found."

    # Check for valid program (optional, but good practice)
    valid_programs = [
        "TB Program", "Malaria Program", "HIV Program", "Diabetes Management Program",
        "Hypertension Control Program", "Maternal Health Program", "Child Wellness Program",
        "Asthma Care Program", "Cancer Screening Program", "Mental Health Support Program",
        "Substance Abuse Program", "Nutrition Counseling Program", "Immunization Program",
        "Eye Care Program", "Dental Health Program", "Cardiovascular Health Program",
        "Respiratory Health Program", "Geriatric Care Program", "Pediatric Care Program",
        "Emergency Care Training"
    ]
    if program not in valid_programs:
        return None, f"Invalid program name: {program}"

    # Check if already enrolled
    for enrollment in enrollments:
        if enrollment["clientId"] == client_id and enrollment["program"] == program: # changed client_id
            return None, f"Client {client_id} is already enrolled in {program}."

    enrollment_data = {
        "clientId": client_id, # changed client_id
        "program": program,
        "enrollmentDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # changed enrollment_date
    }
    enrollments.append(enrollment_data)
    return enrollment_data, None



def search_clients(search_term):
    """
    Searches for clients by ID or name.

    Args:
        search_term (str): The ID or name to search for.

    Returns:
        list: A list of matching client records. Empty list if no matches.
        str: Error message, None if no error.
    """
    if not search_term:
        return [], "Search term is required."

    results = []
    for client_id, client in clients.items():
        if search_term.lower() in client["id"].lower() or search_term.lower() in client["name"].lower(): # changed client_id
            results.append(client)
    return results, None



def get_client_profile(client_id):
    """
    Retrieves a client's profile by their ID.

    Args:
        client_id (str): The ID of the client.

    Returns:
        dict: The client's profile information, or None if not found.
        str: Error message, None if no error.
    """
    if not client_id:
        return None, "Client ID is required."

    if client_id not in clients:
        return None, f"Client with ID {client_id} not found."

    return clients[client_id], None



def get_enrollments_by_client(client_id):
    """
    Retrieves all program enrollments for a given client ID.

    Args:
        client_id (str): The ID of the client.

    Returns:
        list: A list of enrollment records for the client.
        str: Error message, None if no error.
    """
    if not client_id:
        return [], "Client ID is required."
    client_enrollments = [e for e in enrollments if e['clientId'] == client_id] # changed client_id
    return client_enrollments, None

# Flask routes to integrate with your HTML
@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html is in a folder named templates

@app.route('/api/clients', methods=['POST'])
def api_register_client():
    """
    API endpoint to register a new client.
    Handles POST requests with client data.
    Returns JSON response.
    """
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')
    contact_info = data.get('contact') # Changed from contact_info
    client, error = register_client(name, dob, contact_info)
    if error:
        return jsonify({'error': error}), 400  # Use 400 for bad request
    return jsonify({'message': 'Client registered successfully', 'client': client}), 201 # Added client


@app.route('/api/enrollments', methods=['POST'])
def api_enroll_client():
    """
    API endpoint to enroll a client in a program.
    Handles POST requests with client ID and program data.
    Returns JSON response.
    """
    data = request.get_json()
    client_id = data.get('clientId') # Changed from client_id
    program = data.get('program')
    enrollment, error = enroll_client_in_program(client_id, program)
    if error:
        return jsonify({'error': error}), 400  # Use 400 for bad request
    return jsonify({'message': 'Client enrolled successfully', 'enrollment': enrollment}), 201 # Added enrollment


@app.route('/api/clients/search', methods=['GET'])
def api_search_clients():
    """
    API endpoint to search for clients.
    Handles GET requests with a search term.
    Returns JSON response.
    """
    search_term = request.args.get('term')  # Get the 'term' from the query string
    results, error = search_clients(search_term)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'results': results}), 200  # Changed 'result' to 'results'


@app.route('/api/clients/<client_id>', methods=['GET'])
def api_get_client_profile(client_id):
    """
    API endpoint to get a client's profile.
    Handles GET requests with a client ID.
    Returns JSON response.
    """
    profile, error = get_client_profile(client_id)
    if error:
        return jsonify({'error': error}), 404  # Use 404 for not found
    enrollments, _ = get_enrollments_by_client(client_id) # Get enrollments for the client
    return jsonify({'client': profile, 'enrollments': enrollments}), 200 # Return both


@app.route('/api/client_enrollments/<client_id>', methods=['GET']) # Not used in current js
def api_get_enrollments_by_client(client_id):
    """
    API endpoint to get a client's enrollments.
    Handles GET requests with a client ID.
    Returns JSON response.
    """
    enrollments, error = get_enrollments_by_client(client_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'enrollments': enrollments}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    