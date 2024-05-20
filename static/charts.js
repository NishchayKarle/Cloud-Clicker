function transformArray(arr) {
    const length = arr.length;

    // If the array length is less than 5, retain all elements
    if (length < 5) {
        return arr;
    }

    // If the array length is 5 or more, retain 5 elements that are evenly spaced
    const retainCount = 5;
    const retainIndices = [];

    // Calculate the step size to evenly space the retained indices
    const stepSize = Math.floor(length / retainCount);

    for (let i = 0; i < retainCount - 1; i++) {
        retainIndices.push(i * stepSize);
    }

    // Always retain the last element
    retainIndices.push(length - 1);

    // Create a new array with the same length filled with empty strings
    const result = new Array(length).fill('');

    // Retain original values at the specified indices
    retainIndices.forEach(index => {
        result[index] = arr[index];
    });

    return result;
}


// Dashboard obj
let dashboard = NaN;


function displayDashboard() {
    // Destroy the previous chart if it exists
    if (dashboard) {
        dashboard.destroy();
    }

    const ctx = document.getElementById('clickChart');
    const token = sessionStorage.getItem('token');
    const username = sessionStorage.getItem('username');
    const userNameElement = document.getElementById('user-name');

    if (token == null) {
        // User is not logged in
        userNameElement.textContent = 'Welcome, Guest';

        const logoutButton = document.querySelector('.nav-button button');
        logoutButton.textContent = 'Login';
    } else {
        userNameElement.textContent = `Welcome, ${username}`;
    }

    // Fetch the click counts from the server
    // Use the token for authentication
    // Update the chart with the new data

    fetch('/api/clicks/log', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // Set clicks per minute
            document.getElementById('clicksPerMinute').textContent = 'Overall clicks per min: ' + data.clicks_per_minute;

            // Extract the first elements into one array and the second elements into another array
            const firstElements = data.click_logs.map(item => item[0]);
            const secondElements = data.click_logs.map(item => item[1]);

            // X axis is the time intervals
            // Y axis is the total clicks over the last few intervals
            dashboard = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: transformArray(secondElements),
                    datasets: [{
                        label: 'Recent Clicks',
                        data: firstElements,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Clicks'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Central Time'
                            },
                        },
                    },
                }
            });
        })
        .catch(error =>
            console.error('Error:', error)
        );

}

function refreshDashboard() {
    // Fetch the latest data from the server when refresh button is clicked
    // Update the chart with the new data
    displayDashboard();
}

// Display the dashboard when the DOM is loaded
// Refresh the dashboard every 5 minutes
document.addEventListener('DOMContentLoaded', () => {
    displayDashboard();
    setInterval(displayDashboard, 1000 * 60 * 5);
    console.log('Dashboard refreshed!')
});
