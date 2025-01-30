window.addEventListener('load', function() {
        const popUp = document.getElementById('custom-pop-up');
        const popUpClose = document.getElementById('custom-pop-up-close');

        if (popUp && popUpClose) {
           // Делегирование события клика на весь документ
            document.addEventListener('click', function(event) {
               if(event) {
                   console.log(event.target);
                     // Проверяем, был ли клик по элементу с классом custom-open-pop-up
                       if (event.target.classList.contains('custom-open-pop-up')) {
                           event.preventDefault(); // Предотвращаем стандартное поведение ссылки (если это ссылка)
                             popUp.classList.add('active');
                       }
                   }
            });
        });
        });