function toggleSubfilters(buttonElement) {
  const parentItem = buttonElement.closest(".filter-item");
  if (parentItem) {
    parentItem.classList.toggle("open");
  }
}

function toggleSidebar() {
  const sidebar = document.querySelector(".sidebar");
  if (sidebar) {
    sidebar.classList.toggle("active");
  }
}

const searchInput = document.querySelector(".search-input");
const suggestionsContainer = document.querySelector(".suggestions");

let timeout = null;

searchInput.addEventListener("input", function () {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    const query = searchInput.value;
    if (query.trim().length === 0) {
      suggestionsContainer.innerHTML = "";
      suggestionsContainer.style.display = "none";
      return;
    }

    fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        suggestionsContainer.innerHTML = "";

        if (data.suggestions && data.suggestions.length > 0) {
          suggestionsContainer.style.display = "block";

          data.suggestions.forEach((item) => {
            const suggestionItem = document.createElement("div");
            suggestionItem.classList.add("suggestion-item");

            if (item.poster) {
              const img = document.createElement("img");
              img.src = item.poster;
              img.alt = item.title;
              suggestionItem.appendChild(img);
            }

            const contentDiv = document.createElement("div");
            contentDiv.classList.add("suggestion-content");

            const titleSpan = document.createElement("span");
            titleSpan.classList.add("suggestion-title");
            titleSpan.textContent = item.title;
            contentDiv.appendChild(titleSpan);

            const typeSpan = document.createElement("span");
            typeSpan.classList.add("suggestion-type");
            typeSpan.textContent = item.type;
            contentDiv.appendChild(typeSpan);

            suggestionItem.appendChild(contentDiv);

            suggestionItem.addEventListener("click", () => {
              window.location.href = item.url;
            });

            suggestionsContainer.appendChild(suggestionItem);
          });
        } else {
          suggestionsContainer.style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Ошибка при получении подсказок:", error);
        suggestionsContainer.style.display = "none";
      });
  }, 300);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-wrapper")) {
    suggestionsContainer.style.display = "none";
  }
});

suggestionsContainer.addEventListener("click", (event) => {
  event.stopPropagation();
});
