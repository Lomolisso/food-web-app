// formulario:
const form = document.getElementById('event-form');

// pop-up:
const popUpTitle = document.getElementById('pop-up-title');
const popUpBody = document.getElementById('pop-up-body');
const popUpOverlay = document.getElementById('pop-up-overlay');
const confirmButton = document.getElementById('confirm-btn');
const regretButton = document.getElementById('regret-btn');


confirmButton.addEventListener('click', () => {
	form.submit();
});

regretButton.addEventListener('click', () => {
  	const popUp = regretButton.closest('.pop-up');
  	closePopUp(popUp);
});

function openPopUp(popUp) {
    if (popUp == null) return;
    popUp.classList.add('active');
    popUpOverlay.classList.add('active');
};

function closePopUp(popUp) {
    if (popUp == null) return;
    popUp.classList.remove('active');
    popUpOverlay.classList.remove('active');
};