#
#    Resume Graph
#    Copyright (C) 2016 Brandon C Tardio
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
#    Contact: BTardio@gmail.com
#             818 424 6838
#

from defines import defines_for_cell
from random import randint
from math import fabs
from operator import xor
from xcb.xproto import ImplementationError



class defines_for_geometrymanager():
    
    pass

def distance_between_centered_segment(a, b, c, d):

    #  |------a      b----c    d------|
    #            \/         \/
    #            e          f
    # finds e, f where e = f
    
    btwnad = d - a
    halfbtwnad = btwnad / 2.0
    
    btwnbc = c - b
    halfbtwnbc = btwnbc / 2.0
    
    left = halfbtwnad - halfbtwnbc
        
    #right = halfbtwnad + halfbtwnbc
    
    dleft = fabs(btwnad - btwnbc - left)
    
    return dleft   

def center_equal_space_multiple(a,b,c,d,numsegments):
    
    #  |------a      b----c      b----c    d------|
    #            \/         \/          \/
    #            e          f           g
    # finds e, f, g where e = f = g
    
    # find
    # |----ab----cb----c...b----c      d------|
    #                              \/
    #                              h
    btwnad = d - a
    btwnbc = c - b
    
    allbc = btwnbc * numsegments
    
    if btwnad - allbc < 0: raise ValueError('Number of segments exceeds segment area.')

    h = btwnad - allbc
    
    inbetween = float(h) / (float(numsegments) + 1.0)
    
    return inbetween


class area():
    
    # window dimensions
    height = None
    width = None
    
    items = []
        
    # when an item is added this determines if it will be added to itemswide or itemshigh
    growx = False
    growy = False
    
    fill = False
    
    # distribute distance between items
    distributex = False
    distributey = False
    
    # alignment of items # possible values of left, center, right | top, center, bottom 
    alignx = None
    aligny = None
        
    padvertical = 0.0
    padhorizontal = 0.0
    
    parent = None
        
    # init method
    def __init__(self, *vargs, **kwargs):
        self.items = []
        
        
        
        for arg in kwargs:
            if hasattr(self, arg): setattr(self, arg, kwargs[arg])
            
        if self.height != self.width:
            raise ValueError('Expecting height width equality but h:%s w:%s' % (str(self.height), str(self.width)))
        return
    
    # string method
    def __str__(self):
        var = ''
        for arg in vars(self):
            var += str(arg) + ': ' + str(getattr(self, arg)) + '\n'
            
        var += str(self.items)
        return var
    
    def svgmargin(self):
        
        
        lst = []

        # margin left        
        r = {}
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = self.fleft() + 5 
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = self.itop() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = self.padhorizontal - 10
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = self.iheight() - 10        
        lst.append(r)
        
        # margin right
        r = {}
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = self.iright() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = self.itop() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = self.padhorizontal - 10
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = self.iheight() - 10
        lst.append(r)

        # margin top        
        r = {}
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = self.ileft() + 5 
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = self.ftop() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = self.iwidth() - 10
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = self.padvertical - 10
        lst.append(r)
         
        # margin bottom
        r = {}
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = self.ileft() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = self.ibottom() + 5
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = self.iwidth() - 10
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = self.padvertical - 10
        lst.append(r)

        
        s = ''
        for r in lst:
            s += '<'
            s += 'rect'
            for item in r:
                s += ' '
                s += item
                s += '='
                s += '"'
                s += str(r[item])
                s += '"'
            s += ' '
            s += 'style="fill:rgb(%d,%d,%d);stroke:rgb(%d,%d,%d);"'%(20,40,60,
                                                                     255,255,255)
            s += '>'
            s += '</'
            s += 'rect'
            s += '>'
        
        return s
        
    
    def svg(self):

        r = {}

        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = self.ileft()
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = self.itop()
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = self.iwidth()
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = self.iheight()
        
        s = '<'
        s += 'rect'
        for item in r:
            s += ' '
            s += item
            s += '='
            s += '"'
            s += str(r[item])
            s += '"'
        s += ' '
        s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(100,255), randint(100,255), randint(100,255))
        s += '>'
        s += '</'
        s += 'rect'
        s += '>'
        
        return s
    
    # push a new item into items list after setting the new items parent to self
    def push(self, var):
        if isinstance(var, area):
            var.parent = self
            self.items.append(var)
            
        else: raise TypeError('Expected an instance of class area, received %s.' % type(var))
        return
    
    # vertical margins
    def vps(self):
        return self.padvertical * 2.0
    
    # horizontal margins
    def hps(self):
        return self.padhorizontal * 2.0
        
    # find full square dimensions
    def fsd(self, horw=None):
        rvar = None
        
        
        if horw == None or self.parent == None or self.parent.fill == False:
            if self.parent == None:
                rvar = min(self.height, self.width)
            elif len(self.parent.items) == 1:
                rvar = min(self.parent.iheight(), self.parent.iwidth())
            else:
                rvar = min(self.parent.iheight() / len(self.parent.items), 
                           self.parent.iwidth() / len(self.parent.items))

        elif self.parent != None and (horw == 'w' or horw == 'width') and self.parent.fill == True:
            if self.parent == None:
                rvar = self.width
            elif len(self.parent.items) == 1:
                rvar = self.parent.iwidth()
            else:
                if self.parent.growx: rvar = self.parent.iwidth() / len(self.parent.items)
                else: rvar = self.parent.iwidth()
            
        elif self.parent != None and (horw == 'h' or horw == 'height') and self.parent.fill == True:
            if self.parent == None:
                rvar = self.height
            elif len(self.parent.items) == 1:
                rvar = self.parent.iheight()
            else:
                if self.parent.growy: rvar = self.parent.iheight() / len(self.parent.items)
                else: rvar = self.parent.iheight()
                
        return rvar
        
        
        
    # find inner square dimensions
    def isd(self, horw=None):
        rvar = None
            
        if horw == None or self.parent == None or self.parent.fill == False:
            rvar = self.fsd(horw) - max(self.vps(), self.hps())
            
        elif self.parent != None and (horw == 'w' or horw == 'width') and self.parent.fill == True:
            rvar = self.fsd(horw) - self.hps()
            
        elif self.parent != None and (horw == 'h' or horw == 'height') and self.parent.fill == True:
            rvar = self.fsd(horw) - self.vps()

    
        return rvar
        
    # retrieve the full top value
    def ftop(self):
        rvar = None
        
        if self.parent == None:
            rvar = 0.0
        
        elif len(self.parent.items) == 1 or self.parent.growx == True:
            if self.parent.aligny == 'top':
                rvar = self.parent.itop()
            elif self.parent.aligny == 'center':
                d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd('h'), self.parent.ibottom())
                rvar = self.parent.itop() + d
            elif self.parent.aligny == 'bottom':
                rvar = self.parent.ibottom() - self.fsd('h')
            else:
                raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)            

        else:

            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.ftopm()


        return rvar
    
    # growy
    def ftopm(self):
        
        rvar = None
            
        if self.parent.aligny == 'top':
            ix = self.parent.items.index(self) 
            rvar = self.parent.itop() + (self.fsd('h') * ix)
        elif self.parent.aligny == 'center':
            ix = self.parent.items.index(self) 
            d = distance_between_centered_segment(self.parent.itop(), 
                                                  0, (self.fsd('h') * len(self.parent.items)), 
                                                  self.parent.ibottom())
            #d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd(), self.parent.ibottom())
            rvar = self.parent.itop() + (self.fsd('h') * ix) + d
        elif self.parent.aligny == 'bottom':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.ibottom() - (self.fsd('h') * ix)
            
            #pass
            #rvar = self.parent.ibottom() - self.fsd()
        else:
            raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)            

        return rvar
    
    # retrieve the inner top value
    # rules: should never need to subtract self.padtop
    # rules: should never need to introduce self.padbottom
    def itop(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.padvertical
            
        elif len(self.parent.items) == 1 or self.parent.growx == True:
            if self.parent.aligny == 'top':
                rvar = self.parent.itop() + self.padvertical
            elif self.parent.aligny == 'center':
                d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd('h'), self.parent.ibottom())
                rvar = self.parent.itop() + self.padvertical + d
                
            elif self.parent.aligny == 'bottom':
                
                rvar = self.parent.ibottom() - (self.fsd('h') - self.padvertical)
            else:
                raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)
        
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.itopm()
        
        return rvar

    # growy
    def itopm(self):
        
        rvar = None
        
        if self.parent.aligny == 'top':
            ix = self.parent.items.index(self)
            rvar = self.parent.itop() + (self.fsd('h') * ix) + self.padvertical

        elif self.parent.aligny == 'center':
            ix = self.parent.items.index(self)
            d = distance_between_centered_segment(self.parent.itop(), 
                                                  0, (self.fsd('h') * len(self.parent.items)), 
                                                  self.parent.ibottom())
            #d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd(), self.parent.ibottom())
            rvar = self.parent.itop() + (self.fsd('h') * ix) + self.padvertical + d
            
        elif self.parent.aligny == 'bottom':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.ibottom() - (self.fsd('h') * ix) + self.padvertical
            
            #pass
            #rvar = self.parent.ibottom() - (self.fsd() - self.padvertical)
        else:
            raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)
        
        return rvar
    
    def fbottom(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.height
        
        elif len(self.parent.items) == 1 or self.parent.growx == True:
            if self.parent.aligny == 'top':
                rvar = self.parent.itop() + self.fsd('h')
            elif self.parent.aligny == 'center':
                d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd('h'), self.parent.ibottom())
                rvar = self.parent.itop() + self.fsd('h') + d
            elif self.parent.aligny == 'bottom':
                rvar = self.parent.ibottom()
            else:
                raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)            
        else:
            
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.fbottomm()
        
        return rvar
    
    # growy
    def fbottomm(self):
        
        rvar = None
        
        if self.parent.aligny == 'top':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.itop() + (self.fsd('h') * ix)

        elif self.parent.aligny == 'center':
            ix = self.parent.items.index(self) + 1
            d = distance_between_centered_segment(self.parent.itop(), 
                                                  0, (self.fsd('h') * len(self.parent.items)), 
                                                  self.parent.ibottom())
            
            #d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd(), self.parent.ibottom())
            rvar = self.parent.itop() + (self.fsd('h') * ix) + d
        elif self.parent.aligny == 'bottom':
            ix = self.parent.items.index(self)
            rvar = self.parent.ibottom() - (self.fsd('h') * ix)
            
            #pass
            #rvar = self.parent.ibottom()
        else:
            raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)                    
        
        return rvar        

    
    def ibottom(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.height - self.padvertical

        elif len(self.parent.items) == 1 or self.parent.growx == True:
            if self.parent.aligny == 'top':
                rvar = self.parent.itop() + self.isd('h') + self.padvertical
            elif self.parent.aligny == 'center':
                d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd('h'), self.parent.ibottom())
                rvar = self.parent.itop() + self.fsd('h') + d  - self.padvertical
            elif self.parent.aligny == 'bottom':
                rvar = self.parent.ibottom() - self.padvertical
            else:
                raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)            
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')
                
            rvar = self.ibottomm()
            
        return rvar
    
    # growy
    def ibottomm(self):
        rvar = None
        
        if self.parent.aligny == 'top':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.itop() + (self.fsd('h') * ix) - self.padvertical
            
        elif self.parent.aligny == 'center':
            ix = self.parent.items.index(self) + 1
            d = distance_between_centered_segment(self.parent.itop(), 
                                                  0, (self.fsd('h') * len(self.parent.items)), 
                                                  self.parent.ibottom())
            
            #d = distance_between_centered_segment(self.parent.itop(), 0, self.fsd(), self.parent.ibottom())
            rvar = self.parent.itop() + (self.fsd('h') * ix) + d  - self.padvertical
        elif self.parent.aligny == 'bottom':
            ix = self.parent.items.index(self)
            rvar = self.parent.ibottom() - (self.fsd('h') * ix) - self.padvertical

            #pass
            #rvar = self.parent.ibottom() - self.padvertical
        else:
            raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)            
        
        return rvar        
    
    # retrieve the full height
    def fheight(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.height

        else: 
            rvar = self.fsd('h')
                    
        return rvar
    
    # retrieve the inner height
    def iheight(self):
        rvar = None

        if self.parent == None:
            rvar = self.height - self.vps()
            
        else:
            # rvar = self.fsd()
            #rvar = self.fsd() - self.vps()
            rvar = self.isd('h')
    
        return rvar
    








    # retrieve the full left value
    def fleft(self):
        rvar = None
        
        if self.parent == None:
            rvar = 0.0
        
        elif len(self.parent.items) == 1  or self.parent.growy == True:
            if self.parent.alignx == 'left':
                rvar = self.parent.ileft()
            elif self.parent.alignx == 'center':
                d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
                rvar = self.parent.ileft() + d

            elif self.parent.alignx == 'right':
                rvar = self.parent.iright() - self.fsd('w')
            else:
                raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
            
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')
            
            rvar = self.fleftm()

        return rvar
    
    # growx
    def fleftm(self):
        rvar = None

        if self.parent.alignx == 'left':
            ix = self.parent.items.index(self)
            rvar = self.parent.ileft() + (self.fsd('w') * ix)

        elif self.parent.alignx == 'center':
            ix = self.parent.items.index(self)
            d = distance_between_centered_segment(self.parent.ileft(), 
                                                  0, (self.fsd('w') * len(self.parent.items)), 
                                                  self.parent.iright())
            #d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
            rvar = self.parent.ileft() + (self.fsd('w') * ix) + d

        elif self.parent.alignx == 'right':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.iright() - (self.fsd('w') * ix)            
            
            #pass
            #rvar = self.parent.iright() - self.fsd('w')
        else:
            raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
            
        return rvar                
    
    # retrieve the inner left value
    # rules: should never need to subtract self.padleft
    # rules: should never need to introduce self.padright
    def ileft(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.padhorizontal
            
        elif len(self.parent.items) == 1  or self.parent.growy == True:
            if self.parent.alignx == 'left':
                rvar = self.parent.ileft() + self.padhorizontal
            elif self.parent.alignx == 'center':
                d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
                rvar = self.parent.ileft() + d + self.padhorizontal

            elif self.parent.alignx == 'right':
                
                rvar = self.parent.iright() - (self.fsd('w') - self.padhorizontal)
            else:
                raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.ileftm()
        return rvar
    
    # growx
    def ileftm(self):
        rvar = None
        
        if self.parent.alignx == 'left':
            ix = self.parent.items.index(self)
            rvar = self.parent.ileft() + (self.fsd('w') * ix) + self.padhorizontal
            
        elif self.parent.alignx == 'center':
            ix = self.parent.items.index(self)
            d = distance_between_centered_segment(self.parent.ileft(), 
                                                  0, (self.fsd('w') * len(self.parent.items)), 
                                                  self.parent.iright())
            #d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
            rvar = self.parent.ileft() + (self.fsd('w') * ix) + d + self.padhorizontal

        elif self.parent.alignx == 'right':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.iright() - (self.fsd('w') * ix) + self.padhorizontal            
            
            #pass
            #rvar = self.parent.iright() - (self.fsd('w') - self.padhorizontal)
        else:
            raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
        
        return rvar                
    
    def fright(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.width
        
        elif len(self.parent.items) == 1  or self.parent.growy == True:
            if self.parent.alignx == 'left':
                rvar = self.parent.ileft() + self.fsd('w')
            elif self.parent.alignx == 'center':
                d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
                rvar = self.parent.ileft() + self.fsd('w') + d

            elif self.parent.alignx == 'right':
                rvar = self.parent.iright() 
            else:
                raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
        
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.frightm()    
        
        return rvar
    
    # growx
    def frightm(self):
        rvar = None
        
        if self.parent.alignx == 'left':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.ileft() + (self.fsd('w') * ix)
            
        elif self.parent.alignx == 'center':
            ix = self.parent.items.index(self) + 1
            d = distance_between_centered_segment(self.parent.ileft(), 
                                                  0, (self.fsd('w') * len(self.parent.items)), 
                                                  self.parent.iright())
            #d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
            rvar = self.parent.ileft() + (self.fsd('w') * ix) + d

        elif self.parent.alignx == 'right':
            ix = self.parent.items.index(self)
            rvar = self.parent.iright() - (self.fsd('w') * ix)

            #pass
            #rvar = self.parent.iright() 
        else:
            raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
        
        return rvar                
        
    
    def iright(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.width - self.padhorizontal

        elif len(self.parent.items) == 1  or self.parent.growy == True:
            if self.parent.alignx == 'left':
                rvar = self.parent.ileft() + self.fsd('w') - self.padhorizontal
            elif self.parent.alignx == 'center':
                d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
                rvar = self.parent.ileft() + self.fsd('w') + d - self.padhorizontal

            elif self.parent.alignx == 'right':
                
                rvar = self.parent.iright() - self.padhorizontal
            else:
                raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
        else:
            if self.parent.growx == self.parent.growy:
                raise ValueError('Containers with more than one element must designate growx or growy.')

            rvar = self.irightm()
        
        return rvar

    # growx
    def irightm(self):
        rvar = None

        if self.parent.alignx == 'left':
            ix = self.parent.items.index(self) + 1
            rvar = self.parent.ileft() + (self.fsd('w') * ix) - self.padhorizontal
            
        elif self.parent.alignx == 'center':
            ix = self.parent.items.index(self) + 1
            d = distance_between_centered_segment(self.parent.ileft(), 
                                                  0, (self.fsd('w') * len(self.parent.items)), 
                                                  self.parent.iright())
            #d = distance_between_centered_segment(self.parent.ileft(), 0, self.fsd('w'), self.parent.iright())
            rvar = self.parent.ileft() + (self.fsd('w') * ix) + d - self.padhorizontal

        elif self.parent.alignx == 'right':
            ix = self.parent.items.index(self)
            rvar = self.parent.iright() - (self.fsd('w') * ix) - self.padhorizontal

            #pass
            #rvar = self.parent.iright() - self.padhorizontal
        else:
            raise ValueError('Expecting left or center or right for alignx, received %s.' % self.parent.alignx)            
        
        return rvar                  
    # retrieve the full width
    def fwidth(self):
        rvar = None
        
        if self.parent == None:
            rvar = self.width

        else:
            rvar = self.fsd('w')
        
        return rvar
    
    # retrieve the inner width
    def iwidth(self):
        rvar = None

        if self.parent == None:
            rvar = self.width - self.hps()
            
        else:
            rvar = self.isd('w')
    
        return rvar



def creationloop():
    lst = []
    
    heightvar = 1000

    widthvar = 1000

    

    for fillvar in [True, False]:
        for growvar in [True, False]:
            
            for alignyvar in ['bottom','center', 'top']:
            #for alignyvar in ['bottom', 'top']:
            #if True: 
                #alignyvar = 'top'
                for alignxvar in ['left', 'right', 'center']:
                #for alignxvar in ['left', 'right']:
                #if True: 
                    #alignxvar = 'left'
                    for padhorizontalvar in [50, 100, 150]: # [randint(45, 55), randint(95, 105), randint(145, 155)]:
                    #if True:
                        #padhorizontalvar = 50
                        
                        for padverticalvar in [50, 100, 150]: # [randint(45, 55), randint(95, 105), randint(145, 155)]:
                        #if True:
                            #padverticalvar = 100
                            for nia in [1, 2, 3]:
                                g = area(height=heightvar,
                                         width=widthvar,
                                         alignx=alignxvar,
                                         aligny=alignyvar,
                                         padhorizontal=padhorizontalvar,
                                         padvertical=padverticalvar,
                                         growx=not growvar,
                                         growy=growvar,
                                         fill=fillvar)
                                 
                                print(printclassmethods(g))
                                
                                for _ in range(0, nia):
                                    ga = area(padhorizontal=50, padvertical=50) 
                                    g.push(ga)
                                    #gb = area(padhorizontal=50, padvertical=50)
                                    #g.push(gb)
                                    #gc = area(padhorizontal=50, padvertical=50)
                                    #g.push(gc)
                                
                                print(printclassmethods(ga))
                                #print(printclassmethods(gb))
                                #print(printclassmethods(gc))
                                
                                lst.append(g)
    return lst     




def printclassmethods(var):
    rvar = ''
    rvar += '\nclass methods:\n'
    for name, method in area.__dict__.iteritems():
        if callable(method):
            if (name == '__str__' or name == '__init__' or name == 'push' or name == 'svg' or 
                name == 'svgmargin' or name == 'ftopm' or name == 'itopm' or name == 'fbottomm' or
                name == 'ibottomm' or name == 'fleftm' or name == 'ileftm' or name == 'frightm' or
                name == 'irightm'):
                pass
            elif (name == 'fsd' or name == 'isd'):
                rvar += str(name) + 'height:' + str(method(var, 'h')) + '\n'
                rvar += str(name) + 'width:' + str(method(var, 'w')) + '\n'
            else: rvar += str(name) + ':' + str(method(var)) + '\n'
    return rvar

def createmultiple():
    f = open('../../geometrymanager.html', 'w')
    f.write('<html><head><title></title></head><body>\n')
    
    
    lst = creationloop()
    
    for g in lst:
    
        f.write('g.height:' + str(g.height) + ' g.width:' + str(g.width))
        f.write(' g.alignx:' + str(g.alignx) + ' g.aligny:' + str(g.aligny))
        f.write(' g.padhorizontal:' + str(g.padhorizontal) + ' g.padvertical:' + str(g.padvertical))
        f.write('\n<BR>')
        f.write('<svg width="'+str(g.width)+'" height="'+str(g.height) + '">\n')
        f.write('<rect width="'+str(g.width)+'" height="'+str(g.height)+'" style="fill:rgb(14,17,14);"></rect>\n')
              
        f.write(g.svg() + '\n')
        f.write(g.svgmargin() + '\n')
        
        for ga in g.items:
        
            f.write(ga.svg() + '\n')
            f.write(ga.svgmargin() + '\n')
            
        
        f.write('</svg><br>~<br>')
                           
    f.write('</body></html>')
      
    f.close()




import unittest

class area_test(unittest.TestCase):
    
    
    def setUp(self):
        self.lst = creationloop()

    def _constraintlesstests(self, p, v):
        errorstring = 'hp:' + str(p.padhorizontal) + 'vp:' + str(p.padvertical) 
        errorstring += str(v.alignx) + str(v.aligny) + str(p.alignx) + str(p.aligny)
        
        self.assertTrue(v.iheight() == v.isd('h'), errorstring)
        self.assertTrue(v.fheight() == v.fsd('h'), errorstring)
        self.assertTrue(v.iwidth() == v.isd('w'), errorstring)
        self.assertTrue(v.fwidth() == v.fsd('w'), errorstring)
        
        self.assertTrue(p.fright() == p.fbottom(), errorstring)
        
        self.assertAlmostEqual(v.fheight() - v.iheight(), v.padvertical * 2.0)
        self.assertAlmostEqual(v.fwidth() - v.iwidth(), v.padhorizontal * 2.0)

        self.assertAlmostEqual(p.fheight() - p.iheight(), p.padvertical * 2.0)
        self.assertAlmostEqual(p.fwidth() - p.iwidth(), p.padhorizontal * 2.0)
        
        #self.assertAlmostEqual((v.ibottom() - v.itop()) ** 2.0, (v.iright() - v.ileft()) ** 2.0)
        
    
    def test_area(self):
        
        for p in self.lst:
            
            if len(p.items) == 1:
                v = p.items[0]
                
                errorstring = 'hp:' + str(p.padhorizontal) + 'vp:' + str(p.padvertical) 
                errorstring += str(v.alignx) + str(v.aligny) + str(p.alignx) + str(p.aligny)
                
                #self.assertAlmostEqual(v.fheight(), v.fwidth())
                #self.assertAlmostEqual(p.fheight() - v.fheight(), max(p.hps(), p.vps()))
                
                self.assertTrue(p.vps() == p.padvertical * 2.0)
                self.assertTrue(p.hps() == p.padhorizontal * 2.0)
                

                self._constraintlesstests(p, v)
                    
                if p.padhorizontal == p.padvertical:
                    self.assertTrue(p.iwidth() == v.fwidth())
                    self.assertTrue(p.iwidth() - v.hps() == v.iwidth())
                    self.assertTrue(p.iwidth() - v.vps() == v.iwidth())
                    self.assertTrue(p.iheight() == v.fheight())
                    self.assertTrue(p.iheight() - v.vps() == v.iwidth())
                    self.assertTrue(p.iheight() - v.hps() == v.iwidth())
                    
                    self.assertTrue(p.isd('w') == p.fsd('w') - p.hps())
                    self.assertTrue(v.isd('w') == p.isd('w') - v.hps())
                    self.assertTrue(p.isd('h') == p.fsd('h') - p.vps())
                    self.assertTrue(v.isd('h') == p.isd('h') - v.vps())


                ep = fabs(p.vps() - p.hps())

                if p.aligny != 'center':
                    self.assertTrue(v.ftop() == p.itop() or v.ftop() - ep == p.itop(), errorstring) 
                    self.assertTrue(v.fbottom() == p.ibottom() or v.fbottom() + ep == p.ibottom(), errorstring)
 
                    self.assertTrue((v.itop() - v.padvertical == p.itop() or 
                                     v.itop() - ep - v.padvertical == p.itop()), errorstring)
                    self.assertTrue((v.ibottom() + v.padvertical == p.ibottom() or 
                                     v.ibottom() + ep + v.padvertical == p.ibottom()), errorstring)
                    
                    if ep != 0:
                        if p.aligny != 'center' and p.alignx != 'center':
                            if v.fill == True:
                                self.assertFalse(xor(xor(
                                                        v.itop() - ep - v.padvertical == p.itop(), 
                                                        v.ibottom() + ep + v.padvertical == p.ibottom()),
                                                    xor(
                                                        v.ileft() - ep - v.padhorizontal == p.ileft(),
                                                        v.iright() + ep + v.padvertical == p.iright())))
#                             else:
#                                 self.assertTrue(xor(xor(
#                                                         v.itop() - ep - v.padvertical == p.itop(), 
#                                                         v.ibottom() + ep + v.padvertical == p.ibottom()),
#                                                     xor(
#                                                         v.ileft() - ep - v.padhorizontal == p.ileft(),
#                                                         v.iright() + ep + v.padvertical == p.iright())))
                                

                    if p.aligny == 'top':
                        self.assertTrue(v.itop() == p.itop() + v.padvertical)
                        
                        self.assertTrue(v.ibottom() == p.itop() + v.fsd('h') - v.padvertical)
                        self.assertTrue(v.ibottom() == p.itop() + v.isd('h') + v.padvertical)
                    
                    if p.aligny == 'bottom':
                        self.assertTrue(v.ibottom() == p.ibottom() - v.padvertical)
                        
                        self.assertTrue(v.itop() == p.ibottom() - v.fsd('h') + v.padvertical)
                        self.assertTrue(v.itop() == p.ibottom() - v.isd('h') - v.padvertical)

                else:
                    self.assertTrue(v.ftop() - p.itop() == p.ibottom() - v.fbottom())
                     
 
                if p.alignx != 'center':
                    self.assertTrue(v.fleft() == p.ileft() or v.fleft() - ep == p.ileft(), errorstring)
                    self.assertTrue(v.fright() == p.iright() or v.fright() + ep == p.iright(), errorstring)
                     
                    self.assertTrue((v.ileft() - v.padhorizontal == p.ileft() or 
                                     v.ileft() - ep - v.padhorizontal == p.ileft()), errorstring)
                    self.assertTrue((v.iright() + v.padhorizontal == p.iright() or 
                                     v.iright() + ep + v.padhorizontal == p.iright()), errorstring)
                    
                    if ep != 0:
                        if p.aligny != 'center' and p.alignx != 'center':
                            if v.fill == True:
                                self.assertFalse(xor(xor(
                                                v.itop() - ep - v.padvertical == p.itop(), 
                                                v.ibottom() + ep + v.padvertical == p.ibottom()),
                                            xor(
                                                v.ileft() - ep - v.padhorizontal == p.ileft(),
                                                v.iright() + ep + v.padvertical == p.iright())))
#                             else:
#                                 self.assertTrue(xor(xor(
#                                                 v.itop() - ep - v.padvertical == p.itop(), 
#                                                 v.ibottom() + ep + v.padvertical == p.ibottom()),
#                                             xor(
#                                                 v.ileft() - ep - v.padhorizontal == p.ileft(),
#                                                 v.iright() + ep + v.padvertical == p.iright())))
                                
                            
                    
                    if p.alignx == 'left':
                        self.assertTrue(v.ileft() == p.ileft() + v.padhorizontal)
                        
                        self.assertTrue(v.iright() == p.ileft() + v.fsd('w') - v.padhorizontal)
                        self.assertTrue(v.iright() == p.ileft() + v.isd('w') + v.padhorizontal)
                    
                    if p.alignx == 'right':
                        self.assertTrue(v.iright() == p.iright() - v.padhorizontal)
                        
                        self.assertTrue(v.ileft() == p.iright() - v.fsd('w') + v.padhorizontal)
                        self.assertTrue(v.ileft() == p.iright() - v.isd('w') - v.padhorizontal)
                        
                    
                else:
                    self.assertTrue(v.fleft() - p.ileft() == p.iright() - v.fright())

            if len(p.items) > 1:
                
                errorstring = 'hp:' + str(p.padhorizontal) + 'vp:' + str(p.padvertical) 
                errorstring += str(p.alignx) + str(p.aligny)

                
                citop = cftop = cibottom = cfbottom = cileft = cfleft = ciright = cfright = None
                if p.growx == True:
                    citop = p.items[0].itop()
                    cftop = p.items[0].ftop()
                    cibottom = p.items[0].ibottom()
                    cfbottom = p.items[0].fbottom()
                elif p.growy == True:
                    cileft = p.items[0].ileft()
                    cfleft = p.items[0].fleft()
                    ciright = p.items[0].iright()
                    cfright = p.items[0].fright()
                
                nui = len(p.items)
                
                svp = shp = sidv = sidh = 0.0 
                sileft = siright = sfleft = sfright = 0.0
                sitop = sibottom = sftop = sfbottom = 0.0
                
                for ies in p.items:
                    
                    self._constraintlesstests(p, ies)
                    
                    
                    #if p.growy == True:
                    #    self.assertAlmostEqual(ies.fsd('h') * nui,p.isd('h'))
                    
                    #if p.growx == True:
                    #    self.assertAlmostEqual(ies.fsd('w') * nui,p.isd('w'))
                    
                    svp += ies.vps()
                    shp += ies.hps()
                    sidv += ies.isd('h')
                    sidh += ies.isd('w') 
                    sfright += ies.fright()
                    sfbottom += ies.fbottom()
                    
                    if p.growx == True:
                        self.assertTrue(ies.itop() == citop, errorstring)
                        self.assertTrue(ies.ftop() == cftop, errorstring)
                        self.assertTrue(ies.ibottom() == cibottom, errorstring)
                        self.assertTrue(ies.fbottom() == cfbottom, errorstring)
                        
                        
                        
                    elif p.growy == True:
                        self.assertTrue(ies.ileft() == cileft, errorstring)
                        self.assertTrue(ies.fleft() == cfleft, errorstring)
                        self.assertTrue(ies.iright() == ciright, errorstring)
                        self.assertTrue(ies.fright() == cfright, errorstring)

                    if p.padhorizontal == p.padvertical:
                        
                        if p.fill == False:
                            self.assertAlmostEqual(p.iwidth(), ies.fwidth() * nui)
                            self.assertAlmostEqual(p.iwidth() , (ies.iwidth() * nui) + (ies.hps() * nui))
                            self.assertAlmostEqual(p.iwidth() , (ies.iwidth() * nui) + (ies.vps() * nui))
                            self.assertAlmostEqual(p.iheight(), ies.fheight() * nui)
                            self.assertAlmostEqual(p.iheight(), (ies.iwidth() * nui) + (ies.vps() * nui))
                            self.assertAlmostEqual(p.iheight(), (ies.iwidth() * nui) + (ies.hps() * nui))

                        
                            self.assertTrue(p.isd('w') == p.fsd('w') - p.hps())
                            self.assertAlmostEqual(ies.isd('w'), (p.isd('w') / nui) - ies.hps())
                            self.assertTrue(p.isd('h') == p.fsd('h') - p.vps())
                            self.assertAlmostEqual(ies.isd('h'), (p.isd('h') / nui) - ies.vps())

                    if p.fill == True and p.growx == True:
                        self.assertAlmostEqual(p.iwidth(), ies.fwidth() * nui)
                        self.assertAlmostEqual(p.iwidth() , (ies.iwidth() * nui) + (ies.hps() * nui))
                        #self.assertAlmostEqual(ies.isd('w'), (p.isd('w') / nui) - ies.hps())
                    
                    if p.fill == True and p.growy == True:
                        self.assertAlmostEqual(p.iheight(), ies.fheight() * nui)
                        self.assertAlmostEqual(p.iheight(), (ies.iheight() * nui) + (ies.hps() * nui))
                        #self.assertAlmostEqual(ies.isd('h'), (p.isd('h') / nui) - ies.vps())

                    
                    if p.aligny == 'top':
                        multiple = 0
                        if p.growy == True:
                            multiple = p.items.index(ies)
                        self.assertAlmostEqual(ies.itop() - (ies.fsd('h') * multiple), 
                                               p.itop() + ies.padvertical)
                        
                        #self.assertAlmostEqual(ies.ibottom(), p.itop() + ies.fsd() - ies.padvertical)
                        #self.assertAlmostEqual(ies.ibottom(), p.itop() + ies.isd() + ies.padvertical)
                    
                    if p.aligny == 'bottom':
                        multiple = 0
                        if p.growy == True:
                            multiple = p.items.index(ies)
                        self.assertAlmostEqual(ies.ibottom() + (ies.fsd('h') * multiple), 
                                               p.ibottom() - ies.padvertical)
                        
                        #self.assertAlmostEqual(ies.itop(), p.ibottom() - ies.fsd() + ies.padvertical)
                        #self.assertAlmostEqual(ies.itop(), p.ibottom() - ies.isd() - ies.padvertical)

                    if p.alignx == 'left':
                        multiple = 0
                        if p.growx == True:
                            multiple = p.items.index(ies)
                        self.assertAlmostEqual(ies.ileft() - (ies.fsd('w') * multiple), 
                                               p.ileft() + ies.padhorizontal)
                        
                        #self.assertAlmostEqual(ies.iright(), p.ileft() + ies.fsd() - ies.padhorizontal)
                        #self.assertAlmostEqual(ies.iright(), p.ileft() + ies.isd() + ies.padhorizontal)
                    
                    if p.alignx == 'right':
                        multiple = 0
                        if p.growx == True:
                            multiple = p.items.index(ies)
                        self.assertAlmostEqual(ies.iright() + (ies.fsd('w') * multiple), 
                                               p.iright() - ies.padhorizontal)
                        
                        #self.assertTrue(ies.ileft() == p.iright() - ies.fsd() + ies.padhorizontal)
                        #self.assertTrue(ies.ileft() == p.iright() - ies.isd() - ies.padhorizontal)

                
                #self.assertAlmostEqual(svp + sidh, p.isd('h'))
                #self.assertAlmostEqual(shp + sidv, p.isd('w'))
                
                #self.assertTrue(sfright - (p.ileft() * nui) == (ies.fsd() * nui) + p.ileft(), errorstring)




#if __name__ == '__main__':
    
#    unittest.main()            




def inpractice():
    
    f = open('../../geometrymanager.html', 'w')
    f.write('<html><head><title></title></head><body>\n')
    
    g = area(height=3000, width=3000, aligny='center', alignx='center', growy = True,
             padhorizontal=100, padvertical=100, fill=True)
    
    ga = area(aligny='center', alignx='center', growy = True, padhorizontal=20, padvertical=20, fill=True)
    gb = area(aligny='center', alignx='center', padhorizontal=20, padvertical=20, fill=True)
    g.push(ga)
    g.push(gb)
    
    
    
    numrows = 3
    graphsperrow = 4
    for rowcount in range(0, numrows):
        gc = area(aligny='center', alignx='center', growx = True, padhorizontal=20, padvertical=20, fill=True)
        ga.push(gc)
        
        for columncount in range(0, graphsperrow):
            gd = area(aligny='center', alignx='center', padhorizontal=20, padvertical=20)
            gc.push(gd)
    

    f.write('g.height:' + str(g.height) + ' g.width:' + str(g.width))
    f.write(' g.alignx:' + str(g.alignx) + ' g.aligny:' + str(g.aligny))
    f.write(' g.padhorizontal:' + str(g.padhorizontal) + ' g.padvertical:' + str(g.padvertical))
    f.write('\n<BR>')
    f.write('<svg width="'+str(g.width)+'" height="'+str(g.height) + '">\n')
    f.write('<rect width="'+str(g.width)+'" height="'+str(g.height)+'" style="fill:rgb(14,17,14);"></rect>\n')
              
    f.write(g.svg() + '\n')
    f.write(g.svgmargin() + '\n')
            
    for ga in g.items:
    
        f.write(ga.svg() + '\n')
        f.write(ga.svgmargin() + '\n')
        
        for gb in ga.items:
            f.write(gb.svg() + '\n')
            f.write(gb.svgmargin() + '\n')
            
            for gc in gb.items:
                f.write(gc.svg() + '\n')
                f.write(gc.svgmargin() + '\n')
                
    
    f.write('</svg><br>~<br>')
                           
    f.write('</body></html>')
      
    f.close()
    




#inpractice()

#createmultiple()

#while True:
#    suite = unittest.TestLoader().loadTestsFromTestCase(area_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)
#    break












# 
#  
# glst = []
#  
# glst.append(area(height=2000,width=1000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=100))
#  
# if True:
#     glst.append(area(height=2000,width=1000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=200))
#      
#     glst.append(area(height=2000,width=1000,alignx='right',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='top',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=2000,width=1000,alignx='left',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=2000,width=1000,alignx='left',aligny='top',padhorizontal=200,padvertical=200))
#              
#     glst.append(area(height=2000,width=1000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=2000,width=1000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=200))
#  
#  
# glst.append(area(height = 1000, width = 2000, alignx = 'bottom', aligny = 'bottom', padhorizontal = 100, padvertical = 100))
#  
# if True:
#     glst.append(area(height=1000,width=2000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=2000,alignx='right',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='top',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=2000,alignx='left',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=2000,alignx='left',aligny='top',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=2000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=2000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=200))
#  
# glst.append(area(height = 1000, width = 1000, alignx = 'bottom', aligny = 'bottom', padhorizontal = 100, padvertical = 100))
#  
# if True:
#     glst.append(area(height=1000,width=1000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='bottom',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=1000,alignx='right',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='top',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=1000,alignx='left',aligny='top',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='top',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='top',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=1000,alignx='left',aligny='top',padhorizontal=200,padvertical=200))
#          
#     glst.append(area(height=1000,width=1000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=100))
#     if True:
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=100))
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='bottom',padhorizontal=100,padvertical=200))
#         glst.append(area(height=1000,width=1000,alignx='right',aligny='bottom',padhorizontal=200,padvertical=200))
#  
#  
#  
# #ga = area(padhorizontal = 30, padvertical = 30)
# #gb = area(padhorizontal = 30, padvertical = 30)
# #gc = area(padhorizontal = 30, padvertical = 30)
# #gd = area(padhorizontal = 30, padvertical = 30)
#  
# #g.push(ga)
# #g.push(gb)
# #g.push(gc)
# #g.push(gd)
#  
#  
#  
# #print('g.svg():' + str(g.svg()))
#  
# f = open('../../geometrymanager.html', 'w')
# f.write('<html><head><title></title></head><body>\n')
#  
# for item in glst:
#     f.write('<svg width="'+str(item.width)+'" height="'+str(item.height) + '">\n')
#     f.write('<rect width="'+str(item.width)+'" height="'+str(item.height)+'" style="fill:rgb(14,17,14);"></rect>\n')
#     ga = area()
#     item.push(ga)
#      
#     f.write(item.svg() + '\n')
#     f.write(ga.svg() + '\n')
#     #f.write(item.svgmargin(), '\n')
#     f.write('</svg><br>~<br>')
#  
# #f.write(g.svg() + '\n')
# #f.write(ga.svg() + '\n')
# # f.write(gb.svg() + '\n')
# # f.write(gc.svg() + '\n')
# # f.write(gd.svg() + '\n')
#  
#  
# #f.write(g.svgmargin() + '\n')
# #f.write(ga.svgmargin() + '\n')
# # f.write(gb.svgmargin() + '\n')
# # f.write(gc.svgmargin() + '\n')
# # f.write(gd.svgmargin() + '\n')
#  
#  
#                   
# f.write('</body></html>')
#  
# f.close()

    
# class item():
#     
#     # item dimensions
#     i_height = None
#     i_width = None
#     
#     evenlydistributeweightsx = True
#     evenlydistributeweightsy = True

    
    
    # divisions of window
    


# 
# print(g)
# print()
# 
# print('g._width():' + str(g._width()))
# # print('ga._width():' + str(ga._width()))
# # print('gb._width():' + str(gb._width()))
# # print('gc._width():' + str(gc._width()))
# # print('gd._width():' + str(gd._width()))
# 
# print('g._height():' + str(g._height()))
# # print('ga._height():' + str(ga._height()))
# # print('gb._height():' + str(gb._height()))
# # print('gc._height():' + str(gc._height()))
# # print('gd._height():' + str(gd._height()))
# 
# print('g.left():' + str(g.left()))
# # print('ga.left():' + str(ga.left()))
# # print('gb.left():' + str(gb.left()))
# # print('gc.left():' + str(gc.left()))
# # print('gd.left():' + str(gd.left()))
# 
# print('g.right():' + str(g.right()))
# # print('ga.right():' + str(ga.right()))
# # print('gb.right():' + str(gb.right()))
# # print('gc.right():' + str(gc.right()))
# # print('gd.right():' + str(gd.right()))
# 
# print('g.top():' + str(g.top()))
# # print('ga.top():' + str(ga.top()))
# # print('gb.top():' + str(gb.top()))
# # print('gc.top():' + str(gc.top()))
# # print('gd.top():' + str(gd.top()))
# 
# print('g.bottom():' + str(g.bottom()))
# # print('ga.bottom():' + str(ga.bottom()))
# # print('gb.bottom():' + str(gb.bottom()))
# # print('gc.bottom():' + str(gc.bottom()))
# # print('gd.bottom():' + str(gd.bottom()))

#     
# class old():
#     
#     
#     # retrieve the relative value of the top pixel in screen coordinates
#     def top(self):
#         rvar = None
#         
#         # if there is no parent
#         if self.parent == None:
#             rvar = self.padtop
#         
#         elif len(self.parent.items) == 1:
#             rvar = self.parent.top() + self.padtop
#             
#         else:
#             # if we are growing the items added to the container horizontally
#             if self.parent.growx:
#                 
#                 if self.parent.aligny == 'center':
#                     print('self._height():' + str(self._height()))
#                     var = distance_between_centered_segment(self.parent.top(),0,
#                                                             self._height() + self.padtop + self.padbottom,
#                                                             self.parent.bottom())
#                     rvar = self.parent.top() + var
#                     
#                     print('rvar:' + str(rvar))
#                     
#                 elif self.parent.aligny == 'top':
#                     rvar = self.parent.top() + self.padtop
#                 elif self.parent.aligny == 'bottom':
#                     rvar = self.parent.bottom() - self._height() - self.padbottom
#                 else:
#                     raise ValueError('Expecting top or center or bottom for aligny, received %s.' % self.parent.aligny)
#             
#             # if we are growing the items added to the container vertically
#             else:
#                 
#                 sumvar = 0
#                 indexofself = self.parent.items.index(self)
#                 for i in range(0, indexofself):
#                     sumvar += self.parent.items[i]._height() + self.padtop + self.padbottom
#                 rvar = sumvar + self.padtop + self.parent.top()
# 
#         return rvar
#     
#     # retrieve the relative value of the left pixel in screen coordinates
#     def left(self):
#         rvar = None
#         
#         # if there is no parent
#         if self.parent == None:
#             rvar = self.padleft
#         
#         elif len(self.parent.items) == 1:
#             rvar = self.parent.left() + self.padleft
#         
#         else:
#             if self.parent.growx:
#                 sumvar = 0
#                 indexofself = self.parent.items.index(self)
#                 for i in range(0, indexofself):
#                     sumvar += self.parent.items[i]._width() + self.padleft + self.padright
#                 rvar = sumvar + self.padleft + self.parent.left()
#             else:
#                 
#                 
#                 
#                 rvar = self.parent.left() + self.padleft
#         return rvar
#     
#     # retrieve the relative value of the right pixel in screen coordinates
#     def right(self):
#                     
#         rvar = self._width() + self.left()
#                     
#         return rvar
# 
#     # retrieve the relative value of the bottom pixel in screen coordinates
#     def bottom(self):
#         
#         rvar = self._height() + self.top()
#         
#         return rvar
# 
#     # retrieve the relative width
#     def _width(self):
#         rvar = None
#         
#         # if this item has no parent
#         if self.parent == None:
#             # the width is the canvas width minus padding
#             rvar = self.width - self.padleft - self.padright
# 
#         # if this item is the only item in the container
#         elif len(self.parent.items) == 1:
#             # the width is the parent width minus padding
#             rvar = self.parent._width() - self.padleft - self.padright
#             
#         else:
#             
#             pitemslen = len(self.parent.items)
#             pwidth = self.parent._width()
#             pheight = self.parent._height()
#             
#             # if the parent is a container growing horizontally
#             if self.parent.growx:
#                 
#                 # if the parent container grows horizontally parent width is divided by number of items
#                 fpwidth = pwidth / pitemslen
#                 
#                 # width will be the minimum btwn parent height and fraction parent width
#                 if fpwidth >= pheight: rvar = pheight - self.padleft - self.padright
#                 else: rvar = fpwidth - self.padleft - self.padright
#                 
#             
#             # if the parent is a container growing vertically
#             elif self.parent.growy:
#                 
#                 # if the parent container grows vertically parent height is divided by number of items
#                 fpheight = pheight / pitemslen
#                 
#                 # width will be the minimum btwn fraction parent height and parent width
#                 if pwidth >= fpheight: rvar = fpheight - self.padleft - self.padright
#                 else: rvar = pwidth - self.padleft - self.padright
#                 
#         
#         return rvar
#         
#     
#     
#     
#     # retrieve the full height with margins
#     def fheight(self):
#         rvar = None
#         
#         # if this item has no parent
#         if self.parent == None:
#             # height is the class var self.height
#             rvar = self.height
#         # if the parent has only one item in the container
#         elif len(self.parent.items) == 1:
#             #
#             rvar = 
#         
#     
#     
#     # retrieve the inner height without margins
#     def iheight(self):
#         rvar = None
#         
#         # if this item has no parent
#         if self.parent == None:
#             # the height is the canvas height minus padding
#             rvar = self.height - self.padtop - self.padbottom
# 
#         # if this item is the only item in the container
#         elif len(self.parent.items) == 1:
#             # the height is the parent height minus padding
#             rvar = self.parent._height() - self.padtop - self.padbottom
#             
#         else:
#             
#             pitemslen = len(self.parent.items)
#             pwidth = self.parent._width() 
#             pheight = self.parent._height()
#             
#             # if the parent is a container growing horizontally
#             if self.parent.growx:
#                 
#                 # if the parent container grows horizontally parent width is divided by number of items
#                 fpwidth = pwidth / pitemslen
#                 
#                 # height will be the minimum btwn parent height and fraction parent width
#                 if fpwidth >= pheight: rvar = pheight - self.padtop - self.padbottom
#                 else: rvar = fpwidth - self.padtop - self.padbottom
#                 
#             
#             # if the parent is a container growing vertically
#             elif self.parent.growy:
#                 
#                 # if the parent container grows vertically parent height is divided by number of items
#                 fpheight = pheight / pitemslen
#                 
#                 # height will be the minimum btwn fraction parent height and parent width
#                 if pwidth >= fpheight: rvar = fpheight - self.padtop - self.padbottom
#                 else: rvar = pwidth - self.padtop - self.padbottom
# 
#         return rvar
