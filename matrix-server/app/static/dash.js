/**
 * Utilized to accomplish any native functionality needed for the Matrix Systems Dashboard.
 *
 * @date 4-3-22
 * @author Christian Saltarelli
 */

// Dashboard Device Dropdown Behavior
const dash_device_dropdown_btn = document.querySelector('#device-menu-button');
const dash_device_dropdown_menu = document.querySelector('#device-dropdown');
const dash_device_dropdown_icon = document.querySelector('#dropdown-icon');
let dropdown_icon_rotation = 0;

dash_device_dropdown_btn.addEventListener('click', () => {
    if (window.getComputedStyle(dash_device_dropdown_menu)['display'] === 'none') {
        dash_device_dropdown_menu.classList.remove('hidden');
    } else {
        dash_device_dropdown_menu.classList.add('hidden');
    }

    dropdown_icon_rotation -= 180;
    dash_device_dropdown_icon.setAttribute("transform", "rotate(" + dropdown_icon_rotation + ")");
})

// Chart.js Population + Behavior
const chart_data = [];

function setChartData(title, headers, data) {
    chart_data.push([title, headers, data]);
}

function updateChartData() {
    const chart_data_ref = chart_data[current_index];

    // Clear the current Chart Shown
    let main_chart_status = Chart.getChart('chart');
    if (main_chart_status !== undefined) {
        main_chart_status.destroy();
    }

    // Update Chart w/ Respective Data
    const chart_ctx = document.querySelector('.main-chart').getContext('2d');
    const chart_instance = new Chart(chart_ctx, {
        type: 'line',
        data: {
            labels: chart_data_ref[1],
            datasets: [{
                label: chart_data_ref[0],
                data: chart_data_ref[2],
                borderWidth: 3,
                fill: false,
                borderColor: "rgb(53, 125, 233)",
                lineTension: 0.2
            }],

        },
        options: {
            responsive: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (current_index ==2) {
                                let label = context.dataset.label || '';

                                if (context.parsed.y !== null) {
                                    label = formatFileSize(context.parsed.y, 2);
                                }

                                return label;
                            } else {
                                return context.dataset.label + ': ' + context.parsed.y + '%';
                            }

                        }
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        display: false,
                        callback: function(value, index, ticks) {
                            if (current_index == 2) {
                                return formatFileSize(value, 2);
                            } else {
                                return value + '%';
                            }
                        }
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 10
                        },
                        callback: function(value, index, ticks) {
                            if (current_index == 2) {
                                return formatFileSize(value, 2);
                            } else {
                                return Math.round(value * 100) / 100 + '%';
                            }
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function formatFileSize(bytes,decimalPoint) {
   if(bytes === 0) return '0 Bytes';
   let k = 1000,
       dm = decimalPoint || 2,
       sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
       i = Math.floor(Math.log(bytes) / Math.log(k));

   if (bytes > 0 && bytes < 1) {
       return "." + bytes + sizes[0] + "/s";
   }

   return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i] + "/s";
}

// Metric Carousel Behavior
const dash_chart_title = document.querySelector('.chart-title');
const dash_carousel_prev = document.querySelector('.carousel-control-prev');
const dash_carousel_next = document.querySelector('.carousel-control-next');

const dash_chart_indicators = [
    document.querySelector('.carousel-indicator-0'),
    document.querySelector('.carousel-indicator-1'),
    document.querySelector('.carousel-indicator-2')
];

let current_index = 0;

dash_carousel_prev.addEventListener('click', () => {
    if (current_index === 0) {
        current_index = 2;
    } else {
        current_index--;
    }

    updateChartView();
    updateChartTitle();
});

dash_carousel_next.addEventListener('click', () => {
    if (current_index === 2) {
        current_index = 0;
    } else {
        current_index++;
    }

    updateChartView();
    updateChartTitle();
});

function updateChartView() {
    for(let i = 0; i < dash_chart_indicators.length; i++) {
        if (i === current_index) {
            dash_chart_indicators[i].classList.add('active-indicator');
            dash_chart_indicators[i].classList.remove('inactive-indicator');

        } else {
            dash_chart_indicators[i].classList.add('inactive-indicator');
            dash_chart_indicators[i].classList.remove('active-indicator');
        }
    }

    updateChartData();
}

function updateChartTitle() {
    dash_chart_title.innerHTML = chart_data[current_index][0];
}

/* Metric Process Behavior */
function updateTableView() {
    // Entries Length Selector
    const entries = document.querySelector('.dataTables_length');
    entries.classList.add('entries-text');

    const entries_select = document.getElementsByName('process_table_length')[0];
    entries_select.classList.add('entries-select');

    // Search Bar
    const table_filter = document.querySelector('.dataTables_filter');
    table_filter.classList.add('table-filter');

    const table_search_bar = document.querySelectorAll('input[type=search]')[0];
    table_search_bar.classList.add('table-search-bar');

    table_search_bar.addEventListener('keypress', () => {
            updateTableView();
    });

    // Table Information
    const table_info = document.querySelector('.dataTables_info');
    table_info.classList.add('table-info', '!h-full');

    // Process Pages
    const previous_btn = document.querySelector('a.previous');
    previous_btn.remove();

    const next_btn = document.querySelector('a.next');
    next_btn.remove();

    // Page List
    let page_numbers = document.querySelectorAll('.paginate_button');

    page_numbers.forEach( page => {
                if (page.classList.contains('current')) {
                    page.style.removeProperty('background');
                    page.classList.remove('current');
                    page.classList.add('!font-bold', 'hover:!bg-gray-200');
                }
            })

    addPageListeners(page_numbers);
}

function addPageListeners(pages) {
    pages.forEach( page => {
        page.classList.add('!bg-transparent', '!bg-opacity-0', '!font-matrix_body', '!text-matrix_gray-100', '!border-0', 'hover:!bg-gray-50', '!rounded-lg', 'hover:!border-0');

        page.addEventListener('click', () => {
            // Remove Added Elements
            document.querySelector('a.previous').remove();
            document.querySelector('a.next').remove();

            // Update Page Number Reference
            page_numbers = document.querySelectorAll('.paginate_button');

            pages.forEach( page => {
                if (page.classList.contains('current')) {
                    page.style.removeProperty('color');
                    page.classList.remove('current');
                    page.classList.add("!font-sans", '!font-bold', 'hover:!bg-opacity-0');
                }
            })

            // Recursively Call Function on Event to Update New Elements (If any)
            addPageListeners(page_numbers)
        });
    });
}

