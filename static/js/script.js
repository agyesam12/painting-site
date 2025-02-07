// Handle form submission
document
  .getElementById("booking-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {};

    formData.forEach((value, key) => {
      data[key] = value;
    });

    console.log("Form Submitted:", data);

    // Here you would send the form data to an email or API.
  });
