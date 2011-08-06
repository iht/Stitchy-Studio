import wx
from wx import xrc
from numpy import zeros
import numpy

class MyApp(wx.App):

    def __init__ (self, xrcfn):

        self._xrcfn = xrcfn

        self._grid = Grid()
        
        wx.App.__init__ (self)

    def OnInit (self):
        self._res = xrc.XmlResource (self._xrcfn)
        self._init_frame()

        return True

    def OnPaint (self, event):

        dc = wx.PaintDC (event.GetEventObject())
        dc.Clear()
        self._panel.DoPrepareDC(dc)
        self._grid.draw_grid (dc)

        event.Skip()

    def _init_frame (self):
        self._frame = self._res.LoadFrame (None,'MyMainFrame')
        self._panel = xrc.XRCCTRL (self._frame, 'MainPanel')
        self._panel.SetScrollbars(20,20,0,0)
        self._panel.SetVirtualSize ((1200,800))

        self._toolbar = self._frame.GetToolBar()
        self._menubar = self._frame.GetMenuBar()
        self._statusbar = self._frame.GetStatusBar()
        
        self._panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self._panel.Bind(wx.EVT_MOUSE_EVENTS, self._print_cell)
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom_out, id = xrc.XRCID('zoomout'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom_in, id = xrc.XRCID('zoomin'))

        self._frame.SetSize ((800,600))
        self._panel.FitInside()
        self._frame.SetTitle ("Stitchy Studio")
        
        self.SetTopWindow (self._frame)
        self._frame.Show()
        
    def _print_cell (self, event):

        mousex, mousey = self._panel.CalcUnscrolledPosition(event.GetX(), event.GetY())
               
        if event.ButtonDown(wx.MOUSE_BTN_LEFT) or event.Dragging():

            dc = wx.ClientDC (event.GetEventObject())
            self._panel.DoPrepareDC (dc)

            self._grid.add_cell (mousex, mousey, dc)
                
        event.Skip()

    def _set_zoom_out (self, event):

        zoom = self._grid.decrease_zoom()
        size = self._grid.get_size()
        self._panel.SetVirtualSize(size)
        self._panel.SetScrollRate(zoom/10, zoom/10)
        self._panel.Refresh()
        event.Skip()

    def _set_zoom_in (self, event):

        zoom = self._grid.increase_zoom()
        size = self._grid.get_size()
        self._panel.SetVirtualSize(size)
        self._panel.SetScrollRate(zoom/10, zoom/10)
        self._panel.Refresh()
        event.Skip()
            
class Grid:

    def __init__ (self):

        self._xcells = 120
        self._ycells = 80

        self._xsize = 1200
        self._ysize = 800
        
        self._zoom_factor = 100        

        self._cells = zeros ((self._xcells, self._ycells), dtype=numpy.bool)

    def decrease_zoom (self):

        self._zoom_factor = self._zoom_factor - 50
        self._xsize = self._xsize - 50
        self._ysize = self._ysize - 50

        return self._zoom_factor

    def increase_zoom (self):

        self._zoom_factor = self._zoom_factor + 50
        self._xsize = self._xsize + 50
        self._ysize = self._ysize + 50

        return self._zoom_factor

    def get_size (self):

        return (self._xsize, self._ysize)
    
    def draw_grid(self, dc):

        step = self._xsize / self._xcells * self._zoom_factor / 100
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
                    self._paint_cell (x, y, dc)
            
    def add_cell (self, x, y, dc):

        step = self._xsize / self._xcells * self._zoom_factor / 100
        
        xcell = int(x/step)
        ycell = int(y/step)

        self._cells[xcell][ycell] = True        
        self._paint_cell (xcell, ycell, dc)

    def _paint_cell (self, xcell, ycell, dc):

        step = self._xsize / self._xcells * self._zoom_factor / 100

        px = xcell * step
        py = ycell * step
        
        dc.SetPen (wx.RED_PEN)
        dc.SetBrush (wx.RED_BRUSH)

        dc.DrawRectangle(px+1,py+1,step - 2,step - 2)
