document.addEventListener('DOMContentLoaded', function() {
    // Инициализация Swiper для слайдера видеоклипов
    const swiperVideo = new Swiper('.video_clip', {
        loop: false,
        slidesPerView: 'auto',
        spaceBetween: 40,
        freeMode: true,
        mousewheel: {
            forceToAxis: true
        },
        wrapperClass: 'video-clip-wrapper',
        slideClass: 'video_clip_item',
        noSwiping: true
    });

    // Инициализация Swiper для слайдера изображений
    const swiper = new Swiper('.image-slider', {
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        autoHeight: true, // Исправлено: autoHeight вместо autoheight
        slidesPerView: 'auto',
        spaceBetween: 10,
        freeMode: true,
    });

    const innerSliders = document.querySelectorAll('.image-slider__inner-slider');
    const innerSwipers = {}; // Храним экземпляры вложенных слайдеров
    innerSliders.forEach((slider, index) => {
        innerSwipers[index] = new Swiper(slider, {
            pagination: {
                el: slider.querySelector('.image-slider__inner-pagination'),
                clickable: true,
            },
            slidesPerView: 1,
            loop: true,
        });
    });

    const updateSlideBackground = (slide) => {
        const imageContainer = slide.querySelector('.image-slider_image');
        if (imageContainer) {
            const imageUrl = imageContainer.getAttribute('data-background');
            imageContainer.style.backgroundImage = `url('${imageUrl}')`;
        }
    };

    // Убедимся, что swiper инициализирован перед использованием
    if (swiper) {
        swiper.on('slideChange', () => {
            swiper.slides.forEach(slide => {
                const imageContainer = slide.querySelector('.image-slider_image');
                if (imageContainer) {
                    imageContainer.style.backgroundImage = '';
                }
            });
            const activeSlide = swiper.slides[swiper.activeIndex];
            updateSlideBackground(activeSlide);

            // Обновляем вложенный слайдер при смене активного слайда
            const activeInnerSlider = activeSlide.querySelector('.image-slider__inner-slider');
            if (activeInnerSlider) {
                const index = Array.from(innerSliders).indexOf(activeInnerSlider);
                innerSwipers[index].update(); // Обновляем Swiper на активном слайде
            }
        });

        swiper.slides.forEach(slide => {
            updateSlideBackground(slide);
        });
    }

    // Обработка pop-up
    const popUp = document.getElementById('custom-pop-up');
    const popUpClose = document.getElementById('custom-pop-up-close');

    if (popUp && popUpClose) {
        document.addEventListener('click', function(event) {
            if (event.target.classList.contains('custom-open-pop-up')) {
                event.preventDefault();
                console.log('Кнопка "Оставить заявку" нажата'); // Отладка
                popUp.classList.add('active');
            }
        });

        popUpClose.addEventListener('click', () => {
            popUp.classList.remove('active');
        });
    } else {
        console.error("Один или несколько элементов pop-up не найдены!");
    }
});

const swiperChina = new Swiper('.image-slider', {
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },
    autoHeight: true,
    slidesPerView: 'auto',
    spaceBetween: 10,
    freeMode: true,
});

const innerSlidersChina = document.querySelectorAll('.image-slider__inner-slider');
const innerSwipersChina = {};
innerSlidersChina.forEach((slider, index) => {
    innerSwipersChina[index] = new Swiper(slider, {
        pagination: {
            el: slider.querySelector('.image-slider__inner-pagination'),
            clickable: true,
        },
        slidesPerView: 1,
        loop: true,
    });
});