document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('feedback-form');
    const popup = document.getElementById('success-popup');
    const closeButton = document.querySelector('.close-popup');

    // Функция для получения CSRF-токена
    const getCSRFToken = () => {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return null;
    };

    // Обработчик отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        try {
            const formData = new FormData(form);
            const response = await fetch('/submit-feedback/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Успешная отправка
                popup.style.display = 'block';
                form.reset();
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке формы');
        }
    });

    // Закрытие pop-up окна
    const closePopup = () => {
        popup.style.display = 'none';
    };

    closeButton.addEventListener('click', closePopup);

    popup.addEventListener('click', (e) => {
        if (e.target === popup) closePopup();
    });
});