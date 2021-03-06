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

import tkinter, functools

widget_area = None

on_dnd_start = None

class CoreWidget:

    row = column = 0

    def __init__(self, widget_type, display_widget, *args, **kwargs):
        '''
        Takes:
        - self
        - widget_type -- The type of tkinter widget that the instance will be
        - display_widget -- The widget the CoreWidget will display as
        '''

        self.widget_type = widget_type

        self.widget = "tkinter.{0}(widget_area.canvas,".format(display_widget)

        if args:
            self.widget += ", ".join(
                [
                    "'{0}'".format(arg) if arg[0] != "$"
                    else "{0}".format(arg[1:])
                    for arg in args
                ]
            ) + ", "


        self.widget += str(kwargs) + ")"
        self.widget = eval(self.widget)


        self.widget.grid(row=CoreWidget.row, column=CoreWidget.column)

        if CoreWidget.column == 1:
            CoreWidget.row += 1
            CoreWidget.column = 0
        else:
            CoreWidget.column = 1

        self.widget.bind("<ButtonPress>", functools.partial(on_dnd_start, widget_type=widget_type, display_widget=display_widget))
