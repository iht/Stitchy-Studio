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
from wx import xrc
from grid import Grid

class MyApp(wx.App):

    def __init__ (self, xrcfn, colorsfn):

        self._xrcfn = xrcfn
        self._colorsfn = colorsfn
        self._scroll_rate = 10
        self._erase_tool = False
        self._grid = Grid()
        
        wx.App.__init__ (self)

    def OnInit (self):

        # Colors must be imported before creating the frame
        self._import_colors ()
        self.current_color = None
        
        # Create main frame
        self._res = xrc.XmlResource (self._xrcfn)
        self._init_frame()
        
        return True

    def _import_colors (self):

        f = open(self._colorsfn, 'r')
        ls = f.readlines()
        f.close()

        self._colors = {}
        for l in ls:
            dmc, name, code = l.split(',')
            self._colors[dmc] = (code, name)
    
    def OnPaint (self, event):

        dc = wx.PaintDC (event.GetEventObject())
        dc.Clear()
        self._panel.DoPrepareDC(dc)
        self._grid.draw_grid (dc)

        event.Skip()

    def _init_frame (self):
        self._frame = self._res.LoadFrame (None,'MyMainFrame')
        self._panel = xrc.XRCCTRL (self._frame, 'MainPanel')
        self._panel.SetScrollRate (self._scroll_rate, self._scroll_rate)
        self._panel.SetVirtualSize (self._grid.get_size ())

        self._toolbar = self._frame.GetToolBar () 
        self._toolbar.ToggleTool (xrc.XRCID('editgrid'), not self._erase_tool)
        self._toolbar.ToggleTool (xrc.XRCID('erase'), self._erase_tool)
        
        color_choice_id = 54 # Random int
        color_list = []
        for k in self._colors.keys():
            dmc = k
            code, name = self._colors[k]
            
            color_list.append('%s (%s)' % (name, dmc))

        self._color_choice = wx.Choice (self._toolbar, color_choice_id, (-1,-1), (-1,-1), color_list )
        self._toolbar.AddControl (self._color_choice)
        self._change_color(None)
        
        self._menubar = self._frame.GetMenuBar()
        self._statusbar = self._frame.GetStatusBar()
        
        self._panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self._panel.Bind(wx.EVT_MOUSE_EVENTS, self._print_cell)
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom, id = xrc.XRCID('zoomout'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom, id = xrc.XRCID('zoomin'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_edit, id = xrc.XRCID('editgrid'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_edit, id = xrc.XRCID('erase'))
        self._toolbar.Bind,wx.EVT_CHOICE(self, color_choice_id, self._change_color)
        
        self._frame.SetSize ((800,600))
        self._panel.FitInside()
        self._frame.SetTitle ("Stitchy Studio")
        
        self.SetTopWindow (self._frame)
        self._frame.Show()


    def _change_color (self, event):

        selection = self._color_choice.GetStringSelection()

        dmc = selection.split("(")[1].split(")")[0]

        color, _name = self._colors[dmc]

        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)

        self.current_color = wx.Colour (red=red, green=green, blue=blue)

        if event:
            event.Skip()
        
    def _print_cell (self, event):

        mousex, mousey = self._panel.CalcUnscrolledPosition(event.GetX(), event.GetY())
               
        if event.ButtonDown(wx.MOUSE_BTN_LEFT) or event.Dragging():

            dc = wx.ClientDC (event.GetEventObject())
            self._panel.DoPrepareDC (dc)

            self._grid.add_cell (mousex, mousey, dc, self.current_color, self._erase_tool)
            
        event.Skip()

    def _set_zoom (self, event):

        if event.GetId() == xrc.XRCID('zoomout'):
            self._grid.decrease_zoom()
        elif event.GetId() == xrc.XRCID('zoomin'):
            self._grid.increase_zoom()

        size = self._grid.get_size()
        self._panel.SetVirtualSize(size)
        self._panel.FitInside()
        
        self._panel.SetScrollRate(size[0]/10, size[1]/10)
        self._panel.Refresh()
        event.Skip()

    def _set_edit (self, event):

        if event.GetId() == xrc.XRCID('editgrid'):
            self._erase_tool = False
        elif event.GetId() == xrc.XRCID('erase'):
            self._erase_tool = True

        self._toolbar.ToggleTool (xrc.XRCID('editgrid'), not self._erase_tool)
        self._toolbar.ToggleTool (xrc.XRCID('erase'), self._erase_tool)
            
        event.Skip()
