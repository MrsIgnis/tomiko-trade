document.addEventListener('DOMContentLoaded', function() {
    const brandFilter = document.getElementById('brand-filter');
    const modelFilter = document.getElementById('model-filter');
    const urlParams = new URLSearchParams(window.location.search);

    // Функция для загрузки моделей
    async function loadModels(brand) {
        if (!brand) {
            modelFilter.innerHTML = '<option value="">Модель авто</option>';
            modelFilter.disabled = true;
            return;
        }

        try {
            const country = window.location.pathname.split('/')[1];
            const response = await fetch(`/${country}/get_models_by_brand/?brand=${encodeURIComponent(brand)}`);
            const models = await response.json();

            modelFilter.innerHTML = '<option value="">Модель авто</option>';
            models.forEach(model => {
                const option = new Option(model, model);
                modelFilter.add(option);
            });

            // Восстанавливаем выбранную модель
            const selectedModel = urlParams.get('model');
            if (selectedModel) {
                modelFilter.value = selectedModel;
            }

            modelFilter.disabled = false;
        } catch (error) {
            console.error('Error loading models:', error);
        }
    }

    // Инициализация при загрузке страницы
    const initialBrand = urlParams.get('brand') || brandFilter.value;
    if (initialBrand) {
        brandFilter.value = initialBrand;
        loadModels(initialBrand);
    }

    // Обработчик изменения бренда
    brandFilter.addEventListener('change', function() {
        modelFilter.value = ''; // Сбрасываем выбор модели
        loadModels(this.value);
    });

    // Обработчик отправки формы
    document.querySelector('form').addEventListener('submit', function() {
        // Сохраняем выбранный бренд и модель в localStorage
        localStorage.setItem('selectedBrand', brandFilter.value);
        localStorage.setItem('selectedModel', modelFilter.value);
    });

    // Восстановление из localStorage (опционально)
    const savedBrand = localStorage.getItem('selectedBrand');
    const savedModel = localStorage.getItem('selectedModel');
    if (savedBrand) {
        brandFilter.value = savedBrand;
        loadModels(savedBrand).then(() => {
            if (savedModel) modelFilter.value = savedModel;
        });
    }
});