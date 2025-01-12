import { fetchSentimentValue } from "./handler.js";

const searchInput = document.getElementById("searchBar");
const searchButton = document.getElementById("searchButton");
const sliderContainer = document.querySelector(".slider-container");
const popupScoreContainer = document.querySelector(".popup-score-container");
let isLoaded = false;

//Functions

function updateSlider(value) {
    const slider = document.getElementById('sentimentSlider');
    const pointer = document.getElementById('sliderPointer');
    document.getElementById('popup-score').textContent = value;

    sliderContainer.style.display = "block";
    popupScoreContainer.style.display = "inline-block";

    if (value >= -5 && value <= 5) {
        slider.value = value;

        const sliderWidth = slider.offsetWidth;
        const min = parseInt(slider.min, 10);
        const max = parseInt(slider.max, 10);
        const position = ((value - min) / (max - min)) * sliderWidth;

        pointer.style.left = `${position}px`;
    } else {
        console.error('Value out of range: Must be between -5 and 5.');
    }
}

function updateLoader() {
    if (isLoaded) {
        document.querySelector('.loader-container').style.display = 'flex';
    } else {
        document.querySelector('.loader-container').style.display = 'none';
    }
}


// Event listeners

searchInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        searchButton.click();
    }
});

searchButton.addEventListener("click", function () {
    const query = searchInput.value.trim();
    searchInput.style.border = "1px solid #ccc";
    sliderContainer.style.display = "none";
    popupScoreContainer.style.display = "none";

    if (query) {
        //Om sökrutan innehåller text så kallas fetch metoden som kommmunicerar med backenden
        isLoaded = true;
        updateLoader();

        fetchSentimentValue(query).then(response => {
            updateSlider(response);
            isLoaded = false;
            updateLoader();
        });
    } else {
        //Om sökrutan är tom så markeras den med en röd border
        isLoaded = false;
        updateLoader();
        searchInput.style.border = "1px solid red";
        sliderContainer.style.display = "none";
        popupScoreContainer.style.display = "none";
    }
});

document.addEventListener('DOMContentLoaded', () => {
    isLoaded = false;
    updateLoader();
});