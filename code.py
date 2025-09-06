# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

from random import randrange
import board
import displayio
import framebufferio
import rgbmatrix
import adafruit_imageload
import time
import keypad
from adafruit_display_shapes.rect import Rect

## Multiple panel guide
### https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/advanced-multiple-panels
## rgbmatrix lib
### https://circuitpython.readthedocs.io/en/latest/shared-bindings/rgbmatrix/index.html
## Display IO Lib
### https://learn.adafruit.com/circuitpython-display-support-using-displayio
## Display IO API Doc
### https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/

## UI
### https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart
## Transparent BMP
### https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics


bit_depth = 4
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine = True

width = base_width * chain_across
height = base_height * tile_down
rgb_pins=[
    board.MTX_R1,
    board.MTX_G1,
    board.MTX_B1,
    board.MTX_R2,
    board.MTX_G2,
    board.MTX_B2
]
addr_pins=[
    board.MTX_ADDRA,
    board.MTX_ADDRB,
    board.MTX_ADDRC,
    board.MTX_ADDRD,
    # board.MTX_ADDRE,
]
clock_pin = board.MTX_CLK
latch_pin = board.MTX_LAT
oe_pin = board.MTX_OE


displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=width,
    height=height,
    bit_depth=bit_depth,
    rgb_pins=rgb_pins,
    addr_pins=addr_pins,
    clock_pin=clock_pin,
    latch_pin=latch_pin,
    output_enable_pin=oe_pin,
    tile=tile_down,
    serpentine=serpentine,
)

display = framebufferio.FramebufferDisplay(matrix)

# Get the display brightness (0.0 to 1.0)
brightness = 0.05
display.brightness = brightness


# --- Setup buttons ---
buttons = keypad.Keys((board.BUTTON_UP, board.BUTTON_DOWN), value_when_pressed=False, pull=True)

# Colors
# Online tool used to get the correct shade
# https://www.color-hex.com/color/6633ff
beige = 0xfc9# ffcc99 -> 66513d
pink = 0xf9f# ff99ff -> 663d66
fiusha = 0xf39# FF3399 -> 66143d
grey = 0x999# 999999 -> 3d3d3d
salmon = 0xf99# ff9999 -> 663d3d
white = 0xfff# ffffff -> 666666
key = 0x00ff00
bg = 0x061e39# 0f4d8f -> 061e39
red = 0x660000# ff0000 -> 660000
orange = 0x663d00# ff9900 -> 663d00
yellow =0x666600# ffff00 -> 666600
green = 0x146600# 33ff00 -> 146600
blue = 0x003d66# 0099ff -> 003d66
purple = 0x6633ff# 6633ff -> 281466

# Groups to hold sprites
group = displayio.Group(scale=2)
group_rainbow = displayio.Group()
group_cat = displayio.Group()
group_star = displayio.Group()

# Background
# Bitmap - width, height, value_count
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/index.html#displayio.Bitmap
color_bitmap = displayio.Bitmap(
        64,# width
        64,# height
        1# number of possible pixel values
    )
# Palette - color_count
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/index.html#displayio.Palette
color_palette = displayio.Palette(
        1# number colors
    )
color_palette[0] = bg

# TileGrid - bitmap, pixel_shader, width, height, tile_width, tile_height, default_tile, x, y
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/index.html#displayio.TileGrid
bg_sprite = displayio.TileGrid(
        color_bitmap,# 2D array of pixels
        pixel_shader=color_palette,# list of color values
        x=0,# X position within the parent.
        y=0# Y position within the parent.
    )
group.append(bg_sprite)

# Load the sprite sheet (bitmap)
sprite_star, palette_star = adafruit_imageload.load(
        "/stars.bmp",
        bitmap=displayio.Bitmap,
        palette=displayio.Palette
    )
palette_star.make_transparent(0)

# Create a sprite (tilegrid)
star = displayio.TileGrid(sprite_star, pixel_shader=palette_star,
                            width = 3,# Number of tiles x
                            height = 2,# Number of tiles y
                            tile_width = 5,# Tile width in pixels
                            tile_height = 5,# Tile height in pixels
                            x = 0,
                            y = 0
                        )# Tile height in pixels
# Add the sprite to the Group
group_star.append(star)

star_a = displayio.TileGrid(sprite_star, pixel_shader=palette_star,
                            width = 3,# Number of tiles x
                            height = 2,# Number of tiles y
                            tile_width = 5,# Tile width in pixels
                            tile_height = 5,# Tile height in pixels
                            x = 7,
                            y = 7
                        )
star_b = displayio.TileGrid(sprite_star, pixel_shader=palette_star,
                            width = 3,# Number of tiles x
                            height = 2,# Number of tiles y
                            tile_width = 5,# Tile width in pixels
                            tile_height = 5,# Tile height in pixels
                            x = 14,
                            y = 14
                        )
star_c = displayio.TileGrid(sprite_star, pixel_shader=palette_star,
                            width = 3,# Number of tiles x
                            height = 2,# Number of tiles y
                            tile_width = 5,# Tile width in pixels
                            tile_height = 5,# Tile height in pixels
                            x = 27,
                            y = 27
                        )
group_star.append(star_a)
group_star.append(star_b)
group_star.append(star_c)

# rectangle - X, Y, width, height
rec_red = Rect(0, 7, 5, 2, fill=red)
rec_orange = Rect(0, 9, 5, 2, fill=orange)
rec_yellow = Rect(0, 11, 5, 2, fill=yellow)
rec_green = Rect(0, 13, 5, 2, fill=green)
rec_blue = Rect(0, 15, 5, 2, fill=blue)
rec_purple = Rect(0, 17, 5, 2, fill=purple)

group_rainbow.append(rec_red)
group_rainbow.append(rec_orange)
group_rainbow.append(rec_yellow)
group_rainbow.append(rec_green)
group_rainbow.append(rec_blue)
group_rainbow.append(rec_purple)


# Load the sprite sheet (bitmap)
sprite_cat, palette_cat = adafruit_imageload.load(
        "/original.bmp",
        bitmap=displayio.Bitmap,
        palette=displayio.Palette
    )
palette_cat.make_transparent(0)
# #00FF00
# index 0

# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_cat, pixel_shader=palette_cat,
                            width = 1,# Number of tiles x
                            height = 1,# Number of tiles y
                            tile_width = 34,# Tile width in pixels
                            tile_height = 21,# Tile height in pixels
                            x = -2,
                            y = 4
                        )# Tile height in pixels

# Add the sprite to the Group
group_cat.append(sprite)

# Add child groups to parent group
group.append(group_star)
group.append(group_rainbow)
group.append(group_cat)


# Add the Group to the Display
display.root_group = group

# Set sprite location
group.x = 0
group.y = 0

source_index = 0
rainbow_index = 0
star_index = 0
star_a_index = 2
star_b_index = 4
star_c_index = 6
t = time.monotonic()
p = time.monotonic()
frame = 0
rate = 1
frame_b = 0
rate_b = 2

# --- Main loop ---
while True:
    event = buttons.events.get()
    if event:
        if event.pressed:
            if event.key_number == 0:   # UP button
                brightness = min(1.0, brightness + 0.05)
                display.brightness = brightness
            elif event.key_number == 1: # DOWN button
                brightness = max(0.0, brightness - 0.05)
                display.brightness = brightness
    
    t = time.monotonic()
    if (p + 0.1) < t:
        p = t
        frame += 1
        frame_b += 1

    if frame == rate:
        # Loop through each sprite in the sprite sheet
        sprite[0] = source_index % 6
        source_index -= 1

        group_rainbow.y = rainbow_index % 2
        rainbow_index += 1
        frame = 0
    if frame_b == rate_b:
        frame_b = 0

        star[0] = star_index % 6
        star_index += 1

        star_a[0] = star_a_index % 6
        star_a_index += 1

        star_b[0] = star_b_index % 6
        star_b_index += 1

        star_c[0] = star_c_index % 6
        star_c_index += 1
        
        if star.x < 0:
            star.x = randrange(0, 28)
            star.y = randrange(0, 28)
        if star_a.x < 0:
            star_a.x = randrange(0, 28)
            star_a.y = randrange(0, 28)
        if star_b.x < 0:
            star_b.x = randrange(0, 30)
            star_b.y = randrange(0, 28)
        if star_c.x < 0:
            star_c.x = randrange(0, 32)
            star_c.y = randrange(0, 28)
        
        star.x -= 1
        star_a.x -= 1
        star_b.x -= 1
        star_c.x -= 1