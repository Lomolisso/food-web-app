let accessToken = "pk.eyJ1IjoibG9tb2xpc3NvIiwiYSI6ImNrdnZoYWUzcDh2Z2kyd21zbDIyeGwyeTIifQ.zqErDIiCCo6Gs3HSsSvY5A";
let mymap = L.map('map').setView([-33.4500000, -70.6666667], 10);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: accessToken
}).addTo(mymap);

function getMarkersJSON(data) {
    /** @type string */ let response = data.currentTarget.responseText.trim();
    markersJSON = {}
    if (response === '' || response === '{}') {
        console.log("RESPONSE VACIO")
        return;
    }
    
    try {
        // noinspection JSUnresolvedVariable
        markersJSON = JSON.parse(response);
    } catch (e) {
        write_error(response);
        return;
    }

    console.log(markersJSON)
    
    for (const key in markersJSON) {
        let commJSON = markersJSON[key];
        let lat = parseFloat(commJSON["info"]["lat"]);
        let lng = parseFloat(commJSON["info"]["lng"]);

        let html_marker = "<div id='"+key+"-info-container'>";
        
        let status = 1;
        let eventCounter = Object.keys(commJSON["eventos"]).length
        for (const event_id in commJSON["eventos"]) {
            let event_info = commJSON["eventos"][event_id];
            if (status == 1) {
                html_marker += "<div class='info-active'>";
                status = 0;
            }
            else {
                html_marker += "<div class='info-not-active'>";
            }

            html_marker += ("<div class='event-txt-container'>");

            html_marker += ("<p><b>Dia y hora de inicio:</b> " + event_info["dia_hora_inicio"] + "</p>");
            html_marker += ("<p><b>Dia y hora de termino:</b> " + event_info["dia_hora_termino"] + "</p>");
            html_marker += ("<p><b>Tipo:</b> " + event_info["tipo"] + "</p>");
            html_marker += ("<p><b>Sector:</b> " + event_info["sector"] + "</p>");

            html_marker += ("</div>");

            let photoList = event_info["fotos"];
            html_marker += "<div class='marker-img-container'>"; 
            for (let i = 0; i < photoList.length; i++) {
                html_marker += ("<img class='marker-img' src='"+ photoList[i] + "'>");   
            }

            html_marker += "</div>";
            
            html_marker += "<div class='btn-container'>";
            if (eventCounter > 1) {
                html_marker += ("<button type='button' class='select-btn' onclick='showInfo(0,`"+key+"`)'>prev"+"</button>");
            }
            html_marker += ("<button type='button' class='event-btn' onclick='window.location.href=`../cgi-bin/event_info.py?evento_id="+event_info["id"]+"`'>ver evento"+"</button>");
            if (eventCounter > 1) {
                html_marker += ("<button type='button' class='select-btn' onclick='showInfo(1,`"+key+"`)'>sgte"+"</button>");
            }
            html_marker += "</div>";
            html_marker += "</div>";
            
        }
        html_marker += "</div>"
        

        let markerOptions = {
            title: "fotos: " + commJSON["info"]["total_fotos"],
            clickable: true
        };

        let marker = L.marker([lat, lng], markerOptions);
        let popup = L.popup();

        function onMapClick(e) {
            popup
                .setLatLng(e.latlng)
                .setContent(html_marker)
                .openOn(mymap);
        }

        marker.on('click', onMapClick);
        marker.addTo(mymap);
    }
}

// Creates the request
let xhr = new XMLHttpRequest();
// Configures the xhr request
xhr.open('GET', './marker_json.py');
xhr.timeout = 1000;

xhr.onload = getMarkersJSON;

xhr.onerror = function () {
    write_error('An error has happened while loading the messages');
}
xhr.send();


function showInfo(mode, commune) {
    let childDivs = document.getElementById(commune+"-info-container").children;
    let infoIndex = 0;
    for(let i = 0; i < childDivs.length; i++ ) {
        let childDiv = childDivs[i];
        if (childDiv.classList.contains("info-active")) {
            childDiv.classList.add("info-not-active");
            childDiv.classList.remove("info-active");
            infoIndex = i;
        }
    }

    // mode = 0 -> prev
    // mode = 1 -> next
    if (mode) {
        if (infoIndex + 1 != childDivs.length) {infoIndex += 1;}
        else {infoIndex = 0;}
    }
    else {
        if (infoIndex - 1 != -1) {infoIndex -= 1;}
        else {infoIndex = childDivs.length - 1;}
    }

    childDivs[infoIndex].classList.add("info-active");
    childDivs[infoIndex].classList.remove("info-not-active");
}