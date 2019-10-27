window.addEventListener('load', function () {
  $('#homeWelcome').modal('show')

});

// $("#form-container").submit(function(e) {
//     e.preventDefault();
// });
const carouselSlide = document.querySelector('#carousel')
const formContainer = document.querySelector('#form-container')

const carousel = () => {
  console.log('hi');
  carouselSlide.style.width = '60%';
  carouselSlide.style.height = '400px';
  formContainer.style.display = 'none';

}
