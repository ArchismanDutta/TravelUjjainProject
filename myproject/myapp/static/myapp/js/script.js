

  // Smooth scroll for anchor links like #packages
  document.querySelectorAll('a.nav-link[href^="#"]').forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  const userPanel = document.getElementById('userSidePanel');
  const toggleBtn = document.getElementById('userPanelToggle');
  const closeBtn = document.getElementById('closeSidePanel');

  function togglePanel() {
    userPanel.style.display = (userPanel.style.display === 'block') ? 'none' : 'block';
  }

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent body click from triggering immediately
    togglePanel();
  });

  closeBtn.addEventListener('click', () => {
    userPanel.style.display = 'none';
  });

  // Hide panel if clicked outside
  document.addEventListener('click', (e) => {
    if (userPanel.style.display === 'block' && !userPanel.contains(e.target) && e.target !== toggleBtn) {
      userPanel.style.display = 'none';
    }
  });
