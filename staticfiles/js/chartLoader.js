const horizontalLinePlugin = {
    afterDatasetDraw: chart => {
        if (typeof chart.config.options.lineAt == 'undefined') return;
        lineAt = chart.config.options.lineAt;
        ctxPlugin = chart.chart.ctx;
        xAxe = chart.scales[chart.config.options.scales.xAxes[0].id];
        yAxe = chart.scales[chart.config.options.scales.yAxes[0].id];

        if (yAxe.min != 0) return;
        ctxPlugin.strokeStyle = "red";
        ctxPlugin.beginPath();
        lineAt = (lineAt - yAxe.min) * (100 / yAxe.max);
        lineAt = (100 - lineAt) / 100 * (yAxe.height) + yAxe.top;
        ctxPlugin.moveTo(xAxe.left, lineAt);
        ctxPlugin.lineTo(xAxe.right, lineAt);
        ctxPlugin.stroke();
    }
};
Chart.pluginService.register(horizontalLinePlugin);

const style = getComputedStyle(document.body);
const fg = style.getPropertyValue('--foreground');
const colors = ['1', '2', '3', '4', '6'].map(n => style.getPropertyValue('--color' + n).substr(1));
const borderColor = new Array(50).fill(colors).flat();

const backgroundColor = borderColor.map(c => c.concat('bb'));

Chart.defaults.global.defaultFontColor = fg;

const instantiateChart = (chart_tag, data_obj) => {
    labels = data_obj.labels || [];
    data = data_obj.data || [];
    average_GPA = data_obj.average_GPA || null;

    switch (data_obj.chartType) {
        case "doughnut":
            options = {
                maintainAspectRatio: false,
                plugins: {
                    doughnutlabel: {
                        labels: [
                            { text: 'Average GPA', font: { size: '50' } },
                            { text: average_GPA, font: { size: '60' }, }
                        ]
                    }
                }
            };
            break;
        case "bar":
            options = {
                maintainAspectRatio: false,
                legend: { display: false },
                scales: { yAxes: [{ ticks: { beginAtZero: true } }] },
                lineAt: average_GPA,
            };
            break
        default:
            options = {};
            break;
    }

    new Chart(chart_tag, {
        type: data_obj.chartType,
        data: {
            labels,
            datasets: [{ data, backgroundColor, borderColor, borderWidth: 1 }]
        },
        options
    });
}

document.addEventListener("DOMContentLoaded", () =>
    document.querySelectorAll('.templateTagChart').forEach(chart_tag =>
        fetch(chart_tag.getAttribute("url-path"))
            .then(res => res.ok ? res.json() : Promise.reject(res.status))
            .then(data => instantiateChart(chart_tag, data))
            .catch(error => console.error(error))));
