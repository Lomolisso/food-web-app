const regionesHTML = document.getElementById("region");
const comunasHTML = document.getElementById("comuna");
const sectorHTML = document.getElementById("sector");
const nombreHTML = document.getElementById("nombre");
const emailHTML = document.getElementById("email");
const celularHTML = document.getElementById("celular");
const redSocialHTML = document.getElementById("social-net-container");
const dHInicioHTML = document.getElementById("dia-hora-inicio");
const dHTerminoHTML = document.getElementById("dia-hora-termino");
const descripcionHTML = document.getElementById("descripcion-evento");
const tipoComidaHTML = document.getElementById("tipo-comida");
const fotoComidaHTML = document.getElementById("file-input-container");

let regionsLoaded = false;
let regionChanged = false;
let socialNetsCounter;
let photosCounter;

const regionesComunasObj = {  
    "Región de Tarapacá": ["Camiña","Huara","Pozo Almonte","Iquique","Pica","Colchane","Alto Hospicio"],
    "Región de Antofagasta": ["Tocopilla","Maria Elena","Ollague","Calama","San Pedro Atacama","Sierra Gorda","Mejillones","Antofagasta","Taltal"],
    "Región de Atacama": ["Diego de Almagro","Chañaral","Caldera","Copiapo","Tierra Amarilla","Huasco","Freirina","Vallenar","Alto del Carmen"],
    "Región de Coquimbo": ["La Higuera","La Serena","Vicuña","Paihuano","Coquimbo","Andacollo","Rio Hurtado","Ovalle","Monte Patria","Punitaqui","Combarbala","Mincha","Illapel","Salamanca","Los Vilos"],
    "Región de Valparaíso": ["Petorca","Cabildo","Papudo","La Ligua","Zapallar","Putaendo","Santa Maria","San Felipe","Pencahue","Catemu","Llay Llay","Nogales","La Calera","Hijuelas","La Cruz","Quillota","Olmue","Limache","Los Andes","Rinconada","Calle Larga","San Esteban","Puchuncavi","Quintero","Viña del Mar","Villa Alemana","Quilpue","Valparaiso","Juan Fernandez","Casablanca","Concon","Isla de Pascua","Algarrobo","El Quisco","El Tabo","Cartagena","San Antonio","Santo Domingo"],
    "Región del Libertador Bernardo Ohiggins": ["Mostazal","Codegua","Graneros","Machali","Rancagua","Olivar","Doñihue","Requinoa","Coinco","Coltauco","Quinta Tilcoco","Las Cabras","Rengo","Peumo","Pichidegua","Malloa","San Vicente","Navidad","La Estrella","Marchigue","Pichilemu","Litueche","Paredones","San Fernando","Peralillo","Placilla","Chimbarongo","Palmilla","Nancagua","Santa Cruz","Pumanque","Chepica","Lolol"],
    "Región del Maule": ["Teno","Romeral","Rauco","Curico","Sagrada Familia","Hualañe","Vichuquen","Molina","Licanten","Rio Claro","Curepto","Pelarco","Talca","Pencahue","San Clemente","Constitucion","Maule","Empedrado","San Rafael","San Javier","Colbun","Villa Alegre","Yerbas Buenas","Linares","Longavi","Retiro","Parral","Chanco","Pelluhue","Cauquenes"],
    "Región del Biobío": ["Tome","Florida","Penco","Talcahuano","Concepcion","Hualqui","Coronel","Lota","Santa Juana","Chiguayante","San Pedro de la Paz","Hualpen","Cabrero","Yumbel","Tucapel","Antuco","San Rosendo","Laja","Quilleco","Los Angeles","Nacimiento","Negrete","Santa Barbara","Quilaco","Mulchen","Alto Bio Bio","Arauco","Curanilahue","Los Alamos","Lebu","Cañete","Contulmo","Tirua"],
    "Región de La Araucanía": ["Renaico","Angol","Collipulli","Los Sauces","Puren","Ercilla","Lumaco","Victoria","Traiguen","Curacautin","Lonquimay","Perquenco","Galvarino","Lautaro","Vilcun","Temuco","Carahue","Melipeuco","Nueva Imperial","Puerto Saavedra","Cunco","Freire","Pitrufquen","Teodoro Schmidt","Gorbea","Pucon","Villarrica","Tolten","Curarrehue","Loncoche","Padre Las Casas","Cholchol"],
    "Región de Los Lagos": ["San Pablo","San Juan","Osorno","Puyehue","Rio Negro","Purranque","Puerto Octay","Frutillar","Fresia","Llanquihue","Puerto Varas","Los Muermos","Puerto Montt","Maullin","Calbuco","Cochamo","Ancud","Quemchi","Dalcahue","Curaco de Velez","Castro","Chonchi","Queilen","Quellon","Quinchao","Puqueldon","Chaiten","Futaleufu","Palena","Hualaihue"],
    "Región Aisén del General Carlos Ibáñez del Campo": ["Guaitecas","Cisnes","Aysen","Coyhaique","Lago Verde","Rio Iba?ez","Chile Chico","Cochrane","Tortel","O''Higins"],
    "Región de Magallanes y la Antártica Chilena": ["Torres del Paine","Puerto Natales","Laguna Blanca","San Gregorio","Rio Verde","Punta Arenas","Porvenir","Primavera","Timaukel","Antartica"],
    "Región Metropolitana de Santiago": ["Tiltil","Colina","Lampa","Conchali","Quilicura","Renca","Las Condes","Pudahuel","Quinta Normal","Providencia","Santiago","La Reina","Ñuñoa","San Miguel","Maipu","La Cisterna","La Florida","La Granja","Independencia","Huechuraba","Recoleta","Vitacura","Lo Barrenechea","Macul","Peñalolen","San Joaquin","La Pintana","San Ramon","El Bosque","Pedro Aguirre Cerda","Lo Espejo","Estacion Central","Cerrillos","Lo Prado","Cerro Navia","San Jose de Maipo","Puente Alto","Pirque","San Bernardo","Calera de Tango","Buin","Paine","Peñaflor","Talagante","El Monte","Isla de Maipo","Curacavi","Maria Pinto","Melipilla","San Pedro","Alhue","Padre Hurtado"],
    "Región de Los Ríos": ["Lanco","Mariquina","Panguipulli","Mafil","Valdivia","Los Lagos","Corral","Paillaco","Futrono","Lago Ranco","La Union","Rio Bueno"],
    "Región Arica y Parinacota": ["Gral. Lagos","Putre","Arica","Camarones"],
    "Región del Ñuble": ["Cobquecura","Ñiquen","San Fabian","San Carlos","Quirihue","Ninhue","Trehuaco","San Nicolas","Coihueco","Chillan","Portezuelo","Pinto","Coelemu","Bulnes","San Ignacio","Ranquil","Quillon","El Carmen","Pemuco","Yungay","Chillan Viejo"]
}

let foodTypes = ['Al Paso', 'Alemana', 'Árabe', 'Argentina', 'Asiática', 'Australiana', 'Brasileña', 'Café y Snacks', 'Carnes', 'Casera', 'Chilena', 'China', 'Cocina de Autor', 'Comida Rápida', 'Completos', 'Coreana', 'Cubana', 'Española', 'Exótica', 'Francesa', 'Gringa', 'Hamburguesa', 'Helados', 'India', 'Internacional', 'Italiana', 'Latinoamericana', 'Mediterránea', 'Mexicana', 'Nikkei', 'Parrillada', 'Peruana', 'Pescados y mariscos', 'Picoteos', 'Pizzas', 'Pollos y Pavos', 'Saludable', 'Sándwiches', 'Suiza', 'Japonesa', 'Sushi', 'Tapas', 'Thai', 'Vegana', 'Vegetariana'];

function initRegions(regName) {
	for (const item of Object.entries(regionesComunasObj) ) {
		let option = document.createElement("option");
		option.value = item[0];
		option.innerText = item[0];
		if (item[0] == regName) {
			option.setAttribute("selected", "true");
		}
		regionesHTML.appendChild(option);
	}
	regionsLoaded = true;
}

function initCommunes(comName) {
	const region = document.getElementById("region").value;
    const comunas = regionesComunasObj[region];

	for (let i = 0; i < comunas.length; i++) {
		let option = document.createElement("option");
		option.value = comunas[i];
		option.innerText = comunas[i];
		if (comunas[i] == comName) {
			option.setAttribute("selected", "true")
		}
		comunasHTML.appendChild(option);
	}
	communesInit = true;
}

function initSocialNets(counter) {
	socialNetsCounter = counter;
}

function initPhotos(counter) {
	photosCounter = counter;
}

function initTextField(element, val) {
	element.value = val;
}

function initType(aFoodType) {
    for (let i = 0; i < foodTypes.length; i++) {
		let option = document.createElement("option");
		option.value = foodTypes[i];
		option.innerText = foodTypes[i];
		if (foodTypes[i] == aFoodType) {
			option.setAttribute("selected", "true")
		}
		tipoComidaHTML.appendChild(option);
	}
}


function populateForm(regName, commName, sector, userName, email, celNum, dHI, dHT, desc, snCount, phCount, typeFood, svInvalidField) {
	if (svInvalidField) {
        valNotifications.style.display = "block";
    }
    initRegions(regName);
	initCommunes(commName);
	initTextField(sectorHTML, sector);
	initTextField(nombreHTML, userName);
	initTextField(emailHTML, email);
	initTextField(celularHTML, celNum);
	initSocialNets(snCount);
	initTextField(dHInicioHTML, dHI);
	initTextField(dHTerminoHTML, dHT);
	initTextField(descripcionHTML, desc);
	initType(typeFood);
	initPhotos(phCount);
}


// MANEJO DE REGIONES Y COMUNAS:
function loadRegions() {
	if (!regionsLoaded) {
        for (const item of Object.entries(regionesComunasObj) ) {
            let option = document.createElement("option");
            option.value = item[0];
            option.innerText = item[0];
            regionesHTML.appendChild(option);
        }
        regionsLoaded = true;
    }
}

function enableCommunes() {
    comunasHTML.disabled = false;
    // Se limpian las comunas previas.
    let n = comunasHTML.childElementCount;
    for (i = n - 1; i >= 0; i--) {
        comunasHTML.remove(i);
    }

	let defaultOption = document.createElement("option");
	defaultOption.value = "";
	defaultOption.innerText = "Seleccione una comuna";
	defaultOption.setAttribute("hidden", "true")
	defaultOption.setAttribute("selected", "true")
	comunasHTML.appendChild(defaultOption)

    regionChanged = true;
}

function loadCommunes() {
	if (regionChanged) {
        const region = document.getElementById("region").value;
        const comunas = regionesComunasObj[region];
    
        // Se limpian las comunas previas.
        let n = comunasHTML.childElementCount;
        for (i = n - 1; i > 0; i--) {
            comunasHTML.remove(i);
        }
  
        // Se rellena la lista con las nuevas comunas.
        for (let i = 0; i < comunas.length; i++) {
            let option = document.createElement("option");
            option.value = comunas[i];
            option.innerText = comunas[i];
            comunasHTML.appendChild(option);
        }
        regionChanged = false;
    }
}

// MANEJO DE INPUT REDES SOCIALES:

let containerRedSocial = document.getElementById("social-net-container");
let selectorRedSocialHTML = document.getElementById("red-social");
let redesPosibles = ["twitter", "instagram", "facebook", "tiktok", "otra"];
 
function generateTextInput() {
    let redSocial = selectorRedSocialHTML.value.toLowerCase()

    let div = document.createElement("div");
    div.setAttribute("class", "form-input");

    let divLabel = document.createElement("div");
    let label = document.createElement("label");
    label.innerText = "URL perfil de " + redSocial;
    label.setAttribute("for", "sn-"+socialNetsCounter+"-"+redSocial);
    divLabel.appendChild(label);

    let textInput = document.createElement("input");
    textInput.setAttribute("name", "sn-"+socialNetsCounter+"-"+redSocial);
    textInput.setAttribute("id", "sn-"+socialNetsCounter+"-"+redSocial);
    textInput.setAttribute("class", "sn-txt-input");
    textInput.setAttribute("type", "text");

    div.appendChild(divLabel);
    div.appendChild(textInput);

    socialNetsCounter++;
    containerRedSocial.appendChild(div);
}

function handleSocialNetInput() {
    if (socialNetsCounter<5){
        generateTextInput();
        selectorRedSocialHTML.value=""
    }
}

// MANEJO DE INPUT FOTOS:

let containerFileInput = document.getElementById("file-input-container");
let addFileInputButton = document.getElementById("add-file-input-btn");

function generateFileInput() {
    let div = document.createElement("div");
    div.setAttribute("class", "form-input");

    let divLabel = document.createElement("div");
    let label = document.createElement("label");
    label.innerText = "Foto extra (Nro. "+ photosCounter+")";
    label.setAttribute("for", "file-input-"+photosCounter);
    divLabel.appendChild(label);

    let divFileInput = document.createElement("div");
    divFileInput.setAttribute("class", "input-file-btns-container");
    let fileInput = document.createElement("input");
    fileInput.setAttribute("name", "file-input-"+photosCounter);
    fileInput.setAttribute("id", "file-input-"+photosCounter);
    fileInput.setAttribute("type", "file");
    fileInput.required = true;
    divFileInput.appendChild(fileInput);

    div.appendChild(divLabel);
    div.appendChild(divFileInput);

    photosCounter++;
    containerFileInput.appendChild(div);
}

function handleInputFile() {
    if (photosCounter<5){
        generateFileInput();
    }
}