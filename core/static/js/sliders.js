
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

            popUpClose.addEventListener('click', () => {
                popUp.classList.remove('active');
            });
        } else {
            console.error("Один или несколько элементов pop-up не найдены!");
        }
 // Инициализация Swiper для слайдера изображений
        const sliders = document.querySelectorAll('.wrapper');
        sliders.forEach(container => {
                const swiper = new Swiper(container.querySelector('.image-slider'), {
                        navigation: {
                            nextEl: container.querySelector('.swiper-button-next'),
                            prevEl: container.querySelector('.swiper-button-prev')
                         },
                        autoheight: true,
                        slidesPerView: 'auto',
                        spaceBetween: 10,
                        freeMode: true,
                    });

                    const innerSliders = container.querySelectorAll('.image-slider__inner-slider');
                    const innerSwipers = {}; // Храним экземпляры вложенных слайдеров
                     innerSliders.forEach((slider, index) => {
                           innerSwipers[index] = new Swiper(slider, {
                                pagination: {
                                     el: slider.querySelector('.image-slider__inner-pagination'),
                                    clickable: true,
                                },
                              slidesPerView: 1,
                               loop: true,
                                navigation:{
                                  nextEl: slider.querySelector('.image-slider__inner-button-next'),
                                     prevEl: slider.querySelector('.image-slider__inner-button-prev'),
                                   },

                            });
                       });
                    const updateSlideBackground = (slide) => {
                          const imageContainer = slide.querySelector('.image-slider_image');
                           if (imageContainer) {
                                const imageUrl = imageContainer.getAttribute('data-background');
                                imageContainer.style.backgroundImage = `url('${imageUrl}')`;
                            }
                    };
                     swiper.slides.forEach(slide => {
                        updateSlideBackground(slide);
                    });
                     swiper.on('slideChange', function() {
                        swiper.slides.forEach(slide => {
                            const imageContainer = slide.querySelector('.image-slider_image');
                            if(imageContainer){
                                imageContainer.style.backgroundImage = '';
                             }
                       });
                        const activeSlide = swiper.slides[swiper.activeIndex];
                            updateSlideBackground(activeSlide);

                          const activeInnerSlider = activeSlide.querySelector('.image-slider__inner-slider');
                           if (activeInnerSlider) {
                                const index = Array.from(innerSliders).indexOf(activeInnerSlider);
                                innerSwipers[index].update();
                          }
                           updateActiveThumbnail();
                    });
                    const thumbnails = container.querySelectorAll('.thumbnail-item');
                   thumbnails.forEach(thumbnail => {
                        thumbnail.addEventListener('click', function() {
                            const slideIndex = parseInt(this.getAttribute('data-slide-index'));
                             swiper.slideTo(slideIndex);
                         });
                   });

                    const updateActiveThumbnail = () => {
                      thumbnails.forEach(thumbnail => {
                          thumbnail.classList.remove('active');
                        });
                     const activeThumbnail = container.querySelector(`.thumbnail-item[data-slide-index="${swiper.activeIndex}"]`);
                        if (activeThumbnail) {
                           activeThumbnail.classList.add('active');
                        }
                   };
                  updateActiveThumbnail();
         });



    });

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

