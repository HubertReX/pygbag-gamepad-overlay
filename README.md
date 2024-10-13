# Pygbag gamepad overlay demo

A template for pygbag that adds overlay that allows to emulated the use of gamepad when running Python (pygame-ce) game in web browser.

Current template is replication of this solution: [mobile-gamepads](https://github.com/Blendify-Games/PublicGists/blob/main/pygame-web/mobile-gamepads_en-us.md)

Live demo: [link](https://hubertrex.github.io/pygbag-gamepad-overlay/main/demo.html)

For test purposes, the detection of mobile browser is skipped and a mobile version is enforced (to actually show the overlay).

## Instructions

Install dependencies:

`pip install -r requirements.txt`

Start web server:

`python -m pygbag --ume_block 0 --template gamepad_overlay.tmpl --no_opt project`

Open

[http://localhost:8000/demo.html](http://localhost:8000/demo.html)
