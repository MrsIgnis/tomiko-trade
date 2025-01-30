document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('id_phone_number');

    // Функция форматирования номера телефона
    function formatPhoneNumber(value) {
        // Удаление всех нецифровых символов кроме плюса
        let numbers = value.replace(/[^\d+]/g, '');

        // Обеспечиваем начало номера телефона с +7
        if (!numbers.startsWith('+7')) {
            numbers = '+7' + numbers.replace(/^\+?7?/, '');
        }

        // Ограничиваем длину номера
        const maxDigits = 12;
        numbers = numbers.slice(0, maxDigits);

        // Форматируем номер телефона с пробелами
        let formatted = '+7';
        const digits = numbers.slice(2).replace(/\D/g, ''); // Дополнительная проверка

        if (digits.length > 0) {
            formatted += ' ' + digits.slice(0, 3);
        }
        if (digits.length >= 4) {
            formatted += ' ' + digits.slice(3, 6);
        }
        if (digits.length >= 7) {
            formatted += ' ' + digits.slice(6, 8);
        }
        if (digits.length >= 9) {
            formatted += ' ' + digits.slice(8, 10);
        }

        return formatted;
    }

    // Обработчик ввода
    phoneInput.addEventListener('input', function(e) {
        const startPos = e.target.selectionStart;
        const oldValue = e.target.value;

        // Форматируем значение
        const formatted = formatPhoneNumber(oldValue);
        e.target.value = formatted;

        // Корректируем позицию курсора
        let newPos = startPos;
        if (formatted.length > oldValue.length) {
            newPos += formatted.length - oldValue.length;
        }
        e.target.setSelectionRange(newPos, newPos);
    });

    // Обработчик удаления
    phoneInput.addEventListener('keydown', function(e) {
        // Блокирование удаления знаков форматирования
        if (e.key === 'Backspace' || e.key === 'Delete') {
            const selectionStart = e.target.selectionStart;
            const value = e.target.value;

            // Запрет на удаление "+7"
            if (selectionStart <= 3 && (e.key === 'Backspace' || e.key === 'Delete')) {
                e.preventDefault();
            }

            // Удаление только цифр, сохраняя при этом форматирование
            if (value[selectionStart] === ' ') {
                e.preventDefault();
                const newValue = value.slice(0, selectionStart - 1) + value.slice(selectionStart);
                e.target.value = newValue;
                e.target.setSelectionRange(selectionStart - 1, selectionStart - 1);
            }
        }
    });

    // Обработчик вставки
    phoneInput.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedData = (e.clipboardData).getData('text');
        const numbers = pastedData.replace(/[^\d]/g, '');
        const newValue = formatPhoneNumber('+7' + numbers);
        document.execCommand('insertText', false, newValue.slice(3));
    });
});