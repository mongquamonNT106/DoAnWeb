const navbarsIcon = document.querySelector('.nav_bars-btn');
const navbarscloseIcon = document.querySelector('.nav_mobile-close');
const hdChonRap = document.querySelector('.main');

navbarsIcon.addEventListener('click', () => {
    hdChonRap.classList.toggle('active');
});
navbarscloseIcon.addEventListener('click', () => {
    hdChonRap.classList.toggle('active');
});



