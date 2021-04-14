const popupElem = document.querySelector('.popup')
const popupImg = document.querySelector('.popup__image')

function openPopup(src) {
  popupImg.src = src;
  popupElem.style = 'display: flex';
}

function closePopup () {
  popupElem.style = 'display: none';
}
