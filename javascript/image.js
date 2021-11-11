const imageView = document.getElementById('image-view');
const imageViewBody = document.getElementById('image-view-body');
const images = document.querySelectorAll('.event-image');
const overlay = document.getElementById('image-view-overlay');
const closeButton = document.getElementById('close-btn');

const modifyImageViewBody = (img) => {
    while (imageViewBody.firstChild){
        imageViewBody.removeChild(imageViewBody.firstChild);
    }
    let newImage = document.createElement("img");
    newImage.setAttribute('src', img.src);
    newImage.setAttribute('class','image-view-target');
    imageViewBody.appendChild(newImage);
};

images.forEach(image => {
    image.addEventListener('click', () => {
        modifyImageViewBody(image);
        openImageView(imageView);
    });
});

overlay.addEventListener('click', () => {
    closeImageView(imageView);
});

closeButton.addEventListener('click', () => {
    closeImageView(imageView);
});

function openImageView(imageView) {
    if (imageView == null) return
    imageView.classList.add('active')
    overlay.classList.add('active')
}

function closeImageView(imageView) {
    if (imageView == null) return
    imageView.classList.remove('active')
    overlay.classList.remove('active')
}