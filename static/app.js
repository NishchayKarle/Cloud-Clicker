// Disable console.log in production
window.console.log = () => { };

var a = document.getElementById("loginBtn");
var b = document.getElementById("registerBtn");
var x = document.getElementById("login");
var y = document.getElementById("register");

/**
 * Show the login form
 * 
 * @returns {void}
 */
function showLogin() {
    x.style.left = "4px";
    y.style.right = "-520px";
    a.className += " white-btn";
    b.className = "btn";
    x.style.opacity = 1;
    y.style.opacity = 0;
}

/**
 * Show the register form
 * 
 * @returns {void}
 */
function showRegister() {
    x.style.left = "-510px";
    y.style.right = "5px";
    a.className = "btn";
    b.className += " white-btn";
    x.style.opacity = 0;
    y.style.opacity = 1;
}

/**
 * Show the clicks page
 * 
 * @returns {void}
 */
function showClicks() {
    window.location.href = '/clicks';
}

/**
 * Clear the sign in form
 * 
 * @returns {void}
 */
function clearSignIn() {
    document.getElementById('signin-message-valid').textContent = '';
    document.getElementById('signin-message-invalid').textContent = '';
}

/**
 * Clear the sign up form
 * 
 * @returns {void}
 */
function clearSignUp() {
    document.getElementById('signup-message-valid').textContent = '';
    document.getElementById('signup-message-invalid').textContent = '';
}

/**
 * Sign in the user
 *  
 * @returns {void}
 */
function signIn() {
    // Clear the sign up form messages, if any
    clearSignUp();

    // Get the username and password
    const username = document.getElementById('signin-username').value;
    const password = document.getElementById('signin-password').value;

    console.log('Sending API request to login user :', username)
    // Send login request to the server
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(result => {
            if (result.status === 200) {
                // Save the auth token and username in the session storage
                let token = result.body.access_token;
                sessionStorage.setItem('token', token);
                sessionStorage.setItem('username', username);

                document.getElementById('signin-message-valid').textContent = 'Logging in...';
                setTimeout(() => {
                    document.getElementById('signin-message-valid').textContent = '';

                    // Move to the clicker page
                    showClicks();
                }, 300);

                // Clear the sign in form on successful login
                document.getElementById('signin-username').value = '';
                document.getElementById('signin-password').value = '';
                console.log("Successfully logged in user : ", username);

            } else {
                // Show the error message
                document.getElementById('signin-message-invalid').textContent = result.body.msg;

                console.log('Failed to login user :', username);
            }
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Sign up the user
 * 
 *  @returns {void}
 */
function signUp() {
    clearSignIn();

    // Get the username and password
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    console.log('Sending API request to register user :', username);
    // Send the register request to the server
    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(result => {
            if (result.status === 201) {
                document.getElementById('signup-message-valid').textContent = 'User registered successfully. Please sign in.';
                // Clear the sign up form on successful registration
                document.getElementById('signup-username').value = '';
                document.getElementById('signup-password').value = '';

                console.log('Successfully registered user :', username);

                // Show the login form
                showLogin();

                // clear message
                document.getElementById('signup-message-valid').textContent = '';
            } else {
                // Show the error message
                document.getElementById('signup-message-invalid').textContent = result.body.msg;
                console.log('Failed to register user :', username);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Add event listener to the clicker button
// Periodically check for updates of the click counts
document.addEventListener('DOMContentLoaded', () => {
    // While on the clicker page
    if (window.location.pathname === '/clicks') {
        // Get the token and username from the session storage
        const token = sessionStorage.getItem('token');
        const username = sessionStorage.getItem('username');

        // Get the necessary elements
        const userNameElement = document.getElementById('user-name');
        const clickButton = document.getElementById('clicker');
        const userClicksElement = document.getElementById('user-clicks').parentElement;
        const loginMessage = document.getElementById('login-message');
        const logoutButton = document.querySelector('.nav-button button');

        if (username && token) {
            // Set the welcome message
            userNameElement.textContent = `Welcome, ${username}`;

            // User is logged in
            // Show the clicker button, user click counts and logout button
            clickButton.parentElement.style.display = 'block';
            userClicksElement.style.display = 'block';
            logoutButton.style.display = 'block';

            // get the click counts
            getClickCounts(token);

            // Periodically check and update the click counts
            setInterval(() => {
                getClickCounts(token);
            }, 100);
        } else {
            // User is not logged in
            userNameElement.textContent = 'Welcome, Guest';
            // Show the login message
            loginMessage.style.display = 'block';

            // Only show the total click counts
            getClickCounts();

            // Periodically update the total click counts
            setInterval(() => {
                getClickCounts();
            }, 100);

        }
    }
});

/**
 * Get the total click counts from the server
 * @param {string} token 
 * 
 * @returns {void}
 */
function getClickCounts(token = null) {
    // Make a GET request to the server to get the click counts
    fetch('/api/clicks', {
        method: 'GET',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-clicks').textContent = data.total_clicks;
            if (data.user_clicks !== undefined) {
                document.getElementById('user-clicks').parentElement.style.display = 'block';
                document.getElementById('user-clicks').textContent = data.user_clicks;
            }
        });
}

/**
 * Increment the user click counts
 * 
 * @returns {void}
 */
function incrementClickUser() {
    // Get the token from the session storage
    const token = sessionStorage.getItem('token');

    // Make a POST request to the server to increment the user click counts
    fetch('/api/clicks', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-clicks').textContent = data.total_clicks;
            document.getElementById('user-clicks').textContent = data.user_clicks;
        });
}

/**
 * Delete the tokens from the session storage
 * 
 * @returns {void}
 */
function deleteTokens() {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('username');
}

/**
 * Logout the user
 * 
 * @returns {void}
 */
function logout() {
    deleteTokens();
    window.location.href = '/';
}
