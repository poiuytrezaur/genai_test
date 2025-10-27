// Weather page handler
document.addEventListener('DOMContentLoaded', function() {
    const messageDiv = document.getElementById('message');
    const getWeatherBtn = document.getElementById('getWeatherBtn');
    const getCurrentLocationBtn = document.getElementById('getCurrentLocationBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const weatherDisplay = document.getElementById('weatherDisplay');
    const locationButtons = document.querySelectorAll('.btn-location');

    // Check authentication status
    checkAuth();

    // Get weather button click
    getWeatherBtn.addEventListener('click', function() {
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);

        if (isNaN(latitude) || isNaN(longitude)) {
            showMessage('Please enter valid coordinates', 'error');
            return;
        }

        fetchWeather(latitude, longitude);
    });

    // Get current location button click
    getCurrentLocationBtn.addEventListener('click', function() {
        if (navigator.geolocation) {
            getCurrentLocationBtn.textContent = 'Getting location...';
            getCurrentLocationBtn.disabled = true;

            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    document.getElementById('latitude').value = latitude.toFixed(4);
                    document.getElementById('longitude').value = longitude.toFixed(4);

                    fetchWeather(latitude, longitude);

                    getCurrentLocationBtn.textContent = 'Use Current Location';
                    getCurrentLocationBtn.disabled = false;
                },
                function(error) {
                    showMessage('Unable to get your location. Please enter manually.', 'error');
                    getCurrentLocationBtn.textContent = 'Use Current Location';
                    getCurrentLocationBtn.disabled = false;
                }
            );
        } else {
            showMessage('Geolocation is not supported by your browser', 'error');
        }
    });

    // Popular location buttons
    locationButtons.forEach(button => {
        button.addEventListener('click', function() {
            const lat = parseFloat(this.dataset.lat);
            const lon = parseFloat(this.dataset.lon);

            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lon;

            fetchWeather(lat, lon);
        });
    });

    // Logout button
    logoutBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
            });

            if (response.ok) {
                window.location.href = '/login';
            }
        } catch (error) {
            showMessage('Logout failed', 'error');
        }
    });

    async function checkAuth() {
        try {
            const response = await fetch('/api/auth/me');
            const data = await response.json();

            if (response.ok) {
                document.getElementById('userInfo').textContent = `Hello, ${data.user.username}`;
                logoutBtn.style.display = 'inline-block';
            } else {
                window.location.href = '/login';
            }
        } catch (error) {
            window.location.href = '/login';
        }
    }

    async function fetchWeather(latitude, longitude) {
        try {
            const response = await fetch(
                `/api/weather/current?latitude=${latitude}&longitude=${longitude}`
            );

            const data = await response.json();

            if (response.ok) {
                displayWeather(data.weather);
                showMessage('', 'success');
            } else {
                if (response.status === 401) {
                    window.location.href = '/login';
                } else {
                    showMessage(data.error || 'Failed to fetch weather data', 'error');
                }
            }
        } catch (error) {
            showMessage('Network error. Please try again.', 'error');
        }
    }

    function displayWeather(weather) {
        document.getElementById('weatherLocation').textContent = 
            `${weather.latitude.toFixed(2)}°, ${weather.longitude.toFixed(2)}°`;
        document.getElementById('temperature').textContent = weather.temperature;
        document.getElementById('weatherDescription').textContent = weather.description;
        document.getElementById('windSpeed').textContent = weather.windspeed;
        document.getElementById('windDirection').textContent = weather.winddirection;
        document.getElementById('weatherTime').textContent = new Date(weather.time).toLocaleString();

        weatherDisplay.style.display = 'block';
    }

    function showMessage(message, type) {
        if (message) {
            messageDiv.textContent = message;
            messageDiv.className = `message ${type}`;
        } else {
            messageDiv.className = 'message';
            messageDiv.textContent = '';
        }
    }
});
