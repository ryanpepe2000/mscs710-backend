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
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        display: false
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 10
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
    switch(current_index) {
        case 0:
            dash_chart_title.innerHTML = "CPU Utilization"
            break;

        case 1:
            dash_chart_title.innerHTML = "Memory Utilization"
            break;

        case 2:
            dash_chart_title.innerHTML = "Disk Utilization"
            break;
    }
}

/* Metric Process Behavior */
const process_view_wrapper = document.querySelector('.view-more-btn');
const process_view_text = document.querySelector('button.view-btn');
const process_hidden_rows = document.querySelectorAll('.hidden-row');

let rotation = 0;

process_view_wrapper.addEventListener('click', () => {
   for (let i = 0; i < process_hidden_rows.length; i++) {
       process_hidden_rows[i].classList.toggle('hidden');
   }

   if (process_view_text.innerHTML.includes('view more')) {
       process_view_text.innerHTML = 'view less';
   } else {
       process_view_text.innerHTML = 'view more';
   }
});

