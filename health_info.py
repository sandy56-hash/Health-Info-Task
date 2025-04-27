import datetime

# Store client data.  Using a dictionary for simplicity,
# but in a real application, this would be a database.
clients = {}

# Store enrollment data.
enrollments = []

def generate_client_id():
    """
    Generates a unique client ID.  For simplicity, this uses a counter,
    but in a real application, you'd want a more robust method
    (e.g., UUIDs) to avoid collisions.
    """
    global client_id_counter
    client_id_counter += 1
    return f"CLIENT-{client_id_counter:04d}"  # Ensure 4 digits with leading zeros

client_id_counter = 0 # Initialize counter

def register_client(name, dob, contact_info):
    """
    Registers a new client.

    Args:
        name (str): The client's full name.
        dob (str): The client's date of birth (YYYY-MM-DD).
        contact_info (str): The client's contact information.

    Returns:
        dict: The newly registered client's data, including the generated ID.
              Returns None if there is an error.
    """
    try:
        # Basic input validation
        if not name or not dob or not contact_info:
            print("Error: Name, date of birth, and contact information are required.")
            return None

        datetime.datetime.strptime(dob, "%Y-%m-%d")  # Check DOB format

        client_id = generate_client_id()
        client = {
            "client_id": client_id,
            "name": name,
            "dob": dob,
            "contact_info": contact_info,
        }
        clients[client_id] = client
        print(f"Client registered successfully: {client}")
        return client
    except ValueError:
        print("Error: Invalid date format. Please use %Y-%m-%d.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



def enroll_client_in_program(client_id, program):
    """
    Enrolls an existing client in a health program.

    Args:
        client_id (str): The ID of the client to enroll.
        program (str): The name of the health program.

     Returns:
        dict:  Returns the enrollment data if successful, None otherwise
    """
    if not client_id or not program:
        print("Error: Client ID and program name are required.")
        return None

    if client_id not in clients:
        print(f"Error: Client with ID {client_id} not found.")
        return None

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
        print(f"Error: Invalid program name: {program}")
        return None

    # Check if already enrolled (optional, depending on requirements)
    for enrollment in enrollments:
        if enrollment["client_id"] == client_id and enrollment["program"] == program:
            print(f"Client {client_id} is already enrolled in {program}.")
            return None

    enrollment_data = {
        "client_id": client_id,
        "program": program,
        "enrollment_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    enrollments.append(enrollment_data)
    print(f"Client {client_id} enrolled in {program} successfully.")
    return enrollment_data



def search_clients(search_term):
    """
    Searches for clients by ID or name.

    Args:
        search_term (str): The ID or name to search for.

    Returns:
        list: A list of matching client records.  Empty list if no matches.
    """
    if not search_term:
        print("Error: Search term is required.")
        return []

    results = []
    for client_id, client in clients.items():
        if search_term.lower() in client["client_id"].lower() or search_term.lower() in client["name"].lower():
            results.append(client)
    print(f"Search results for '{search_term}': {results}")
    return results



def get_client_profile(client_id):
    """
    Retrieves a client's profile by their ID.

    Args:
        client_id (str): The ID of the client.

    Returns:
        dict: The client's profile information, or None if not found.
    """
    if not client_id:
        print("Error: Client ID is required.")
        return None

    if client_id not in clients:
        print(f"Error: Client with ID {client_id} not found.")
        return None

    print(f"Client profile for {client_id}: {clients[client_id]}")
    return clients[client_id]

def get_enrollments_by_client(client_id):
    """
    Retrieves all program enrollments for a given client ID.

    Args:
        client_id (str): The ID of the client.

    Returns:
       list: A list of enrollment records for the client.
    """
    if not client_id:
        print("Error: Client ID is required.")
        return []
    client_enrollments = [e for e in enrollments if e['client_id'] == client_id]
    return client_enrollments

def display_all_clients():
    """
    Displays all registered clients.  For debugging.
    """
    if not clients:
        print("No clients registered.")
        return
    print("All Clients:")
    for client_id, client in clients.items():
        print(f"  {client_id}: {client}")

def display_all_enrollments():
    """
    Displays all enrollments. For debugging.
    """
    if not enrollments:
        print("No enrollments.")
        return
    print("All Enrollments:")
    for enrollment in enrollments:
        print(f"  {enrollment}")

if __name__ == "__main__":
    #  Run a simple test scenario
    print("\n")
    print("Starting Health Info Connect API Test...")

    # Register some clients
    client1 = register_client("Alice Smith", "1990-05-15", "555-1234")
    client2 = register_client("Bob Johnson", "1985-10-22", "555-5678")
    client3 = register_client("Alice Smith", "1990-05-15", "555-1234") #duplicate
    client4 = register_client("Bob Johnson", "1985-10-22", "555-5678")
    client5 = register_client("Charlie Brown", "2001-03-01", "555-9012")
    client6 = register_client("Diana Miller", "1998-07-10", "555-2345")

    #check invalid date
    client_invalid_date = register_client("Eve Green", "2023-14-01", "555-2345")

    # Enroll clients in programs
    enrollment1 = enroll_client_in_program("CLIENT-0001", "TB Program")
    enrollment2 = enroll_client_in_program("CLIENT-0002", "Malaria Program")
    enrollment3 = enroll_client_in_program("CLIENT-0001", "HIV Program")
    enrollment4 = enroll_client_in_program("CLIENT-0003", "Invalid Program") # Invalid program
    enrollment5 = enroll_client_in_program("CLIENT-0005", "Nutrition Counseling Program")
    enrollment6 = enroll_client_in_program("CLIENT-0005", "Nutrition Counseling Program") #duplicate enrollment

    #check client does not exist
    enrollment7 = enroll_client_in_program("CLIENT-0010", "Nutrition Counseling Program")

    # Search for clients
    search_results1 = search_clients("Alice")
    search_results2 = search_clients("Smith")
    search_results3 = search_clients("CLIENT-0002")
    search_results4 = search_clients("xyz")  # No results

    # View client profiles
    profile1 = get_client_profile("CLIENT-0001")
    profile2 = get_client_profile("CLIENT-0002")
    profile3 = get_client_profile("CLIENT-0010")  # Client not found

    # Get enrollments by client
    enrollments_client1 = get_enrollments_by_client("CLIENT-0001")
    enrollments_client2 = get_enrollments_by_client("CLIENT-0010") #client not found

    # Display all data (for demonstration)
    display_all_clients()
    display_all_enrollments()

    print("\n")
    print("End of Test.")
