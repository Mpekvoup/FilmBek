function toggleSubfilters(buttonElement) {
    const parentItem = buttonElement.closest('.filter-item');
    if (parentItem) {
        parentItem.classList.toggle('open');
    }
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}
const searchInput = document.querySelector('.search-input');
const suggestionsContainer = document.querySelector('.suggestions');

let timeout = null;

searchInput.addEventListener('input', function() {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    const query = searchInput.value;
    if (query.trim().length === 0) {
      suggestionsContainer.innerHTML = '';
      suggestionsContainer.style.display = 'none';
      return;
    }

    fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        suggestionsContainer.innerHTML = '';
        if (data.suggestions.length > 0) {
          suggestionsContainer.style.display = 'block';
        } else {
          suggestionsContainer.style.display = 'none';
        }
        data.suggestions.forEach(item => {
          const suggestionItem = document.createElement('div');
          suggestionItem.classList.add('suggestion-item');
          if (item.poster) {
            const img = document.createElement('img');
            img.src = item.poster;
            img.alt = item.title;
            img.style.width = '40px';
            img.style.height = '60px';
            img.style.objectFit = 'cover';
            img.style.marginRight = '10px';
            suggestionItem.appendChild(img);
          }

          const titleSpan = document.createElement('span');
          titleSpan.textContent = item.title;
          suggestionItem.appendChild(titleSpan);

          suggestionItem.addEventListener('click', () => {
            searchInput.value = item.title;
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
          });

          suggestionsContainer.appendChild(suggestionItem);
        });
      })
      .catch(error => {
        console.error('Ошибка при получении подсказок:', error);
      });
  }, 300); 
});
document.addEventListener('click', (event) => {
  if (!document.querySelector('.search-wrapper').contains(event.target)) {
    suggestionsContainer.innerHTML = '';
    suggestionsContainer.style.display = 'none';
  }
});