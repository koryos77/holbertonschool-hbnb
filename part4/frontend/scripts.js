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
          document.cookie = `token=${data.access_token}; path=/; max-age=7200`; // Expires in 2 hours
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

  // Function to get the cookie by its name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // Function to get the place ID from URL
  function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
  }

  // Check authentication and manage connection link or place details
  function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();
    // Manage authentication for login link display
    if (loginLink) {
      if (!token) {
        loginLink.style.display = 'block'; // Display if no token
      } else {
        loginLink.style.display = 'none'; // Hide if token
        fetchPlaces(token);
      }
    }
    // Manage authentication for review section display
    if (addReviewSection) {
      if (!token) {
        addReviewSection.style.display = 'none';
      } else {
        addReviewSection.style.display = 'block';
      }
    }
    // if placeId load details
    if (placeId) {
      fetchPlaceDetails(token, placeId);
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
        console.error('Error during loading places:', response.status, await response.text());
      }
    } catch (error) {
      console.error('Network Error:', error.message);
    }
  }

  // Display places on the page
  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';
  
    places.forEach(place => {
      const placeElement = document.createElement('div');
      placeElement.className = 'place-cards';
      placeElement.dataset.price = place.price;
      const imagePath = getImagePathFromTitle(place.title);
  
      placeElement.innerHTML = `
        <img src="${imagePath}" alt="${place.title}" class="place-image">
        <div class="place-info">
          <h2>${place.title}</h2>
          <p>${place.description}</p>
          <p>Latitude: ${place.latitude}</p>
          <p>Longitude: ${place.longitude}</p>
          <p>Price per night: $${place.price}</p>
          <a class="details-button" href="place.html?id=${place.id}">View Details</a>
        </div>
      `;
      placesList.appendChild(placeElement);
    });
  
    filterPlaces();
  }

  // Function to generate the path for the place image based on its title
  function getImagePathFromTitle(title) {
    const imageMap = {
      'Beach House': 'places_photos/beach_house.jpg',
      'Forest Cabin': 'places_photos/forest_cabin.jpg',
      'Mountain Cabin': 'places_photos/mountain_cabin.jpg',
    };
    return imageMap[title] || 'places_photos/default.jpg'; // Default image if title doesn't match
  }

  // Fetch place details from API
  async function fetchPlaceDetails(token, placeId) {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    try {
      const response = await fetch(`http://127.0.0.1:5501/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: headers
      });
      if (!response.ok) {
        throw new Error('Failed to fetch place details');
      }
      const place = await response.json();
      displayPlaceDetails(place);
    } catch (error) {
      console.error('Error fetching place details:', error);
      const placeDetails = document.getElementById('place-details');
      if (placeDetails) {
        placeDetails.innerHTML = '<p>Oops something went wrong. Error while loading details.</p>';
      }
    }
  }

  // Display the details of a place including its image and reviews
  function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const imagePath = getImagePathFromTitle(place.title);

    placeDetails.innerHTML = `
      <div id="place-name">
        <h1>${place.title}</h1>
      </div>
      <div id="place-image">
        <img src="${imagePath}" alt="${place.title}" class="place-image">
      </div>
      <div id="place-description">
        <h4>Host: ${place.owner_id}</h4>
        <h4>Price per night: $${place.price}</h4>
        <h4>Description: ${place.description}</h4>
        <h4>Latitude: ${place.latitude}</h4>
        <h4>Longitude: ${place.longitude}</h4>
        <h4>${place.location}</h4>
        <h4>Amenities: ${place.amenities || 'No amenity in this place.'}</h4>
      </div>
    `;

    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;
    reviewsSection.innerHTML = '<h3>Reviews</h3>';
    if (place.reviews && place.reviews.length > 0) {
      const reviewsList = document.createElement('div');
      reviewsList.className = 'review-cards';
      place.reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.innerHTML = `
          <h4>User ID: ${review.user_id}</h4>
          <p>${review.text}</p>
        `;
        reviewsList.appendChild(reviewElement);
      });
      reviewsSection.appendChild(reviewsList);
    } else {
      reviewsSection.innerHTML += '<p>No review for the moment.</p>';
    }
  }

  // Filtering places by price
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', filterPlaces);
  }

  function filterPlaces() {
    const selectedPrice = document.getElementById('price-filter')?.value;
    if (!selectedPrice) return; // Exit if filter doesn't exist
    const placeItems = document.querySelectorAll('.place-cards');
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
