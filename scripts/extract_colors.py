#!/usr/bin/env python2

import sys
from BeautifulSoup import BeautifulSoup as bs

if __name__ == '__main__':

    fn = sys.argv[1]
    f = open(fn,'r')
    ls = f.readlines()
    f.close()

    html = bs(''.join(ls))
    
    dmcs = {}

    for x in html.findAll('td',{'nowrap':'noWrap'}):

        try:
            name = x.next.next.replace('\n','')
        except:
            name = x.p.next.next.replace('\n','')
            
        name = ' '.join(name.split())
            
        y = x.findPreviousSibling('td')

        try:
            dmc = y.next.next.replace('\n','')
        except:
            dmc = y.p.next.next.replace('\n','')

        dmc = ' '.join(dmc.split())
            
        z = x.findNextSibling('td')
        color = z['bgcolor']
        
        print '%s,%s,%s' % (dmc, name, color)
                
