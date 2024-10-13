import asyncio
import re
import pygame
from rich import print
# 00000000000000000000000000000000,XInput Controller,a:b0,b:b1,back:b6,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,
# dpup:h0.1,guide:b10,leftshoulder:b4,leftstick:b8,lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b9,righttrigger:a5,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Windows,
# SDL_GAMECONTROLLERCONFIG=030000005e040000ea02000000007801,XInput ControllerA-B,
# platform:Windows,a:b1,b:b0,
# import os
# os.environ["SDL_GAMECONTROLLERCONFIG"] =\
#     "0300938d5e040000ea02000000007200,XInput ControllerA-B,platform:Windows,a:b1,b:b0,"
# a = "030000005e040000ea02000000000000"

# initialise the joystick module
import sys
import platform

if sys.platform == "emscripten":
    IS_WEB = True
    platform.window.canvas.style.imageRendering = "pixelated"
else:
    IS_WEB = False

pygame.init()
pygame.joystick.init()
DUMMY_JOYSTICK_ID = 101
USE_EMULATION = False

if USE_EMULATION:
    IS_WEB = True

DUMMY_DATA: list[tuple[str, int | float]] = [
    ("button-0", 1),
    ("button-1", 0),
    ("button-2", 1),
    ("axis-0", -1.0),
    ("axis-1", 1.0),
    ("axis-4", 0.0),
    ("hat-0-X", -1),
    ("hat-0-Y", 1),
    ("ball-0-X", 1.0),
    ("ball-0-Y", -1.0),
]
MOBILE_INPUTS: dict[str, float] = {}

# define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# define font
font_size = 30
font = pygame.font.SysFont(None, font_size)

VALUE_X_OFFSET = 200
ROW_HEIGHT = font.get_linesize()
LABEL_COLOR = pygame.Color("royalblue")
VALUE_COLOR = pygame.Color("crimson")
SLIDER_BORDER = 4
SLIDER_SPACING = 1
FPS = 60
JOY_OFFSET = 50


def draw_text(screen:  pygame.Surface, text: str, font: pygame.Font, text_col: pygame.Color, x: int, y: int) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_slider(screen:  pygame.Surface, val: float, x: int, y: int) -> None:
    pygame.draw.rect(
        screen,
        LABEL_COLOR,
        (x, y + SLIDER_SPACING,
         VALUE_X_OFFSET, ROW_HEIGHT - 2 * SLIDER_SPACING),
        SLIDER_BORDER)

    pygame.draw.rect(
        screen,
        VALUE_COLOR,
        (x + SLIDER_BORDER, y + SLIDER_BORDER + SLIDER_SPACING,
         ((val + 1.0) / 2.0) * (VALUE_X_OFFSET - 2 * SLIDER_BORDER), ROW_HEIGHT - 2 * (SLIDER_BORDER + SLIDER_SPACING)))


def draw_text_property(screen:  pygame.Surface, label: str, val: str, x: int, y: int) -> None:
    draw_text(screen, label, font, LABEL_COLOR, x, y)
    draw_text(screen, val, font, VALUE_COLOR, x + VALUE_X_OFFSET, y)


def draw_float_property(screen:  pygame.Surface, label: str, val: float, x: int, y: int) -> None:
    draw_text(screen, label, font, LABEL_COLOR, x, y)
    draw_slider(screen, val, x + VALUE_X_OFFSET, y)


def draw_properties(screen:  pygame.Surface, properties: list[tuple[int, str, str | float | int]]) -> None:
    for row_no, property in enumerate(properties):
        x = JOY_OFFSET + property[0] * (VALUE_X_OFFSET + JOY_OFFSET) * 2
        y = JOY_OFFSET + (row_no * ROW_HEIGHT)

        if type(property[2]) is str:
            draw_text_property(screen, property[1], property[2], x, y)
        elif type(property[2]) in [float, int]:
            draw_float_property(screen, property[1], float(property[2]), x, y)
        else:
            print(f"Unknown property type {type(property[2])}")


class Joystick():
    def __init__(self, id: int) -> None:
        self.id = id
        if id == DUMMY_JOYSTICK_ID:
            self.joy = DummyJoystick(DUMMY_JOYSTICK_ID)
        else:
            self.joy = pygame.joystick.Joystick(id)  # type: ignore[assignment]
        self.guid = self.joy.get_guid()
        self.name = self.joy.get_name()
        self.power_level = self.joy.get_power_level()
        self.numaxes     = self.joy.get_numaxes()
        self.numballs    = self.joy.get_numballs()
        self.numbuttons  = self.joy.get_numbuttons()
        self.numhats     = self.joy.get_numhats()

        self.axis: list[float] = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball: list[tuple[float, float]] = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button: list[bool] = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat: list[tuple[int, int]] = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


class DummyJoystick():
    def __init__(self, id: int) -> None:
        self.id = id
        self.guid = "00000000000000000000000000000000"
        self.name = "Dummy Joystick"
        self.power_level = "unknown"
        self.numaxes    = 6
        self.numballs   = 1
        self.numbuttons = 16
        self.numhats    = 1

    def quit(self) -> None:
        ...

    def get_init(self) -> bool:
        return True

    def get_id(self) -> int:
        return self.id

    def get_instance_id(self) -> int:
        return self.id

    def get_guid(self) -> str:
        return self.guid

    def get_power_level(self) -> str:
        return self.power_level

    def get_name(self) -> str:
        return self.name

    def get_numaxes(self) -> int:
        return self.numaxes

    def get_axis(self, axis_number: int, /) -> float:
        return 0.0

    def get_numballs(self) -> int:
        return self.numballs

    def get_ball(self, ball_number: int, /) -> tuple[float, float]:
        return (0.0, 0.0)

    def get_numbuttons(self) -> int:
        return self.numbuttons

    def get_button(self, button: int, /) -> bool:
        return False

    def get_numhats(self) -> int:
        return self.numhats

    def get_hat(self, hat_number: int, /) -> tuple[int, int]:
        return (0, 0)

    def rumble(
        self, low_frequency: float, high_frequency: float, duration: int
    ) -> bool:
        return False

    def stop_rumble(self) -> None:
        ...


def draw_joystick(screen:  pygame.Surface, id: int, joystick: Joystick) -> None:
    if id == DUMMY_JOYSTICK_ID:
        offset = 0
        rumble = ""
    else:
        offset = id
        rumble = f"Press [{id + 1}] to test vibrations (rumble)"
    properties: list[tuple[int, str, str | float]] = []
    properties.append((offset, f"GUID:{joystick.guid}", ""))
    properties.append((offset, rumble, ""))
    properties.append((offset, "Name:", str(joystick.name)))
    properties.append((offset, "Battery level:", joystick.power_level))
    properties.append((offset, "No. of axes:", str(joystick.numaxes)))
    properties.append((offset, "No. of balls:", str(joystick.numballs)))
    properties.append((offset, "No. of hats:", str(joystick.numhats)))
    properties.append((offset, "No. of buttons:", str(joystick.numbuttons)))

    for axis_id in range(joystick.numaxes):
        properties.append((offset, f"Axis({axis_id}):", joystick.axis[axis_id]))

    for ball_id in range(joystick.numballs):
        properties.append((offset, f"Ball({ball_id}).x:", str(joystick.ball[ball_id][0])))
        properties.append((offset, f"Ball({ball_id}).y:", str(joystick.ball[ball_id][1])))

    for hat_id in range(joystick.numhats):
        properties.append((offset, f"Hat({hat_id}).x:", str(joystick.hat[hat_id][0])))
        properties.append((offset, f"Hat({hat_id}).y:", str(joystick.hat[hat_id][1])))

    properties.append((offset, "Buttons pressed:", ", ".join((str(no) for no, b in enumerate(joystick.button) if b))))

    draw_properties(screen, properties)


def process_events(screen:  pygame.Surface, joysticks: dict[int, Joystick]) -> bool:

    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            id = event.device_index
            joysticks[id] = Joystick(id)
        elif event.type == pygame.JOYDEVICEREMOVED:
            id = event.instance_id
            if id in joysticks:
                del joysticks[id]
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.JOYAXISMOTION:
            joysticks[event.joy].axis[event.axis] = event.value
        elif event.type == pygame.JOYBALLMOTION:
            joysticks[event.joy].ball[event.ball] = event.rel
        elif event.type == pygame.JOYHATMOTION:
            joysticks[event.joy].hat[event.hat] = event.value
        elif event.type == pygame.JOYBUTTONUP:
            joysticks[event.joy].button[event.button] = False
        elif event.type == pygame.JOYBUTTONDOWN:
            joysticks[event.joy].button[event.button] = True
        elif event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q]:
            return False
        elif event.type == pygame.KEYDOWN and event.key in range(pygame.K_1, pygame.K_9 + 1):
            id = event.key - pygame.K_1
            if id in joysticks:
                joysticks[id].joy.rumble(1, 1, 250)

    if IS_WEB:
        if USE_EMULATION:
            data = DUMMY_DATA
        else:
            if platform.window.pressedButtons:  # type: ignore[attr-defined]
                data = platform.window.pressedButtons  # type: ignore[attr-defined]
            else:
                data = []
                # print("NO pressedButtons !!!")
                draw_text(screen, "pressedButtons object not available !!!", font, LABEL_COLOR, 50, 300)

        # platform.window.console.log("[#########] pyton got the event")
        # print("pressedButtons found !!!")

        # print(type(platform.window.pressedButtons))
        # print(platform.window.pressedButtons)

        # platform.window.console.log(platform.window.pressedButtons)

        for i, el_data in enumerate(data):
            draw_text_property(
                screen, str(el_data[0]), str(el_data[1]),
                (VALUE_X_OFFSET + JOY_OFFSET) * 2, 50 + (i * ROW_HEIGHT))

            elements = str(el_data[0]).split("-")
            el_type = elements[0]
            el_no_str = elements[1]
            try:
                el_no = int(el_no_str)
            except ValueError:
                el_no = -1

            dj = joysticks[DUMMY_JOYSTICK_ID]
            if el_type == "button" and el_no > -1 and el_no < dj.numbuttons:
                joysticks[DUMMY_JOYSTICK_ID].button[el_no] = bool(el_data[1])
            if el_type == "axis" and el_no > -1 and el_no < dj.numaxes:
                joysticks[DUMMY_JOYSTICK_ID].axis[el_no] = float(el_data[1])
            if el_type == "hat" and el_no > -1 and el_no < dj.numhats:
                prev_hat_val = joysticks[DUMMY_JOYSTICK_ID].hat[el_no]
                if elements[2] == "X":
                    joysticks[DUMMY_JOYSTICK_ID].hat[el_no] = (int(el_data[1]), prev_hat_val[1])
                elif elements[2] == "Y":
                    joysticks[DUMMY_JOYSTICK_ID].hat[el_no] = (prev_hat_val[0],     int(el_data[1]))
            if el_type == "ball" and el_no > -1 and el_no < dj.numballs:
                prev_ball_val = joysticks[DUMMY_JOYSTICK_ID].ball[el_no]
                if elements[2] == "X":
                    joysticks[DUMMY_JOYSTICK_ID].ball[el_no] = (float(el_data[1]), prev_ball_val[1])
                elif elements[2] == "Y":
                    joysticks[DUMMY_JOYSTICK_ID].ball[el_no] = (prev_ball_val[0],     float(el_data[1]))

    return True


async def main() -> None:

    # create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Gamepad demo")

    # create clock for setting game frame rate
    clock = pygame.time.Clock()

    # create empty list to store joysticks
    joysticks: dict[int, Joystick] = {}
    if IS_WEB:
        dj = Joystick(DUMMY_JOYSTICK_ID)
        joysticks[DUMMY_JOYSTICK_ID] = dj

    # game loop
    run = True

    while run:

        clock.tick(FPS)

        # update background
        screen.fill(pygame.Color("midnightblue"))

        # show number of connected joysticks
        draw_text_property(screen, "Controllers count:", str(pygame.joystick.get_count()), 10, 10)
        for id, joystick in joysticks.items():
            draw_joystick(screen, id, joystick)

        # emulate 2 controllers
        # if len(joysticks.keys()) > 0:
        #     key = list(joysticks.keys())[0]
        #     draw_joystick(screen, 0, joysticks[key])
        #     draw_joystick(screen, 1, joysticks[key])

        # event handler
        run = process_events(screen, joysticks)

        # update display
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
