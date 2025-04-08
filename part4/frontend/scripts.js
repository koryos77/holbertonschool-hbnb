/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

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
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          const errorData = await response.json()
          alert('Connection failed : ' + (errorData.message || response.statusText));
        }
      } catch (error) {
          alert('A network error has occured : ' + error.message);
      }
    });
  }
});
