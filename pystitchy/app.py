# Copyright (c) 2012 Israel Herraiz <isra@herraiz.org>

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
from image_importer import ImageImporter
from math import sqrt

class MyApp(wx.App):

    def __init__ (self, xrcfn, colorsfn):

        self._xrcfn = xrcfn
        self._colorsfn = colorsfn
        self._scroll_rate = 10
        self._erase_tool = False
        self._grid = Grid()

        self._operations = []
        self._current_operation = None
        self._max_undo = 100

        self._timer = None
        self._current_mouse_pos = (-1, -1)
        
        wx.App.__init__ (self)

    def OnInit (self):

        # Colors must be imported before creating the frame
        self._import_colors ()
        self._current_color = None
        
        # Create main frame
        self._res = xrc.XmlResource (self._xrcfn)
        self._init_frame()
        # Load palette selector dialog
        self._palette_dialog = self._res.LoadDialog(self._frame, "SelectColorPaletteDialog")

        self._avlb_id = 1234
        self._available_listbox = wx.SimpleHtmlListBox(
                                  self._palette_dialog,
                                  self._avlb_id,
                                  style=wx.HLB_MULTIPLE,
                                  size=(230,460)) 

        self._selb_id = 1235
        self._select_listbox = wx.SimpleHtmlListBox(
                                  self._palette_dialog,
                                  self._selb_id,
                                  style=wx.HLB_MULTIPLE,
                                  size=(230,460))
        
        for dmc in self._colors.keys():
            code, name = self._colors[dmc]
            self._available_listbox.Append('<table><tr><td bgcolor="%s" colspan="15" nowrap> </td><td>%s #%s</td></tr></table>' % (code[0:7], name, dmc))
            

        self._res.AttachUnknownControl(
                             'AvailableColorListUnknown',
                             self._available_listbox,
                             self._palette_dialog)
        
        self._res.AttachUnknownControl(
                             'SelectedColorListUnknown',
                             self._select_listbox,
                             self._palette_dialog)

        
        self._palette_dialog.Bind(wx.EVT_BUTTON, self._add_colors_to_palette, id = xrc.XRCID ('AddColorBtn'))
        self._palette_dialog.Bind(wx.EVT_BUTTON, self._remove_colors_from_palette, id = xrc.XRCID ('RemoveColorBtn'))
        self._palette_dialog.Bind(wx.EVT_BUTTON, self._set_current_palette, id = xrc.XRCID ('PaletteAcceptBtn'))
            
        return True

    def _set_current_palette (self, event):

        dmcs = [x.split("#")[2].split("<")[0] for x in self._select_listbox.GetStrings()]
        self._current_palette = {}
        for d in dmcs:
            self._current_palette[d] = self._colors[d]

        event.Skip()

        self._palette_dialog.Show(False)
        
    def _add_colors_to_palette (self, event):

        remove = []
        item, cookie = self._available_listbox.GetFirstSelected()

        while wx.NOT_FOUND != item:
            s = self._available_listbox.GetString(item)
            self._select_listbox.Append(s)
            remove.append(item)
            item, cookie = self._available_listbox.GetNextSelected(cookie)


        for r in remove:
            self._available_listbox.Delete(r)

        self._available_listbox.DeselectAll()
        self._select_listbox.DeselectAll()

        event.Skip()
            
    def _remove_colors_from_palette (self, event):

        remove = []
        item, cookie = self._select_listbox.GetFirstSelected()
        
        while wx.NOT_FOUND != item:
            s = self._select_listbox.GetString(item)
            self._available_listbox.Append(s)
            remove.append(item)
            item, cookie = self._select_listbox.GetNextSelected(cookie)

        for r in remove:
            self._select_listbox.Delete(r)        

        self._select_listbox.DeselectAll()
        self._available_listbox.DeselectAll()

        event.Skip()
        
    def _import_colors (self):

        f = open(self._colorsfn, 'r')
        ls = f.readlines()
        f.close()

        self._colors = {}
        for l in ls:
            dmc, name, code = l.split(',')
            self._colors[dmc] = (code, name)            

        self._current_palette = self._colors
        
    def _find_dmc_color (self, color):
        for dmc in self._colors.keys():
            code, name = self._colors[dmc]

            red = int(code[1:3], 16)
            green = int(code[3:5], 16)
            blue = int(code[5:7], 16)

            if red == color.Red() and green == color.Green() and blue == color.Blue():
                return '%s #%s' % (name, dmc)

        return 'None'

    def _find_closest_dmc_color (self, color):

        distance = 1000
        
        red = color.Red()
        green = color.Green()
        blue = color.Blue()

        bestred, bestgreen, bestblue = (None, None, None)
        
        for dmc in self._current_palette.keys():
            code, name = self._current_palette[dmc]

            dred = int(code[1:3], 16)
            dgreen = int(code[3:5], 16)
            dblue = int(code[5:7], 16)

            r = (dred + red) / 2
            dr = dred - red
            dg = dgreen - green
            db = dblue - blue

            ndistance = (2+r/256)*dr**2 + 4*dg**2 + (2+(255-r)/256)*db**2
            ndistance = sqrt(ndistance)
            
            if ndistance < distance:
                distance = ndistance
                bestred, bestgreen, bestblue = (dred, dgreen, dblue)

        return wx.Colour (bestred, bestgreen, bestblue)
            
            
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
        self._toolbar.Bind(wx.EVT_TOOL, self._undo,     id = xrc.XRCID('undo'))
        self._toolbar.Bind(wx.EVT_TOOL, self._redo,     id = xrc.XRCID('redo'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom, id = xrc.XRCID('zoomout'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_zoom, id = xrc.XRCID('zoomin'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_edit, id = xrc.XRCID('editgrid'))
        self._toolbar.Bind(wx.EVT_TOOL, self._set_edit, id = xrc.XRCID('erase'))
        self._toolbar.Bind,wx.EVT_CHOICE(self, color_choice_id, self._change_color)

        self._frame.Bind(wx.EVT_MENU, self._import_image, id = xrc.XRCID('importimage'))

        self._timer = wx.Timer()
        self._timer.Bind(wx.EVT_TIMER, self._show_tooltip)
        
        
        self._frame.SetSize ((800,600))
        self._panel.FitInside()
        self._frame.SetTitle ("Stitchy Studio")

        self._timer.Start(3000,True)
        
        self.SetTopWindow (self._frame)
        self._frame.Show()


    def _import_image (self, event):

        path = wx.FileSelector ('Choose an image',
                               wildcard = "BMP|*.bmp|GIF|*.gif|JPEG|*.jp*g|PNG|*.png|PCX|*.pcx|TIFF|*.tiff|Other|*",
                               flags = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                               parent = self._frame)
                            
        if path:
            self._palette_dialog.Fit()
            self._palette_dialog.ShowModal()
            importer = ImageImporter ()
            importer.load_image (path)
            importer.scale_image()
            
            height, width = importer.get_size ()

            dc = wx.ClientDC (self._panel)

            self._panel.DoPrepareDC (dc)

            for x in range (0, width):
                for y in range (0, height):
                    color = importer.get_color (x, y)
                    bestcolor = self._find_closest_dmc_color (color)
                    self._grid.add_cell (x, y, dc, bestcolor, False)
            
        event.Skip()

    def _change_color (self, event):

        selection = self._color_choice.GetStringSelection()

        dmc = selection.split("(")[1].split(")")[0]

        color, _name = self._colors[dmc]

        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)

        self._current_color = wx.Colour (red=red, green=green, blue=blue)

        if event:
            event.Skip()
        
    def _print_cell (self, event):

        mousex, mousey = self._panel.CalcUnscrolledPosition(event.GetX(), event.GetY())

        self._current_mouse_pos = (mousex, mousey)
        color = self._grid.get_color_by_mouse (mousex, mousey)
        if not color:
            color_name = 'None'
        else:
            color_name = self._find_dmc_color (color)
            
        self._statusbar.SetStatusText('Color: %s' % str(color_name))
        
        if event.GetButton() == wx.MOUSE_BTN_LEFT or event.Dragging():

            dc = wx.ClientDC (event.GetEventObject())
            self._panel.DoPrepareDC (dc)
                
            xcell, ycell = self._grid.mouse2cell (mousex, mousey)
            color_index = self._grid.add_cell (xcell, ycell, dc, self._current_color, self._erase_tool)
            # Add operation for undo and redo
            op = (xcell, ycell, color_index, self._erase_tool)
            if (len(self._operations) == 0) or (not op in self._operations):
                self._operations.append (op)
                self._current_operation = len(self._operations) - 1

        elif event.Moving():
            self._timer.Start(3000,True)
                
        event.Skip()

    def _undo (self, event):

        if self._current_operation:
            op = self._operations[self._current_operation]
            
            xcell, ycell,  color_index, erase = op

            dc = wx.ClientDC (self._panel)
            self._panel.DoPrepareDC (dc)

            if erase:
                if color_index > 0:
                    cur_color = self._grid.get_color_by_index (xcell, ycell, color_index-1) 
                    self._grid.add_cell (xcell, ycell, dc, cur_color, False)                    
            else:
                if color_index > 0:
                    cur_color = self._grid.get_color_by_index (xcell, ycell, color_index-1)
                    self._grid.add_cell (xcell, ycell, dc, cur_color, False)                    
                else:
                    self._grid.add_cell (xcell, ycell, dc, None, True)                    
            
            self._current_operation = self._current_operation - 1
            if self._current_operation < 0:
                self._current_operation = None

    def _redo (self, event):
        if not self._current_operation:
            self._current_operation = 0

        try:
            op = self._operations[self._current_operation+1]
            xcell, ycell, color_index, erase = op

            cur_color = self._grid.get_color_by_index (xcell, ycell, color_index)
            
            dc = wx.ClientDC (self._panel)
            self._panel.DoPrepareDC (dc)
            if erase:
                self._grid.add_cell (xcell, ycell, dc, None, True)
            else:
                self._grid.add_cell (xcell, ycell, dc, cur_color, False)

            self._current_operation += 1
            
        except IndexError:
            # No actions to redo
            pass

        
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


    def _show_tooltip (self, event):

        x, y = self._current_mouse_pos
        
        color = self._grid.get_color_by_mouse (x, y)

        if color:
            
            red = color.Red()
            green = color.Green()
            blue = color.Blue()
        
            color = self._find_dmc_color (color)            
            tip = wx.TipWindow (self._frame, "Color: %s\n\nRGB: (%s, %s, %s)\n\nClick tooltip to close" % (str(color),red,green,blue))

        
        event.Skip()
