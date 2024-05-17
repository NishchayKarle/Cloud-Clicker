var a = document.getElementById("loginBtn");
var b = document.getElementById("registerBtn");
var x = document.getElementById("login");
var y = document.getElementById("register");

function showLogin() {
    x.style.left = "4px";
    y.style.right = "-520px";
    a.className += " white-btn";
    b.className = "btn";
    x.style.opacity = 1;
    y.style.opacity = 0;

    logout();
}

function showRegister() {
    x.style.left = "-510px";
    y.style.right = "5px";
    a.className = "btn";
    b.className += " white-btn";
    x.style.opacity = 0;
    y.style.opacity = 1;
}

function showClicks() {
    window.location.href = '/clicks';
}

function clearSignIn() {
    document.getElementById('signin-message-valid').textContent = '';
    document.getElementById('signin-message-invalid').textContent = '';
}

function clearSignUp() {
    document.getElementById('signup-message-valid').textContent = '';
    document.getElementById('signup-message-invalid').textContent = '';
}

function signIn() {
    clearSignUp();

    const username = document.getElementById('signin-username').value;
    const password = document.getElementById('signin-password').value;

    document.getElementById('signin-username').value = '';
    document.getElementById('signin-password').value = '';

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
                console.log("Logged in");
                let token = result.body.access_token;
                sessionStorage.setItem('token', token);
                sessionStorage.setItem('username', username);

                document.getElementById('signin-message-valid').textContent = 'Logging in...';
                setTimeout(() => {
                    document.getElementById('signin-message-valid').textContent = '';

                    // Move to the clicker page
                    showClicks();
                }, 300);
            } else {
                document.getElementById('signin-message-invalid').textContent = result.body.msg;
            }
        })
        .catch(error => console.error('Error:', error));
}

function signUp() {
    clearSignIn();

    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

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
                document.getElementById('signup-username').value = '';
                document.getElementById('signup-password').value = '';

                // Wait for 1 second before showing the login form
                setTimeout(() => {
                    showLogin();
                    // clear message
                    document.getElementById('signup-message-valid').textContent = '';
                }, 1000);
            } else {
                document.getElementById('signup-message-invalid').textContent = result.body.msg;
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    // On the clicker page
    if (window.location.pathname === '/clicks') {
        const username = sessionStorage.getItem('username');
        const token = sessionStorage.getItem('token');
        const userNameElement = document.getElementById('user-name');
        const clickButton = document.getElementById('clicker');
        const userClicksElement = document.getElementById('user-clicks').parentElement;
        const logoutButton = document.querySelector('.nav-button button');

        if (username && token) {
            userNameElement.textContent = `Welcome, ${username}`;
            clickButton.parentElement.style.display = 'block';
            userClicksElement.style.display = 'block';
            logoutButton.style.display = 'block';
            getClickCounts(token);
            getUserClickCounts(token);

            // Periodically update the click counts
            setInterval(() => {
                getClickCounts(token);
                getUserClickCounts(token);
            }, 100);
        } else {
            userNameElement.textContent = 'Welcome, Guest';
            getClickCounts();

            // Periodically update the click counts
            setInterval(() => {
                getClickCounts();
            }, 100);
        }
    }
});

function getClickCounts(token) {
    fetch('/api/clicks', {
        method: 'GET',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-clicks').textContent = data.count;
        });
}

function getUserClickCounts(token) {
    fetch('/api/user_clicks', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('user-clicks').textContent = data.user_clicks;
        });
}

function incrementClickUser() {
    const token = sessionStorage.getItem('token');
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

function logout() {
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('token');
    window.location.href = '/';
}
