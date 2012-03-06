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

class ImageImporter:

    def __init__ (self):

        self._image = None

        wx.InitAllImageHandlers ()

    def load_image (self, path):

        self._image = wx.Image (path)

    def scale_image (self):

        height = self._image.GetHeight ()
        width = self._image.GetWidth ()

        ratio = width / height

        if width > height:
            self._image.Rescale (120,80/ratio)
        else:
            self._image.Rescale (ratio*80,80)

    def get_size (self):

        height = self._image.GetHeight ()
        width = self._image.GetWidth ()

        return (height, width)

    def get_color (self, x, y):
        green = self._image.GetGreen (x,y)
        red = self._image.GetRed (x,y)
        blue = self._image.GetBlue (x,y)

        return wx.Colour (red, green, blue)
