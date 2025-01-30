const openPopUp = document.getElementById('open_pop_up');
const closePopUp = document.getElementById('pop_up_close');
const popUp = document.getElementById('pop_up');

closePopUp.addEventListener('click', () => {
    popUp.classList.remove('active');
  setTimeout(() => {
      popUp.style.display = 'none';
  }, 400);
});

popUp.addEventListener('click', (event) => {
    if (event.target === popUp) {
      popUp.classList.remove('active');
      setTimeout(() => {
          popUp.style.display = 'none';
      }, 400);
    }
});


openPopUp.addEventListener('click', function(e) {
    e.preventDefault();
    popUp.style.display = 'flex';
    setTimeout(() => {
      popUp.classList.add('active');
    }, 100);
});

$(function() {
    $(window).on("scroll", function() {
        var introH = $("#intro").innerHeight();
        console.log(introH);
    });
});

 $(window).on("scroll", function() {
   var introH = $("#intro").innerHeight();
   console.log(introH);
 });
});

