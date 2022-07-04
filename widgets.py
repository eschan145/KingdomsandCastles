from arcade import create_rectangle_filled, draw_rectangle_outline, \
     draw_rectangle_filled, enable_timings,  get_fps, get_window, \
     load_texture, run,schedule, unschedule
from arcade import Sprite, SpriteList, Text, Window

from color import BLACK, COOL_BLACK, DARK_GRAY, DARK_SLATE_GRAY, RED, WHITE
from color import four_byte
from constants import BOTTOM, CENTER, DEFAULT_FONT, DISABLE_ALPHA, \
     ENTRY_BLINK_INTERVAL, LEFT, MULTIPLE, SINGLE, SLIDER_VELOCITY, \
     TOGGLE_FADE, TOGGLE_VELOCITY, TOP
from file import button, entry_normal, knob, none, slider_horizontal, \
     toggle_false, toggle_true, toggle_false_hover, toggle_true_hover
from geometry import Point
from key import ENTER, KEY_LEFT, KEY_RIGHT, \
     MOUSE_BUTTON_LEFT, SHIFT, SPACE, TAB
from key import Keys

from pyglet.event import EventDispatcher
from pyglet.text import decode_text
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout


MAX = 2**32

enable_timings()

def insert(index, text, add):
    return text[:index] + add + text[index:]

def delete(start, end, text):
    if len(text) > end:
        text = text[0: start:] + text[end + 1::]
    return text


class Container(EventDispatcher):
    def __init__(self, window=None, shadow=True):
        EventDispatcher.__init__(self)

        self.focus = None
        self.enable = True

        self.shadow = shadow
        
        self.widgets = SpriteList()

        self.window = window or get_window()
        
        self.window.push_handlers(self.on_key_press)

        self.window.background_color = WHITE
        
    def append(self, widget):
        self.widgets.append(widget)

        widget.container = self

    def draw(self):
        for widget in self.widgets:
            widget.draw()
            widget.frame.draw()

##            if self.shadow:
##                draw_rectangle_filled(widget.x, widget.y,
##                                      widget.width + 1, widget.height + 1,
##                                      BLACK)

    def draw_bbox(self, width=1, padding=0):
        for widget in self.widgets: widget.draw_bbox(width, padding)

    def exit(self):
        for widget in self.widgets: widget.destroy()

        self.enable = False
        
    def on_key_press(self, keys, modifiers):
       if keys == TAB:
            if modifiers & SHIFT:
                direction = -1
            else:
                direction = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                direction = 0
            
            self.focus = self.widgets[(i + direction) % len(self.widgets)]

            self.focus.focus = True

##            if isinstance(self.focus, Button):
##                self.focus.image.scale = FOCUS_SIZE
##            elif isinstance(self.focus, Toggle) or \
##                 isinstance(self.focus, Slider):
##                self.focus.bar.scale = FOCUS_SIZE
##                self.focus.knob.scale = FOCUS_SIZE
##
            for widget in self.widgets:
                if not widget == self.focus:
                    widget.focus = False


class Frame:
    def __init__(self, x, y, width=200, height=200, direction=BOTTOM):
        self.x = x
        self.y = y

        self.width = self.x
        self.height = self.y

        self.direction = direction
        self.color = WHITE

        self.widgets = []

        self.shape = create_rectangle_filled(self.x, self.y,
                                             10, 10,
                                             self.color)

    def append(self, widget):
        self.widgets.append(widget)

    def draw(self):
        self.shape.draw()

    
class Widget(Sprite, EventDispatcher):
    
    def __init__(self, image=none, scale=1.0, frame=None):
        Sprite.__init__(self, image, scale)

        self.frame = frame or Frame(0, 0)
        
        self.x = 0
        self.y = 0

        self.frame.append(self)

        self.hover = False
        self.press = False
        self.disable = False
        
        self.drag = False

        self.focus = False

        self.component = None
        self.container = None

        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
        
        self.frames = 0

        self.keys = Keys()

        self.window = get_window()

        self.window.push_handlers(
            self.on_key_press,
            self.on_key_release,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_mouse_drag,
            self.on_text_motion_select,
            self.on_update
        )

    def _get_x(self):
        return self._position[0]

    def _set_x(self, new_value):
        if new_value != self._position[0]:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._position = (new_value, self._position[1])
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_location(self)

    def _get_y(self):
        return self._position[1]

    def _set_y(self, new_value):
        if new_value != self._position[1]:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._position = (self._position[0], new_value)
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_location(self)

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

    def center(self, width, height):
        self.x = width / 2
        self.y = height / 2

    def _check_collision(self, x, y):
        return (0 < x - self.x < self.width and
                0 < y - self.y < self.height)

    def check_collision(self, x, y):
        if self._right and \
           self._left and \
           self._top and \
           self._bottom:
            return x > self._left and x < self._right and \
                   y > self._bottom and y < self._top
        
        return x > self.left and x < self.right and \
               y > self.bottom and y < self.top

    def draw_bbox(self, width=1, padding=0):
        draw_rectangle_outline(self.x, self.y,
                                      self.width, self.height,
                                      RED, width)

    def destroy(self):
        self.keys = []
        self.disable = True
        self.focus = False
        
        self.window.remove_handlers(
            self.on_key_press,
            self.on_key_release,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_mouse_drag,
            self.on_text_motion_select,
            self.on_update)
        
        self.remove_from_sprite_lists()
        
    def on_key_press(self, keys, modifiers):
        if self.disable:
            return
        
        self.dispatch_event("on_key", keys, modifiers)

        if self.focus:
            self.dispatch_event("on_focus")
            
    def on_key_release(self, keys, modifiers):
        if self.disable:
            return
        
        self.press = False

        self.dispatch_event("on_lift", keys, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.disable:
            return
        
        if self.check_collision(x, y):
            self.hover = True
            
            self.dispatch_event("on_hover", x, y, dx, dy)
        else:
            self.hover = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.disable:
            return
        
        if self.check_collision(x, y):
            self.press = True
            self.focus = True

            self.dispatch_event("on_press", x, y, buttons, modifiers)
            self.dispatch_event("on_focus")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.disable:
            return
        
        self.press = False

        if not self.check_collision(x, y):
            self.focus = False

        self.drag = False

        self.dispatch_event("on_release", x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.disable:
            return
        
        self.drag = True

        if self.check_collision(x, y):
            self.dispatch_event("on_drag", x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, mouse, direction):
        if self.disable:
            return
        
        if self.check_collision(x, y):
            if self.disable:
                return
        
            self.dispatch_event("on_scroll", x, y, mouse, direction)

    def on_text_motion_select(self, motion):
        self.dispatch_event("on_text_select", motion)

    def on_update(self, delta_time):
        self.frames += 1
        
        if self.component:
            self.x = self.component.x
            self.y = self.component.y
            
            self.width = self.component.width
            self.height = self.component.height

            self.left = self.component.left
            self.right = self.component.right
            self.top = self.component.top
            self.bottom = self.component.bottom

            self.hit_box = self.component.hit_box

            if self.disable:
                self.component.alpha = DISABLE_ALPHA

        if self.container and not self.container.enable:
            self.disable = True
            
        self.dispatch_event("update")

   
Widget.register_event_type("update")

Widget.register_event_type("on_key")
Widget.register_event_type("on_lift")
Widget.register_event_type("on_hover")
Widget.register_event_type("on_press")
Widget.register_event_type("on_release")
Widget.register_event_type("on_drag")
Widget.register_event_type("on_scroll")
Widget.register_event_type("on_focus")

Widget.register_event_type("on_text_select")


class Image(Widget):
    
    def __init__(self, image, x, y, scale=1):
        Widget.__init__(self, image, scale)

        self.image = image
        
        self.x = x
        self.y = y
            
    def on_enter(self, x, y, dx, dy):pass
    def on_leave(self, x, y, dx, dy):pass
    def on_key(self, keys, modifiers):pass
    def on_text(self, text):pass
    def on_press(self, x, y, buttons, modifiers):pass
    def on_release(self, x, y, buttons, modifiers):pass
    def update(self):pass
        
   
class Label(Widget):
    
    def __init__(self, text, x, y, frame=None,
                 colors=[BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)],
                 font=DEFAULT_FONT, title=False,
                 justify=LEFT, width=0, multiline=False,
                ):
        
        # For new arcade installations, change the self.label property in
        # Text to a HTMLLabel for HTML scripting
        #
        # self._label = pyglet.text.HTMLLabel(
        #     text=text,
        #     x=start_x,
        #     y=start_y,
        #     width=width,
        #     multiline=multiline
        # )
        #
        # The Label widget is the only widget with a LEFT x anchor.
        #

        if not text:
            text = "Label"
            
        self.label = Text(f"{text}", x, y,
                          anchor_x=LEFT, anchor_y=CENTER,
                          width=width, multiline=multiline)
        
        Widget.__init__(self, frame=frame)

        self.x = x + self.frame.x
        self.y = y + self.frame.y
        
        if self.frame.direction == TOP:
            self.x = self.frame.x - x
            self.y = self.frame.y - y
                
        self.text = text
        self.colors = colors
        self.font = font
        self.title = title
        self.justify = justify
        self.width = width
        self.multiline = multiline
    
        self.activated = False

        self.document = None
        self.length = 0
        
    def draw(self):
        self.label.draw()
        
        self.width = self.label._label.content_width
        self.height = self.label._label.content_height

        if self.text == "Label":
            self.label.visible = False
        else:
            self.label.visible = True

        self._left = self.label.left
        self._right = self.label.right
        self._top = self.label.top
        self._bottom = self.label.bottom
        
        self.activated = True

    def update(self):
        if not self.activated:
            return
        
        # The following section has been tested dozens of times. The performace
        # is incredibly slow, with about 1 fps for 100 Labels. Usually, for a
        # single Label the processing time is about one-hundredth of a second.
        #
        # With the .begin_update and .end_update functions for the label, the
        # processing time is much faster. With 100 Labels, the fps is about 8.
        
        self.label._label.begin_update()
        
        self.label.value = self.text
        self.label.x = self.x
        self.label.y = self.y
        self.label.font_name = self.font[0]
        self.label.font_size = self.font[1]
        self.label.opacity = self.alpha
        self.label.align = self.justify
        self.label.multiline = self.multiline

        self.label._label.end_update()

        self.document = self.label._label.document
        self.length = len(self.text)
            
        # States
        if self.hover:
            self.document.set_style(0, self.length,
                                    {"color" : four_byte(self.colors[1][0])})
        if self.press:
            self.document.set_style(0, self.length,
                                    {"color" : four_byte(self.colors[1][1])})
        if self.disable:
            self.document.set_style(0, self.length,
                                    {"color" : four_byte(self.colors[1][2])})

        if self.focus:
            self.document.set_style(0, self.length,
                                    {"color" : four_byte(self.colors[1][0])})

        
class Button(Widget):
    
    def __init__(
                 self, text, x, y, command=None, parameters=[], 
                 colors=["yellow", BLACK], font=DEFAULT_FONT,
                 callback=SINGLE
                ):

        # A two-component widget:
        #     - Image
        #     - Label

        self.image = Image(button[f"{colors[0]}_button_normal"], x, y)
        self.label = Label(text, x, y, font=font)
                
        Widget.__init__(self)
        
        self.text = text
        self.x = x
        self.y = y
        self.command = command
        self.parameters = parameters
        self.colors = colors
        self.font = font
        self.callback = callback

        self.keys = []

        self.normal_image = load_texture(button[f"{colors[0]}_button_normal"])
        self.hover_image = load_texture(button[f"{colors[0]}_button_hover"])
        self.press_image = load_texture(button[f"{colors[0]}_button_press"])
        self.disable_image = load_texture(button[f"{colors[0]}_button_disable"])
        
        self.activated = False

    def bind(self, *keys):
        self.keys = [*keys]
        return self.keys

    def unbind(self, *keys):
        for key in keys:
            self.keys.remove(key)
        return self.keys
        
    def invoke(self):
        if self.disable or not self.command:
            return
        
        self.press = True
        
        if self.parameters:
            self.command(self.parameters)
        else:
            self.command()
            
    def draw(self):
        self.image.draw()
        self.label.draw()
            
        self.label.text = self.text
        self.label.colors[0] = self.colors[1]
        self.label.font = self.font
        self.label.label.anchor_x = CENTER
        
        self.component = self.image
        
        self.activated = True

    def on_press(self, x, y, buttons, modifiers):
        if buttons == MOUSE_BUTTON_LEFT:
            self.invoke()
        
    def on_key(self, keys, modifiers):
        if keys == SPACE and self.focus:
            self.invoke()
            
        if isinstance(self.keys, list):
            if keys in self.keys:
                self.invoke()

        else:
            if self.keys == keys:
                self.invoke()
            
    def update(self):
        if not self.activated:
            return
        
        if self.hover:
            self.image.texture = self.hover_image
        if self.press:
            self.image.texture = self.press_image
        if self.disable:
            self.image.texture = self.disable_image
        if not self.hover \
           and not self.press \
           and not self.disable:
            self.image.texture = self.normal_image

        if self.callback == MULTIPLE and self.press:
            self.invoke()

        # .update is not called for the Label, as it is uneccessary for the
        # Label to switch colors on user events.
        
        self.image.update()


class Toggle(Widget):
    
    def __init__(
                 self, text, x, y,
                 colors=BLACK, font=DEFAULT_FONT,
                 default=True, padding=160
                ):

        # A three-component widget:
        #     - Image
        #     - Image
        #     - Label

        if default:
            image = toggle_true
        else:
            image = toggle_false
        
        self.bar = Image(image, x, y)
        self.knob = Image(knob, x, y)

        self.label = Label(knob, x, y, font=font)
                
        Widget.__init__(self)
        
        self.text = text
        self.x = x
        self.y = y
        self.colors = colors
        self.font = font
        self.padding = padding

        self.true_image = load_texture(toggle_true)
        self.false_image = load_texture(toggle_false)
        self.hover_true_image = load_texture(toggle_true_hover)
        self.hover_false_image = load_texture(toggle_false_hover)

        self.knob.left = self.bar.left + 2

        self.on_left = True
        self.on_right = False
        self.value = None
        self.switch = False
        
        self.activated = False
            
    def draw(self):
        self.bar.draw()
        self.knob.draw()
        self.label.draw()

        # Repositioning
        self.knob.y = self.y
        
        self.label.x = self.bar.left - self.padding
        self.label.y = self.y
        
        self.label.text = self.text
        self.label.colors[0] = self.colors
        self.label.font = self.font
        self.label.disable = self.disable
        
        self.component = self.bar
        
        self.activated = True

    def on_press(self, x, y, buttons, modifiers):
        self.switch = True

    def on_key(self, keys, modifiers):
        if self.focus:
            if keys == SPACE or keys == ENTER:
                self.switch = True
        
    def update(self):
        if not self.activated:
            return
        
        if self.on_left:
            self.value = True
        else:
            self.value = False

        if self.switch:
            if self.on_left:
                # Knob on the left, moving towards the right
                if self.knob.right < self.bar.right - 2:
                    self.knob.x += TOGGLE_VELOCITY
                else:
                    self.on_right = True
                    self.on_left = False

                    self.switch = False
                    
                if self.knob.x < self.x:
                    try: self.bar.alpha -= TOGGLE_FADE
                    except ValueError: pass
                elif self.knob.x > self.x: # More than halfway
                    try: self.bar.alpha += TOGGLE_FADE
                    except ValueError: pass

                    self.bar.texture = self.false_image
                    if self.hover: self.bar.texture = self.hover_false_image

            elif self.on_right:
                # Knob on the right, moving towards the left
                if self.knob.left > self.bar.left + 2:
                    self.knob.x -= TOGGLE_VELOCITY
                else:
                    self.on_left = True
                    self.on_right = False

                    self.switch = False

                if self.knob.x > self.x:
                    try: self.bar.alpha -= TOGGLE_FADE
                    except ValueError: pass
                elif self.knob.x < self.x:
                    try: self.bar.alpha += TOGGLE_FADE
                    except ValueError: pass

                    self.bar.texture = self.hover_true_image
                    if self.hover: self.bar.texture = self.hover_true_image

        else:
            if self.hover:
                if self.value: self.bar.texture = self.hover_true_image
                else: self.bar.texture = self.hover_false_image
            else:
                if self.value: self.bar.texture = self.true_image
                else: self.bar.texture = self.false_image

        if self.disable:
            if self.value: self.bar.texture = self.true_image
            else: self.bar.texture = self.false_image

        self.bar.update()
        self.knob.update()


class Slider(Widget):
    
    def __init__(self, text, x, y, colors=BLACK, font=DEFAULT_FONT,
                 size=10, length=200, padding=50):
        
        self.bar = Image(slider_horizontal, x, y)
        self.knob = Image(knob, x, y)
        self.label = Label(text, x, y, font=font)
        
        Widget.__init__(self)
        
        self.x = x
        self.y = y
        self.text = text
        self.colors = colors
        self.font = font
        self.size = size
        self.length = length
        self.padding = padding
        
        self.knob.left = self.bar.x - self.length / 2
        self.label.x = self.bar.left - self.padding
        
        self.value = 0
        self.switching = 0

    def update_knob(self, x):
        self.switching = x
        self.value = round(abs(((self.knob.x - self.left) * self.size) \
                         / (self.left - self.right)))
        
    def draw(self):
        self.bar.draw()
        self.knob.draw()
        self.label.draw()

        if not self.text:
            self.text = "Label"

        # Repositioning
        self.knob.y = self.y
        
        self.label.x = self.bar.left - self.padding
        self.label.y = self.y
        
        self.label.text = self.text
        self.label.font = self.font
        self.label.colors[0] = self.colors

        self.bar.width = self.length
        self.component = self.bar

    def on_press(self, x, y, buttons, modifiers):
        self.update_knob(x)

    def on_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_knob(x)

    def on_scroll(self, x, y, mouse, direction):
        if self.knob.left > self.left and \
           self.knob.right < self.right:
            self.switching += direction
            self.knob.x += direction
        
    def update(self):
        if self.switching:
            if self.knob.x <= self.switching and \
               self.knob.right <= self.right:
                # Knob too left, moving to the right
                self.knob.x += SLIDER_VELOCITY
            if self.knob.x > self.switching and \
               self.knob.left >= self.left:
                # Knob too right, moving to the left
                self.knob.x -= SLIDER_VELOCITY

        if self.knob.left > self.left and \
           self.knob.right < self.right and \
           self.focus:
            if self.keys[KEY_RIGHT]:
                self.switching += SLIDER_VELOCITY
                self.knob.x += SLIDER_VELOCITY
            if self.keys[KEY_LEFT]:
                self.switching -= SLIDER_VELOCITY
                self.knob.x -= SLIDER_VELOCITY
                
        self.bar.update()
        self.knob.update()

        
class Caret(Caret):
    def _update(self, line=None, update_ideal_x=True):
        if line is None:
            line = self._layout.get_line_from_position(self._position)
            self._ideal_line = None
        else:
            self._ideal_line = line
        x, y = self._layout.get_point_from_position(self._position, line)
        if update_ideal_x:
            self._ideal_x = x

        # x -= self._layout.view_x
        # y -= self._layout.view_y
        # add 1px offset to make caret visible on line start
        x += self._layout.x + 1

        y += self._layout.y + self._layout.height - 11

        font = self._layout.document.get_font(max(0, self._position - 1))
        self._list.position[:] = [x, y + font.descent, x, y + font.ascent]

        if self._mark is not None:
            self._layout.set_selection(min(self._position, self._mark), max(self._position, self._mark))

        self._layout.ensure_line_visible(line)
        self._layout.ensure_x_visible(x)


class Entry(Widget):

    def __init__(self, x, y, text="f", font=DEFAULT_FONT):
        self.document = decode_text(text)
        
        self.layout = IncrementalTextLayout(self.document, 190, 25)

        self.caret = Caret(self.layout)
        self.image = Image(entry_normal, x, y)

        Widget.__init__(self)

        self.x = x
        self.y = y
        self.default = text
        self.font = font

        self.blinking = True
        self.index = 0
        self.length = 0

        self.window.push_handlers(
            self.on_text,
            self.on_text_motion
        )

    def blink(self, delta_time):
        if self.caret.color == list(BLACK):
            self.caret.color = WHITE
        else:
            self.caret.color = BLACK
            
    def get(self):
        return self.document.text

    def set(self, text):
        self.document.text = text
        self.index = len(text)
        
    def insert(self, index, text):
        self.document.text = insert(index, self.document.text, text)

    def delete(self, start, end):
        self.document.text = delete(start, end, self.document.text)

    def draw(self):
        self.image.draw()
        
        self.image.x = self.x
        self.image.y = self.y
        
        self.layout.width = 190

        self.layout.x = self.x - self.layout.width / 2
        self.layout.y = self.y - 2
        
        self.layout.anchor_x = LEFT
        self.layout.anchor_y = CENTER

        with get_window().ctx.pyglet_rendering():
            self.layout.draw()

        self.component = self.image

    def on_key(self, keys, modifiers):
        if keys == ENTER:
            self.delete(self.length - 1, self.length)
            self.focus = False

    def on_focus(self):
        if self.get() == self.default:
            self.set("")
            self.index = 0
            
    def on_text(self, text):
        if self.focus:
            self.caret.on_text(text)
            
            self.index = self.caret.position
            
    def on_text_motion(self, motion):
        if self.focus:
            self.caret.on_text_motion(motion)

            self.index = self.caret.position

    def on_text_select(self, motion):
        if self.focus:
            self.caret.on_text_motion_select(motion)

            self.index = self.caret.position

    def on_press(self, x, y, buttons, modifiers):
        self.caret.on_mouse_press(x, y, button, modifiers)

        self.index = self.caret.position

    def on_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

            self.index = self.caret.position
        
    def update(self):
        self.caret.position = self.index

        self.length = len(self.get())
        
        if self.focus:
            self.caret.visible = True
            
            if not self.blinking:
                schedule(self.blink, ENTRY_BLINK_INTERVAL)

                self.blinking = True
            
        else:
            self.caret.visible = False
            self.caret.mark = 0
            self.caret.position = 0
            self.blinking = False

            unschedule(self.blink)

        
##class Entry(Widget, EventDispatcher):
##    
##    def __init__(self, x, y, default="Enter here", validate=string.printable,
##                 font=DEFAULT_FONT):
##        
##        self.image = Image(entry_normal, x, y)
##        self.input = Input(default, x - self.image.width / 2 + 5, y - 15, font)
##        
##        Widget.__init__(self)
##
##        self.x = x
##        self.y = y
##        self.default = default
##        self.font = font
##
##        self.hover = False
##        self.focus = False
##        self.disable = False
##
##        self.text = default
##        self.index = len(default)
##        self.length = 0
##        
##        self.activated = False
##
##    def draw(self):
##        self.image.draw()
##        self.input.draw()
##
##        self.input.x = self.x
##        self.input.y = self.y
##        self.input.font = self.font
##        self.input.align = [LEFT, CENTER]
##        
##        self.input.focus = self.focus
##        
##        self.component = self.image
##        
##        self.activated = True

        
class MyWindow(Window):
    def __init__(self, title, width, height):
        super().__init__(
            width, height, title
        )

        self.container = Container()

        self.label = Label(
            "Label",
            10,
            60,
            multiline=True,
            width=500)

        self.button = Button(
            "Click me!",
            250,
            250,
            command=self.click)

        self.toggle = Toggle(
            "Show fps",
            250,
            350)
        
        self.slider = Slider(
            None,
            250,
            300)

        self.entry = Entry(
            250,
            160)
        
        self.container.append(self.label)
        self.container.append(self.button)
        self.container.append(self.toggle)
        self.container.append(self.slider)
        self.container.append(self.entry)
        
        self.button.bind(ENTER)

    def click(self):
        print(self.entry.get())

    def on_draw(self):
        self.clear()
        
        self.container.draw()

        if self.toggle.value:
            self.label.text = f"{int(get_fps())} fps"
        else:
            self.label.text = "Label"

        self.slider.text = str(self.slider.value)

if __name__ == "__main__":
    window = MyWindow("Button", 500, 400)
    run()
