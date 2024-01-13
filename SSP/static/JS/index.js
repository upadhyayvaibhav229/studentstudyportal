document.addEventListener('DOMContentLoaded', function () {
    const themeButton = document.getElementById('theme-button');
    const body = document.body;

    // Check the current theme on page load
    if (localStorage.getItem('theme') === 'dark') {
      body.classList.add('dark-theme');
    }

    // Toggle the theme on button click
    themeButton.addEventListener('click', function () {
      body.classList.toggle('dark-theme');

      // Save the current theme in localStorage
      const currentTheme = body.classList.contains('dark-theme') ? 'dark' : 'light';
      localStorage.setItem('theme', currentTheme);
    });
  });