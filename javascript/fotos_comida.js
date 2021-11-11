let containerFileInput = document.getElementById("file-input-container");
let addFileInputButton = document.getElementById("add-file-input-btn");
let fileInputCounter = 1;

function generateFileInput() {
    let div = document.createElement("div");
    div.setAttribute("class", "form-input");

    let divLabel = document.createElement("div");
    let label = document.createElement("label");
    label.innerText = "Foto extra (Nro. "+ fileInputCounter+")";
    label.setAttribute("for", "file-input-"+fileInputCounter);
    divLabel.appendChild(label);

    let divFileInput = document.createElement("div");
    divFileInput.setAttribute("class", "input-file-btns-container");
    let fileInput = document.createElement("input");
    fileInput.setAttribute("name", "file-input-"+fileInputCounter);
    fileInput.setAttribute("id", "file-input-"+fileInputCounter);
    fileInput.setAttribute("type", "file");
    fileInput.required = true;
    divFileInput.appendChild(fileInput);

    div.appendChild(divLabel);
    div.appendChild(divFileInput);

    fileInputCounter++;
    containerFileInput.appendChild(div);
}

function handleInputFile() {
    if (fileInputCounter<5){
        generateFileInput();
    }
}