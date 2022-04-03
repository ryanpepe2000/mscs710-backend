/**
 * Utilized to accomplish any native functionality needed for the Matrix Systems Client.
 *
 * @date 4-3-22
 * @author Christian Saltarelli
 */

// Responsive Primary Navigation Behavior
const nav_mobile_btn = document.querySelector('button.nav-button')
const nav_mobile_menu = document.querySelector('.nav-menu')
const nav_mobile_menu_icon = document.querySelector('.menu-icon');
const nav_mobile_exit_icon = document.querySelector('.exit-icon');

nav_mobile_btn.addEventListener('click', () => {
    if (window.getComputedStyle(nav_mobile_menu)['display'] === 'none') {
        nav_mobile_menu_icon.classList.add("hidden");
        nav_mobile_exit_icon.classList.remove('hidden');
        nav_mobile_menu.classList.toggle('hidden');
        nav_mobile_menu.classList.add('flex');
    } else {
        nav_mobile_menu_icon.classList.remove('hidden');
        nav_mobile_exit_icon.classList.add('hidden');
        nav_mobile_menu.classList.toggle('hidden');
    }
});



