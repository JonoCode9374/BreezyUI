# `DndWidget`

_A class allowing for draggable widgets to be created like tkinter widgets would_

`DndWidget`.**\_\_init\_\_**(_self_, _widget_, _\*\*kwargs_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`self`|self|The required self for class initialisation|
|`widget`|`str`|The type of widget the instance of `DndWidget` will be|
|`**kwargs`|`dict` [`str` : _mixed_]|The arguments to build the widget|

Creates a `DndWidget` object which stores a tkinter widget that is able to be dragged around. It also stores the id of the widget, the canvas position of the widget. Doesn't return anything.

`DndWidget`.**attach**(_self_, _canvas_, _x=10_, _y=10_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`canvas`|`tkinter.Canvas`| The canvas which the `DndWidget` will be stored on|
|`x`|`int`|The x position where the `DndWidget` will be placed (optional)|
|`y`|`int`|The y position where the `DndWidget` will be placed (optional)|

Creates the draggable tkinter widget, places it at the specified co-ordinates (default `(10, 10)`) and enables it to be edited. Doesn't return anything.

`DndWidget`.**detach**(_self_)

Simply detaches the widget from the canvas and destroys it. Doesn't return anything.

`DndWidget`.**press**(_self_, _event_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`event`|_Unknown_|The event given when the widget is pressed|

Updates the x and y position of the pointer and returns nothing.

`DndWidget`.**move**(_self_, _event_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`event`|_Unknown_|The event given to the widget when moved|

Moves the widget on the canvas and updates the x and y position of the widget. Doesn't return anything.