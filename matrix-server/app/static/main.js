/**
 * Utilized to accomplish any native functionality needed for the Matrix Systems Client.
 *
 * @date 4-3-22
 * @author Christian Saltarelli
 */

// Responsive Primary Navigation Behavior
const nav_mobile_btn = document.querySelector('button.nav-button');
const nav_mobile_menu = document.querySelector('.nav-menu');
const nav_mobile_menu_icon = document.querySelector('.menu-icon');
const nav_mobile_exit_icon = document.querySelector('.exit-icon');

nav_mobile_btn.addEventListener('click', () => {
    if (window.getComputedStyle(nav_mobile_menu)['display'] === 'none') {
        nav_mobile_menu_icon.classList.add("hidden");
        nav_mobile_exit_icon.classList.remove('hidden');
        nav_mobile_menu.classList.toggle('hidden');
        nav_mobile_menu.classList.add('flex', 'bg-white', 'border', 'border-matrix_blue-100', 'shadow-lg');
    } else {
        nav_mobile_menu_icon.classList.remove('hidden');
        nav_mobile_exit_icon.classList.add('hidden');
        nav_mobile_menu.classList.toggle('hidden');
        nav_mobile_menu.classList.remove('bg-white', 'border', 'border-matrix_blue-100', 'shadow-lg');
    }
});

// Dashboard Device Dropdown Behavior
const dash_device_dropdown_btn = document.querySelector('#device-menu-button');
const dash_device_dropdown_menu = document.querySelector('#device-dropdown');

dash_device_dropdown_btn.addEventListener('click', () => {
    if (window.getComputedStyle(dash_device_dropdown_menu)['display'] === 'none') {
        dash_device_dropdown_menu.classList.remove('hidden');
        // TODO:- Implement JS POST Request w/ Device Name (Device Name will be the ID of the element
    } else {
        dash_device_dropdown_menu.classList.add('hidden');
    }
})

// Flash Message Display Behavior
const flash_banner = document.querySelector('#flash-banner');

flash_banner.addEventListener('click', () => {
   flash_banner.classList.add("hidden");
});




