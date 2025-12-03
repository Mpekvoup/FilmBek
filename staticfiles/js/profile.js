document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            // Show corresponding tab pane
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Watchlist filtering
    const statusSelect = document.getElementById('watchlist-status');
    const watchlistItems = document.querySelectorAll('.watchlist-item');

    if (statusSelect) {
        statusSelect.addEventListener('change', () => {
            const selectedStatus = statusSelect.value;

            watchlistItems.forEach(item => {
                if (selectedStatus === 'all' || item.dataset.status === selectedStatus) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Like button functionality
    const likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const commentId = btn.dataset.commentId;
            try {
                const response = await fetch(`/api/comments/${commentId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    btn.innerHTML = `❤ ${data.likes_count}`;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
}); 