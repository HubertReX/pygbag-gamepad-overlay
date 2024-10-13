# Pygbag gamepad overlay demo

A template for pygbag that adds overlay that allows to emulated the use of gamepad when running Python (pygame-ce) game in web browser.

Current template is replication of this solution: [mobile-gamepads]([mobile-gamepads_en-us](https://github.com/Blendify-Games/PublicGists/blob/main/pygame-web/mobile-gamepads_en-us.md))

## Instructions

Install dependencies:

`pip install -r requirements.txt`

Start web server:

`python -m pygbag --ume_block 0 --template gamepad_overlay.tmpl --no_opt project`

Open

[http://localhost:8000/demo.html](http://localhost:8000/demo.html)
