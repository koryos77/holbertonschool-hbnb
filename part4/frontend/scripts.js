document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  // Prevent reload of webpage with preventDefault()
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Handle submit data
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      // try ... catch block to handle network errors
      try {
        const response = await fetch('http://127.0.0.1:5501/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password }),
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/; max-age=7200`; //Expires in 2 hours
          window.location.href = 'index.html';
        } else {
          const errorData = await response.json();
          alert('Connection failed : ' + (errorData.message || response.statusText));
        }
      } catch (error) {
        alert('A network error has occurred : ' + error.message);
      }
    });
  }

  // Function to get the cookie by his name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // Check authentication and manage connection link
  function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
      if (loginLink) loginLink.style.display = 'block'; // display if no token
    } else {
      if (loginLink) loginLink.style.display = 'none'; // Hide if token
      fetchPlaces(token);
    }
  }

  // Fetch places from API
  async function fetchPlaces(token) {
    try {
      const response = await fetch('http://127.0.0.1:5501/api/v1/places/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const places = await response.json();
        console.log('Places fetched successfully: ', places);
        displayPlaces(places);
      } else {
        console.error('Error during loading places:', response.status, await response.text())
      }
    } catch (error) {
      console.error('Network Error:', error.message)
    }
  }

  // Display places on the page
  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return; // Leave if element doesn't exist

    placesList.innerHTML = ''; // Empty actual content

    places.forEach(place => {
      const placeElement = document.createElement('div');
      placeElement.className = 'place-item'; // for css (??)
      placeElement.dataset.price = place.price; // stock price for filtering
      placeElement.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.description}</p>
        <p>Latitude: ${place.latitude}</p>
        <p>Longitude: ${place.longitude}</p>
        <p>Price per night: $${place.price}</p>
        <a class="details-button" href="place.html"><button class="details-button">View Details</button></a>
      `;
      placesList.appendChild(placeElement);
    });

    filterPlaces(); // Apply initial filter
  }

  // Filtering places by price
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', filterPlaces);
  }

  function filterPlaces() {
    const selectedPrice = document.getElementById('price-filter')?.value;
    if (!selectedPrice) return; // Exit if filter doesn't exist

    const placeItems = document.querySelectorAll('.place-item');

    placeItems.forEach(item => {
      const price = parseFloat(item.dataset.price);
      if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
        item.style.display = 'block'; // Display if selected
      } else {
        item.style.display = 'none'; // Hide if not in price selected
      }
    });
  }

  // Initialize page
  checkAuthentication();
});
