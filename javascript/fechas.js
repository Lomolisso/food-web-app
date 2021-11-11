function loadDate(id, delay) {
    let input = document.getElementById(id);
    let today = new Date().toISOString().split("T");
    let rest = today[1].split(":")
    let time = parseInt((rest[0]+delay)%24)+":"+rest[1];
    let defaultText = today[0] + " " + time;
    input.defaultValue = defaultText;
}

loadDate("dia-hora-inicio", 0);
loadDate("dia-hora-termino", 3);