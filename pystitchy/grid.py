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
        self._xoffset = self._xsize / self._xcells * 5
        self._yoffset = self._xoffset


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

        self._xoffset = self._xsize / self._xcells * 5
        self._yoffset = self._xoffset
        
    def increase_zoom (self):

        self._xsize = self._xsize + self._zoom_factor
        self._ysize = self._ysize + self._zoom_factor

        self._xoffset = self._xsize / self._xcells * 5
        self._yoffset = self._xoffset
        
    def get_size (self):

        return (self._xsize + self._xoffset, self._ysize + self._yoffset)
    
    def draw_grid(self, dc):

        step = self._xsize / self._xcells
        boldstep = step * 10

        # Vertical lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))
        for x in range(self._xcells+1):
            xsize = x*step
            ysize = step * self._ycells
            dc.DrawLine(self._xoffset + xsize, self._yoffset, xsize + self._xoffset, ysize + self._yoffset)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,1))
        for x in range((self._xcells)/10+1):
            xsize = x*boldstep
            ysize = step * self._ycells
            dc.DrawLine(xsize + self._xoffset, self._yoffset, xsize + self._xoffset, ysize + self._yoffset)

            
        # Horizontal lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))

        for y in range(self._ycells+1):
            ysize = y*step
            xsize = self._xcells*step
            dc.DrawLine(self._xoffset, ysize + self._yoffset, xsize + self._xoffset, ysize + self._yoffset)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,1))
        for y in range((self._ycells)/10+1):
            ysize = y*boldstep
            xsize = self._xcells*step
            dc.DrawLine(self._xoffset, ysize + self._yoffset, xsize + self._xoffset, ysize + self._yoffset)

        for x in range(self._xcells):
            for y in range(self._ycells):
                
                if self._cells[x][y]:
                    self._paint_cell (x, y, dc, self._colors[(x,y)])
            

    def add_cell (self, xcell, ycell, dc, color, erase):

        if not erase:
            if xcell >= 0 and ycell >= 0 and xcell < self._xcells and ycell < self._ycells:
                self._cells[xcell][ycell] = True
                self._colors[(xcell,ycell)] = color
                self._paint_cell (xcell, ycell, dc, color)
        else:
            if xcell >= 0 and ycell >= 0 and xcell < self._xcells and ycell < self._ycells:
                self._cells[xcell][ycell] = False
                self._colors[(xcell,ycell)] = None
                self._paint_cell (xcell, ycell, dc, color, erase)

    def get_color_by_mouse (self, x, y):
        
        step = self._xsize / self._xcells
        
        xcell = int((x - self._xoffset)/step)
        ycell = int((y - self._yoffset)/step)

        try:
            return self._colors[(xcell, ycell)]
        except KeyError:
            return None

    def mouse2cell (self, mousex, mousey):

        step = self._xsize / self._xcells
        
        xcell = int((mousex - self._xoffset)/step)
        ycell = int((mousey - self._yoffset)/step)
        
        return (xcell, ycell)

    def cell2mouse (self, xcell, ycell):

        step = self._xsize / self._xcells

        mousex = int(xcell*step + self._xoffset)
        mousey = int(ycell*step + self._yoffset)

        return (mousex, mousey)
        
        
    def _paint_cell (self, xcell, ycell, dc, color, erase = False):

        step = self._xsize / self._xcells

        px = xcell * step + self._xoffset
        py = ycell * step + self._yoffset

        if not erase:
            dc.SetPen (wx.Pen(color))
            dc.SetBrush (wx.Brush (color))
        else:
            dc.SetPen (wx.WHITE_PEN)
            dc.SetBrush (wx.WHITE_BRUSH)

        dc.DrawRectangle(px + 1,py + 1,step - 1,step - 1)
