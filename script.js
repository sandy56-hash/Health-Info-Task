document.addEventListener('DOMContentLoaded', () => {
    // --- Helper Functions ---

    /**
     * Displays a notification message to the user.
     * @param {string} message - The message to display.
     * @param {string} type - The type of notification ('success' or 'error').
     */
    function showNotification(message, type) {
        const messageBox = document.getElementById('message-box');
        messageBox.textContent = message;
        messageBox.className = `notification ${type}`;
        messageBox.classList.remove('hidden');

        setTimeout(() => {
            messageBox.classList.add('hidden');
            messageBox.className = 'notification hidden';
        }, 5000);
    }

    /**
     * Sends data to the backend API using the Fetch API.
     * @param {string} endpoint - The API endpoint URL.
     * @param {string} method - The HTTP method (e.g., 'POST', 'GET').
     * @param {object} data - The data to send (optional).
     * @returns {Promise<object>} - A promise that resolves with the response data, or rejects with an error.
     */
    async function sendRequest(endpoint, method, data = null) {
        const url = `http://localhost:5000/api/${endpoint}`; // Adjust the base URL if needed

        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: data ? JSON.stringify(data) : undefined
        };

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                // Handle HTTP errors (e.g., 400, 500)
                const errorData = await response.json(); // Attempt to get error message from server
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            return await response.json(); // Parse the JSON response
        } catch (error) {
            console.error('API request failed:', error);
            throw error; // Re-throw the error to be caught by the caller
        }
    }

    // --- Event Listeners ---

    // --- Client Management ---
    const registerClientForm = document.getElementById('register-client-form');
    if (registerClientForm) {
        registerClientForm.addEventListener('submit', async (event) => { // Make the callback async
            event.preventDefault();

            const clientId = document.getElementById('client-id').value.trim();
            const clientName = document.getElementById('client-name').value.trim();
            const clientDob = document.getElementById('client-dob').value;
            const clientContact = document.getElementById('client-contact').value.trim();

            if (!clientId || !clientName || !clientDob || !clientContact) {
                showNotification('Please fill in all fields.', 'error');
                return;
            }

            const newClient = {
                id: clientId,
                name: clientName,
                dob: clientDob,
                contact: clientContact,
            };

            try {
                const responseData = await sendRequest('clients', 'POST', newClient); // Await the response
                showNotification(responseData.message, 'success');
                registerClientForm.reset();
            } catch (error) {
                showNotification(error.message, 'error'); // Display the error message from the server
            }
        });
    }

    // --- Enrollment Management ---
    const enrollProgramForm = document.getElementById('enroll-program-form');
    if (enrollProgramForm) {
        enrollProgramForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const clientId = document.getElementById('enroll-client-id-program').value.trim();
            const selectedProgram = document.getElementById('selected-program').value;

            if (!clientId || !selectedProgram) {
                showNotification('Please fill in all fields.', 'error');
                return;
            }

            const enrollmentData = {
                clientId: clientId,
                program: selectedProgram,
            };

            try {
                const responseData = await sendRequest('enrollments', 'POST', enrollmentData);
                showNotification(responseData.message, 'success');
                enrollProgramForm.reset();
            } catch (error) {
                showNotification(error.message, 'error');
            }
        });
    }

    // --- Search Records ---
    const searchClientForm = document.getElementById('search-client-form');
    if (searchClientForm) {
        searchClientForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const searchTerm = document.getElementById('search-term').value.trim();

            if (!searchTerm) {
                showNotification('Please enter a search term.', 'error');
                return;
            }

            try {
                const responseData = await sendRequest(`clients/search?term=${searchTerm}`, 'GET'); // Pass searchTerm as a query parameter
                const searchResults = responseData.results;

                const searchResultsList = document.getElementById('search-results-list');
                const searchResultsContainer = document.getElementById('search-results');
                searchResultsList.innerHTML = '';

                if (searchResults.length === 0) {
                    searchResultsList.innerHTML = '<li>No matching clients found.</li>';
                } else {
                    searchResults.forEach(client => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<b>ID:</b> ${client.id}, <b>Name:</b> ${client.name}, <b>DOB:</b> ${client.dob}, <b>Contact:</b> ${client.contact}`;
                        searchResultsList.appendChild(listItem);
                    });
                }
                searchResultsContainer.classList.remove('hidden');
            } catch (error) {
                showNotification(error.message, 'error');
            }
        });
    }

    // --- View Client Profile ---
    const viewProfileForm = document.getElementById('view-profile-form');
    if (viewProfileForm) {
        viewProfileForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const clientIdToView = document.getElementById('profile-client-id').value.trim();

            if (!clientIdToView) {
                showNotification('Please enter a Client ID.', 'error');
                return;
            }

            try {
                const responseData = await sendRequest(`clients/${clientIdToView}`, 'GET'); // Get client by ID
                const client = responseData.client;
                const enrollments = responseData.enrollments;

                const profileDetailsDiv = document.getElementById('profile-details');
                const clientProfileContainer = document.getElementById('client-profile');
                profileDetailsDiv.innerHTML = '';

                if (!client) {
                    profileDetailsDiv.innerHTML = '<p>Client not found.</p>';
                } else {
                    profileDetailsDiv.innerHTML = `
                        <p><b>Client ID:</b> ${client.id}</p>
                        <p><b>Name:</b> ${client.name}</p>
                        <p><b>Date of Birth:</b> ${client.dob}</p>
                        <p><b>Contact Info:</b> ${client.contact}</p>
                    `;
                    if (enrollments && enrollments.length > 0) {
                        profileDetailsDiv.innerHTML += `<p><b>Enrolled Programs:</b></p><ul>`;
                        enrollments.forEach(enrollment => {
                            profileDetailsDiv.innerHTML += `<li>${enrollment.program} (Enrolled on: ${enrollment.enrollmentDate})</li>`;
                        });
                        profileDetailsDiv.innerHTML += `</ul>`;
                    } else {
                        profileDetailsDiv.innerHTML += `<p><b>Enrolled Programs:</b> No programs enrolled.</p>`;
                    }
                }
                clientProfileContainer.classList.remove('hidden');
            } catch (error) {
                showNotification(error.message, 'error');
            }
        });
    }

    // --- Page Load Effects ---  (These do not involve backend communication)
    document.body.addEventListener('mouseover', () => {
        document.body.style.backgroundColor = '#f0f8ff';
    });

    const modules = document.querySelectorAll('.module');
    modules.forEach(module => {
        module.addEventListener('click', () => {
            const lightColor = ['#e0f7fa', '#b0e0e6', '#87cefa'][Math.floor(Math.random() * 3)];
            module.style.backgroundColor = lightColor;
        });
    });

    const navLinks = document.querySelectorAll('.top-left-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});