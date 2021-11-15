function getGraphsJSON(data) {
    /** @type string */ let response = data.currentTarget.responseText.trim();
    graphsJSON = {}
    if (response === '' || response === '{}') {
        console.log("RESPONSE VACIO")
        return;
    }
    
    try {
        // noinspection JSUnresolvedVariable
        graphsJSON = JSON.parse(response);
    } catch (e) {
        write_error(response);
        return;
    }
    
    dataGraph1 = graphsJSON["graph-1"];


    for (const i in dataGraph1) {
        dataGraph1[i][0] = Date.parse(dataGraph1[i][0])
    }


    $.plot($('#graph-1'),[dataGraph1], {
        xaxis: {
            mode: "time",
            tickSize: [1, "day"],
            tickLength: 0
        },
        yaxis: {
            tickSize: 1,
            tickDecimals: 0
        },
        series: {
            lines: {
                show: true,
            },
            points: {
                show: true,
            }
        }
    });


    dataGraph2 = graphsJSON["graph-2"]

    $.plot($("#graph-2"), dataGraph2, { 
        series: {
             pie: {
                 show: true,
                 label: {
                     show: true,
                     formatter: function(label, point){
                         return '<div>'+ label + '</div>';
                     }
                 }
            }
        },        
        legend: {show: true}
    });

    
    dataGraph31 = graphsJSON["graph-3"]["graph-3-1"]
    dataGraph32 = graphsJSON["graph-3"]["graph-3-2"]
    dataGraph33 = graphsJSON["graph-3"]["graph-3-3"]
    
    $.plot($('#graph-3'), [
    {
        label: "Eventos iniciados en la mañana",
        data: dataGraph31,
        bars: {
            show: true,
            barWidth: 0.2,
        }
    },
    {
        label: "Eventos iniciados a medio día",
        data: dataGraph32,
        bars: {
            show: true,
            barWidth: 0.2,
        }
    },
    {
        label: "Eventos iniciados en la tarde",
        data: dataGraph33,
        bars: {
            show: true,
            barWidth: 0.2,
        }
    }
    ],
    {
        xaxis: {
            mode: "categories",
            tickLength: 0
        }
    });

}

$(document).ready(function() {
    // Creates the request
    let xhr = new XMLHttpRequest();
    // Configures the xhr request
    xhr.open('GET', './graph_json.py');
    xhr.timeout = 1000;
    
    xhr.onload = getGraphsJSON;
    
    xhr.onerror = function () {
        write_error('An error has happened while loading the messages');
    }
    xhr.send();
});