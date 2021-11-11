let containerRedSocial = document.getElementById("social-net-container");
let selectorRedSocialHTML = document.getElementById("red-social");
let redesPosibles = ["twitter", "instagram", "facebook", "tiktok", "otra"];
let contador = 0;

function generateTextInput() {
    let redSocial = selectorRedSocialHTML.value.toLowerCase()

    let div = document.createElement("div");
    div.setAttribute("class", "form-input");

    let divLabel = document.createElement("div");
    let label = document.createElement("label");
    label.innerText = "URL perfil de " + redSocial;
    label.setAttribute("for", "sn-"+contador+"-"+redSocial);
    divLabel.appendChild(label);

    let textInput = document.createElement("input");
    textInput.setAttribute("name", "sn-"+contador+"-"+redSocial);
    textInput.setAttribute("id", "sn-"+contador+"-"+redSocial);
    textInput.setAttribute("class", "sn-txt-input");
    textInput.setAttribute("type", "text");

    div.appendChild(divLabel);
    div.appendChild(textInput);

    contador++;
    containerRedSocial.appendChild(div);
}

function handleSocialNetInput() {
    if (contador<5){
        generateTextInput();
        selectorRedSocialHTML.value=""
    }
}