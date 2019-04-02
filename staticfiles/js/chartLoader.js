var horizontalLinePlugin = {
    afterDatasetDraw: function(chart) {
        if (typeof chart.config.options.lineAt == 'undefined') return;
        var lineAt = chart.config.options.lineAt;
        var ctxPlugin = chart.chart.ctx;
        var xAxe = chart.scales[chart.config.options.scales.xAxes[0].id];
        var yAxe = chart.scales[chart.config.options.scales.yAxes[0].id];
        
        if(yAxe.min != 0) return;
        console.log('got here')
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

const genColArr = num => {
    genBaseArr = num => {
        dynamicBase = () => {
            c = () => Math.floor(Math.random() * 255);
            return "rgb(" + c() + "," + c() + "," + c();
        };
        
        return Array.apply(null, Array(num)).map(dynamicBase)
    }
    
    baseArr = genBaseArr(num)
    return {
        background: baseArr.map(c => c + ', 0.2)'),
        border: baseArr.map(c => c + ', 1)'),
    }
}
colArr = genColArr(100)

function instantiateChart(chart_tag, data_obj, colors) {
    function setChart(tag, chartType, labels, data, average_GPA, colors) {
        switch(chartType) {
            case "doughnut":
                options = {
                    plugins: {
                        doughnutlabel: { labels: [
                            { text: 'Average GPA', font: { size: '50' } },
                            { text: average_GPA, font: { size: '60' }, }
                        ] }
                    }		
                };
                break;
            case "bar":
                options = {
                    legend: { display: false },
                    scales: { yAxes: [{ ticks: { beginAtZero: true } }] },
                    lineAt: average_GPA
                };
                break
            default:
                options = {};
                break;
        }

        var myChart = new Chart(tag, {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    borderWidth: 1
                }]
            },
            options: options
        });
    }

    setChart(
        chart_tag,
        data_obj.chartType,
        data_obj.labels || [],
        data_obj.data || [],
        data_obj.average_GPA || null,
        colors
    )
}

document.addEventListener("DOMContentLoaded", function(event) { 
    document.querySelectorAll('.templateTagChart').forEach(function(chart_tag) {
        fetch(chart_tag.getAttribute("url-path"))
        .then(response => 
            response.ok ? response.json() : Promise.reject(response.status)
        )
        .then(data => instantiateChart(chart_tag, data, colArr))
        .catch(error => console.log('error:', error));
    });
});
