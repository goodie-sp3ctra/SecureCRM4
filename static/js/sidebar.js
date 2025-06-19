document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('collapsed');
    document.getElementById('mainContent').classList.toggle('collapsed');

    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.classList.toggle('collapsed');
    });
});