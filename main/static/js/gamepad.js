const gamepad = document.getElementById('gamepad');
const dpad_c = document.querySelectorAll('#gamepad__1__container button');
const frame = document.getElementById('gamepad_overlay__mobile__game-frame');

var ACTIVE_BUTTONS = [];
// var BUTTONS_DATA = [];

window.oncontextmenu = function(event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
};

function toggle(button, on) {
    var opposite = null;
    if (button.id.includes("-left")) {
        var new_id = button.id.replace("-left", "-right");
        opposite = document.getElementById(new_id);
    }
    if (button.id.includes("-right")) {
        var new_id = button.id.replace("-right", "-left");
        opposite = document.getElementById(new_id);
    }
    for (let i = 0; i < ACTIVE_BUTTONS.length; i++) {
        if (ACTIVE_BUTTONS[i][0] == button.id) {
            var new_val = on ? parseFloat(button.getAttribute("val")) : 0.0;

            if (opposite !== null && new_val == 0.0) {
                new_val = parseFloat(opposite.getAttribute("val"))
            }
            ACTIVE_BUTTONS[i][1] = new_val
        }
    }

    if(on) {
        button.classList.add('pressed');
        // var is_present = false;
        // if (!is_present) {
        //     ACTIVE_BUTTONS.push([button, 1]);
        // }
        // if(!(ACTIVE_BUTTONS.includes(button.id)))
        //     ACTIVE_BUTTONS.push(button.id);
            // BUTTONS_DATA.push([button.id, 1]);
        // ACTIVE_BUTTONS.set(btn.id, 1);
        // if (ACTIVE_BUTTONS[btn.id] === undefined || ACTIVE_BUTTONS[btn.id] == 0) {
        // }
    }
    else {
        button.classList.remove('pressed');
        // ACTIVE_BUTTONS = ACTIVE_BUTTONS.filter(el => el[0] != button.id);
        // BUTTONS_DATA.push([button.id, 1]);
        // ACTIVE_BUTTONS.set(btn.id, 0);
    }
    // console.log("[#########] sending message:");
    // console.log("[#########]", ACTIVE_BUTTONS);
    frame.contentWindow.postMessage(ACTIVE_BUTTONS, "*");
}

function getButtonFromPoint(x, y) {
    dpad_c.forEach(btn => {
        const rect = btn.getBoundingClientRect();
        if(x >= rect.left && x <= rect.right &&
           y >= rect.top &&  y <= rect.bottom)
           return btn;
    })
}

function handleTouchOn(e) {
    e.preventDefault();
    const touches = e.touches;
    for(let i = 0; i < touches.length; i++) {
        const touch = touches[i];
        const button = getButtonFromPoint(touch.clientX, touch.clientY)
        if(button && button.tagName.toLowerCase() == 'button') {
            toggle(button, true);
        }
    }
}

function handleTouchOff(e) {
    e.preventDefault();
    const touches = e.changedTouches;
    for(let i = 0; i < touches.length; i++) {
        const touch = touches[i];
        const button = getButtonFromPoint(touch.clientX, touch.clientY)
        if(button && button.tagName.toLowerCase() == 'button') {
            toggle(button, false);
        }
    }
}

gamepad.addEventListener('touchstart', handleTouchOn, false);
gamepad.addEventListener('touchend', handleTouchOff, false);
// for (element in dpad_c) {
//     gamepad.addEventListener('onmousedown', handleTouchOn, false);
// }

dpad_c.forEach(button => {
    // console.log("[#########] adding event listeners", btn);
    ACTIVE_BUTTONS.push([button.id, 0]);
    // hasAttribute
    button.onmousedown = () => {
        toggle(button, true);
    };
    button.onmouseup = () => {
        toggle(button, false);
    };
    // btn.addEventListener('onmousedown',  ()=>  {
    //     toggle(this, true);
    // });
    // btn.addEventListener('onmouseup',  ()=>  {
    //     toggle(this, false);
    // });
});
