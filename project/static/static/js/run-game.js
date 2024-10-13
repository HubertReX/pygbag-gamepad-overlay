var URL_GAME;
var GAME_FRAME;
var FS_DISPLAY;

const run_button_container =
    document.getElementById('gamepad_overlay__run-button-container');
const game_container =
    document.getElementById('gamepad_overlay__game-container');
const game_frame_fsbutton =
    document.getElementById('gamepad_overlay__game-frame-fsbutton');
const run_button =
    document.getElementById('gamepad_overlay__run-button');

// modifiers
document.addEventListener('webkitfullscreenchange', fullscreenChange);
document.addEventListener('mozfullscreenchange', fullscreenChange);
document.addEventListener('fullscreenchange', fullscreenChange);
document.addEventListener('MSFullscreenChange', fullscreenChange);

// listeners
run_button.addEventListener('click', (e) => {
    run_button_container.style.display = 'none';
    game_container.style.display = 'block';
    GAME_FRAME.src = URL_GAME;
});

// fullscreen

function init_fullscreen_mode() {
    if (document.fullscreenEnabled ||
        document.webkitFullscreenEnabled ||
        document.mozFullScreenEnabled ||
        document.msFullscreenEnabled) {
        if (FS_DISPLAY.requestFullscreen) {
            FS_DISPLAY.requestFullscreen();
        } else if (FS_DISPLAY.webkitRequestFullscreen) {
            FS_DISPLAY.webkitRequestFullscreen();
        } else if (FS_DISPLAY.mozRequestFullScreen) {
            FS_DISPLAY.mozRequestFullScreen();
        } else if (FS_DISPLAY.msRequestFullscreen) {
            FS_DISPLAY.msRequestFullscreen();
        }
    }
}

game_frame_fsbutton.addEventListener('click', (e) => {
    init_fullscreen_mode();
});

function fullscreenChange() {
    if (document.fullscreenEnabled ||
         document.webkitIsFullScreen ||
         document.mozFullScreen ||
         document.msFullscreenElement) {
      console.log('enter fullscreen');
    }
    else {
      console.log('quit fullscreen');
    }
}