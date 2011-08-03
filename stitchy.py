#!/usr/bin/env python2

from pystitchy.main import MyApp

def run():
    app = MyApp('stitchy_gui.xrc')
    app.MainLoop()

if '__main__' == __name__:

    run()
