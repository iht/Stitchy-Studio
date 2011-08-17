# Copyright (c) 2011 Israel Herraiz <isra@herraiz.org>

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import wx
import numpy
from numpy import zeros

class Grid:
    
    def __init__ (self):

        self._xcells = 120
        self._ycells = 80

        self._xsize = 1200
        self._ysize = 800

        self._zoom_factor = 100

        self._init_matrix ()

    def _init_matrix (self):
        
        self._cells = zeros ((self._xcells, self._ycells), dtype=numpy.bool)
        self._colors = {}

        for x in range (self._xcells):
            for y in range (self._ycells):
                self._colors[(x,y)] = None
        
    def decrease_zoom (self):

        self._xsize = self._xsize - self._zoom_factor
        self._ysize = self._ysize - self._zoom_factor
        
    def increase_zoom (self):

        self._xsize = self._xsize + self._zoom_factor
        self._ysize = self._ysize + self._zoom_factor

    def get_size (self):

        return (self._xsize, self._ysize)
    
    def draw_grid(self, dc):

        step = self._xsize / self._xcells
        boldstep = step * 10

        # Vertical lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))
        for x in range(self._xcells+1):
            xsize = x*step
            ysize = step * self._ycells
            dc.DrawLine(xsize, 0, xsize, ysize)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,3))
        for x in range((self._xcells)/10+1):
            xsize = x*boldstep
            ysize = step * self._ycells
            dc.DrawLine(xsize, 0, xsize, ysize)

            
        # Horizontal lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))

        for y in range(self._ycells+1):
            ysize = y*step
            xsize = self._xcells*step
            dc.DrawLine(0, ysize, xsize, ysize)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,3))
        for y in range((self._ycells)/10+1):
            ysize = y*boldstep
            xsize = self._xcells*step
            dc.DrawLine(0, ysize, xsize, ysize)

        for x in range(self._xcells):
            for y in range(self._ycells):
                
                if self._cells[x][y]:
                    self._paint_cell (x, y, dc, self._colors[(x,y)])
            
    def add_cell (self, x, y, dc, color):

        step = self._xsize / self._xcells
        
        xcell = int(x/step)
        ycell = int(y/step)

        self._cells[xcell][ycell] = True
        self._colors[(xcell,ycell)] = color
        self._paint_cell (xcell, ycell, dc, color)

    def _paint_cell (self, xcell, ycell, dc, color):

        step = self._xsize / self._xcells

        px = xcell * step
        py = ycell * step

        if color:
            dc.SetPen (wx.Pen(color))
            dc.SetBrush (wx.Brush (color))
        else:
            dc.SetPen (wx.RED_PEN)
            dc.SetBrush (wx.RED_BRUSH)

        dc.DrawRectangle(px+1,py+1,step - 2,step - 2)
