document.addEventListener('DOMContentLoaded', function() {
  const swiper = new Swiper('.main-slider', {
    autoHeight: true,
    slidesPerView: 'auto',
    spaceBetween: 10,
  });

  const updateActiveThumbnail = () => {
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    thumbnails.forEach(thumbnail => {
      thumbnail.classList.remove('active');
    });
    const activeThumbnail = document.querySelector(`.thumbnail-item[data-slide-index="${swiper.activeIndex}"]`);
    if (activeThumbnail) {
      activeThumbnail.classList.add('active');
    }
  };

  const thumbnails = document.querySelectorAll('.thumbnail-item');
  thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', function() {
      const slideIndex = parseInt(this.getAttribute('data-slide-index'));
      swiper.slideTo(slideIndex);
    });
  });

  const slidePrevButtons = document.querySelectorAll('.slider-button-prev');
  slidePrevButtons.forEach(button => {
    button.addEventListener('click', () => {
      swiper.slidePrev();
    });
  });

  const slideNextButtons = document.querySelectorAll('.slider-button-next');
  slideNextButtons.forEach(button => {
    button.addEventListener('click', () => {
      swiper.slideNext();
    });
  });

  swiper.on('slideChange', () => {
    updateActiveThumbnail();
  });

  updateActiveThumbnail();

});

