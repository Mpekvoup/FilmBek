document.addEventListener('DOMContentLoaded', () => {
    const tabs   = document.querySelectorAll('.tab-button');
    const panes  = document.querySelectorAll('.tab-pane');
  
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab; // например "watchlist" или "favorites"
  
        // 1) Снимаем active со всех кнопок и панелей
        tabs.forEach(t => t.classList.remove('active'));
        panes.forEach(p => p.classList.remove('active'));
  
        // 2) Делаем активной текущую кнопку...
        tab.classList.add('active');
        // ...и соответствующую панель по id
        const pane = document.getElementById(target);
        if (pane) pane.classList.add('active');
      });
    });
  });
  