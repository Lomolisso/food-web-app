const valNotifications = document.getElementById("val-notification");
const sendButton = document.getElementById("send-btn");
const inputNames = ["Región", "Comuna", "Sector", "Nombre", "Email", "Número de Celular", "Red social", "Día y hora de inicio", "Día y hora de término", "Tipo", "Foto"];
let valStatus = new Array(11).fill(true);

let generateNotification = (msg) => {
    valNotifications.innerText = msg;
    valNotifications.style.display = "block";
    window.scrollTo(0,0);
};

let deleteNotifications = () => {
    valNotifications.innerText = "";
    valNotifications.style.display = "none";
    valStatus = new Array(11).fill(true);;
};

let resetForm = () => {
    form.reset();
    deleteNotifications(); 
};


let displayNotifications = (valStatus) => {
    let incorrectInputs = [];
        for (let i = 0; i < valStatus.length; i++) {
            if (!valStatus[i]) {
                incorrectInputs.push(inputNames[i]);
            }
        }
        let valNotification = "Su formulario falló en: ";
        for (let i = 0; i < (incorrectInputs.length-1); i++) {
            valNotification += incorrectInputs[i] + ", "
        }
        valNotification += incorrectInputs[incorrectInputs.length-1] + ".";
        generateNotification(valNotification);
}


let validateEmail = (email) => {
    const regEx = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return regEx.test(email);
}

let validateCel = (cel) => {
    const regEx = /^\+?\(?([0-9]{3})\)?[- ]?([0-9]{4})[- ]?([0-9]{4})$/;
    return regEx.test(cel);
}

// importante: se pide que valide formato, no que las fechas tengan "sentido".
// EJ: "0000-00-00 00:00" no tiene sentido pero cumple con el formato.
let validateDate = (fecha) => {
    const regEx = /^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{2})$/;
    return regEx.test(fecha);
}

let validateURL = (url) => {
    const regEx = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g;
    return regEx.test(url);
}

let validateInputs = () => {
    deleteNotifications();

    // recuperamos los campos a validar.
    let fRegion = document.getElementById("region").value;
    let fComuna = document.getElementById("comuna").value;
    let fSector = document.getElementById("sector").value;
    let fNombre = document.getElementById("nombre").value;
    let fEmail = document.getElementById("email").value;
    let fCelular = document.getElementById("celular").value;
    let fRedSocial = document.getElementById("social-net-container");
    let fDHInicio = document.getElementById("dia-hora-inicio").value;
    let fDHTermino = document.getElementById("dia-hora-termino").value;
    let fTipoComida = document.getElementById("tipo-comida").value;
    let fFotoComida = document.getElementById("file-input-container");
    
    // validamos la region: si fRegion = "" => No selecciono opcion.
    valStatus[0] = Boolean(fRegion);

    // validamos la comuna: si fComuna = "" => No selecciono opcion.
    valStatus[1] = Boolean(fComuna);

    // validamos el sector:
    valStatus[2] = (fSector.length <= 100);

    // validamos el nombre:
    valStatus[3] = Boolean(fNombre) && (fNombre.length <= 200);

    // validamos el email:
    valStatus[4] = validateEmail(fEmail);

    // validamos el celular:
    valStatus[5] = validateCel(fCelular);

    // validamos las redes sociales:

    // Recuperamos el numero de hijos de fRedSocial. Notar que al menos 1 hijo,
    // el menu de seleccion.

    let n = fRedSocial.childElementCount;
    let countTextInputs = n - 1;

    // Ademas validamos que cada input sea en formato de url.
    let urls = document.getElementsByClassName("sn-txt-input");
    let urlValid = true;
    for (let i = 0; i < urls.length; i++) {
        urlValid = urlValid && validateURL(urls[i].value);
    }

    // validamos que hayan a lo mas 5 inputs de texto.
    valStatus[6] = (countTextInputs >= 0) && (countTextInputs <= 5) && urlValid;
 
    // validamos fechas de inicio y termino:
    valStatus[7] = validateDate(fDHInicio);
    valStatus[8] = validateDate(fDHTermino);

    // validamos tipo comida:
    valStatus[9] = Boolean(fTipoComida);

    // validamos foto comida:
    
    // Recuperamos el numero de hijos de fFotoComida.
    let countFileInputs = fFotoComida.childElementCount;

    // validamos que hayan al menos 1 input de archivo y a lo mas 5.
    let valFileInputs1 = (countFileInputs >= 1) && (countFileInputs <= 5);

    // validamos que cada input de archivos tenga un elemento cargado.
    let childFileInputs = fFotoComida.getElementsByTagName("input");
    let arr = [];

    for(let i = 0; i < childFileInputs.length; i++ ) {
        arr.push(childFileInputs[i].files.length === 1);
    }

    let reducer = (acc, x) => {return acc && x};
    let valFileInputs2 = arr.reduce(reducer);

    // el resultado final de la validacion es true siempre que ambos casos se cumplan.
    valStatus[10] = valFileInputs1 && valFileInputs2;

    // se revisa la correctitud del formulario.
    let formStatus = valStatus.reduce(reducer);

    if (formStatus) {
        deleteNotifications();
        let popUp = document.querySelector('#pop-up');
        openPopUp(popUp);
    }
    else{
        displayNotifications(valStatus);
    }
};
