// RANSOM SYNTAX - small UI helpers
document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 6 seconds
  document.querySelectorAll('.alert').forEach(function (alertEl) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 6000);
  });

  // Smooth scroll for in-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
