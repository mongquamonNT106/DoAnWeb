//Search
const searchIcon = document.querySelector('.search_icon');
/*const searchPanel = document.querySelector('.search_panel_form_content');*/
const hdSearch = document.querySelector('.hd_search');

searchIcon.addEventListener('click', () => {
    hdSearch.classList.toggle('show');
});
/*searchPanel.addEventListener('click', () => {
    hdSearch.classList.toggle('dis');
});*/

//Re + Lo
const reloAva = document.querySelector('.hd_register_login_ava');
/*const searchPanel = document.querySelector('.search_panel_form_content');*/
const hdReLo = document.querySelector('.hd_register_login');

reloAva.addEventListener('click', () => {
    hdReLo.classList.toggle('show');
});
/*searchPanel.addEventListener('click', () => {
    hdSearch.classList.toggle('dis');
});*/
