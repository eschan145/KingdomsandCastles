"""GUI interface and widgets. Documentation and details can be found at:
https://github.com/eschan145/Armies/blob/main/README.md.

More than meets the eye in this example. To see all features, look at the source
code of each widget.
"""


from cmath import tau
from string import printable
from time import time
from tkinter import Tk
from typing import Tuple
from webbrowser import open_new, open_new_tab

from arcade import (PointList, ShapeElementList, Sprite, SpriteList, Window,
					create_rectangle_filled, create_rectangle_outline,
					draw_rectangle_outline, enable_timings, get_fps,
					get_window, load_texture, run, schedule, unschedule)
from pyglet.event import EventDispatcher
from pyglet.graphics import Batch
from pyglet.shapes import (Arc, BorderedRectangle, Circle, Ellipse, Line,
						   Polygon, Sector, Star, Triangle)
from pyglet.text import HTMLLabel, decode_text
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout
from pymunk import shapes

from color import (BLACK, BLUE_YONDER, COOL_BLACK, DARK_GRAY, DARK_SLATE_GRAY,
				   RED, WHITE, four_byte)
from constants import (BOTTOM, CENTER, DEFAULT_FONT, DEFAULT_FONT_FAMILY,
					   DEFAULT_FONT_SIZE, DISABLE_ALPHA, ENTRY_BLINK_INTERVAL,
					   KNOB_HOVER_SCALE, LEFT, MULTIPLE, SINGLE,
					   SLIDER_VELOCITY, TOGGLE_FADE, TOGGLE_VELOCITY, TOP, Y)
from file import (combobox_bottom_normal, combobox_middle_normal,
				  combobox_top_normal, entry_normal, knob, none,
				  slider_horizontal, toggle_false, toggle_false_hover,
				  toggle_true, toggle_true_hover, widgets)
from geometry import Point, Pointlist, is_point_in_polygon
from key import (CONTROL, ENTER, KEY_LEFT, KEY_RIGHT, MOTION_BACKSPACE,
				 MOTION_BEGINNING_OF_FILE, MOTION_BEGINNING_OF_LINE,
				 MOTION_COPY, MOTION_DELETE, MOTION_DOWN, MOTION_END_OF_FILE,
				 MOTION_END_OF_LINE, MOTION_LEFT, MOTION_NEXT_WORD,
				 MOTION_PREVIOUS_WORD, MOTION_RIGHT, MOTION_UP,
				 MOUSE_BUTTON_LEFT, SHIFT, SPACE, TAB, A, C, Keys, V, X)

MAX = 2 ** 32

enable_timings()

clipboard = Tk()
clipboard.withdraw()

_widgets = SpriteList()
batch = Batch()
widgets_list = SpriteList()


def clipboard_get():
	"""Get some text from the clipboard.

	returns: str
	"""

	return clipboard.clipboard_get()

def clipboard_append(text):
	"""Append some text to the clipboard.

	text - text to append to the clipboard

	parameters: str
	"""

	clipboard.clipboard_append(text)

def insert(index, text, add):
	"""Insert some text to a string given an index. This was originally used for
	the Entry widget but was deceprated when we found a faster and more
	efficient way to insert text.

	index - index of the text addition
	text - string to be edited
	add - new text to be inserted

	parameters: int, str, str
	returns: str
	"""

	return text[:index] + add + text[index:]

def delete(start, end, text):
	"""Delete some text to a string given an index. This was originally used for
	the Entry widget but was deceprated when we found a faster and more
	efficient way to delete text.

	start - start index of the text removal
	end - end index of the text removal
	text - string to be edited

	parameters: int, int, str
	returns: str
	"""

	if len(text) > end:
		text = text[0: start:] + text[end + 1::]
	return text


class Font:
	"""An object-oriented Font."""

	def __init__(self,
				 family=DEFAULT_FONT_FAMILY,
				 size=DEFAULT_FONT_SIZE
				):

		"""Initialize an object-oriented Font. This is an experimental
		feature developed on August 4th 2022 and has no effect.

		family - family of the font (style)
		size - size of the font (not in pixels

		parameters: int, int
		"""

		self.family = family
		self.size = size

		self.list = [self.family, self.size]

	def __getitem__(self, item):
		"""Get an item from the list.

		item - item whose value to be returned

		parameters: int
		returns: str or int
		"""

		return self.list[item]

	def __setitem__(self, index, item):
		"""Get an item from the list.

		item - item whose value to be set

		parameters: int, str or int
		"""

		self.list[index] = item


default_font = Font()


class Container(EventDispatcher):
	""""Container class to draw and update widgets. One current problem is that
	each widget in its widget spritelist is being drawn every frame
	individually. Though it is much faster to draw in a batch, this has not
	been implemented.
	"""
	
	focus = None
	enable = True

	widgets = []

	_window = None

	def __init__(self, window=None, shadow=False):
		EventDispatcher.__init__(self)

	def _get_window(self):
		"""Get the current pyglet window of the container.
		
		returns: Window
		"""

		return self._window

	def _set_window(self, window):
		"""Set the current pyglet window of the container.
		
		window - window of the container
		
		parameters: Window
		"""

		self._window = window or get_window()

		self._window.push_handlers(self)
	
	window = property(_get_window, _set_window)

	def append(self, widget):
		"""Add a widget to the drawing list. Unfortunately each widget must be
		drawn individually instead of drawing them in a batch, which really
		slows down performance with hundreds of widgets.

		widget - widget to add to the list

		parameters: Widget
		"""

		assert self.window, (
			"No window is active. It has not been created yet, or it was "
			"closed. Be sure to set the window property of the container before "
			"adding any widgets."
		)

		self.widgets.append(widget)

		widget.container = self

	def draw(self):
		"""Draw the container's widgets. This just loops through all of the
		widgets in its list and draws them, which is terribly inefficient.
		"""
		
		widgets_list.draw()

		for widget in self.widgets:
			widget.draw()

		with self.window.ctx.pyglet_rendering():
			batch.draw()

			# A shadow effect not in progress anymore

			# Interesting feature:
			# Press Control + slash when on the line with "shade = 1"
			# The text "shade" will turn light green for a second.

			# shade = 1

			# if self.shadow:
			#	 for i in range(1, 100):
			#		 shade += 0.01
			#		 print(scale_color(self.shadow, int(shade)))
			#		 draw_rectangle_outline(widget.x, widget.y,
			#								 widget.width + 1, widget.height + 1,
			#								 RED)

	def draw_bbox(self, width=1, padding=0):
		"""Draw the bounding box of each widget in the list. The drawing is
		cached in a ShapeElementList so it won't take up more time. This can
		also be called draw_hitbox or draw_hit_box.

		width - width of the bounding box outline
		padding - padding around the widget
		"""

		for widget in self.widgets:
			widget.draw_bbox(width, padding)

	draw_hitbox = draw_bbox # Alias
	draw_hit_box = draw_bbox

	def exit(self):
		"""Exit the event sequence and destroy all widgets. This sets its
		enable property to False.
		"""

		for widget in self.widgets:
			widget.destroy()

		self.enable = False

	def on_key_press(self, keys, modifiers):
		"""A key is pressed. This is used to detect focus change by pressing
		Tab and Shift-Tab."""

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

##			if isinstance(self.focus, Button):
##				self.focus.image.scale = FOCUS_SIZE
##			elif isinstance(self.focus, Toggle) or \
##				 isinstance(self.focus, Slider):
##				self.focus.bar.scale = FOCUS_SIZE
##				self.focus.knob.scale = FOCUS_SIZE
##
			for widget in self.widgets:
				if not widget == self.focus:
					widget.focus = False


container = Container()


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
	"""Create a user interface GUI widget. This is a high-level class, and is
	not suitable for very complex widgets. It comes with built-in states,
	which can be accessed just by getting its properties. Dispatching events
	makes subclassing a widget and creating your own very easy.

	Widgets can have components, which are essentially smaller, secondary
	widgets that are inside the widget. For example, a button widget has a
	Label and an Image for components. A widget can have a main component,
	which takes the hitbox used for detecting states. For a button widget the
	main component would be the Image.

	Plenty of things are built-in here. For example, you can access the
	current window just by using the window property. Or the key state handler
	with the key property. You can draw the hit box of a widget for debugging,
	and performance is not lost because the drawing is cached. When removing a
	widget, use its delete function.
	"""

	def __init__(self, widgets=(), image=none, scale=1.0, frame=None):
		"""
		Here's an example of a widget. This _colorchooser dispatches events, so
		a widget that subclasses it can use it.

		>>> class _Colorchooser(Widget):

				def __init__(self):
					Widget.__init__(self)

				def on_press(self, x, y, buttons, modifiers):
					color = self.get_color_from_pos(x, y)
					self.dispatch_event("on_color_pick", color)

				def get_color_from_pos(self, x, y):
					# Get a color from x, y
					pass

		>>> _Colorchooser.register_event_type("on_color_pick")

		On lines 1-5 we create and initialize the widget. An event is
		dispatched by the widget called on_press when the widget is pressed.
		This _colorchooser widget then dispatches an event, called
		"on_color_pick", with its parameters listed beside it. At the end of
		defining the widget you have to register it, so we do that in the last
		line. This just confirms to pyglet that we're creating an event.

		Now, the actual colorchooser would look like this:

		>>> class Colorchooser(_Colorchooser):

				def __init__(self):
					_Colorchooser.__init__(self)

				def on_color_pick(self, color):
					print("Color picked: ", color)

		_______________________________________________________________


		widgets - widgets and components to be added. If you are creating
				components, add them before initializing the widget.
		image - image to be displayed. Use this only for defining an image
				widget, though one is already pre-defined.
		scale - scale of the widget. This has been deceprated, as setting this
				to a value different that one will mess up the widget's bbox
		frame - not yet implemented. This is supposed to have a frame widget,
				which stores multiple widgets. It's similar to tkinter's Frame.
		"""

		Sprite.__init__(self, image, scale)

		self.frame = frame or Frame(0, 0)

		self.frame.append(self)

		self.hover = False
		self.press = False
		self.disable = False

		self.widgets = widgets

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
		self.shapes = None

		container.append(self)
		
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

	def _check_collision(self, x, y):
		"""Check if a x and y position exists within the widget's hit box. This
		is an alternative to check_collision, and should only be used if you
		are not using any components (ex. label widget).

		TODO: replace x and y parameters with a Point

		x - x position of point
		y - y position of point

		parameters: int, int
		returns: bool
		"""

		return (0 < x - self.x < self.width and
				0 < y - self.y < self.height)

	def check_collision(self, x, y):
		"""Check if a x and y position exists within the widget's hit box. This
		should be used if you are using components.

		TODO: replace x and y parameters with a Point

		x - x position of point
		y - y position of point

		parameters: int, int
		returns: bool
		"""

		if self._right and \
		   self._left and \
		   self._top and \
		   self._bottom:
			return x > self._left and x < self._right and \
				   y > self._bottom and y < self._top

		return x > self.left and x < self.right and \
			   y > self.bottom and y < self.top

	def draw_bbox(self, width=1, padding=0):
		"""Draw the bounding box of the widget. The drawing is cached in a
		ShapeElementList so it won't take up more time. This can also be called
		draw_hitbox or draw_hit_box.

		width - width of the bounding box outline
		padding - padding around the widget

		parameters: int, int
		"""

		if self.shapes is None:
			shape = create_rectangle_outline(self.x, self.y,
											 self.width + padding,
											 self.height + padding,
											 RED, width
											)

			self.shapes = ShapeElementList()
			self.shapes.append(shape)

			self.shapes.center_x = self.x
			self.shapes.center_y = self.y
			self.shapes.angle = self.angle

	draw_hitbox = draw_bbox # Alias
	draw_hit_box = draw_bbox

	def delete(self):
		"""Delete this widget and remove it from the event stack. The widget
		is not drawn and will not be accepting any events. You may want to
		override this if creating your own custom widget.
		"""

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

	def on_mouse_scroll(self, x, y, sx, sy):
		if self.disable:
			return

		if self.check_collision(x, y):
			if self.disable:
				return

			self.dispatch_event("on_scroll", x, y, Point(sx, sy))

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
		"""Create an Image widget. This is a simple widget used as the main
		component in many other widgets. It is not suitable to create vast
		numbers of these, because you must create a texture every single time.
		Use this for any sort of Image you are going to draw if you want to
		draw it efficiently.
		
		image - filepath of the image
		x - x position of image
		y - y position of image
		scale - scale of image. See arcade.sprite.Sprite for details.
		"""
		
		Widget.__init__(self, image=image, scale=scale)

		self.image = image

		self.x = x
		self.y = y

		self.normal_image = image
		self.hover_image = load_texture(image)
		self.press_image = load_texture(image)
		self.disable_image = load_texture(image)

		widgets_list.append(self)

	def _get_x(self):
		"""Get the x position of the image.

		returns: int
		"""

		return self.center_x

	def _set_x(self, x):
		"""Set the x position of the image.

		x - new x position of image

		parameters: int
		"""

		self.center_x = x

	def _get_y(self):
		"""Get the y position of the image.

		returns: int
		"""

		return self.center_y

	def _set_y(self, y):
		"""Set the y position of the image.

		y - new y position of image

		parameters: int
		"""

		self.center_y = y

	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)

	def update(self):
		pass
		# if self.hover:
		#	 self.texture = self.hover_image
		# if self.press:
		#	 self.texture = self.press_image
		# if self.disable:
		#	 self.texture = self.disable_image
		# elif not self.hover and \
		#	 not self.press and \
		#	 not self.disable:
		#	 self.image = self.normal_image


class Label(Widget):
	"""Label widget to draw and display HTML text.

	TODO: add to batch for fast drawing
	"""

	def __init__(self, text, x, y, frame=None,
				 colors=[BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)],
				 font=DEFAULT_FONT, title=False,
				 justify=LEFT, width=0, multiline=False,
				 command=None, parameters=[],
				 outline=None
				):

		"""Create a Label widget to display efficiently and advanced HTML text.
		Note that this uses pyglet's HTML decoder, so formats are limited. See
		the full list of formats at:

		https://pyglet.readthedocs.io/en/latest/programming_guide/text.html#html

		text - text to be displayed on the label
		x - x position of label
		y - y position of label
		colors - colors of the text. This is specified in a format
				 [normal, (hover, press, disable)], which are its states and
				 the appropiate colors displayed. Defaults to
				 [BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)]. Their RGB
				 values can be found in the color module.
		font - font of the label. This can be a object-oriented font or just a
			   tuple containing the font description in (family, size).
			   Defaults to DEFAULT_FONT.
		title - the label is drawn as a title. This has long since been
				deprecated.
		justify - horizontal justification of the Label. Its avaliable options
				  are "center", "left", or "right". Defaults to "right".
		width - width of the label. This needs only to be used if the label is
				multiline. Defaults to 0.
		multiline - text is drawn multiline. If this is set to true then the
					width must be set to a value greater than zero, as this
					will be the length each line for wrap.
		command - command called when the label is pressed
		parameters - parameters of the command
		outline - outline of the label as a rectangle. This is specified as
				  (color, padding, width). Defaults to None.

		See https://pyglet.readthedocs.io/en/latest/programming_guide/text.html
		for details regarding text specification and drawing.
		"""

		# For new arcade installations, change the self.label property in
		# Text to a HTMLLabel for HTML scripting
		#
		# self._label = pyglet.text.HTMLLabel(
		#	 text=text,
		#	 x=start_x,
		#	 y=start_y,
		#	 width=width,
		#	 multiline=multiline
		# )
		#
		# The Label widget is the only widget with a LEFT x anchor.
		#

		if not text:
			text = " "

		self.label = HTMLLabel(f"{text}", x, y,
							   anchor_x=LEFT, anchor_y=CENTER,
							   width=width, multiline=multiline,
							   batch=batch
							   )

		Widget.__init__(self, frame=frame)

		self.x = x + self.frame.x
		self.y = y + self.frame.y

		if self.frame.direction == TOP:
			self.x = self.frame.x - x
			self.y = self.frame.y - y

		self.colors = colors
		self.font = font
		self.title = title
		self.justify = justify
		self._width = width
		self.multiline = multiline
		self.command = command
		self.parameters = parameters
		self.outline = outline

		self.keys = []

		self.length = 0

	def _get_x(self):
		"""Get the x position of the lutton.

		returns: int
		"""

		return self.label.x

	def _set_x(self, x):
		"""Set the x position of the Label.

		x - new x position of the Label

		parameters: int
		"""

		self.label.x = x

	def _get_y(self):
		"""Get the y position of the Label.

		returns: int
		"""

		return self.label.y

	def _set_y(self, y):
		"""Set the y position of the Label.

		y - new y position of the Label

		parameters: int
		"""

		self.label.y = y

	def _get_text(self):
		"""Get the text of the Label.

		returns: str
		"""

		return self.document.text

	def _set_text(self, text):
		"""Set the text of the Label.

		text - new text of the Label

		parameters: str
		"""

		if self.label.text == text:
			return

		if not text:
			text = "Label"
		self.label.text = text

	def _get_document(self):
		"""Get the document of the Label.

		returns: str
		"""

		return self.label.document

	def _set_document(self, document):
		"""Set the document of the Label.

		document - new document of the Label

		parameters: pyglet.text.document.HTMLDocument
		"""

		self.label.document = document

	def _get_width(self):
		"""Get the content width of the label. This property cannot be set.
		
		returns: int
		"""

		return self.label.content_width

	def _get_height(self):
		"""Get the content height of the label. This property can not be set.
		
		returns: int
		"""

		return self.label.content_height
	
	text = property(_get_text, _set_text)
	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)
	document = property(_get_document, _set_document)
	width = property(_get_width)
	height = property(_get_height)

	def bind(self, *keys):
		"""Bind some keys to the label. Invoking these keys activates the
		label. If the Enter key was binded to the lutton, pressing Enter will
		invoke its command and switches its display to a pressed state.

		>>> label.bind(ENTER, PLUS)
		[65293, 43]

		*keys - keys to be binded

		parameters: *int (32-bit)
		returns: list
		"""

		self.keys = [*keys]
		return self.keys

	def unbind(self, *keys):
		"""Unbind keys from the label.

		>>> label.bind(ENTER, PLUS, KEY_UP, KEY_DOWN)
		[65293, 43, 65362, 65364]
		>>> label.unbind(PLUS, KEY_UP)
		[65293, 65364]

		parameters: *int(32-bit)
		returns: list
		"""

		for key in keys:
			self.keys.remove(key)
		return self.keys

	def draw_bbox(self, width=1, padding=0):
		"""Draw the hitbox of the label. See Widget.bbox for more details.
        This overrides the Widget.bbox because of its left anchor_x.
        """

		draw_rectangle_outline(
			self.x + self.width / 2,
			self.y, self.width + padding,
			self.height + padding, RED, width
		)

	draw_hitbox = draw_bbox
	draw_hit_box = draw_bbox

	def draw(self):
		if self.outline:
			draw_rectangle_outline(
				self.x + self.width / 2, self.y,
				self.width + self.outline[1],
				self.height + self.outline[1],
				self.outline[0], self.outline[2]
			)

		if self.text:
			if not self._left == self.x - self.width / 2 or \
				not self._right == self.x + self.width / 2 or \
				not self._top == self.y + self.height / 2 or \
				not self._bottom == self.y - self.height / 2:
				self._left = self.x - self.width / 2
				self._right = self.x + self.width / 2
				self._top = self.y + self.height / 2
				self._bottom = self.y - self.height / 2

	def on_key(self, keys, modifiers):
		if isinstance(self.keys, list):
			if keys in self.keys:
				self.invoke()

		else:
			if self.keys == keys:
				self.invoke()

	def on_press(self, x, y, buttons, modifiers):
		if self.disable or not self.command:
			return

		if buttons == MOUSE_BUTTON_LEFT:
			self.invoke()

	def update(self):
		"""Update the Label. This upgrades its properties and registers its
		states and events.

		The following section has been tested dozens of times. The performance
		is incredibly slow, with about 1 fps for 100 Labels. Usually, for a
		single Label the processing time is about one-hundredth of a second.

		With the begin_update() and end_update() functions for the label, the
		processing time is much faster. And with batches, things are more
		efficient and speed is even greater.

		With no other widgets, you can draw 10,000 labels before the fps drops
		below 60.
		"""

		self.label.begin_update()

		# self.label.font_name = self.font[0]
		# self.label.font_size = self.font[1]
		# self.label.opacity = self.alpha
		self.label.align = self.justify
		self.label.multiline = self.multiline

		self.label.end_update()

		self.length = len(self.text)

		if "<u" in self.text or "<\\u>" in self.text:
			# ValueError: Can only assign sequence of same size
			return

		# States
		if self.hover:
			self.document.set_style(0, self.length,
									{"color" : four_byte(self.colors[1][1])})
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
	"""Button widget to invoke and call commands. Pressing on a button invokes
	its command, which is a function or callable.
	"""

	keys = []

	def __init__(
				 self, text, x, y, command=None, parameters=[],
				 link=None,
				 colors=["yellow", BLACK], font=default_font,
				 callback=SINGLE
				):

		"""Initialize a Button. A button has two components: an Image and a
		Label. You can customize the Button's images and display by changing
		its normal_image, hover_image, press_image, and disable_image
		properties, but it is recommended to use the Pushable widget.

		text - text to be displayed on the button
		x - x position of the button
		y - y position of the button
		command - command to be invoked when the button is called
		parameters - parameters of the callable when invoked
		link - website link to go to when invoked
		colors - colors of the button
		font - font of the button
		callback - how the button is invoked:
				   SINGLE - the button is invoked once when pressed
				   DOUBLE - the button can be invoked multiple times in focus
				   MULTIPLE - the button can be invoked continuously

		parameters: str, int, int, callable, list, tuple, Font, str
		"""

		# A two-component widget:
		#	 - Image
		#	 - Label

		self.image = Image(widgets[f"{colors[0]}_button_normal"], x, y)
		self.label = Label(text, x, y, font=font)

		Widget.__init__(self, (self.image, self.label))

		self.text = text
		self.x = x
		self.y = y
		self.command = command
		self.parameters = parameters
		self.link = link
		self.colors = colors
		self.font = font
		self.callback = callback

		self.normal_image = load_texture(widgets[f"{colors[0]}_button_normal"])
		self.hover_image = load_texture(widgets[f"{colors[0]}_button_hover"])
		self.press_image = load_texture(widgets[f"{colors[0]}_button_press"])
		self.disable_image = load_texture(widgets[f"{colors[0]}_button_disable"])

	def _get_x(self):
		"""Get the x position of the button.

		returns: int
		"""

		return self.image.x

	def _set_x(self, x):
		"""Set the x position of the button.

		x - new x position of the button

		parameters: int
		"""

		self.image.x = self.label.x = x

	def _get_y(self):
		"""Get the y position of the button.

		returns: int
		"""

		return self.image.y

	def _set_y(self, y):
		"""Set the y position of the button.

		y - new y position of the button

		parameters: int
		"""

		self.image.y = self.label.y = y

	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)

	def bind(self, *keys):
		"""Bind some keys to the button. Invoking these keys activates the
		button. If the Enter key was binded to the button, pressing Enter will
		invoke its command and switches its display to a pressed state.

		>>> button.bind(ENTER, PLUS)
		[65293, 43]

		*keys - keys to be binded

		parameters: *int (32-bit)
		returns: list
		"""

		self.keys = [*keys]
		return self.keys

	def unbind(self, *keys):
		"""Unbind keys from the button.

		>>> button.bind(ENTER, PLUS, KEY_UP, KEY_DOWN)
		[65293, 43, 65362, 65364]
		>>> button.unbind(PLUS, KEY_UP)
		[65293, 65364]

		parameters: *int(32-bit)
		returns: list
		"""

		for key in keys:
			self.keys.remove(key)
		return self.keys

	def invoke(self):
		"""Invoke the button. This switches its image to a pressed state and
		calls the its associated command with the specified parameters. If the
        Button is disabled this has no effect.
		"""
        
		if self.disable or not self.command:
			return

		self.press = True

		if self.parameters:
			self.command(self.parameters)
		else:
			self.command()

		if self.link:
			open_new(self.link)

	def draw(self):
		"""Draw the button. The component of the button is the image, which takes
		all of the collision points.

		1. Image - background image of the button
		2. Label - text of the button
		"""

		# Update Label properties

		self.label.text = self.text

		if not self.label.colors[0] == self.colors[1] or \
			not self.label.font == self.font or \
			not self.label.label.anchor_x == CENTER:
			self.label.colors[0] = self.colors[1]
			self.label.font = self.font
			self.label.label.anchor_x = CENTER

		self.component = self.image

	def on_press(self, x, y, buttons, modifiers):
		"""The Button is pressed. This invokes its command if the mouse button
		is the left one.

		TODO: add specifying proper mouse button in settings

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		if buttons == MOUSE_BUTTON_LEFT:
			self.invoke()

	def on_key(self, keys, modifiers):
		"""A key is pressed. This is used for keyboard shortcuts when the
		Button has focus.

		keys - key pressed
		modifiers - modifier pressed

		parameters: int (32-bit), int (32-bit)
		"""

		if keys == SPACE and self.focus:
			self.invoke()

		if isinstance(self.keys, list):
			if keys in self.keys:
				self.invoke()

		else:
			if self.keys == keys:
				self.invoke()

	def update(self):
		"""Update the Button. This registers events and updates the Button
		image.
		"""

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


class Slider(Widget):
	"""Slider widget to display slidable values.

	FIXME: even knob moves when setting x property
	TODO: add keyboard functionality

	https://github.com/eschan145/Armies/issues/20
	"""

	_value = 0
	destination = 0

	def __init__(self, text, x, y, colors=BLACK, font=DEFAULT_FONT,
				 size=10, length=200, padding=50, round=0):
		"""Initialize a Slider."""

		self.bar = Image(slider_horizontal, x, y)
		self.knob = Image(knob, x, y)
		self.label = Label(text, x, y, font=font)

		Widget.__init__(self, (self.bar, self.knob))

		self.text = text
		self.colors = colors
		self.font = font
		self.size = size
		self.length = length
		self.padding = padding
		self.round = round

		self.x = x
		self.y = y

		self.knob.left = self.x - self.length / 2

	def _get_value(self):
		"""Get the value or x of the Slider.

		returns: int
		"""

		return self._value

	def _set_value(self, value):
		"""Set the value or x of the Slider.

		value - new value to be set

		parameters: int
		"""

		if self._value >= self.size:
			self._value = self.size
			return
		elif self._value <= 0:
			self._value = 0
			return

		max_knob_x = self.right# + self.knob.width / 2

		self._value = round(value, self.round)

		x = (max_knob_x - self.left) * value / self.size \
			+ self.left + self.knob.width / 2
		self.knob.x = max(self.left, min(x - self.knob.width / 2, max_knob_x))

	def _get_x(self):
		"""Get the x position of the Slider.

		returns: int
		"""

		return self.bar.x

	def _set_x(self, x):
		"""Set the x position of the Slider.

		x - new x position of the Slider

		parameters: int
		"""

		self.bar.x = x
		self.label.x = self.bar.left - self.padding

	def _get_y(self):
		"""Get the y position of the Slider.

		returns: int
		"""

		return self.bar.y

	def _set_y(self, y):
		"""Set the y position of the Slider.

		y - new y position of the Slider

		parameters: int
		"""

		self.bar.y = self.knob.y = self.label.y = y

	value = property(_get_value, _set_value)
	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)

	def update_knob(self, x):
		"""Update the knob and give it a velocity when moving. When calling
		this, the knob's position will automatically update so it is congruent
		with its size.

		x - x position of the position

		parameters: int
		"""

		self.destination = max(self.left,
							   min(x - self.knob.width / 2, self.right))
		self._value = round(abs(((self.knob.x - self.left) * self.size) \
					  / (self.left - self.right)), self.round)

	def reposition_knob(self):
		"""Update the value of the Slider. This is used when you want to move
		the knob without it snapping to a certain position and want to update
		its value. update_knob(x) sets a velocity so the knob can glide.
		"""

		self._value = round(abs(((self.knob.x - self.left) * self.size) \
					  / (self.left - self.right)), self.round)

	def draw(self):
		"""Draw the Slider. The component of the Slider is the bar, which takes
		all of the collision points.

		1. Bar (component)
		2. Knob
		3. Label
		"""

		if not self.text:
			self.text = "Label"

		self.label.text = self.text
		
		if not self.label.font == self.font or \
			not self.label.colors[0] == self.colors or \
			not self.bar.width == self.length:
			self.label.font = self.font
			self.label.colors[0] = self.colors
			self.bar.width = self.length

		self.component = self.bar

	def on_key(self, keys, modifiers):
		"""A key is pressed. This is used for keyboard shortcuts when the Slider
		has focus. On a right key press, the value is incremented by one. On a
		left key press, the value is decremented by one.

		Unfortunately, this is not working currently.

		keys - key pressed
		modifiers - modifier pressed

		parameters: int (32-bit), int (32-bit)
		"""

		if not self.focus:
			return

		if keys == KEY_RIGHT:
			self.knob.x = self.knob.x + (int(self.length / self.size))
			self.reposition_knob()
		elif keys == KEY_LEFT:
			self.knob.x = self.knob.x - (int(self.length / self.size))
			self.reposition_knob()

	def on_press(self, x, y, buttons, modifiers):
		"""The Slider is pressed. This updates the knob to the x position of the
		press.

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		self.update_knob(x)

	def on_drag(self, x, y, dx, dy, buttons, modifiers):
		"""The user dragged the mouse when it was pressed. This updates the knob
		to the x position of the press.

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		self.update_knob(x)

	def on_scroll(self, x, y, mouse):
		"""The user scrolled the mouse wheel. This will change the knob's
		position and adjust its x position.

		x - x position of the mouse scroll
		y - y position of the mouse scroll
		mouse - movement in vector from the last position (x, y)
		direction - direction of mouse scroll

		parameters: int, int, tuple (x, y), float
		"""

		self.update_knob(self.knob.x + self.knob.width / 2 + mouse.y)

	def update(self):
		"""Update the knob. This adjusts its position and adds effects like
		gliding when the knob is moving. This way, the knob doesn't just snap to
		position. When the knob is hovered, its scale is increased by
		KNOB_HOVER_SCALE.
		"""

		if self.destination:
			if self.knob.x <= self.destination and \
			   self.knob.right <= self.right:
				# Knob too left, moving to the right
				self.knob.x += SLIDER_VELOCITY
				self.reposition_knob()
			if self.knob.x > self.destination and \
			   self.knob.left >= self.left:
				# Knob too right, moving to the left
				self.knob.x -= SLIDER_VELOCITY
				self.reposition_knob()

		# Knob hover effect
		if self.knob.hover:
			self.knob.scale = KNOB_HOVER_SCALE
		else:
			self.knob.scale = 1

		self.bar.update()
		self.knob.update()


class Toggle(Widget):
	"""Toggle widget to switch between true and false values. This uses
	a special effect of fading during the switch.

	FIXME: even knob moves when setting x property
	"""

	true_image = load_texture(toggle_true)
	false_image = load_texture(toggle_false)
	hover_true_image = load_texture(toggle_true_hover)
	hover_false_image = load_texture(toggle_false_hover)

	on_left = True
	on_right = False
	value = None
	switch = False

	def __init__(
				 self, text, x, y,
				 colors=BLACK, font=DEFAULT_FONT,
				 default=True, padding=160
				):

		"""Initialize a Toggle. A Toggle is a widget that when pressed, switches
		between True and False values.

		text - text to be displayed alongside the Toggle
		x - x position of the Toggle
		y - y position of the Toggle
		colors - text color of the Label
		font - font of the Label
		default - default value of the Toggle
		padding - padding of the Label and the Toggle

		parameters: str, int, int, tuple, tuple, bool, int
		"""

		# A three-component widget:
		#	 - Image
		#	 - Image
		#	 - Label

		if default:
			image = toggle_true
		else:
			image = toggle_false

		self.bar = Image(image, x, y)
		self.knob = Image(knob, x, y)

		self.label = Label(knob, x, y, font=font)

		Widget.__init__(self, (self.bar, self.knob))

		self.text = text
		self.colors = colors
		self.font = font
		self.padding = padding

		self.x = x
		self.y = y

		self.knob.left = self.bar.left + 2

	def _get_x(self):
		"""Get the x position of the Toggle.

		returns: int
		"""

		return self.bar.x

	def _set_x(self, x):
		"""Set the x position of the Toggle.

		x - new x position of the Toggle

		parameters: int
		"""

		self.bar.x = x
		self.label.x = self.bar.left - self.padding

	def _get_y(self):
		"""Get the y position of the Toggle.

		returns: int
		"""

		return self.bar.y

	def _set_y(self, y):
		"""Set the y position of the Toggle.

		y - new y position of the Toggle

		parameters: int
		"""

		self.bar.y = self.knob.y = self.label.y = y

	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)

	def draw(self):
		"""Draw the Toggle. The component of the toggle is the bar, which takes
		all of the collision points.

		1. Bar (component)
		2. Knob
		3. Label
		"""

		self.label.text = self.text

		if not self.label.colors[0] == self.colors or \
			not self.label.font == self.font:
			self.label.colors[0] = self.colors
			self.label.font = self.font

		self.component = self.bar

	def on_press(self, x, y, buttons, modifiers):
		"""The Toggle is pressed. This switches between True and False values. If
		the Control key is held down during this, this will have no effect.

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		if not modifiers & CONTROL:
			self.switch = True

	def on_key(self, keys, modifiers):
		"""A key is pressed. This is used for keyboard shortcuts when the Toggle
		has focus. If the Space or Enter key is pressed, the Toggle will be
		switched.

		keys - key pressed
		modifiers - modifier pressed

		parameters: int (32-bit), int (32-bit)
		"""

		if self.focus:
			if keys == SPACE or keys == ENTER:
				self.switch = True

	def update(self):
		"""Update the toggle. This updates its position and registers its
		special effects.
		"""

		if self.on_left:
			self.value = True
		else:
			self.value = False

		if self.switch and not self.disable:
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

		if self.knob.hover:
			self.knob.scale = KNOB_HOVER_SCALE
		else:
			self.knob.scale = 1


class Caret(Caret):
	"""Caret used for pyglet.text.IncrementalTextLayout."""

	BLINK_INTERVAL = 0

	def on_text_motion(self, motion, select=False):
		"""The caret was moved or a selection was made with the keyboard.

		motion - motion the user invoked. These are found in the keyboard.
				 MOTION_LEFT				MOTION_RIGHT
				 MOTION_UP				  MOTION_DOWN
				 MOTION_NEXT_WORD		   MOTION_PREVIOUS_WORD
				 MOTION_BEGINNING_OF_LINE   MOTION_END_OF_LINE
				 MOTION_NEXT_PAGE		   MOTION_PREVIOUS_PAGE
				 MOTION_BEGINNING_OF_FILE   MOTION_END_OF_FILE
				 MOTION_BACKSPACE		   MOTION_DELETE
				 MOTION_COPY				MOTION_PASTE
		select - a selection was made simultaneously

		parameters: int (32-bit), bool
		returns: event
		"""

		if motion == MOTION_BACKSPACE:
			if self.mark is not None:
				self._delete_selection()
			elif self._position > 0:
				self._position -= 1
				self._layout.document.delete_text(self._position, self._position + 1)
				self._update()
		elif motion == MOTION_DELETE:
			if self.mark is not None:
				self._delete_selection()
			elif self._position < len(self._layout.document.text):
				self._layout.document.delete_text(self._position, self._position + 1)
		elif self._mark is not None and not select and \
			motion is not MOTION_COPY:
			self._mark = None
			self._layout.set_selection(0, 0)

		if motion == MOTION_LEFT:
			self.position = max(0, self.position - 1)
		elif motion == MOTION_RIGHT:
			self.position = min(len(self._layout.document.text), self.position + 1)
		elif motion == MOTION_UP:
			self.line = max(0, self.line - 1)
		elif motion == MOTION_DOWN:
			line = self.line
			if line < self._layout.get_line_count() - 1:
				self.line = line + 1
		elif motion == MOTION_BEGINNING_OF_LINE:
			self.position = self._layout.get_position_from_line(self.line)
		elif motion == MOTION_END_OF_LINE:
			line = self.line
			if line < self._layout.get_line_count() - 1:
				self._position = self._layout.get_position_from_line(line + 1) - 1
				self._update(line)
			else:
				self.position = len(self._layout.document.text)
		elif motion == MOTION_BEGINNING_OF_FILE:
			self.position = 0
		elif motion == MOTION_END_OF_FILE:
			self.position = len(self._layout.document.text)
		elif motion == MOTION_NEXT_WORD:
			pos = self._position + 1
			m = self._next_word_re.search(self._layout.document.text, pos)
			if not m:
				self.position = len(self._layout.document.text)
			else:
				self.position = m.start()
		elif motion == MOTION_PREVIOUS_WORD:
			pos = self._position
			m = self._previous_word_re.search(self._layout.document.text, 0, pos)
			if not m:
				self.position = 0
			else:
				self.position = m.start()

		self._next_attributes.clear()
		self._nudge()

	def _update(self, line=None, update_ideal_x=True):
		"""Update the caret. This is used internally for the Entry widget.

		line - current line of the caret
		update_ideal_x - x position of line is updated

		parameters: int, bool
		"""

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

		y += self._layout.y + self._layout.height / 2

		font = self._layout.document.get_font(max(0, self._position - 1))
		self._list.position[:] = [x, y + font.descent, x, y + font.ascent]

		if self._mark is not None:
			self._layout.set_selection(min(self._position, self._mark), max(self._position, self._mark))

		self._layout.ensure_line_visible(line)
		self._layout.ensure_x_visible(x)


class Entry(Widget):
	"""Entry widget to display user-editable text. This makes use of the
	pyglet.text.layout.IncrementalTextLayout and a modified version of its
	built-in caret.

	FIXME: caret not showing on line start
		   make caret transparent or invisible instead of changing color
		   caret glitching out on blinks at line end
		   entry taking up much CPU

	TODO
	1. Add rich text formatting (use pyglet.text.document.HTMLDocument)
	2. Add show feature for passwords
	3. Add copy, paste, select all, and more text features (COMPLETED)
	4. Add undo and redo features
	5. Enable updates for the layout for smoother performance. This raises
	   AssertionError, one that has been seen before.

	https://github.com/eschan145/Armies/issues/11

	Last updated: August 4th 2022
	"""

	blinking = True
	length = 0
	max = MAX
	_validate = printable
	_document = None

	undo_stack = []
	redo_stack = []

	# Validations
	VALIDATION_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
	VALIDATION_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	VALIDATION_LETTERS = VALIDATION_LOWERCASE + VALIDATION_UPPERCASE
	VALIDATION_DIGITS = "1234567890"
	VALIDATION_ADVANCED_DIGITS = "1234567890.+-*/^<>[]{}()!|"
	VALIDATION_PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
	VALIDATION_WHITESPACE = " \t\n\r\v\f"
	VALIDATION_REGULAR = None

	def __init__(self, x, y, text="", font=default_font, color=BLACK):
		"""Initialize the Entry. Typically a widget will push events
		automatically, but because there are custom named events, they have
		to be defined here.

		An Entry is a widget where text input can be returned. Typing into
		an Entry appends some text, which can be used for usernames,
		passwords, and more. Text can be removed by many keys.

		x - x position of the Entry
		y - y position of the Entry
		text - default text of the Entry
		font - font of the text in the Entry
		color - color of the text in RGB as a tuple of three ints

		properties:
			document - document of the IncrementalTextLayout
			layout - internal IncrementalTextLayout for efficient rendering
			caret - caret of the Entry
			image - image displayed to give the Entry a graphical look

			x - x position of the Entry
			y - y position of the Entry
			default - default text of the Entry (changing this has no effect)
			font - font of the Entry

			blinking - caret is visible or not visible

			length - length of the text in the Entry
			max - maximum amount of characters in the Entry

			text - displayed text of the Entry
			selection - selected text of the Entry
			layout_colors - layout colors of the Entry
			validate - validation of the characters in the Entry
			index - index of the caret (position)
			view - view vector of the Entry

		methods:
			blink - blink the caret and switch its visibility
			insert - insert some text in the Entry
			delete - delete some text from the Entry
		"""

		self._document = decode_text(text)

		self.layout = IncrementalTextLayout(self._document, 190, 24, batch=batch)

		self.image = Image(entry_normal, x, y)
		self.caret = Caret(self.layout)

		Widget.__init__(self, (self.image))

		self.x = x
		self.y = y
		self.default = text
		self.font = font

		self.layout.anchor_x = LEFT
		self.layout.anchor_y = CENTER

		self._document.set_style(0, len(text), dict(font_name=DEFAULT_FONT[0],
											  font_size=DEFAULT_FONT[1],
											  color=four_byte(color)))

		self.window.push_handlers(
			self.on_text,
			self.on_text_motion
		)

	def _get_document(self):
		"""Get the current document of the Entry.

		returns: pyglet.text.document.UnformattedDocument
		"""

		return self.layout.document

	def _set_document(self, document):
		"""Set the current document of the Entry.

		document - new document of Entry

		parameters: pyglet.text.document.UnformattedDocument
		"""

		self.layout.document = document

	def _get_text(self):
		"""Return the text of the Entry.

		returns: str
		"""

		return self.document.text

	def _set_text(self, text):
		"""Set the text of the Entry.

		text - new text to be displayed. This can be a string or a tuple
		change_index - index is changed after text input. If True, the index
					   is set to the end of the Entry.

		parameters: str or tuple
		"""

		if isinstance(text, Tuple):
			# self.document._delete_text(0, self.max)
			# self.document._insert_text(0, text[0], None)
			self.document.text = text

			if text[1]:
				# Put the caret to the end
				self.index = self.max

			return

		# self.document._delete_text(0, self.max)
		# self.document._insert_text(0, text, None)
		self.document.text = text

	def _get_x(self):
		"""Get the x position of the Entry.

		returns: int
		"""

		return self.image.x

	def _set_x(self, x):
		"""Set the x position of the Entry.

		x - new x position of the Entry

		parameters: int
		"""

		self.layout.x = self.x - self.layout.width / 2
		self.image.x = x

	def _get_y(self):
		"""Get the y position of the Entry.

		returns: int
		"""

		return self.image.y

	def _set_y(self, y):
		"""Set the y position of the Entry.

		y - new y position of the Entry

		parameters: int
		"""

		self.layout.y = y - 5
		self.image.y = y

	def _get_index(self):
		"""Return the index of the current caret position within the
		document.

		returns: int
		"""

		return self.caret.position

	def _set_index(self, index):
		"""Set the index of the current caret position within the document.

		index - new index of the caret position

		parameters: int
		"""

		self.caret.position = index

	def _get_selection(self):
		"""Get the selection indices of the Entry, with the start and end as
		a tuple.

		(start, end)

		returns: tuple (int, int), (start, end)
		"""

		return (
				self.layout.selection_start,
				self.layout.selection_end,
				self.text[
					self.layout.selection_start : self.layout.selection_end
				]
			   )

	def _set_selection(self, selection):
		"""Set the selection indices of the Entry, which are defined with
		the property layout_colors.

		selection - tuple of selection indices (start, end)

		parameters: tuple
		"""

		self.caret.mark = selection[1]

		self.layout.selection_start = selection[0]
		self.layout.selection_end = selection[1]

	def _get_layout_colors(self):
		"""Get the layout colors of the Entry. This will return a tuple of
		three colors defined by _set_layout_color. The selection background
		defaults to (46, 106, 197).

		(selection, caret, text)

		returns: tuple (list, list, list)
		"""

		return (
				self.layout.selection_background_color,
				self.caret.color,
				self.layout.selection_color
				)

	def _set_layout_colors(self, colors):
		"""Set the layout colors of the Entry.

		colors - tuple of three colors. The first item is the background
				color of the selection, while the second item is the caret
				color. The third item is the color of the text selected.

		parameters: tuple (selection, caret, text)
		"""

		self.layout.selection_background_color = colors[0]
		self.layout.selection_color = colors[2]

		self.caret.color = colors[1]

	def _get_validate(self):
		"""Get the validation of the Entry.

		returns: str
		"""

		return self._validate

	def _set_validate(self, validate):
		"""Set the validation of the Entry. This is a string containing all
		of the characters the user is able to type. Common charsets cam be
		found in the string module.

		validate - validation to set

		parameters: str
		"""

		self._validate = validate

	def _get_view(self):
		"""Get the view vector of the Entry.

		returns: tuple (x, y)
		"""

		return (
				self.layout.view_x,
				self.layout.view_y
		)

	def _set_view(self, view):
		"""Set the view vector of the Entry.

		view - vector of x and y views as a Point

		parameters: Point
		"""

		self.layout.view_x = view.x
		self.layout.view_y = view.y

	text = property(_get_text, _set_text)
	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)
	document = property(_get_document, _set_document)
	index = property(_get_index, _set_index)
	selection = property(_get_selection, _set_selection)
	layout_colors = property(_get_layout_colors, _set_layout_colors)
	validate = property(_get_validate, _set_validate)
	view = property(_get_view, _set_view)

	def blink(self, delta):
		"""The caret toggles between white and black colors. This is called
		every 0.5 seconds, and only when the caret has focus.

		delta - delta time in seconds since the function was last called.
				This varies about 0.5 seconds give or take, because of
				calling delay, lags, and other inefficiencies.

		parameters: float
		"""

		if not self.caret._list.colors[3] or \
			not self.caret._list.colors[7]:
			alpha = 255
		else:
			alpha = 0

		self.caret._list.colors[3] = alpha
		self.caret._list.colors[7] = alpha

	def insert(self, index, text, change_index=True):
		"""Insert some text at a given index one character after the index.

		>>> entry.text = "Hello!"
		>>> entry.insert(6, " world")
		>>> entry.text
		"Hello world!"

		"Hello world!"
			  ^^^^^^
			  678...

		index - index of the text addition
		text - text to be added
		change_index - index is updated to the end of the addition

		parameters: int, str
		"""

		# self.text = insert(index, self.text, text)

		self.document._insert_text(index, text, None)

		if change_index:
			self.index = self.index + len(text)

	def delete(self, start, end):
		"""Delete some text at a start and end index, one character after the
		start position and a character after the end position

		>>> entry.text = "Hello world!"
		>>> entry.delete(5, 10)
		>>> entry.text
		"Hello!"

		"Hello world!"
			  ^^^^^^
			  6... 11

		start - start of the text to be deleted
		end - end of the text to be deleted

		parameters: int, int
		"""

		# self.text = delete(start, end, self.text)

		self.document._delete_text(start, end)

	def draw(self):
		"""Draw the Entry. The layout is drawn with pyglet rendering.

		1. Image component
		2. Layout
		"""

		self.component = self.image

	def on_key(self, keys, modifiers):
		"""A key is pressed. This is used for keyboard shortcuts.

		keys - key pressed
		modifiers - modifier pressed

		parameters: int (32-bit), int (32-bit)
		"""

		if keys == SPACE:
			self.undo_stack.append(self.text)

		if modifiers & CONTROL:
			if keys == V:
				self.insert(self.index, clipboard_get(), change_index=True)
			elif keys == C:
				clipboard_append(self.selection[2])
			if keys == X:
				clipboard_append(self.selection[2])
				self.caret._delete_selection()
			elif keys == A:
				self.index = 0
				self.selection = (0, self.length, self.text)

	def on_focus(self):
		"""The Entry has focus, activating events. This activates the caret
		and stops a few errors.
		"""

		if self.text == self.default:
			self.text = ""
			self.index = 0
			self.mark = None

	def on_text(self, text):
		"""The Entry has text input. The Entry adds text to the end.
		Internally, the Entry does a few things:

			- Remove all selected text
			- Update the caret position
			- Appends text to the end of the layout

		text - text inputed by the user

		parameters: str
		"""

		if self.focus and \
			self.length < self.max:
			if self.validate:
				if text in self.validate:
					self.caret.on_text(text)

					return

		self.caret.on_text(text)

	def on_text_motion(self, motion):
		"""The Entry has caret motion. This can be moving the caret's
		position to the left with the Left key, deleting a character
		previous with the Backspace key, and more.

		motion - motion used by the user. This can be one of many motions,
				 defined by keyboard constants found in the keyboard module.

				 MOTION_LEFT				MOTION_RIGHT
				 MOTION_UP				  MOTION_DOWN
				 MOTION_NEXT_WORD		   MOTION_PREVIOUS_WORD
				 MOTION_BEGINNING_OF_LINE   MOTION_END_OF_LINE
				 MOTION_NEXT_PAGE		   MOTION_PREVIOUS_PAGE
				 MOTION_BEGINNING_OF_FILE   MOTION_END_OF_FILE
				 MOTION_BACKSPACE		   MOTION_DELETE
				 MOTION_COPY				MOTION_PASTE

				 You can get the list of all text motions with
				 motions_string() in the keyboard module.

		parameters: int (32-bit)
		"""

		if self.focus:
			try:
				self.caret.on_text_motion(motion)
			except AssertionError: # assert self.glyphs
				pass

	def on_text_select(self, motion):
		"""Some text in the Entry is selected. When this happens, the
		selected text will have a blue background to it. Moving the caret
		with a text motion removes the selection (does not remove the text).

		NOTE: this is not called with caret mouse selections. See on_press.

		motion - motion used by the user. These can be made with the user.

				 SHIFT + LEFT			   SHIFT + RIGHT
				 SHIFT + UP				 SHIFT + DOWN
				 CONTROL + SHIFT + LEFT	 CONTROL + SHIFT + RIGHT

		parameters: int (32-bit)
		"""

		if self.focus:
			self.caret.on_text_motion_select(motion)

			self.index = self.caret.position

	def on_press(self, x, y, buttons, modifiers):
		"""The Entry is pressed. This will do a number of things.

			- The caret's position is set to the nearest character.
			- If text is selected, the selection will be removed.
			- If the Shift key is being held, a selection will be created
			  between the current caret index and the closest character to
			  the mouse.
			- If two clicks are made within 0.5 seconds (double-click), the
			  current word is selected.
			- If three clicks are made within 0.5 seconds (triple-click), the
			  current paragraph is selected.

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		_x, _y = x - self.layout.x, y - self.layout.y

		self.caret.on_mouse_press(_x, _y, buttons, modifiers)

	def on_drag(self, x, y, dx, dy, buttons, modifiers):
		"""The user dragged the mouse when it was pressed. This can
		create selections.

		x - x position of the current position
		y - y position of the current position
		dx - movement in x vector from the last position
		dy - movement in y vector from the last position

		buttons - buttons that were dragged with the mouse
		modifiers - modifiers being held down

		parameters: int, int, float, float, int (32-bit), int (32-bit)
		"""

		_x, _y = x - self.layout.x, y - self.layout.y

		if self.press:
			self.caret.on_mouse_drag(_x, _y, dx, dy, buttons, modifiers)

			self.index = self.caret.position
		else:
			if self.focus:
				self.caret.on_mouse_drag(_x, _y, dx, dy, buttons, modifiers)

				self.index = self.caret.position

	def update(self):
		"""Update the caret and Entry. This schedules caret blinking and
		keeps track of focus.
		"""

		if not self.length == len(self.text):
			self.length = len(self.text)

		if self.focus:
			if not self.blinking:
				schedule(self.blink, ENTRY_BLINK_INTERVAL)

				self.blinking = True

		else:
			self.index = 0
			self.mark = None
			self.blinking = False

			unschedule(self.blink)


class Combobox(Widget, EventDispatcher):

	_display = []
	_view = None
	displayed = False
	last_text = None
	scroller = None

	def __init__(self, x, y, options, color="yellow", default=0):

		self.entry = Entry(x, y)
		self.button = Pushable(None, x, y, self.reset_display,
							   images=(widgets[f"{color}_button_square_normal"],
									   widgets[f"{color}_button_square_hover"],
									   widgets[f"{color}_button_square_press"])
							   )
		self.button.image.scale = 0.5

		self.buttons = []

		Widget.__init__(self, [self.entry])

		self.x = x
		self.y = y
		self.options = options
		self.display = options

		_widgets.append(self.entry.image)
		_widgets.append(self.button.image)

	def _get_text(self):
		return self.entry.text

	def _set_text(self, text):
		self.entry.text = text

	def _get_x(self):
		"""Get the x position of the Combobox.

		returns: int
		"""

		return self.entry.x

	def _set_x(self, x):
		"""Set the x position of the Combobox.

		x - new x position of the Combobox

		parameters: int
		"""

		self.entry.x = x

	def _get_y(self):
		"""Get the y position of the Combobox.

		returns: int
		"""

		return self.entry.y

	def _set_y(self, y):
		"""Set the y position of the Combobox.

		y - new y position of the Combobox

		parameters: int
		"""

		self.entry.y = y

	def _get_view(self):
		"""Get the vertical view of the Combobox.

		returns: int
		"""

		return self._view

	def _set_view(self, view):
		"""Set the vertical view of the Combobox.

		view - vertical view of the Combobox

		parameters: int
		"""

		self._view = view
		self.display = self.display[view : view + 3]

	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)
	view = property(_get_view, _set_view)

	def _get_display(self):
		return self._display

	def _set_display(self, display):
		self.buttons.clear()

		identifier = 1

		for option in display:
			identifier += 1

			if identifier == 2: image = (combobox_top_normal, combobox_top_normal)
			elif identifier == len(display) + 1: image = (combobox_bottom_normal, combobox_bottom_normal)
			else: image = (combobox_middle_normal, combobox_middle_normal)

			button = Pushable(
					  option, 0,
					  Y,
					  images=image,
					  command=self.switch,
					  parameters=identifier
					  )

			button.y = (self.x - 70) - 24 * identifier

			self.buttons.append(button)
			_widgets.append(button)

	text = property(_get_text, _set_text)
	display = property(_get_display, _set_display)

	def switch(self, identifier):
		if len(self.buttons) > 1:
			self.text = self.buttons[identifier - 2].text
		elif len(self.buttons) == 1:
			self.text = self.buttons[0].text

	def reset_display(self):
		self.display = self.options

	def draw(self):
		self.entry.draw()
		self.button.draw()

		self.button.x = self.right - 16

		for button in self.buttons:
			button.image.left = self.left
			button.label.x = self.left + 10

		self.component = self.entry

		if not self.displayed:
			self.display = self.options[:3]
			self.displayed = True

		if self.last_text is not self.entry.text and \
			self.entry.text:

			if self.entry.text == "" and \
				self.display is not self.options:
				self.display = self.options[:3]
				return

			self.display = []
			self.increment = (0, 0)
			# If filter removed show all data

			filtered_data = list()
			for item in self.options:
				if self.entry.text in item:
					filtered_data.append(item)

			self.display = filtered_data[:3]
			self.last_text = self.entry.text


class Pushable(Widget):
	"""Pushable widget to invoke and call commands. This is an extended version
	of the Button and allows more modifications.

	TODO: add specifying border properties (left, right, top, bottom)
	"""

	def __init__(
				 self, text, x, y, command=None, parameters=[],
				 images=(), font=default_font,
				 **kwargs
				):

		"""Initialize a Button. A Button has two components: an Image and a
		Label. You can customize the Button's images and display by changing
		its normal_image, hover_image, press_image, and disable_image
		properties, but it is recommended to use the CustomButton widget.

		text - text to be displayed on the Button
		x - x position of the Button
		y - y position of the Button
		command - command to be invoked when the Button is called
		parameters - parameters of the callable when invoked
		image - image of the Button as an Image
		font - font of the Button

		The last parameter is for parameters of the Image.

		parameters: str, int, int, callable, list, tuple, Font, str
		"""

		# A two-component widget:
		#	 - Image
		#	 - Label

		self.image = Image(images[0], x, y)
		self.label = Label(text, x, y, font=font)

		Widget.__init__(self, (self.image))

		self.text = text
		self.x = x
		self.y = y
		self.command = command
		self.parameters = parameters
		self.font = font

		self.normal_image = load_texture(images[0])
		self.hover_image = load_texture(images[1])
		self.press_image = load_texture(images[1])
		self.disable_image = load_texture(images[1])

	def _get_x(self):
		"""Get the x position of the Button.

		returns: int
		"""

		return self.image.x

	def _set_x(self, x):
		"""Set the x position of the Button.

		x - new x position of the Button

		parameters: int
		"""

		self.image.x = x

	def _get_y(self):
		"""Get the y position of the Button.

		returns: int
		"""

		return self.image.y

	def _set_y(self, y):
		"""Set the y position of the Button.

		y - new y position of the Button

		parameters: int
		"""

		self.image.y = self.label.y = y

	x = property(_get_x, _set_x)
	y = property(_get_y, _set_y)

	def invoke(self):
		"""Invoke the Button. This switches its image to a pressed state
		calls the command with the specified parameters. If the Button is
		disabled this will do nothing.
		"""

		if self.disable or not self.command:
			return

		self.press = True

		if self.parameters:
			self.command(self.parameters)
		else:
			self.command()

	def draw(self):
		"""Draw the Button. The component of the Button is the image, which takes
		all of the collision points.

		1. Image - background image of the Button
		2. Label - text of the Button
		"""

		self.image.draw()

		# Update Label properties

		self.label.text = self.text
		self.label.colors[0] = BLACK
		self.label.font = self.font

		self.component = self.image

	def on_press(self, x, y, buttons, modifiers):
		"""The Button is pressed. This invokes its command if the mouse button
		is the left one.

		TODO: add specifying proper mouse button in settings

		x - x position of the press
		y - y position of the press
		buttons - buttons that were pressed with the mouse
		modifiers - modifiers being held down

		parameters: int, int, int (32-bit), int (32-bit)
		"""

		if buttons == MOUSE_BUTTON_LEFT:
			self.invoke()

	def on_key(self, keys, modifiers):
		"""A key is pressed. This is used for keyboard shortcuts when the
		Button has focus.

		keys - key pressed
		modifiers - modifier pressed

		parameters: int (32-bit), int (32-bit)
		"""

		if keys == SPACE and self.focus:
			self.invoke()

		if isinstance(self.keys, list):
			if keys in self.keys:
				self.invoke()

		else:
			if self.keys == keys:
				self.invoke()

	def update(self):
		"""Update the Button. This registers events and updates the Button
		image.
		"""

		self.image.normal_image = self.normal_image
		self.image.hover_image = self.hover_image
		self.image.press_image = self.press_image

		if self.disable:
			self.image.texture = self.disable_image

		# .update is not called for the Label, as it is uneccessary for the
		# Label to switch colors on user events.

		self.image.update()


class Shape(Widget):
	"""Primitive drawing shape. This is subclassed by all shapes."""

	def __init__(self):
		"""Initialize a Shape. When using a Shape, be sure to create vertex
		lists from pyglet.graphics.vertex_list(), then draw them with pyglet
		rendering. Refer to the pyglet.shapes module for more information.

		A shape should not need an update function. Instead, put all of the
		properties as function-defined ones. This saves time and GPU. Also,
		instead of having x and y properties seperately, use a Point or a
		PointList.

		A shape should look like one from the pyglet.shapes module, but should
		be drawn with pyglet rendering. It should subclass a Widget or a Shape,
		but that is not necessary. If you do, however, keep in mind that the
		events of a widget will be dispatched, like draw and update. You can
		also add the shape's vertex list to a pyglet.graphics.Batch() for
		faster performance and draw the batch instead of drawing the vertex
		list.

		See https://pyglet.readthedocs.io/en/latest/modules/graphics/index.html
		"""

		Widget.__init__(self)

	def draw(self):
		"""Draw the shape with pyglet rendering. You may need to override this
		when creating your custom shapes.

		This was deprecated in favor of pyglet batching.
		"""

		# with self.window.ctx.pyglet_rendering():
		# 	self.shape.draw()

	def _get_alpha(self):
		"""Get the alpha or transparency of the shape. You may need to override
		this if creating your own custom shapes. An alpha of zero is completely
		transparent and invisible. An alpha of 255 is completely opaque.

		returns: int
		"""

		return self.shape.opacity

	def _set_alpha(self, alpha):
		"""Set the alpha or transparency of the shape. You may need to override
		this if creating your own custom shapes. An alpha of zero is completely
		transparent and invisible. An alpha of 255 is completely opaque.

		alpha - new alpha

		parameters: int
		"""

		if alpha > 255: alpha = 255
		if alpha < 0: alpha = 0

		self.shape.opacity = alpha

	alpha = property(_get_alpha, _set_alpha)

	def delete(self):
		"""Delete the shape and its events. The shape is not drawn. You may
		need to override this if creating your own custom shapes.
		"""

		self.shape.delete()


_Circle = Circle
_Ellipse = Ellipse
_Sector = Sector
_Line = Line
_Triangle = Triangle
_Star = Star
_Polygon = Polygon
_Arc = Arc


class Rectangle(Shape):
	"""A rectangular shape."""

	def __init__(self, x, y, width, height, border=1,
				 colors=(WHITE, BLACK), label=None):

		"""Create a rectangle.

		x - x position of rectangle
		y - y position of rectangle
		width - width of rectangle
		height - height of rectangle
		border - border width. The bigger this value is, the more three
				 dimensional effect there will be. If set to 0 there will be no
				 effect.
		colors - color of the rectangle in RGB as a tuple of three ints. There
				 are two tuples in a list, the first one for the shape fill and
				 the second one for the outline color. The default for this is:
				 [(255, 255, 255), (0, 0, 0)]
		label - draw a label over the rectangle. This must be a Label, not a
				string of its text.

		parameters: int, int, int, int, int, list [(RGB), (RGB)], Label
		"""

		self.shape = BorderedRectangle(
							x, y, width, height,
							border, colors[0], colors[1],
							batch=batch
						)

		Shape.__init__(self) # Do this after defining self.shape

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.border = border
		self.colors = colors
		self.label = label

	def update(self):
		self.shape.x = self.x - self.width / 2
		self.shape.y = self.y - self.height / 2
		self.shape.width = self.width
		self.shape.height = self.height
		self.shape.color = self.colors[0]
		self.shape.border_color = self.color[1]
		self.shape.border = self.border

		if self.label:
			self.label.x = self.x + self.width / 2
			self.label.y = self.y + self.height / 2


class Circle(Shape):
	"""A circular shape."""

	def __init__(self, x, y, radius, segments=None, color=BLACK):
		"""Create a circle.

		x - x position of the circle
		y - y position of the circle
		radius - radius of the circle (see _set_radius)
		segments - number of segments of the circle. This is the number of
				   distinct triangles should the circle be formed from. If not
				   specified it is calculated with

				   max(14, int(radius ÷ 1.25))
		color - color of the circle in RGB as a tuple of three ints

		parameters: int, int, int, int, tuple (RGB)
		"""

		if not segments:
			segments = max(14, int(radius / 1.25))

		self.shape = _Circle(x, y, radius, segments, color, batch=batch)

		Shape.__init__(self)

		self._point = Point(x, y)
		self.radius = radius
		self.segments = segments
		self.color = color

	def _get_point(self):
		"""Get the Point of the Circle.

		returns: Point
		"""

		return self._point

	def _set_point(self, point):
		"""Set the Point of the Circle. A Point and its documentation can be
		found at the geometry file.

		>>> circle.point = Point(3, 5)

		point - new Point

		parameters: int
		"""

		self.shape.x = point.x
		self.shape.y = point.y

		self._point = point

	def _get_radius(self, radius):
		"""Get the radius of the Circle (the distance from the center to the
		edge). The radius is the same throughout the whole circle.

		returns: int
		"""

		return self.shape.radius

	def _set_radius(self, radius):
		"""Set the radius of the Circle (the distance from the center to the
		edge). The radius is the same throughout the whole circle.

		radius - new radius

		parameters: int
		"""

		self.shape.radius = radius

	def _get_segments(self):
		"""Get the number of segments in the Circle. This is the number of
		distinct triangles that the Circle is made from.

		returns: int
		"""

		return self.shape._segments

	def _set_segments(self, segments):
		"""Set the number of segments in the Circle. This is the number of
		distinct triangles that the Circle is made from. On default, it is
		calculated by:

		max(14, int(radius ÷ 1.25))

		Note this must be used because you cannot draw a perfect circle on a
		pixeled monitor.

		parameters: int
		"""

		self.shape._segments = segments
		self.shape._update_position()

	point = property(_get_point, _set_point)
	radius = property(_get_radius, _set_radius)
	segments = property(_get_segments, _set_segments)


class Ellipse(Shape):
	"""An elliptical shape."""

	def __init__(self, x, y, a, b, color=BLACK):
		"""Create a ellipse. This can also be called Oval.

		x - x position of the ellipse
		y - y position of the ellipse
		a - semi-major axes of the ellipse. If this and height are equal, a
			circle will be drawn. To draw a circle, set the a and b equal and
			divide their desired width and height by two for the radius.
		b - semi-minor axes of the ellipse. See a for more information.
		color - color of the ellipse in RGB as a tuple of three ints

		parameters: int, int, int, int, tuple (RGB)

		"""

		self.shape = _Ellipse(x, y, a, b, color, batch=batch)

		Shape.__init__(self)

		self._point = Point(x, y)
		self.a = a
		self.b = b

	def _get_point(self):
		"""Get the Point of the Ellipse.

		returns: Point
		"""

		return self._point

	def _set_point(self, point):
		"""Set the Point of the Ellipse.

		>>> self.ellipse.point = Point(5, 3)

		point - new Point

		parameters: Point
		"""

		self.shape.x = point.x
		self.shape.y = point.y

		self._point = point

	def _get_a(self):
		"""Get the semi-major axes of the ellipse.

		returns: int
		"""

		return self.shape.a

	def _set_a(self, a):
		"""Set the semi-major axes of the ellipse.

		a - new semi-minor axes

		parameters: int
		"""

		self.shape.a = self.a

	def _get_b(self):
		"""Get the semi-minor axes of the ellipse.

		returns: int
		"""

		return self.shape.b

	def _set_b(self, b):
		"""Set the semi-minor axes of the ellipse.

		b - new semi-minor axes

		parameters: int
		"""

		self.shape.b = self.b

	def _set_ab(self, ab):
		"""Set the width and height of the ellipse as a tuple.

		This is equivalant to:

		>>> ellipse.a = a
		>>> ellipse.b = b

		ab - new width and height

		parameters: tuple (width, height)
		"""

		self.a = ab[0]
		self.b = ab[1]

	point = property(_get_point, _set_point)
	a = property(_get_a, _set_a)
	b = property(_get_b, _set_b)


Oval = Ellipse


class Sector(Shape):
	"""A sector or pie slice of a circle."""

	def __init__(self, x, y, radius, segments=None,
				 angle=tau, start=0, color=BLACK):

		"""Create a sector. A sector is essentially a slice of a circle. The
		sector class was created from the arc class in pyglet.

		x - x position of the sector
		y - y position of the sector
		radius - radius of the sector (see _set_radius)
		segments - number of segments of the sector. This is the number of
				   distinct triangles should the sector be formed from. If not
				   specified it is calculated with

				   max(14, int(radius ÷ 1.25))
		angle - angle of the sector in radians. This defaults to tau, which
				is approximately equal to 6.282 or 2π
		start - start angle of the sector in radians

		parameters: int, int, int, int, int
		"""

		self.shape = _Sector(x, y, radius, segments, angle, start, color, batch=batch)

		Shape.__init__(self)

		self._point = Point(x, y)
		self.radius = radius
		self.segments = segments
		self.rotation = angle
		self.start = start
		self.color = color

	def _get_point(self):
		"""Get the Point of the sector.

		returns: Point
		"""

		return self._point

	def _set_point(self, point):
		"""Set the Point of the sector.

		>>> sector.point = Point(5, 3)

		point - new Point

		parameters: Point
		"""

		self._point = point

		self.shape.x = point.x
		self.shape.y = point.y

	def _get_radius(self):
		"""Get the radius of the sector. This is the distance from the center of
		the circle to its edge.

		returns: int
		"""

		return self.shape.radius

	def _set_radius(self, radius):
		"""Set the radius of the sector. This is the distance from the center of
		the circle to its edge.

		radius - new radius

		parameters: int
		"""

		self.shape.radius = radius

	def _get_start(self):
		"""Get the start angle of the sector.

		returns: int
		"""

		return self.shape.start_angle

	def _set_start(self, start):
		"""Set the start angle of the sector.

		start - new start angle

		parameters: int
		"""

		self.shape.start = self.start

	def _get_segments(self):
		"""Get the number of segments in the sector. This is the number of
		distinct triangles that the sector is made from.

		returns: int
		"""

		return self.shape._segments

	def _set_segments(self, segments):
		"""Set the number of segments in the sector. This is the number of
		distinct triangles that the sector is made from. On default, it is
		calculated by:

		max(14, int(radius ÷ 1.25))

		Note this must be used because you cannot draw a perfect sector on a
		pixeled monitor.

		parameters: int
		"""

		self.shape._segments = self.segments
		self.shape._update_position()

	point = property(_get_point, _set_point)
	radius = property(_get_radius, _set_radius)
	start = property(_get_start, _set_start)
	segments = property(_get_segments, _set_segments)


class Line(Shape):
	"""A line shape."""

	def __init__(self, point1, point2, width=1, color=BLACK):
		"""Create a line. Unlike other shapes, a line has a start point and an
		endpoint.

		point1 - first start coordinate pair of line
		point2 - second end coordinate pair of line
		width - width, weight or thickness
		color - color of the line in RGB in a tuple of three ints

		parameters: Point, Point, int, tuple (RGB)
		"""

		# Normally we don't format like this. But it makes it neater and more
		# consistent when we use three lines instead of one.

		self.shape = _Line(point1.x, point1.y,
						   point2.x, point2.y,
						   width, color, batch=batch)

		Shape.__init__(self)

		self._point1 = point1
		self._point2 = point2
		self.width = width
		self.color = color

	def _get_point1(self):
		"""Get the first Point of the line.

		returns: Point
		"""

		# We can't return thea new Point, as it would have a different id

		return self._point1

	def _set_point1(self, point1):
		"""Set the first Point of the line.

		point1 - new Point

		parameters: Point
		"""

		self._point1 = point1

		self.shape.x1 = point1.x
		self.shape.y1 = point1.y

	def _get_point2(self):
		"""Get the second Point of the line.

		returns: Point
		"""

		# We can't return thea new Point, as it would have a different id

		return self._point2

	def _set_point2(self, point2):
		"""Set the second Point of the line.

		point1 - new Point

		parameters: Point
		"""

		self._point2 = point2

		self.shape.x2 = point2.x
		self.shape.y2 = point2.y

	def _get_width(self):
		"""Get the width of the line.

		returns: int
		"""

		return self.shape._width

	def _set_width(self, width):
		"""Set the width of the line. This has an alias called thickness and
		another called weight.

		width - new width

		parameters: int
		"""

		self.shape._width = width

	point1 = property(_get_point1, _set_point1)
	point2 = property(_get_point2, _set_point2)
	width = property(_get_width, _set_width)

	# Alias
	thickness = width
	weight = width


class Triangle(Shape):
	"""A triangular shape."""

	def __init__(self, points, color=BLACK):
		"""Create a triangle."""

		self.shape = _Triangle(*points, color, batch=batch)

		Shape.__init__(self)

		self._points = PointList(points)
		self.color = color

	def _get_points(self):
		"""Get the points of the triangle. This is listed as point1, point2,
		and point3, which each have their x and y coordinates.

		returns: Pointlist
		"""

		return self._points

	def _set_points(self, points):
		"""Set the points of the triangle. This is listed as point1, point2,
		and point3, which each have their x and y coordinates.

		points - new pointlist of triangle

		parameters: Pointlist
		"""

		self._points = points

		self.shape.x1 = points[0].x
		self.shape.y1 = points[0].x
		self.shape.x2 = points[1].x
		self.shape.y2 = points[1].x
		self.shape.x3 = points[2].x
		self.shape.y3 = points[2].x

	points = property(_get_points, _set_points)


class Star(Shape):

	def __init__(self, x, y, outer, inner,
				 spikes=5, rotation=0, color=BLACK):

		self.shape = _Star(x, y, outer, inner, spikes, rotation, color, batch=batch)

		Shape.__init__(self)

		self.x = x
		self.y = y
		self.outer = outer
		self.inner = inner
		self.spikes = spikes
		self.rotation = rotation
		self.color = color

	def update(self):
		self.shape.x = self.x
		self.shape.y = self.y
		self.shape.outer_radius = self.outer
		self.shape.inner_radius = self.inner
		self.shape.num_spikes = self.spikes
		self.shape.rotation = self.rotation
		self.shape.color = self.color


class Polygon(Shape):

	def __init__(self, *coordinates, color=BLACK):
		self.shape = _Polygon(*coordinates, color, batch=batch)

		Shape.__init__(self)

		self.coordinates = list(coordinates)
		self.color = color

	def update(self):
		self.shape.coordinates = self.coordinates
		self.shape.color = self.color


class Arc(Shape):

	def __init__(self, x, y, radius, segments=None,
				 angle=tau, start=0, closed=False, color=BLACK):

		self.shape = _Arc(x, y, radius, segments, angle, start, closed, color, batch=batch)

		Shape.__init__(self)

		self.x = x
		self.y = y
		self.radius = radius
		self.segments = segments
		self.rotation = angle
		self.start = start
		self.closed = closed
		self.color = color

	def update(self):
		self.shape.x = self.x
		self.shape.y = self.y
		self.shape.radius = self.radius
		self.shape.segments = self.segments
		self.shape.angle = self.rotation
		self.shape.start = self.start
		self.shape.closed = self.closed


class MyWindow(Window):

	def __init__(self, title, width, height):

		Window.__init__(
			self, width, height, title, style=Window.WINDOW_STYLE_DIALOG,
		)

		from pyglet.image import load

		from file import blank1, blank2

		global shapes

		shapes = ShapeElementList()

		self.set_icon(load(blank1), load(blank2))
		self.set_exclusive_keyboard()

		container.window = self

		time1 = time()

		self.label = Label(
			"<b>Bold</b>, <i>italic</i>, and <u>underline</u> text.",
			10,
			60,
			multiline=True,
			width=500)

		self._label = Label(
			None,
			10,
			80)

		self.button = Button(
			"Click me!",
			250,
			250,
			command=self.click,
			link="office.com")

		self.toggle = Toggle(
			"Show fps",
			250,
			350)

		self.slider = Slider(
			None,
			250,
			300)

		self.entry = Entry(
			300,
			160,
		)
			#["apple", "banana", "mango", "orange"])

		self.circle = Circle(
			100,
			150,
			50,
			color=BLUE_YONDER)

		time2 = time()

		print(time2 - time1)

		self.button.bind(ENTER)

		self.background_color = WHITE

	def click(self):
		self._label.text = self.entry.text

	def on_draw(self):
		self.clear()
		container.draw()

		if self.toggle.value:
			self.label.text = f"{int(get_fps())} fps"
		else:
			self.label.text = "<b>Bold</b>, <i>italic</i>, and <u>underline</u> text in HTML"

		self.slider.text = str(int(self.slider.value))


if __name__ == "__main__":
	window = MyWindow(" ", 500, 400)

	from pyglet.app import run
	run(1/2000)
