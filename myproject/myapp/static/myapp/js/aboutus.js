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
