'''
MIT License

Copyright (c) 2018 JonoCode9374

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#!/usr/bin/env python3

'''

Project: BreezyUI Version b1.3.0 (b1.3.0.py)
Author: JonoCode9374
Date Created: 28/8/2018
Description:

Many Python users who work with graphical interfaces know the pains of
designing and creating a Graphical User Interface with Python’s built-in
graphics library tkinter (Tkinter in Python 2 and tkinter in Python 3) –
creating interfaces requires intense planning (getting the co-ordinates
for where each widget goes), lots of trial and error. This is what I
have personally experienced many times, making programs such as my SpamBot,
DocEdit and my Head Scruiteneer Program.

'''

import sys

if sys.version_info[0] == 2:
    import Tkinter as tkinter
    import Tkinter.dnd
    import tkFileDialog
else:
    import tkinter
    from tkinter import dnd #Accessed with `tkinter.dnd`. Provides drag'n'drop
                            #services
    import tkinter.filedialog


import functools
sys.path.insert(0, '../Libraries')

import screens, bUI
import tkinter.colorchooser as tkColor

class DndWidget():
    id_number = 0
    def __init__(self, widget, **kwargs):
        '''
        Takes:
        - self
        - widget [str] -- The type of widget that this instance will be
        - kwargs [dict] -- Arguments used to build widget later on

        Does:
        - Initalises the instance of DndWidget

        Returns:
        - None
        '''
        self.widget_type = widget
        self.canvas = self.widget = self._id =  None
        self.kwargs = kwargs
        self.name = "object{}".format(DndWidget.id_number)
        DndWidget.id_number += 1


    def attach(self, canvas, x=10, y=10):
        '''
        Takes:
        - self
        - canvas [tkinter.Canvas()] -- The canvas the widget will be attached to
        - x [int] -- The x position of the widget (def. 10)
        - y [int] -- The y position of the widget (def. 10)

        Does:
        - Attaches the widget to the given canvas at the provided co-ordinates
        - Creates the widget
        - Binds it to functions allowing it to function

        Returns:
        - None
        '''

        global target_widget

        if canvas is self.canvas:
            self.canvas.coords(self._id, x, y)
            return

        if self.canvas:
            self.detach()

        if not canvas:
            return

        widget = eval("tkinter.{0}(canvas, {1})".format(self.widget_type, ', '.join([str(x) + '=' + self.kwargs[x] for x in self.kwargs])))



        _id = canvas.create_window(x, y, window=widget, anchor="nw")
        self.canvas = canvas
        self.widget = widget
        self._id = _id
        self.x_off = 0
        self.y_off = 0
        widget.bind("<ButtonPress>", self.press)
        self.widget.bind("<Button-2>", functools.partial(edit_attributes, source=self.widget, dnd_source=self))
        self.txt_var = tkinter.StringVar()

        if self.widget_type == "Entry":
            self.widget["textvariable"] = self.txt_var #I love this line (see fix 001)
        else:
            self.widget["state"] = "normal"

        self.attributes = bUI.get_attributes(self.widget)
    def detach(self):
        '''
        Takes:
        - self

        Does:
        - Detaches the widget from the canvas
        - Destroys the widget

        Returns:
        - None
        '''

        canvas = self.canvas
        if not canvas: return

        _id = self._id
        widget = self.widget
        self.canvas = self.widget = self._id = None
        canvas.delete(_id)
        widget.destroy

    def press(self, event):
        '''
        Takes:
        - self
        - event [?] -- the event that happened when the widget was clicked?

        Does:
        - ?

        Returns:
        - None
        '''

        if tkinter.dnd.dnd_start(self, event):
            # where the pointer is relative to the widget widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self._id)

    def move(self, event):
        '''
        Takes:
        - self
        - event [?] -- don't know what it is for

        Does:
        - Moves the widget on the canvas
        - Updates the internal co-ordinates

        Returns:
        - None
        '''

        x, y = self.where(self.canvas, event)
        self.canvas.coords(self._id, x, y)

    def putback(self):
        '''
        Takes:
        - self

        Does:
        - I'm not too sure

        Returns:
        - None
        '''

        self.canvas.coords(self._id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        '''
        Takes:
        - self
        - canvas [tkinter.Canvas()] -- The canvas which the widget is on
        - event [?] -- ?

        Does:
        - Calculates the relative position of the widget

        Returns:
        - (int) -- A tuple with the relative position of the widget
        '''

        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        '''
        Stub function? I'm not sure. Not much need to document this,
        as it only does nothing. I think that this function is needed
        for compatability with the tkinter.dnd library
        '''

        pass

class DndSpace:
    def __init__(self, root, width, height):
        '''
        Takes:
        - self
        - root [tkinter.Tk()] -- the window which the space will be on
        - width [int] -- the width of the canvas
        - height [int] -- the height of the canvas

        Does:
        - Intalises this instance of DndSpace

        Returns:
        - None
        '''

        self.top = tkinter.Toplevel(root)
        self.top.withdraw()
        self.canvas = tkinter.Canvas(self.top, width=width, height=height)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept


    def show(self):
        self.top.deiconify()

    def hide(self):
        self.top.withdraw()

    #The next function is more of a compability function, I believe, as it just
    #returns self                                                             .

    def dnd_accept(self, source, event):
        '''
        For reasons explained above, there will be no documentation for this
        function
        '''

        return self

    def dnd_enter(self, source, event):
        '''
        Takes:
        - self
        - source [tkinter widget] -- the widget being moved onto the DndSpace
        - event [?] -- ?

        Does:
        - Sets up the widget for when it is dragged onto the DndSpace

        Returns:
        - None
        '''

        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source._id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)

    #I won't comment the next few functions, as I don't quite understand them in
    #enough detail to provide what they take, do and return                    .

    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)

    def dnd_leave(self, source, event):
        self.top.focus_set() # Hide highlight border
        self.canvas.delete(self.dndid)
        self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)

class CoreWidget:

    row = column = 0

    def __init__(self, widget_type, **kwargs):
        '''
        Takes:
        - self
        - widget_type -- The type of tkinter widget that the instance will be
        '''

        self.widget_type = widget_type
        self.widget = eval("tkinter.{0}(widget_area.canvas, {1})".format(widget_type, ', '.join([str(x) + '=' + kwargs[x] for x in kwargs])))

        self.widget.grid(row=CoreWidget.row, column=CoreWidget.column)

        if CoreWidget.column == 1:
            CoreWidget.row += 1
            CoreWidget.column = 0
        else:
            CoreWidget.column = 1

        self.widget.bind("<ButtonPress>", functools.partial(on_dnd_start, widget_type=widget_type))

class Option:
    row = 0

    def __init__(self, name, config_name, attr_var, widget_type, applicable_widgets, *args, **kwargs):
        '''
        Takes:
        - self
        - name [str] -- The name of this option
        - config_name [str] -- The config attribute this affects
        - attr_var [str] -- The variable which the attribute is stored in
        - widget_type [str] -- The type of widget this option is
        - applicable_widgets [[str]] -- The widgets this option shows for
        - **kwargs -- The arguments to construct the widget

        Does:
        - Initalises this instance of option

        Returns:
        - None

        '''

        self.name = name
        self.attribute = config_name
        self.var = attr_var

        #Create the label and widget for this option
        self.label = tkinter.Label(attributes_area, text=name)

        construction = "tkinter.{0}(attributes_area".format(widget_type)

        if args:
            args = ", ".join([str(x) for x in args])
            construction = "{0}, {1}".format(construction, args)
            #At this point, construction would equal something like this:
            #tkinter.widget_type(attributes_area, args

        if kwargs:
            kwargs = ', '.join([str(x) + '=' + kwargs[x] for x in kwargs])
            construction = "{0}, {1}".format(construction, kwargs)
            #If the args wasn't empty, construction would look like this: tkinter.widget_type(attributes_area, args, kwargs

        construction += ")"


        self.option = eval(construction)

        self.x = Option.row
        Option.row += 1

        self.widgets = applicable_widgets


    def show(self, widget_type):
        '''
        Takes:
        - self
        - widget_type [str] -- The type of widget being shown

        Does:
        - Shows the widget in the appropriate location if it is for a widget it supports

        Returns:
        - None
        '''



        if widget_type in self.widgets:
            if self.name == "Display Text":
                self.option.delete(0, tkinter.END)
                self.option.insert(0, target_widget.cget("text"))

            elif self.name == "Background Colour":
                self.option["text"] = target_widget.cget("bg")

            elif self.name == "Border Colour":
                self.option["text"] = target_widget.cget("highlightbackground")

            self.label.grid(row=self.x, column=0)
            self.option.grid(row=self.x, column=1)

    def hide(self):
        '''
        Takes:
        - self

        Does:
        - Hides the widget using `.grid_forget()`

        Returns:
        - None
        '''

        self.label.grid_forget()
        self.option.grid_forget()

def on_dnd_start(event, widget_type):
    '''
    This is invoked when a widget is dragged onto the main canvas.
    '''

    global dragged_widgets

    #Create the widget to be dragged
    if widget_type in ["Label", "Button", "Entry"]:
        dnd_widget = DndWidget(widget_type, text='"Text"', state='"disabled"') #Maybe soon make this dynamic
    else:
        dnd_widget = DndWidget(widget_type, bd="1", relief="'solid'", highlightbackground="'#ffffff'")
    dragged_widgets.append(dnd_widget)
    dnd_widget.attach(widget_area.canvas)
    tkinter.dnd.dnd_start(dnd_widget, event)

def edit_attributes(event, source, dnd_source):
    global target_widget, target_dndw
    target_dndw = dnd_source
    target_widget = source
    attributes_area.geometry("+{0}+{1}".format(width_entry.get(), widget_area.top.winfo_height() + 100))
    attributes_area.deiconify()

    for item in options:
        options[item].hide()

    for item in options:
        options[item].show(w_type(target_widget))

def hide_attributes():
    for item in options:
        options[item].hide()
    options["text"].option.delete("0", tkinter.END)
    options["placeholder"].option.delete("0", tkinter.END)
    attributes_area.withdraw()

def update_widget():
    global target_widget
    widget_type = w_type(target_widget)

    for option in options:
        option = options[option]
        if widget_type in option.widgets:
            if option.attribute == "":
                continue
            if option.attribute[0] != "$":
                target_widget.config({option.attribute : eval(option.var) })

            elif option.attribute == "$type":
                if entry_type.get() == "Password":
                    target_widget.config({"show" : "*"})
                else:
                    continue

            elif option.attribute == "$placeholder":
                target_widget["state"] = "normal"
                target_dndw.txt_var.set(options["placeholder"].option.get())
                target_widget["state"] = "disabled"


            elif option.attribute == "$confirm":
                print("Confirmed")
    hide_attributes()
    target_widget = None


def choose_colour(event):
    global colour
    colour = tkColor.askcolor()[1]
    options["background"].option["bg"] = colour
    options["background"].option["text"] = colour

def choose_border_col(event):
    global border_colour
    border_colour = tkColor.askcolor()[1]
    options["canvas border colour"].option["bg"] = options["canvas border colour"].option["text"] = border_colour

def w_type(source):
    '''
    Takes:
    - source (a tkinter widget)

    Does:
    - See the the return section

    Returns:
    - The type of widget the option has
    '''

    widget_type = str(type(source))

    widget_type = widget_type[widget_type.find(".") + 1 : widget_type.find("'", widget_type.find("."))]

    return widget_type

def new():
    if validate_size(width_entry.get(), height_entry.get()):
        home_screen.hide()
        root.withdraw()
        main_area.show()
        main_area.top.geometry("{0}x{1}".format(width_entry.get(), height_entry.get()))
        widget_area.top.geometry("+{0}+60".format(width_entry.get()))
        widget_area.show()

def back():
    home_screen.show()
    #TODO: Empty entry widgets
    root.deiconify()
    main_area.hide()
    widget_area.hide()
    attributes_area.withdraw()

def validate_size(width, height):
    try:
        int(width)
        int(height)
    except ValueError:
        #TODO: Show that the canvas size is invalid
        return False

    if width == "" or height == "":
        return False

    return True



dragged_widgets = list() #of widgets
target_widget = None
target_dndw = None #Stores the DndWidget form of the target widget (dndw stands for DND Widget)

root = tkinter.Tk()
root.geometry("800x600")
#############################################
#The home screen
home_screen = screens.ScreenXY("BreezyUI", root)

menu_bar = tkinter.Frame(root, height=600, width=200, bg="#878E88")
creation_bar = tkinter.Frame(root, height=200, width=600, bg="#C9CAC9")

width_lbl = tkinter.Label(root, text="Width (px): ", bg="#C9CAC9", font=("Arial", 24))
height_lbl = tkinter.Label(root, text="Height (px): ", bg="#C9CAC9", font=("Arial", 24))

width_entry = tkinter.Entry(root, width=10)
height_entry = tkinter.Entry(root, width=10)


new_button = tkinter.Button(root, text="Create", command=new, width=25)
home_screen.add_item(menu_bar, 0, 0)
home_screen.add_item(creation_bar, 200, 0)
home_screen.add_item(new_button, 200, 100)
home_screen.add_item(width_lbl, 210, 10)
home_screen.add_item(height_lbl, 205, 50)
home_screen.add_item(width_entry, 350, 15)
home_screen.add_item(height_entry, 350, 55)
home_screen.show()

#############################################
#The widgets section
main_area = DndSpace(root, 800, 600)
main_area.top.geometry("+1+60")

widget_area = DndSpace(root, 200, 600)
widget_area.top.geometry("+803+60")



widgets = dict() #A dictionary to store all the widget objects which the clones will come from

widgets["label"] = CoreWidget("Label", text="'Label'")
widgets["button"] = CoreWidget("Button", text="'Button'")
widgets["entry"] = CoreWidget("Entry")
widgets["canvas"] = CoreWidget("Canvas", bd="1", relief="'solid'", highlightbackground="'#ffffff'")

widgets["entry"].widget.delete(0, tkinter.END)
widgets["entry"].widget.insert(0, "Entry")

widgets["entry"].widget["state"] = "disabled"



attributes_area = tkinter.Toplevel()
attributes_area.geometry("+803+160")
attributes_area.withdraw()


colour = "#ffffff"
entry_type = tkinter.StringVar(root, "Plain")
border_colour = "#000000"

options = dict() #A dictionary to store all the attributes shown in the
                 #attributes area

options["text"] = Option("Display Text", "text", "options['text'].option.get()", "Entry", ["Label", "Button"])
options["background"] = Option("Background Colour", "background", "colour", "Label", ["Label"], text="'#ffffff'", borderwidth="2", relief="'flat'", highlightcolor="'black'")

options["background"].option.bind("<Button-1>", choose_colour)

options["entry type"] = Option("Type", "$type", "entry_type", "OptionMenu", ["Entry"], 'entry_type', "'Plain'", "'Password'", "'Numeric'" )
options["placeholder"] = Option("Placeholder", "$placeholder", "placeholder_text", "Entry", ["Entry"])


options["canvas border colour"] = Option("Border Colour", "highlightbackground", "border_colour", "Label", ["Canvas"], text="'#000000'")

options["canvas border colour"].option.bind("<Button-1>", choose_border_col)

options["confirm"] = Option("", "" , "$confirm", "Button", ["Label", "Button", "Entry", "Canvas"], text="'Confirm'", command="update_widget")





def export():
    code = """

#############################################################
#     The following code was pre-generated by BreezyUI.     #
#Don't change any of the code if you don't know what it does#
#############################################################

import sys
if sys.version_info[0] == 2:
    import Tkinter as tkinter #backwards compatability
else:
    import tkinter

root = tkinter.Tk()
root.geometry("{0}x{1}") #Set the size of the window
    """.format(width_entry.get(), height_entry.get()) + "\n"
    for i in range(len(dragged_widgets)):
        widget = dragged_widgets[i]
        to_export = bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))
        code += "{0} = tkinter.{1}(root, {2})".format(widget.name, widget.widget_type, to_export) + "\n"

        code += "{0}.place(x={1},y={2})".format(widget.name, widget.widget.winfo_x(), widget.widget.winfo_y()) + "\n"

        if widget.widget_type == "Entry":
            if widget.widget.get():
                code += "{0}.insert(0, {1})".format(widget.name, widget.widget.get()) + "\n"

    code += ("\n#################END OF GENERATED CODE#################")
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))
    file = open(root.filename + ".py", "w")
    file.write(code)
    file.close()


def save_bUI_file():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))
    file = open(root.filename + ".bui", "w")

    #Generate the bUI file
    for widget in dragged_widgets:
        widget_config = {"id" : widget.name, "type" : widget.widget_type, "x" : widget.widget.winfo_x(), "y" : widget.widget.winfo_y(), "attributes" : bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))}

        if widget.widget_type == "Entry":
            widget_config["attributes"]["Placeholder"] = widget.widget.get()

        file.write(str(widget_config))

    #Add the bUI file to the recents list
    file = open("../Resources/recent.txt", "a")
    file.write(root.filename + ".bui" + "\n")
    file.close()

def load(file):
    '''
    Takes a
    '''
    print("Loading file")

def goof():
    print("Fiddle Riddle Diddle Diddle")

#Make all the menus
menu_bar = tkinter.Menu(root)
file_menu = tkinter.Menu(menu_bar, tearoff=0)
open_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=back)
file_menu.add_command(label="Save", command=save_bUI_file)
file_menu.add_command(label="Export", command=export)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.quit)

#Dynamically generate the open_menu
files = [line.strip("\n") for line in open("../Resources/recent.txt").readlines()]
for file in files:
    open_menu.add_command(label=file, command=goof)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Recent Files", menu=open_menu)
root.config(menu=menu_bar)
root.mainloop()
