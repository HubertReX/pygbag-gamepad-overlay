/*
    Depends on run-game.js
*/

var GAME_PAD;

const run_button_mobile_container =
    document.getElementById('gamepad_overlay__mobile__run-button-container');

const run_button_mobile =
    document.getElementById('gamepad_overlay__mobile__run-button');


run_button_mobile.addEventListener('click', (e) => {
    run_button_mobile_container.style.display = 'none';
    GAME_FRAME.style.display = 'block';
    GAME_FRAME.src = URL_GAME;
    if(GAME_PAD) {
        GAME_PAD.style.display = "block";
    }
});