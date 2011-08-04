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

        self._toolbar = xrc.XRCCTRL (self._frame, 'MyToolBar')
        self._menubar = xrc.XRCCTRL (self._frame, 'MyMenuBar')
        self._statusbar = xrc.XRCCTRL (self._frame, 'MyStatusBar')
        
        self._panel.Bind(wx.EVT_PAINT,self.OnPaint)
        self._panel.Bind(wx.EVT_MOUSE_EVENTS, self._print_cell)


        
        self._frame.SetSize ((800,600))
        self._panel.FitInside()
        self._frame.SetTitle ("Stitchy Studio")
        
        self.SetTopWindow (self._frame)
        self._frame.Show()

        #self._frame.SetScrollbar(wx.VERTICAL,0,20,1024)
        
    def _print_cell (self, event):

        mousex = event.GetX()
        mousey = event.GetY()
        
        if event.ButtonDown(wx.MOUSE_BTN_LEFT) or event.Dragging():

            dc = wx.ClientDC (event.GetEventObject())

            self._grid.add_cell (mousex, mousey, dc)
                
        event.Skip()

            
class Grid:

    def __init__ (self):

        self._xcells = 120
        self._ycells = 80

        self._xsize = 1200
        self._ysize = 800
        
        self._zoom_factor = 1

        self._cells = zeros ((self._xcells, self._ycells), dtype=numpy.bool)
        
    def draw_grid(self, dc):

        step = self._xsize / self._xcells * self._zoom_factor
        boldstep = step * 10

        # Vertical lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))
        for x in range(0,self._xsize + step, step):
            dc.DrawLine(x, 0, x, self._ysize)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,3))
        for x in range(0, self._xsize + boldstep, boldstep):
            dc.DrawLine(x, 0, x, self._ysize)

            
        # Horizontal lines
        dc.SetPen (wx.Pen(wx.LIGHT_GREY, 1))
        for y in range(0, self._ysize + step, step):
            dc.DrawLine(0, y, self._xsize, y)

        # Draw bold lines
        dc.SetPen (wx.Pen(wx.BLACK,3))
        for y in range(0, self._ysize + boldstep, boldstep):
            dc.DrawLine(0, y, self._xsize, y)

        for x in range(self._xcells):
            for y in range(self._ycells):
                
                if self._cells[x][y]:
                    self._paint_cell (x, y, dc)
            
    def add_cell (self, x, y, dc):

        xcell = int(x/10)
        ycell = int(y/10)

        self._cells[xcell][ycell] = True        
        self._paint_cell (xcell, ycell, dc)

    def _paint_cell (self, xcell, ycell, dc):

        px = xcell*10
        py = ycell*10
        
        dc.SetPen (wx.RED_PEN)
        dc.SetBrush (wx.RED_BRUSH)

        dc.DrawRectangle(px+1,py+1,8,8)
