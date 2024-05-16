var a = document.getElementById("loginBtn");
var b = document.getElementById("registerBtn");
var x = document.getElementById("login");
var y = document.getElementById("register");

function login() {
    x.style.left = "4px";
    y.style.right = "-520px";
    a.className += " white-btn";
    b.className = "btn";
    x.style.opacity = 1;
    y.style.opacity = 0;
}

function register() {
    x.style.left = "-510px";
    y.style.right = "5px";
    a.className = "btn";
    b.className += " white-btn";
    x.style.opacity = 0;
    y.style.opacity = 1;
}

function getSignIn() {
    const username = document.getElementById('signin-username').value;
    const password = document.getElementById('signin-password').value;

    document.getElementById('signin-username').value = '';
    document.getElementById('signin-password').value = '';

    console.log('Login: ', username, password);
}

function getSignUp() {
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    document.getElementById('signup-username').value = '';
    document.getElementById('signup-password').value = '';

    console.log('Sign Up: ', username, password);
}


// let token = '';

// function showSignIn() {
//     document.getElementById('signup-form').style.display = 'none';
//     document.getElementById('signin-form').style.display = 'block';
// }

// function showSignUp() {
//     document.getElementById('signin-form').style.display = 'none';
//     document.getElementById('signup-form').style.display = 'block';
// }


// function signup() {
//     const username = document.getElementById('signup-username').value;
//     const password = document.getElementById('signup-password').value;

//     fetch('/api/register', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ username, password })
//     })
//         .then(response => response.json().then(data => ({ status: response.status, body: data })))
//         .then(result => {
//             if (result.status === 201) {
//                 document.getElementById('signup-message').textContent = 'User registered successfully. Please sign in.';
//                 showSignIn();
//             } else {
//                 document.getElementById('signup-message').textContent = result.body.msg;
//             }
//         })
//         .catch(error => console.error('Error:', error));
// }

// function signin() {
//     const username = document.getElementById('signin-username').value;
//     const password = document.getElementById('signin-password').value;

//     fetch('/api/login', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ username, password })
//     })
//         .then(response => response.json().then(data => ({ status: response.status, body: data })))
//         .then(result => {
//             if (result.status === 200) {
//                 token = result.body.access_token;
//                 document.getElementById('auth-forms').style.display = 'none';
//                 document.getElementById('clicker').style.display = 'block';
//                 document.getElementById('user-name').textContent = username;
//                 getClickCounts();
//             } else {
//                 document.getElementById('signin-message').textContent = result.body.msg;
//             }
//         })
//         .catch(error => console.error('Error:', error));
// }

// function getClickCounts() {
//     fetch('/api/clicks', {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     })
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById('total-clicks').textContent = data.count;
//         });

//     fetch('/api/user_clicks', {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     })
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById('user-clicks').textContent = data.user_clicks;
//         });
// }

// function incrementClick() {
//     fetch('/api/clicks', {
//         method: 'POST',
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     })
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById('total-clicks').textContent = data.total_clicks;
//             document.getElementById('user-clicks').textContent = data.user_clicks;
//         });
// }

// function logout() {
//     token = '';
//     document.getElementById('auth-forms').style.display = 'block';
//     document.getElementById('clicker').style.display = 'none';
//     document.getElementById('signin-username').value = '';
//     document.getElementById('signin-password').value = '';
//     document.getElementById('signin-message').textContent = '';
// }
