Health Info Connect: A Basic Health Information System

Overview:
Health Info Connect is a basic health information system designed to manage client data and program enrollments. 

This system allows healthcare providers to:

           Create and manage health programs (e.g., TB, Malaria, HIV).Register new clients.
           
           Enroll clients in health programs.
           
           Search for clients.
           
           View client profiles, including program enrollments.
           
           Expose client profiles via an API.
           
This project was developed as a demonstration of software development skills, emphasizing clean code, clear documentation, 
and a practical approach to addressing the given challenge.


Features:

             Client Management:Register new clients with essential information (name, date of birth, contact information). Unique client identifiers are automatically generated. 
             
             Program Management:Define and manage health programs (e.g., TB, Malaria, HIV).
             
             Enrollment Management:Enroll clients in one or more health programs.View a client's program enrollments.
             
             Client Search:Search for clients by ID or name.Client Profile:View a client's detailed profile, including their personal information and enrolled programs.
             
             API (Simulated):Exposes client profiles via a simulated API (Python functions), allowing other systems to retrieve this information.
             
             Data Storage:Uses in-memory storage (Python dictionaries and lists).
             
             User Interface:Provides a simple and intuitive user interface using HTML.Styled using CSS.Interactive elements implemented with Javascript.
             
             Technical Details: Frontend: HTML, CSS, JavaScript
             
             Backend (Simulated): PythonAPI (Simulated): Python functions
             
             Data Storage: In-memory (Python dictionaries and lists)

             
Setup and Installation: 

             Clone the repository:git clone https://github.com/sandy56-hash/Health-Info-Task.git
             
             cd Health-Info-Task
             
             Open index.html in your web browser: The index.html file provides the front-end user interface.Run the Python API (Optional):python health_info.py
             
*Note: Running the python script is only required to test the simulated API.



Design Choices and Implementation :

               Code Organization: The project is structured to separate the frontend (HTML, CSS, JavaScript) from the backend (Python).
               
               Frontend:HTML provides the structure of the web application.CSS is used for styling and layout.
               
               JavaScript adds interactivity to the user interface.
               
               Backend (Simulated):Python functions simulate API endpoints.Data is stored in memory using dictionaries and lists.
               
               API (Simulated):Python functions are used to represent API endpoints for retrieving client data.
               Error Handling: The Python code includes basic error handling and input validation.
               Data Storage: For simplicity, data is stored in memory. In a real-world application, a database would be used.

               
How to Use:
        Register a Client: Use the "Client Management" section to register a new client by providing their details.
        
        Enroll a Client in a Program: Use the "Client Enrollment in Health Programs" section to enroll a client in a program.
        
        Search for a Client: Use the "Search Client Records" section to search for a client by ID or name.
        
        View Client Profile: Use the "View Client Profile" section to view a client's profile and their enrolled programs.
        
        API Usage (Simulated)The health_info.py script simulates API endpoints. 

        
Here are the available functions:

register_client(name, dob, contact_info): Registers a new client.

enroll_client_in_program(client_id, program): Enrolls a client in a program.

search_clients(search_term): Searches for clients.

get_client_profile(client_id): Retrieves a client's profile.

Test Cases - The health_info.py script includes a series of test cases in the if __name__ == "__main__": block to demonstrate the functionality of the simulated API.

These tests cover: Client registration (including duplicate registration and invalid date format)

Client enrollment (including invalid program and duplicate enrollment)

Client search

Viewing client profiles


Future Enhancements:

Implement a full-fledged backend using a web framework (e.g., Flask). Integrate with a database (e.g., PostgreSQL).

Implement user authentication and authorization. Add more comprehensive error handling.

Implement a more robust front-end. Add unit tests. Deploy the application.
