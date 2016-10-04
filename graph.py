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



#from modular_table.defines import defines_for_cell, defines_for_column, defines_for_row, defines_for_table
#from modular_table.defines import defines_for_datavalues
from defines import defines_for_table, defines_for_datavalues, defines_for_cell
#from django.db.models import Max, Sum, Min
from math import ceil, fabs, log10, sin, cos, pi, acos, tan
from random import randint
from geometrymanager import area
import pandas as pd




TABLE_AS_DATAFRAME = True



class table():
    
    df = None
    
    #table_cells = []
    #table_childcells = []
    
    class datavalues_properties():
        canvasheight = 1000
        canvaswidth = 1000
        margintop = 50
        marginbottom = 50
        marginright = 50
        marginleft = 50
        markscount = 10
        
        orientation = defines_for_datavalues.COLUMN_WISE
        #orientation = defines_for_datavalues.ROW_WISE
        originaxis = defines_for_datavalues.HORIZONTAL_AXIS
        #originaxis = defines_for_datavalues.VERTICAL_AXIS
        

    table_type = defines_for_table.TABLE_PIE
    


# parameters class holds relevant information for use in setting pixel space values and printing svg strings
class parameters():
    valmin = None # the minimum value of all cells or sum of cells in the case of stacked bar
    valmax = None # the maximum value of all cells or sum of cells in the case of stacked bar
    
    # TODO: none of the sums calculated are currently used
    tablesum = None # the sum of all values in the table
    columnsum = None # float value of column sum changes during iteration, set before calling subsequent methods
    rowsum = None # float value of row sum changes during iteration, set before calling subsequent methods
    
    magmin = None # fourth magnitude minimum value
    magmax = None # fouth magnitude maximum value
    
    # minimum and maximum pixel values based on margins
    pixmin_x = None 
    pixmax_x = None
    pixcnt_x = None
    pixmin_y = None
    pixmax_y = None
    pixcnt_y = None
    
    # pixel intervals between grid/marks for category or value axis 
    pixinterval_x = None
    pixinterval_y = None
    
    
    orientation = None # user choice, generate chart from columns or from rows
    originaxis = None # user choice, orient the graph horizontally or vertically (defines_for_datavalues) 
    
    table_type = None
    
    caxismarkscount = None # user choice: number of marks on the category axis
    vaxismarkscount = None # user choice: number of marks on the vertical axis
        
    magmarkslocation = [] # list of fourth magnitude marks
    magintervaldistance = None # distance between fourth magnitude marks
    
    canvasheight = None
    canvaswidth = None
    margintop = None
    marginbottom = None
    marginright = None
    marginleft = None

    vaxismarkslocation = [] # value axis marks locations in pixel space
    caxismarkslocation = [] # category axis marks locations in pixel space
    
    def __str__(self):
        
        r = ''
        
        if self.valmin != None: r += 'minval: %f\n' % self.valmin
        if self.valmax != None: r += 'maxval: %f\n' % self.valmax
        
        if self.tablesum != None: r += 'tablesum: %f\n' % self.tablesum
        if self.columnsum != None: r += 'columnsum: %s\n' % self.columnsum
        if self.rowsum != None: r += 'rowsum: %s\n' % self.rowsum
        
        if self.magmin != None: r += 'minmag: %f\n' % self.magmin
        if self.magmax != None: r += 'maxmag: %f\n' % self.magmax
        
        if self.pixmin_x != None: r += 'pixmin_x: %f\n' % self.pixmin_x
        if self.pixmax_x != None: r += 'pixmax_x: %f\n' % self.pixmax_x
        if self.pixmax_x != None: r += 'pixcnt_x: %f\n' % self.pixcnt_x
        if self.pixmax_x != None: r += 'pixinterval_x: %f\n' % self.pixinterval_x

        if self.pixmin_y != None: r += 'pixmin_y: %f\n' % self.pixmin_y
        if self.pixmax_y != None: r += 'pixmax_y: %f\n' % self.pixmax_y
        if self.pixmax_y != None: r += 'pixcnt_y: %f\n' % self.pixcnt_y
        if self.pixmax_y != None: r += 'pixinterval_y: %f\n' % self.pixinterval_y
        
        if self.vaxismarkscount != None: r += 'vaxismarkscount: %f\n' % self.vaxismarkscount
        if self.caxismarkscount != None: r += 'caxismarkscount: %f\n' % self.caxismarkscount
        
        if self.magintervaldistance != None: r += 'magintervaldistance: %f\n' % self.magintervaldistance
        if self.magmarkslocation != None: r += 'magmarkslocation: %s\n' % self.magmarkslocation
        
        if self.vaxismarkslocation != None: r += 'vaxismarkslocation: %s\n' % self.vaxismarkslocation
        
        if self.table_type != None: r += 'table_type: %s\n' % self.table_type
        
        if self.orientation != None: r += 'orientation: %s\n' % self.orientation
        
        if self.caxismarkslocation != None: r += 'caxismarkslocation: %s\n' % self.caxismarkslocation
        
        return r


# calculate where on the category axis to plot marks for line, returns a list
def calculate_caxis_pixel_plots_for_line(table, orientation, originaxis, categorycount,
                                         pixmin_x, pixmax_x, pixcnt_x, interval_x, 
                                         pixmin_y, pixmax_y, pixcnt_y, interval_y):
        
    markslocationlist = []

    startrange = intervaldistance = None    
    if originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        startrange = pixmin_x
        if categorycount == 1: intervaldistance = pixcnt_x / 2
        else: intervaldistance = pixcnt_x / (categorycount-1)
    elif originaxis == defines_for_datavalues.VERTICAL_AXIS:
        startrange = pixmin_y
        if categorycount == 1: intervaldistance = pixcnt_y / 2
        else: intervaldistance = pixcnt_y / (categorycount-1)
    
    if categorycount == 1:
        for count in range(1, categorycount+1):        
            markslocationlist.append(startrange + (intervaldistance * count))
        
    else:
        for count in range(0, categorycount):        
            markslocationlist.append(startrange + (intervaldistance * count))

    return markslocationlist

# calculate where on the category axis to plot marks for bar, returns a list
def calculate_caxis_pixel_plots_for_bar(table, orientation, originaxis, categorycount,
                                         pixmin_x, pixmax_x, pixcnt_x, interval_x, 
                                         pixmin_y, pixmax_y, pixcnt_y, interval_y):
    
    markslocationlist = []
    
    startrange = intervaldistance = None    
    if originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        startrange = pixmin_x
        intervaldistance = pixcnt_x / (categorycount)
    elif originaxis == defines_for_datavalues.VERTICAL_AXIS:
        startrange = pixmin_y
        intervaldistance = pixcnt_y / (categorycount)
    
    for count in range(0, categorycount):
                
        firstplot = startrange + (intervaldistance * count)
        secondplot = startrange + (intervaldistance * (count+1))
        
        markslocationlist.append(firstplot + ((secondplot - firstplot) / 2))

    return markslocationlist

# calculates where on the category axis to plot marks and gridlines for line or stacked bar, returns a list
def calculate_caxis_pixel_plots(table, table_type, orientation, originaxis, 
                                pixmin_x, pixmax_x, pixcnt_x, interval_x, 
                                pixmin_y, pixmax_y, pixcnt_y, interval_y,
                                categorycount):
    
    var = None
    
    if table_type == defines_for_table.TABLE_LINE:
        var = calculate_caxis_pixel_plots_for_line(table, orientation, originaxis, categorycount,
                                                   pixmin_x, pixmax_x, pixcnt_x, interval_x, 
                                                   pixmin_y, pixmax_y, pixcnt_y, interval_y)
        
    elif table_type == defines_for_table.TABLE_STACKEDBAR:
        var = calculate_caxis_pixel_plots_for_bar(table, orientation, originaxis, categorycount,
                                                  pixmin_x, pixmax_x, pixcnt_x, interval_x, 
                                                  pixmin_y, pixmax_y, pixcnt_y, interval_y)
        
    return var


# returns the magnitude
def getfourthmagnitude(n, exponent):
    maxy = 0

    # between 1000 and 750
    if (n <= (4 * ((10 ** exponent) / 4)) and
        n > (3 * ((10 ** exponent) / 4))):

        maxy = (4 * ((10 ** exponent) / 4))

    # between 750 and 500
    elif (n <= (3 * ((10 ** exponent) / 4)) and
          n > (2 * ((10 ** exponent) / 4))):

        maxy = (3 * ((10 ** exponent) / 4))

    # between 500 and 250
    elif (n <= (2 * ((10 ** exponent) / 4)) and
          n > (1 * ((10 ** exponent) / 4))):

        maxy = (2 * ((10 ** exponent) / 4))

    else:
        maxy = (10 ** exponent) / 4

    return maxy

# returns the magnitude
def getfourthmagnitudeprevious(n, exponent):
        
    maxy = 0

    # between 750 and 500
    if (n >= (3 * ((10 ** exponent) / 4)) and
          n < (4 * ((10 ** exponent) / 4))):

        maxy = (3 * ((10 ** exponent) / 4))

    # between 500 and 250
    elif (n >= (2 * ((10 ** exponent) / 4)) and
          n < (3 * ((10 ** exponent) / 4))):

        maxy = (2 * ((10 ** exponent) / 4))

    # between 250 and 0
    elif (n >= (1 * ((10 ** exponent) / 4)) and
          n < (2 * ((10 ** exponent) / 4))):

        maxy = (1 * ((10 ** exponent) / 4))

    else:
        maxy = (4 * ((10 ** (exponent-1)) / 4))
        
    return maxy


# calculates the minimum maximum values for a single cell if table line or a column/row if stackedbar
def calculate_minimum_maximum_value(table, parameters):

    minval = maxval = columnsum = rowsum = tablesum = None
    
    if table.table_type == defines_for_table.TABLE_LINE:
        if TABLE_AS_DATAFRAME == True:
            m = table.df.min() # the minimum cell of a line table
            minval = min(m)
            m = table.df.max() # the maximum cell of a line table
            maxval = max(m)
        else:
            var = table.childcells.all().aggregate(Min('data_float_var'))
            minval = var['data_float_var__min']
            var = table.childcells.all().aggregate(Max('data_float_var'))
            maxval = var['data_float_var__max']

    elif table.table_type == defines_for_table.TABLE_STACKEDBAR:
        if TABLE_AS_DATAFRAME == True:
            if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
                m = table.df.sum(axis=0)
                maxval = max(m)
                minval = min(m)
            elif parameters.orientation == defines_for_datavalues.ROW_WISE:
                m = table.df.sum(axis=1)
                maxval = max(m)
                minval = min(m)
        else:
            m = []
            items = None
            if parameters.orientation == defines_for_datavalues.COLUMN_WISE: items = table.childcolumns.all()
            elif parameters.orientation == defines_for_datavalues.ROW_WISE: items = table.childrows.all()
            for item in items:
                var = item.childcells.all().aggregate(Sum('data_float_var'))        
                m.append(var['data_float_var__sum'])
            maxval = max(m)
            minval = min(m)

    elif table.table_type == defines_for_table.TABLE_PIE:
        if TABLE_AS_DATAFRAME == True:
            if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
                m = table.df.sum(axis=0)
                maxval = max(m)
                minval = min(m)
                columnsum = []
                tablesum = 0.0
                for item in m:
                    tablesum += item
                    columnsum.append(item)
            elif parameters.orientation == defines_for_datavalues.ROW_WISE:
                m = table.df.sum(axis=1)
                maxval = max(m)
                minval = min(m)
                rowsum = []
                tablesum = 0.0
                for item in m:
                    tablesum += item
                    rowsum.append(item)
        else:
            m = []
            items = None
            if parameters.orientation == defines_for_datavalues.COLUMN_WISE: 
                items = table.childcolumns.all().order_by('index')
            elif parameters.orientation == defines_for_datavalues.ROW_WISE: 
                items = table.childrows.all().order_by('index')
            columnsum = rowsum = []
            tablesum = 0.0
            for item in items:
                var = item.childcells.all().aggregate(Sum('data_float_var'))        
                m.append(var['data_float_var__sum'])
                tablesum += var
                if parameters.orientation == defines_for_datavalues.COLUMN_WISE: columnsum.append(var)
                elif parameters.orientation == defines_for_datavalues.ROW_WISE: rowsum.append(var)
            maxval = max(m)
            minval = min(m)

    return [minval, maxval, tablesum, columnsum, rowsum]


# returns the magnitude for a positive or negative number
def calculate_magnitude_for_number_next(var):

    mag = None
    
    if var > 0.0:
        mag = getfourthmagnitude(fabs(var), ceil(log10(fabs(var)))  )
    elif var < 0.0:
        mag = -getfourthmagnitude(fabs(var), ceil(log10(fabs(var)))  )
    elif var == 0.0:
        mag = 0.0
    
    return mag

# returns the magnitude for a positive or negative number
def calculate_magnitude_for_number_previous(var):
    
    mag = None
    
    if var > 0.0:
        mag = getfourthmagnitude(fabs(var), ceil(log10(fabs(var)))  )
    elif var < 0.0:
        mag = -getfourthmagnitude(fabs(var), ceil(log10(fabs(var)))  )
    elif var == 0.0:
        mag = 0.0
    
    return mag

# returns magnitude start, magnitude stop, and interval for a range
def calculate_magnitude_start_stop_interval(minvalue, maxvalue, markscount):
        
    magmin = calculate_magnitude_for_number_previous(minvalue)
    magmax = calculate_magnitude_for_number_next(maxvalue)
    
    # always include 0 axis
    if magmax > 0.0 and magmin > 0.0:
        magmin = 0.0
    elif magmax < 0.0 and magmin < 0.0:
        magmax = 0.0
    
    # if the min and max are the same divide by 10 in negative and opposite direction and add/subtract this value
    if ( magmin == magmax ):
        magmin -= magmin / 10
        magmax += magmax / 10
        
    # interval is determined by dividing the different of max and min by number of marks
    interval = (magmax - magmin) / markscount

    return (magmin, magmax, interval)

# returns a list of marks locations in value space for the variable axis
def calculate_vaxis_mag_plots(magmin, magmax, magintervaldistance, markscount):
     
    # return value list of plots
    ymarkslocationlist = []

    magplotvar = magmin 

    # iterate through magplots 
    for _ in range(0, int(markscount) + 1):

        # append each mag plot
        ymarkslocationlist.append(magplotvar)
        
        magplotvar += magintervaldistance
        
    return ymarkslocationlist



# returns pixel start, pixel stop, and interval
def calculate_pixel_start_stop_interval(table, tabletype, orientation, originaxis, markscount, 
                                        cheight, cwidth, mtop, mbottom, mright, mleft):

    categorycount = None
    
    if TABLE_AS_DATAFRAME:
        if orientation == defines_for_datavalues.COLUMN_WISE: 
            categorycount = table.df.columns.size
        elif orientation == defines_for_datavalues.ROW_WISE: 
            categorycount = table.df.index.size
    else:
        if orientation == defines_for_datavalues.COLUMN_WISE: 
            categorycount = table.childcolumns.count()
        elif orientation == defines_for_datavalues.ROW_WISE: 
            categorycount = table.childrows.count()    

    pixmin_x = mleft
    pixmax_x = cwidth - mright
    pixcnt_x = cwidth - mright - mleft
    if originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        interval_x = pixcnt_x / categorycount
    elif originaxis == defines_for_datavalues.VERTICAL_AXIS:
        interval_x = pixcnt_x / markscount
    
    pixmin_y = mtop
    pixmax_y = cheight - mbottom
    pixcnt_y = cheight - mtop - mbottom
    if originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        interval_y = pixcnt_y / markscount
    elif originaxis == defines_for_datavalues.VERTICAL_AXIS:
        interval_y = pixcnt_y / categorycount

    return (pixmin_x, pixmax_x, pixcnt_x, interval_x, pixmin_y, pixmax_y, pixcnt_y, interval_y, categorycount)

# returns a list of marks locations in pixel space for the variable axis
def calculate_vaxis_pixel_plots(originaxis, pixmin_x, pixinterval_x, pixmin_y, pixinterval_y, markscount):
    
    markslocationlist = []
    
    if originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        pixplotvar = pixmin_y
        for _ in range(0, int(markscount) + 1):
            markslocationlist.append(pixplotvar) # append each pix plot
            pixplotvar += pixinterval_y
        
    elif originaxis == defines_for_datavalues.VERTICAL_AXIS:
        pixplotvar = pixmin_x
        for _ in range(0, int(markscount) + 1):
            markslocationlist.append(pixplotvar) # append each pix plot
            pixplotvar += pixinterval_x
        
    return markslocationlist

# converts a value into pixel space in preparation for graphing
def value_to_pixel(magmin, magmax, pixmin, pixmax, inputy):
    
    #OldRange = (OldMax - OldMin)  
    #NewRange = (NewMax - NewMin)  
    #NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    #http://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
        
    magrange = (magmax - magmin)
    pixrange = (pixmax - pixmin)
    output = (((inputy - magmin) * pixrange) / magrange) + pixmin
    
    return output

# calculates bounds for screen space plotting, v and c axis grid plots, and stores data such as orientation, origin
def calculate_parameters(table):
    
    var = parameters()
    
    # retrieves data used in calculations from the database
    var.vaxismarkscount = float(table.datavalues_properties.markscount)
    var.canvasheight = float(table.datavalues_properties.canvasheight)
    var.canvaswidth = float(table.datavalues_properties.canvaswidth)
    var.margintop = float(table.datavalues_properties.margintop)
    var.marginbottom = float(table.datavalues_properties.marginbottom)
    var.marginleft = float(table.datavalues_properties.marginleft)
    var.marginright = float(table.datavalues_properties.marginright)
    var.table_type = (table.table_type)
    var.orientation = table.datavalues_properties.orientation
    var.originaxis = table.datavalues_properties.originaxis
    
    # queries database or dataframe and retrieves minimum or maximum value plot
    r = calculate_minimum_maximum_value(table, var)
    
    var.valmin = r[0]
    var.valmax = r[1]
    var.tablesum = r[2]
    var.columnsum = r[3]
    var.rowsum = r[4]
    
    # calculates the fourth magnitude used in determining value axis grid and mark locations
    r = calculate_magnitude_start_stop_interval(var.valmin, var.valmax, var.vaxismarkscount)
    
    var.magmin = r[0]
    var.magmax = r[1]
    var.magintervaldistance = r[2]
    
    # returns a list of fourth magnitude plots determined by vaxismarkscount
    r = calculate_vaxis_mag_plots(var.magmin, var.magmax, var.magintervaldistance, var.vaxismarkscount)
    
    var.magmarkslocation = r
    
    # returns relevant pixel/screen coordinate data bounds for calculations, value to pixel, category to pixel, etc
    r = calculate_pixel_start_stop_interval(table, var.table_type, 
                                            var.orientation, var.originaxis, var.vaxismarkscount,
                                            var.canvasheight, var.canvaswidth,
                                            var.margintop, var.marginbottom, 
                                            var.marginright, var.marginleft)
    
    var.pixmin_x = r[0]
    var.pixmax_x = r[1]
    var.pixcnt_x = r[2]
    var.pixinterval_x = r[3]
    
    var.pixmin_y = r[4]
    var.pixmax_y = r[5]
    var.pixcnt_y = r[6]
    var.pixinterval_y = r[7]
    var.caxismarkscount = r[8]
    
    # returns a list of value axis plots in screen/pixel space
    r = calculate_vaxis_pixel_plots(var.originaxis, 
                                    var.pixmin_x, var.pixinterval_x,
                                    var.pixmin_y, var.pixinterval_y,  
                                    var.vaxismarkscount)
    
    var.vaxismarkslocation = r
    
    # returns a list of category axis plots in screen/pixel space
    r = calculate_caxis_pixel_plots(table, var.table_type, var.orientation, var.originaxis, 
                                    var.pixmin_x, var.pixmax_x, var.pixcnt_x, var.pixinterval_x,
                                    var.pixmin_y, var.pixmax_y, var.pixcnt_y, var.pixinterval_y,
                                    var.caxismarkscount)
    
    var.caxismarkslocation = r
    
    return var # returns parameters class instance


def set_geometry_unitcircle_BEZIER(parameters, xa, ya, xb, yb, xc, yc, xd, yd):
     
    r = {}

    oxz = value_to_pixel(-1,1, 0.0, parameters.pixmax, 0.0)
    oxz += parameters.translatex
    oyz = value_to_pixel(-1,1, 0.0, parameters.pixmax, 0.0)
    oyz += parameters.translatey
    oxa = value_to_pixel(-1,1, 0.0, parameters.pixmax, xa)
    oxa += parameters.translatex
    oya = value_to_pixel(-1,1, 0.0, parameters.pixmax, ya)
    oya += parameters.translatey
    oxb = value_to_pixel(-1,1, 0.0, parameters.pixmax, xb)
    oxb += parameters.translatex
    oyb = value_to_pixel(-1,1, 0.0, parameters.pixmax, yb)
    oyb += parameters.translatey
    oxc = value_to_pixel(-1,1, 0.0, parameters.pixmax, xc)
    oxc += parameters.translatex
    oyc = value_to_pixel(-1,1, 0.0, parameters.pixmax, yc)
    oyc += parameters.translatey
    oxd = value_to_pixel(-1,1, 0.0, parameters.pixmax, xd)
    oxd += parameters.translatex
    oyd = value_to_pixel(-1,1, 0.0, parameters.pixmax, yd)
    oyd += parameters.translatey
    
    outval = ''
    outval += 'M ' + str(oxz) + ' ' + str(oyz) + ' '
    outval += 'L ' + str(oxa) + ' ' + str(oya) + ' '
    outval += 'C ' + str(oxb) + ' ' + str(oyb) + ', '
    outval += str(oxc) + ' ' + str(oyc) + ', '
    outval += str(oxd) + ' ' + str(oyd) + ' '
    outval += 'L ' + str(oxz) + ' ' + str(oyz) + ' '
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PATH_D]] = outval

    s = '<'
            
    s += 'path'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="fill:rgb(%d,%d,%d);stroke:rgb(%d,%d,%d);"' % (randint(100,255),randint(100,255),randint(100,255),
                                                               randint(100,255),randint(100,255),randint(100,255))
    #s += 'fill="transparent" style="stroke:rgb(%d,%d,%d);"' % (randint(100,255), randint(100,255), randint(100,255))
    s += '>'
        
    s += '</'
    s += 'path'
    s += '>'
    
    return s

def set_geometry_unitcircle_seven_point_BEZIER(parameters, xa, ya, xb, yb, xc, yc, xd, yd, xe, ye, xf, yf, xg, yg):
     
    r = {}

    oxz = value_to_pixel(-1,1, 0.0, parameters.pixmax, 0.0)
    oxz += parameters.translatex
    oyz = value_to_pixel(-1,1, 0.0, parameters.pixmax, 0.0)
    oyz += parameters.translatey
    oxa = value_to_pixel(-1,1, 0.0, parameters.pixmax, xa)
    oxa += parameters.translatex
    oya = value_to_pixel(-1,1, 0.0, parameters.pixmax, ya)
    oya += parameters.translatey
    oxb = value_to_pixel(-1,1, 0.0, parameters.pixmax, xb)
    oxb += parameters.translatex
    oyb = value_to_pixel(-1,1, 0.0, parameters.pixmax, yb)
    oyb += parameters.translatey
    oxc = value_to_pixel(-1,1, 0.0, parameters.pixmax, xc)
    oxc += parameters.translatex
    oyc = value_to_pixel(-1,1, 0.0, parameters.pixmax, yc)
    oyc += parameters.translatey
    oxd = value_to_pixel(-1,1, 0.0, parameters.pixmax, xd)
    oxd += parameters.translatex
    oyd = value_to_pixel(-1,1, 0.0, parameters.pixmax, yd)
    oyd += parameters.translatey
    oxe = value_to_pixel(-1,1, 0.0, parameters.pixmax, xe)
    oxe += parameters.translatex
    oye = value_to_pixel(-1,1, 0.0, parameters.pixmax, ye)
    oye += parameters.translatey
    oxf = value_to_pixel(-1,1, 0.0, parameters.pixmax, xf)
    oxf += parameters.translatex
    oyf = value_to_pixel(-1,1, 0.0, parameters.pixmax, yf)
    oyf += parameters.translatey
    oxg = value_to_pixel(-1,1, 0.0, parameters.pixmax, xg)
    oxg += parameters.translatex
    oyg = value_to_pixel(-1,1, 0.0, parameters.pixmax, yg)
    oyg += parameters.translatey
    
    
    outval = ''
    outval += 'M ' + str(oxz) + ' ' + str(oyz) + ' '
    outval += 'L ' + str(oxa) + ' ' + str(oya) + ' '
    outval += 'C ' + str(oxb) + ' ' + str(oyb) + ', '
    outval += str(oxc) + ' ' + str(oyc) + ', '
    outval += str(oxd) + ' ' + str(oyd) + ' '
    outval += 'C ' + str(oxe) + ' ' + str(oye) + ', '
    outval += str(oxf) + ' ' + str(oyf) + ', '
    outval += str(oxg) + ' ' + str(oyg) + ' '
    outval += 'L ' + str(oxz) + ' ' + str(oyz) + ' '
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PATH_D]] = outval

    s = '<'
            
    s += 'path'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="fill:rgb(%d,%d,%d);stroke:rgb(%d,%d,%d);"' % (randint(100,255),randint(100,255),randint(100,255),
                                                               randint(100,255),randint(100,255),randint(100,255))
    #s += 'fill="transparent" style="stroke:rgb(%d,%d,%d);"' % (randint(100,255), randint(100,255), randint(100,255))
    s += '>'
        
    s += '</'
    s += 'path'
    s += '>'
    
    return s


def set_geometry_unitcircle_TEXT(parameters, x, y, anchor):
    
    r = {}
    
    x = x * 1.1
    y = y * 1.1
    
    # TEXT_X
    #if self.cell_type == defines_for_cell.TEXT_X:
    outval = value_to_pixel(-1,1, 0.0, parameters.pixmax, x)
    outval += parameters.translatex
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_X]] = outval
    #self.save(update_fields=['value'])    
    
    # TEXT_Y    
    #elif self.cell_type == defines_for_cell.TEXT_Y:
    outval = value_to_pixel(-1,1, 0.0, parameters.pixmax, y)
    outval += parameters.translatey
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_Y]] = outval
    #self.save(update_fields=['value'])

    # TEXTANCHOR    
    #elif self.cell_type == defines_for_cell.TEXT_TEXTANCHOR:
    outval = defines_for_datavalues.ANCHOR_TYPE_SVG_DICT[anchor]
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_TEXTANCHOR]] = outval
    #self.save(update_fields=['value'])
    

    s = '<'
            
    s += 'text'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(parameters.datavalue)
    
    s += '</'
    s += 'text'
    s += '>'


    #print(s)
    
    return s

def set_geometry_unitcircle_LINE(parameters, xa, ya, xb, yb):
    
    r = {}
    
    outval = value_to_pixel(-1,1,
                            0, parameters.pixmax,
                            xa)
    outval += parameters.translatex
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval

    outval = value_to_pixel(-1,1,
                            0, parameters.pixmax,
                            ya)
    outval += parameters.translatey
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval

    outval = value_to_pixel(-1,1,
                            0, parameters.pixmax,
                            xb)
    outval += parameters.translatex

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval

    outval = value_to_pixel(-1,1,
                            0, parameters.pixmax,
                            yb)
    outval += parameters.translatey
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval

    s = '<'
            
    s += 'line'

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
    s += 'line'
    s += '>'
    
    return s


def set_geometry_arbitrary_LINE(parameters, xa, ya, xb, yb):
    
    r = {}
    
    #LINE_X1
    outval = value_to_pixel(0.0,parameters.canvaswidth,
                            0, parameters.canvaswidth,
                            xa)
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval

    #LINE_Y1
    outval = value_to_pixel(0.0,parameters.canvasheight,
                            0, parameters.canvasheight,
                            ya)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval

    #LINE_X2
    outval = value_to_pixel(0.0,parameters.canvaswidth,
                            0, parameters.canvaswidth,
                            xb)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval

    #LINE_Y2
    outval = value_to_pixel(0.0,parameters.canvasheight,
                            0, parameters.canvasheight,
                            yb)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval

    s = '<'
            
    s += 'line'

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
    s += 'line'
    s += '>'
    
    return s


def set_geometry_PIEDEBUGLINE(parameters, x, y):
    
    r = {}
    
    outval = value_to_pixel(-1,1,
                            parameters.pixmin_x, parameters.pixmax_x,
                            0)
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval

    outval = value_to_pixel(-1,1,
                            parameters.pixmin_x, parameters.pixmax_x,
                            0)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval

    outval = value_to_pixel(-1,1,
                            parameters.pixmin_x, parameters.pixmax_x,
                            x)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval

    outval = value_to_pixel(-1,1,
                            parameters.pixmin_x, parameters.pixmax_x,
                            y)

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval

    s = '<'
            
    s += 'line'

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
    s += 'line'
    s += '>'
    
    return s



def set_geometry_PIEDEBUGCIRC(parameters, x, y):
    
    r = {}
    
    #pair[0] pair[1]
    #columnindexpair[0] columnindexpair[1]
    #caxismarkslocation

    # PLOTCIRC_CX
    #if self.cell_type == defines_for_cell.PLOTCIRC_CX:

    outval = value_to_pixel(-1, 1, # sin and cos range is -1 to 1
                            parameters.pixmin_x, parameters.pixmax_x, 
                            #pixmin, pixmax,
                            x)
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_CX]] = outval
    #self.save(update_fields=['value'])    
    
    
    # PLOTCIRC_CY    
    #elif self.cell_type == defines_for_cell.PLOTCIRC_CY:
    
    
        
    outval = value_to_pixel(-1, 1, 
                            parameters.pixmin_y, parameters.pixmax_y, 
                            #pixmin, pixmax,
                            y)
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_CY]] = outval
    #self.save(update_fields=['value'])
        
    # PLOTCIRC_R
    #elif self.cell_type == defines_for_cell.PLOTCIRC_R

    outval = parameters.size
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_R]] = outval
    #self.save(update_fields=['value'])
    

    s = '<'
            
    s += 'circle'

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
    s += 'circle'
    s += '>'

    return s


def set_geometry_debug_margin_squares(parameters, side):
    
    r = {}

    if side == 'top':
    
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = 0.0       
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = 0.0
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = parameters.margintop
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = parameters.canvaswidth
        
    elif side == 'bottom':
        outval = 0.0
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = outval
        outval = parameters.canvasheight - parameters.marginbottom 
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = outval
        outval = parameters.marginbottom
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = outval
        outval = parameters.canvaswidth
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = outval

    elif side == 'left':
        
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = 0.0        
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = 0.0
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = parameters.canvasheight
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = parameters.marginleft

    elif side == 'right':
        
        outval = parameters.canvaswidth - parameters.marginright
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = outval
        outval = 0.0        
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = outval
        outval = parameters.canvasheight
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = outval
        outval = parameters.marginright
        r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = outval


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
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
        
    s += '</'
    s += 'rect'
    s += '>'

    return s    

def set_geometry_PLOTCIRC(parameters, var):
    
    r = {}
    
    #pair[0] pair[1]
    #columnindexpair[0] columnindexpair[1]
    #caxismarkslocation

    outval = None

    # PLOTCIRC_CX
    #if self.cell_type == defines_for_cell.PLOTCIRC_CX:

    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
            outval = parameters.caxismarkslocation[parameters.columnindexpair[var]]
        elif parameters.orientation == defines_for_datavalues.ROW_WISE:
            outval = parameters.caxismarkslocation[parameters.rowindexpair[var]]
                
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.pair[var])
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_CX]] = outval
    #self.save(update_fields=['value'])    
    
    
    # PLOTCIRC_CY    
    #elif self.cell_type == defines_for_cell.PLOTCIRC_CY:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:    
        
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_y, parameters.pixmax_y, 
                                    parameters.pair[var])
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
            outval = parameters.caxismarkslocation[parameters.columnindexpair[var]]
        elif parameters.orientation == defines_for_datavalues.ROW_WISE:
            outval = parameters.caxismarkslocation[parameters.rowindexpair[var]]
        
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_CY]] = outval
    #self.save(update_fields=['value'])
        
    # PLOTCIRC_R
    #elif self.cell_type == defines_for_cell.PLOTCIRC_R

    outval = parameters.size
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTCIRC_R]] = outval
    #self.save(update_fields=['value'])
    

    s = '<'
            
    s += 'circle'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
        
    s += '</'
    s += 'circle'
    s += '>'

    return s
    
def set_geometry_PLOTRECT(parameters, var):
    
    r = {}
    
    #pair[0] pair[1]
    #columnindexpair[0] columnindexpair[1]
    #caxismarkslocation

    outval = None

    # PLOTRECT_X
    #if self.cell_type == defines_for_cell.PLOTRECT_X:

    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
            
        outval = parameters.caxismarkslocation[parameters.indexpair[var]]
        
        outval -= parameters.size / 2.0
                
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.pair[var])
        outval -= parameters.size / 2.0
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_X]] = outval
    #self.save(update_fields=['value'])    
    
    
    # PLOTRECT_Y    
    #elif self.cell_type == defines_for_cell.PLOTRECT_Y:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:    
        
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_y, parameters.pixmax_y, 
                                    parameters.pair[var])
        outval -= parameters.size / 2.0
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        outval = parameters.caxismarkslocation[parameters.indexpair[var]]
        outval -= parameters.size / 2.0
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_Y]] = outval
    #self.save(update_fields=['value'])
    
    # PLOTRECT_H
    #elif self.cell_type == defines_for_cell.PLOTRECT_H
    outval = parameters.size
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_H]] = outval
    #self.save(update_fields=['value'])
    
    # PLOTRECT_W
    #elif self.cell_type == defines_for_cell.PLOTRECT_W
    outval = parameters.size
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.PLOTRECT_W]] = outval
    #self.save(update_fields=['value'])    

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
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
        
    s += '</'
    s += 'rect'
    s += '>'

    return s

def set_geometry_PLOTSTAR(parameters):
    
    pass

def set_geometry_PLOTDIAMOND(parameters):
    
    pass

def set_geometry_GRIDX(parameters, var):
    r = {}
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    outval = var            
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    outval = parameters.canvasheight - parameters.margintop
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = parameters.marginbottom        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'


    #print(s)
    
    return s


def set_geometry_GRIDY(parameters, var):
    r = {}
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    outval = parameters.canvaswidth - parameters.marginright
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = parameters.marginleft
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'

    return s


def set_geometry_TEXTX_top(parameters, var, tvar):
    
    r = {}
    outval = None
    
    # TEXT_X
    #if self.cell_type == defines_for_cell.TEXT_X:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_X]] = outval
    #self.save(update_fields=['value'])    
    
    # TEXT_Y    
    #elif self.cell_type == defines_for_cell.TEXT_Y:
    #half = (parameters.canvasheight - (parameters.canvasheight - parameters.marginbottom)) / 2
    half = parameters.marginbottom / 2
    outval = parameters.canvasheight - half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_Y]] = outval
    #self.save(update_fields=['value'])


    s = '<'
            
    s += 'text'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(tvar)
    
    s += '</'
    s += 'text'
    s += '>'


    #print(s)
    
    return s


def set_geometry_TEXTX_bottom(parameters, var, tvar):
    
    r = {}
    outval = None
    
    # TEXT_X
    #if self.cell_type == defines_for_cell.TEXT_X:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_X]] = outval
    #self.save(update_fields=['value'])    
    
    # TEXT_Y    
    #elif self.cell_type == defines_for_cell.TEXT_Y:
    half = parameters.marginbottom / 2
    outval = half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_Y]] = outval
    #self.save(update_fields=['value'])


    s = '<'
            
    s += 'text'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(tvar)
    
    s += '</'
    s += 'text'
    s += '>'


    #print(s)
    
    return s


def set_geometry_TEXTY_right(parameters, var, tvar):
    
    r = {}
    outval = None
    
    # TEXT_X
    #if self.cell_type == defines_for_cell.TEXT_X:
    #half = (parameters.canvaswidth - (parameters.canvaswidth - parameters.marginright)) / 2
    half = parameters.marginright / 2
    outval = parameters.canvaswidth - half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_X]] = outval
    #self.save(update_fields=['value'])    
    
    # TEXT_Y    
    #elif self.cell_type == defines_for_cell.TEXT_Y:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_Y]] = outval
    #self.save(update_fields=['value'])


    s = '<'
            
    s += 'text'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(tvar)
    
    s += '</'
    s += 'text'
    s += '>'


    #print(s)
    
    return s

def set_geometry_TEXTY_left(parameters, var, tvar):
    
    r = {}
    outval = None
    
    # TEXT_X
    #if self.cell_type == defines_for_cell.TEXT_X:
    half = parameters.marginleft / 2
    outval = half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_X]] = outval
    #self.save(update_fields=['value'])    
    
    # TEXT_Y    
    #elif self.cell_type == defines_for_cell.TEXT_Y:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.TEXT_Y]] = outval
    #self.save(update_fields=['value'])


    s = '<'
            
    s += 'text'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(tvar)
    
    s += '</'
    s += 'text'
    s += '>'


    #print(s)
    
    return s


def set_geometry_MARKX_top(parameters, var):
    r = {}
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    outval = var            
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    half = parameters.margintop / 2
    outval = parameters.canvasheight - half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = parameters.canvasheight        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'


    #print(s)
    
    return s

def set_geometry_MARKX_bottom(parameters, var):
    r = {}
    
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    outval = var            
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    half = parameters.marginbottom / 2
    outval = half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = 0
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'


    #print(s)
    
    return s

def set_geometry_MARKY_right(parameters, var):
    r = {}
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    half = parameters.marginright / 2
    outval = parameters.canvaswidth - half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = parameters.canvaswidth
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'

    return s


def set_geometry_MARKY_left(parameters, var):
    r = {}
    outval = None
    
    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    half = parameters.marginleft / 2
    outval = half
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    outval = 0
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    outval = var
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])

    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    #s += str(parameters.pair[0])
    #s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'


    #print(s)
    
    return s

# NYI def set_geometry_MARKY_zero(parameters, var):

def set_geometry_RECT(parameters):
    
    r = {}
    
    outval = None
    a = b = None
    
    # RECT_X
    #if self.cell_type == defines_for_cell.RECT_X:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
            outval = parameters.caxismarkslocation[parameters.columnindex]
            outval -= parameters.size / 2
        elif parameters.orientation == defines_for_datavalues.ROW_WISE:
            outval = parameters.caxismarkslocation[parameters.rowindex]
            outval -= parameters.size / 2            
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:

        if parameters.sign >= 0:
            outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                        parameters.pixmin_x, parameters.pixmax_x, 
                                        parameters.runningtotal)

        elif parameters.sign < 0:
            outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                        parameters.pixmin_x, parameters.pixmax_x, 
                                        parameters.runningtotal + parameters.datavalue)
                
        #print('runningtotal:' + str(parameters.runningtotal) + '  outval:' + str(outval))
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_X]] = outval
    #self.save(update_fields=['value'])    
    
    
    # RECT_Y    
    #elif self.cell_type == defines_for_cell.RECT_Y:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:    
        
        if parameters.sign >= 0:
            outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                        parameters.pixmin_y, parameters.pixmax_y, 
                                        parameters.runningtotal)
            
        elif parameters.sign < 0:
            outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                        parameters.pixmin_y, parameters.pixmax_y, 
                                        parameters.runningtotal + parameters.datavalue)
            
        #print('runningtotal:' + str(parameters.runningtotal) + '  outval:' + str(outval))
        
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
            outval = parameters.caxismarkslocation[parameters.columnindex]
            outval -= parameters.size / 2
        elif parameters.orientation == defines_for_datavalues.ROW_WISE:
            outval = parameters.caxismarkslocation[parameters.rowindex]
            outval -= parameters.size / 2            
                
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_Y]] = outval
    #self.save(update_fields=['value'])
        
    # RECT_H
    #elif self.cell_type == defines_for_cell.RECT_H:
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        
            
        a = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_y, parameters.pixmax_y, 
                                    parameters.runningtotal)

        b = value_to_pixel(parameters.magmin, parameters.magmax, 
                           parameters.pixmin_y, parameters.pixmax_y, 
                           parameters.runningtotal + parameters.datavalue)

        if parameters.sign >= 0: outval = b - a
        elif parameters.sign < 0: outval = a - b
        #outval = 5.0
    
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        outval = parameters.size
    
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_H]] = outval
    #self.save(update_fields=['value'])

    # RECT_W
    #elif self.cell_type == defines_for_cell.RECT_W:
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        outval = parameters.size
    
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        a = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.runningtotal)
        
        b = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.runningtotal + parameters.datavalue)

        if parameters.sign >= 0: outval = b - a
        elif parameters.sign < 0: outval = a - b
        #outval = 5.0

    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_W]] = outval
    #self.save(update_fields=['value'])

    # RECT_RX
    #elif self.cell_type == defines_for_cell.RECT_RX:
    outval = 0.5
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_RX]] = outval
    #self.save(update_fields=['value'])
        
    # RECT_RY
    #elif self.cell_type == defines_for_cell.RECT_RY:
    outval = 0.5
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.RECT_RY]] = outval
    #self.save(update_fields=['value'])        

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
    s += 'style="fill:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(parameters.datavalue)
    
    s += '</'
    s += 'rect'
    s += '>'


    #print(s)
    
    return s



def set_geometry_LINE(parameters):

    r = {}
    
    outval = None

    # LINE_X1 = 'lx1'
    #if self.cell_type == defines_for_cell.LINE_X1:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        
        outval = parameters.caxismarkslocation[parameters.indexpair[0]]
                
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:

        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.pair[0])
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X1]] = outval
    #self.save(update_fields=['value'])    
    
    
    # LINE_Y1 = 'ly1'    
    #elif self.cell_type == defines_for_cell.LINE_Y1:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:    
        
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_y, parameters.pixmax_y, 
                                    parameters.pair[0])
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
        
        outval = parameters.caxismarkslocation[parameters.indexpair[0]]        
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y1]] = outval
    #self.save(update_fields=['value'])
        
    # LINE_X2 = 'lx2'
    #if self.cell_type == defines_for_cell.LINE_X2:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
        
        outval = parameters.caxismarkslocation[parameters.indexpair[1]]        
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:

        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_x, parameters.pixmax_x, 
                                    parameters.pair[1])
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_X2]] = outval
    #self.save(update_fields=['value'])    
    
    
    # LINE_Y2 = 'ly2' 
    #elif self.cell_type == defines_for_cell.LINE_Y2:
    
    if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:    
        
        outval = value_to_pixel(parameters.magmin, parameters.magmax, 
                                    parameters.pixmin_y, parameters.pixmax_y, 
                                    parameters.pair[1])
        
    elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:

        outval = parameters.caxismarkslocation[parameters.indexpair[1]]        
        
    r[defines_for_cell.CELL_TYPE_SVG_DICT[defines_for_cell.LINE_Y2]] = outval
    #self.save(update_fields=['value'])


    s = '<'
            
    s += 'line'

    for item in r:
        
        s += ' '
        s += item
        s += '='
        s += '"'
        s += str(r[item])
        s += '"'

    s += ' '
    s += 'style="stroke:rgb(%d,%d,%d);"' % (randint(0,255), randint(0,255), randint(0,255))
    s += '>'
    
    s += str(parameters.pair[0])
    s += str(parameters.pair[1])
    
    s += '</'
    s += 'line'
    s += '>'


    # # # # print(r)

    #print(s)
    
    return s



    
    
# calculates a pie chart with svg paths for a set of cells, modifies parameters.datavalue  
def pie_values_loop(parameters, cell_lst_to_set):

    # control points reference: http://math.stackexchange.com/questions/873224/calculate-control-points-of-cubic-bezier-curve-approximating-a-part-of-a-circle?rq=1

    lst = []

    runningtotal = 0 # values from 0 to 3.14 represent position on circle

    listsum = float(sum(cell_lst_to_set))

    for cell_to_set in cell_lst_to_set:

        percentofpi = pi * (cell_to_set / listsum)

        parameters.datavalue = cell_to_set
        
        angle_a = runningtotal
        angle_b = runningtotal + percentofpi
        
        # plotpoints on unit circle
        xa = cos(2 * angle_a)
        ya = sin(2 * angle_a)
        xb = cos(2 * (angle_b))
        yb = sin(2 * (angle_b))

        # half angle, midpoint, tick mark
        varc = (angle_b - angle_a) / 2.0
        angle_c = angle_a + varc                        
        xt = cos(2 * angle_c)
        yt = sin(2 * angle_c) 
        lst.append(set_geometry_unitcircle_LINE(parameters, 
                                                xt*1.05, yt*1.05,
                                                xt*1.1, yt*1.1))
        
        # control points for bezier
        
        # handles the case where angle between two plots > pi by creating adding controlpoints at midpoint
        if(angle_b - angle_a > pi / 2.0):
            controlptalphaa = acos((ya * yt + xa * xt))
            controlptalphab = acos((yt * yb + xt * xb))
        
            controlptalphaa = 0.25 * controlptalphaa
            controlptalphaa = tan(controlptalphaa)
            controlptalphaa = (4.0/3.0) * controlptalphaa
            
            controlptalphab = 0.25 * controlptalphab
            controlptalphab = tan(controlptalphab)
            controlptalphab = (4.0/3.0) * controlptalphab
            
            xcta = xa + controlptalphaa * - ya
            ycta = ya + controlptalphaa * xa
            
            xctb = xt - controlptalphaa * - yt
            yctb = yt - controlptalphaa * xt
            
            xctc = xt + controlptalphaa * - yt
            yctc = yt + controlptalphaa * xt

            xctd = xb - controlptalphaa * - yb
            yctd = yb - controlptalphaa * xb

            lst.append(set_geometry_unitcircle_seven_point_BEZIER(parameters, 
                                                                  xa, ya, 
                                                                  xcta, ycta, 
                                                                  xctb, yctb,
                                                                  xt, yt,
                                                                  xctc, yctc,
                                                                  xctd, yctd, 
                                                                  xb, yb))
            
        else:
            controlptalpha = acos((ya * yb + xa * xb))
            controlptalpha = 0.25 * controlptalpha
            controlptalpha = tan(controlptalpha)
            controlptalpha = (4.0/3.0) * controlptalpha
            xa_prime = xa + controlptalpha * - ya
            ya_prime = ya + controlptalpha * xa

            xb_prime = xb - controlptalpha * -yb
            yb_prime = yb - controlptalpha * xb

            lst.append(set_geometry_unitcircle_BEZIER(parameters, 
                                                      xa, ya, 
                                                      xa_prime, ya_prime, 
                                                      xb_prime, yb_prime, 
                                                      xb, yb))
        
        # labels
        anchor = None
        if angle_c >= 0 and angle_c < 2 * pi / 3: # between 0 and PI/3 
            anchor = defines_for_datavalues.ANCHOR_START
        elif angle_c >= pi / 3 and angle_c < 2 * pi / 3: # between PI/3 and 2PI/3
            anchor = defines_for_datavalues.ANCHOR_MIDDLE
        elif angle_c >= 2 * pi / 3 and angle_c < 4 * pi / 3: # between 2PI/3 and 4PI/3
            anchor = defines_for_datavalues.ANCHOR_END
        elif angle_c >= 4 * pi / 3 and angle_c < 5 * pi / 3: # between 4PI/3 and 5PI/3
            anchor = defines_for_datavalues.ANCHOR_MIDDLE
        elif angle_c >= 5 * pi / 3 and angle_c < 2 * pi: # between 5PI/3 and 2PI
            anchor = defines_for_datavalues.ANCHOR_START
            
        lst.append(set_geometry_unitcircle_TEXT(parameters, xt, yt, anchor))
                
        runningtotal += percentofpi

    return lst

# creates svg strings for a pie chart, modifies parameters.translatex, parameters.translatey, parameters.pixmax
def set_childtables_values_PIE(table, parameters):
    
    lst = []
    
    orientsize = None # number or columns or number of rows depending on ROW_WISE or COLUMN_WISE
    
    if TABLE_AS_DATAFRAME == True:
        if parameters.orientation == defines_for_datavalues.ROW_WISE: orientsize = table.df.columns.size
        elif parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.df.index.size
    else:
        if parameters.orientation == defines_for_datavalues.ROW_WISE: orientsize = table.size_column()
        elif parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.size_row()
 
    orientsums = [] # list of sums of entire column or row
    
    # root geometrymanager frame
    g = area(height=parameters.canvasheight, width=parameters.canvaswidth, 
             aligny='center', alignx='center',
             padhorizontal=max(parameters.marginleft,parameters.marginright), 
             padvertical=max(parameters.margintop,parameters.marginbottom),
             growy = True, fill = True)
    gsplittop = gsplitbottom = None
    glst = [] # lst of geometrymanager frames
    
    # if there is more than one row or column split the frame and calculate frames for orientsums
    if orientsize > 1:
        
        # split frame bottom
        gsplitbottom = area(aligny='center', alignx='center',
                         padhorizontal=10, 
                         padvertical=10)
        g.push(gsplitbottom)
    
        gsplitbottomc = area(aligny='center', alignx='center',
                         padhorizontal=10, 
                         padvertical=10)
        gsplitbottom.push(gsplitbottomc)

        # split frame top
        gsplittop = area(aligny='center', alignx='center',
                         padhorizontal=10, 
                         padvertical=10, growy=True, fill=True)
        g.push(gsplittop)
        
        # split frame top children
        gperrow = 4 # TODO: designates how many pie charts should each row frame hold
        gnumrows = int(ceil(float(orientsize) / float(gperrow))) # calculates number of row frames
        
        # add rows in splittop frame
        for _ in range(0, gnumrows):
            tempg = area(aligny='center', alignx='center', padhorizontal=1, padvertical=1, 
                         growx=True, fill=True)
            gsplittop.push(tempg)
            
            # add two frames in rowframe, add this frame to the glst, used to receive coords to render charts 
            for __ in range(0, gperrow):
                
                tg = area(aligny='center', alignx='center', padhorizontal=1, padvertical=1)
                tempg.push(tg)
                
                # add a second frame to escape the fill=True and growx=True property and get a square of full size
                tgs = area(aligny='center', alignx='center', padhorizontal=1, padvertical=1)
                tg.push(tgs)
                
                # append the frame to a list so we can use it to get the dimensions for the chart
                glst.append(tgs)
        
    ix = 0 # index, rowindex or columnindex
    
    iterset = None # set of values iterated based on orientation:(COLUMN_WISE,ROW_WISE) or source(TABLE_AS_DATAFRAME)
    if TABLE_AS_DATAFRAME: 
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: iterset = table.df.iterrows()
        else: iterset = table.df.iteritems()
    else: 
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: iterset = table.childrows.all()
        else: iterset = table.childcolumns.all()
    
    for i in iterset:    
        cell_lst_to_set = [] # for each row or column store the row or column's value in a list
        
        if TABLE_AS_DATAFRAME == True:
            for c in i[1]:
                if c < 0.0: # if value is less than 0.0 throw an exception
                    raise ValueError('Unable to plot negative values for pie chart.')    
                if c != 0.0: cell_lst_to_set.append(c) # if value is 0.0 don't include it in the list
        else:
            for c in i.childcells.all():
                if c.data_float_var < 0.0: # if value is less than 0.0 throw an exception
                    raise ValueError('Unable to plot negative values for pie chart.')    
                if c != 0.0: cell_lst_to_set.append(c.data_float_var) # if value is 0.0 don't include it in list

        if orientsize > 1:# display the row/col as a separate chart inside child geomgr frame 
            parameters.translatex = glst[ix].ileft()
            parameters.translatey = glst[ix].itop()
            parameters.pixmax = glst[ix].isd()
            for s in pie_values_loop(parameters, cell_lst_to_set): # iterate through lst of str's with svg
                lst.append(s)
            orientsums.append(sum(cell_lst_to_set)) # append the sum of the row to the orientsum and display at end
            cell_lst_to_set = [] # reset the lst of cells in preparation for the next loop
        ix += 1 # add one to row/col index
    if orientsize == 1: # if there is only one row or column display it using the root frame
        parameters.translatex = g.ileft()
        parameters.translatey = g.itop()
        parameters.pixmax = g.isd()
        for s in pie_values_loop(parameters, cell_lst_to_set):
            lst.append(s)
    elif orientsize > 1: # outside of the row/col loop display a orientsum chart using a bottom geomgr split frame
        parameters.translatex = gsplitbottomc.ileft()
        parameters.translatey = gsplitbottomc.itop()
        parameters.pixmax = gsplitbottomc.isd()
        for s in pie_values_loop(parameters, orientsums):
            lst.append(s)    
        
    return lst # returns lists of strings containing svg tags



# creates svg strs for stackedbar. modifies parameters.(runningtotal, sign, datavalue, size, columnindex, rowindex)
def set_childtables_values_STACKEDBAR(table, parameters):

    lst = [] # return list holds the svg strings
    
    orientsize = None # number of columns or number of rows depending on COLUMN_WISE or ROW_WISE
    
    # assigns the orientsize
    if TABLE_AS_DATAFRAME == True:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.df.index.size
        else: orientsize = table.df.columns.size
    else:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.size_row()
        else: orientsize = table.size_column()
            
    if TABLE_AS_DATAFRAME == True: # if we are not using the database
        
        ix = 0 # row or column index being iterated
        parameters.sign = None # set per row/column describes the sign of row or column
        iterset = None # set of rows or columns being iterated
        
        # assigns the iterset
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: iterset = table.df.iteritems() 
        else: iterset = table.df.iterrows()
        
        # iterate through rows or columns, using a list set the geometry for the row/column append it to return lst
        for i in iterset:
            
            cell_lst_to_set = [] # contains the cells of the row or column
            
            # assign parameters.sign and check for error, append cell to list of cells
            for c in i[1]:
                if parameters.sign == None:
                    if c > 0: parameters.sign = 1
                    elif c < 0: parameters.sign = -1
                    else: parameters.sign = None
                if (parameters.sign != None) and ((parameters.sign > 0 and c < 0) or 
                                                  (parameters.sign < 0 and c > 0)):
                    if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
                        raise ValueError('All numbers in column must be either negative or positive.')
                    else: raise ValueError('All numbers in row must be either negative or positive.')

                cell_lst_to_set.append(c) # append the cell to list of cells
                            
            parameters.runningtotal = 0.0 # prepare running total, all stacked bar start at 0

            for cell_to_set in cell_lst_to_set: # iterate through list of cells,
                # in preparation for setting geometry assign the parameter index to the current row/column index
                if parameters.orientation == defines_for_datavalues.COLUMN_WISE: parameters.columnindex = ix
                else: parameters.rowindex = ix
                
                parameters.datavalue = cell_to_set # prepare to set geometry, assign the datavalue to the cell
                parameters.size = 50.0 # TODO: size determines how wide the bar should be
                lst.append(set_geometry_RECT(parameters)) # append the svg string representing the cell
                parameters.runningtotal += cell_to_set # increase the running total in prep for next cell
                
            parameters.sign = None # reset the sign value in preparation for next column / row
            cell_lst_to_set = [] # empty the cell list
            ix += 1 # increment the index row/column counter

    else: # if we are using the database
        setofcells = None # ordered set of cells being used to create the chart
        # assign an ordered queryset to setofcells based on orientation  
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
            setofcells = table.childcells.all().order_by('parentrow__index').order_by('parentcolumn__index')
        else:
            setofcells = table.childcells.all().order_by('parentcolumn__index').order_by('parentrow__index')
        count = 1 # index into setofcells, resets after row or column
        cell_lst_to_set = [] # set of cells in a row or column, resets after row or column
        for cell in setofcells: # iterate through all table cells
            if parameters.sign == None:
                # keep track of sign and raise an error if column or row has mixed sign values
                if cell.data_float_var > 0: parameters.sign = 1
                elif cell.data_float_var < 0: parameters.sign = -1
                else: parameters.sign = None
            if (parameters.sign != None) and ((parameters.sign > 0 and cell.data_float_var < 0) or 
                                              (parameters.sign < 0 and cell.data_float_var > 0)):
                if parameters.orientation == defines_for_datavalues.COLUMN_WISE:
                    raise ValueError('All numbers in column must be either negative or positive.')
                else: raise ValueError('All numbers in row must be either negative or positive.')

            cell_lst_to_set.append(cell) # append the cell to the list of cells for the row or column

            if count >= orientsize: # if we are at the end of the row or column reset values and set geometry
                parameters.runningtotal = 0.0 # all stacked bar start at 0, the x or y axis
                for cell_to_set in cell_lst_to_set: # iterate the cell list
                    cell_to_set.set_geometry_for_cell(parameters) # set geometry
                    parameters.runningtotal += cell_to_set.data_float_var # increase running total

                parameters.sign = None # reset sign in preparation for next row or column
                count = 0 # reset count 
                cell_lst_to_set = [] # reset cell list
                
            count += 1 # increment count to keep track of column or row index 

    # set marks and text and grid for graph based on originaxis    
    count = 0
    for m in parameters.caxismarkslocation: # iterate the category axis marks location
        if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
            lst.append(set_geometry_MARKX_top(parameters, m))
            lst.append(set_geometry_MARKX_bottom(parameters, m))
            lst.append(set_geometry_TEXTX_top(parameters, m, count))
            lst.append(set_geometry_TEXTX_bottom(parameters, m, count))
            lst.append(set_geometry_GRIDX(parameters, m))
        elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
            lst.append(set_geometry_MARKY_left(parameters, m))
            lst.append(set_geometry_MARKY_right(parameters, m))
            lst.append(set_geometry_TEXTY_left(parameters, m, count))
            lst.append(set_geometry_TEXTY_right(parameters, m, count))            
            lst.append(set_geometry_GRIDY(parameters, m))
        count += 1
  
    # set marks and text and grid for graph based on originaxis
    count = 0
    for m in parameters.vaxismarkslocation: # iterate the value axis marks location
        if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
            lst.append(set_geometry_MARKY_right(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_MARKY_left(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_TEXTY_left(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_TEXTY_right(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_GRIDY(parameters, parameters.vaxismarkslocation[count]))
        elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
            lst.append(set_geometry_MARKX_top(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_MARKX_bottom(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_TEXTX_top(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_TEXTX_bottom(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_GRIDX(parameters, parameters.vaxismarkslocation[count]))
        count += 1
    
    return lst

# assigns values for line graph, returns a list of svg strings, modifies parameters.pair and parameters.indexpair
def set_childtables_values_LINE(table, parameters):
    lst = [] # lst storing svg str values returned by method
    
    orientsize = None # number of columns or number of rows depending on COLUMN_WISE or ROW_WISE
    
    # assigns the orientsize
    if TABLE_AS_DATAFRAME == True:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.df.index.size
        else: orientsize = table.df.columns.size
    else:
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: orientsize = table.size_row()
        else: orientsize = table.size_column()

    if TABLE_AS_DATAFRAME == True:
        
        iterset = None # set of rows or columns being iterated
        
        # assigns the iterset
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: iterset = table.df.iterrows() 
        else: iterset = table.df.iteritems()
        
        for i in iterset: # iterate the rows or columns in the table
            cell_lst_to_set = [] # set of cells in the row or column
            for c in i[1]: # iterate the row appending cells to the row/column set
                cell_lst_to_set.append(c)
            parameters.pair = [None, None] # prepare a pair for the endpoints of a line
            parameters.indexpair = [None, None] # prepare a pair for the category index of a line
            for cell_to_set in cell_lst_to_set: # iterate through the set of cells
                if parameters.pair[0] == None and parameters.pair[1] == None: # if this cell is first in row/col
                    parameters.pair[0] = cell_to_set
                    parameters.indexpair[0] = 0
                elif parameters.pair[0] != None and parameters.pair[1] == None: # all other cells, next if shifts
                    parameters.pair[1] = cell_to_set # set the second pair pair[1] to currently iterated cell
                    parameters.indexpair[1] = parameters.indexpair[0] + 1 # set pair[1] index to +1 pair[0]
                if parameters.pair[0] != None and parameters.pair[1] != None: # if both pairs are not none
                    lst.append(set_geometry_LINE(parameters)) # draw the line with the two pairs
                    parameters.size = 15 # TODO: size of plotpoint
                    lst.append(set_geometry_PLOTRECT(parameters,0)) # draw the first plot point
                    if cell_to_set == cell_lst_to_set[len(cell_lst_to_set)-1]: # if we are at the last cell/plot
                        lst.append(set_geometry_PLOTRECT(parameters,1)) # draw the second plotpoint
                    parameters.pair[0] = parameters.pair[1] # shift pair[1] to [0]
                    parameters.pair[1] = None
                    parameters.indexpair[0] = parameters.indexpair[1] # shift pair[1] to [0]
                    parameters.indexpair[1] = None
            cell_lst_to_set = [] # after iteration of row/column empty the cell_lst_to_set

    else:
        iterset = None # set of rows or columns being iterated
        if parameters.orientation == defines_for_datavalues.COLUMN_WISE: 
            iterset = table.childcells.all().order_by('parentrow__index').order_by('parentcolumn__index')
        else:
            iterset = table.childcells.all().order_by('parentcolumn__index').order_by('parentrow__index')
        
        cell_lst_to_set = [] # holds cells for row or column
        count = 1 

        for cell in iterset:

            cell_lst_to_set.append(cell) # append the cell to the list
            
            if count == orientsize: # once a row or column has been added to lst
                parameters.pair = [None, None] # prepare a pair for the endpoints of a line
                parameters.indexpair = [None, None] # prepare a pair for the category index of a line
                for cell_to_set in cell_lst_to_set: # iterate through the set of cells
                    if parameters.pair[0] == None and parameters.pair[1] == None: # if this cell is first in row/col
                        parameters.pair[0] = cell_to_set
                        parameters.indexpair[0] = 0
                    elif parameters.pair[0] != None and parameters.pair[1] == None: # all other cells, next if shifts
                        parameters.pair[1] = cell_to_set # set the second pair pair[1] to currently iterated cell
                        parameters.indexpair[1] = parameters.indexpair[0] + 1 # set pair[1] index to +1 pair[0]
                    if parameters.pair[0] != None and parameters.pair[1] != None: # if both pairs are not none
                        lst.append(set_geometry_LINE(parameters)) # draw the line with the two pairs
                        parameters.size = 15 # TODO: size of plotpoint
                        lst.append(set_geometry_PLOTRECT(parameters,0)) # draw the first plot point
                        if cell_to_set == cell_lst_to_set[len(cell_lst_to_set)-1]: # if we are at the last cell/plot
                            lst.append(set_geometry_PLOTRECT(parameters,1)) # draw the second plotpoint
                        parameters.pair[0] = parameters.pair[1] # shift pair[1] to [0]
                        parameters.pair[1] = None
                        parameters.indexpair[0] = parameters.indexpair[1] # shift pair[1] to [0]
                        parameters.indexpair[1] = None
                cell_lst_to_set = [] # after iteration of row/column empty the cell_lst_to_set
                count = 1 # after iteration of row/column reset count to 1 in preparation for next row/column
            
            else: count += 1 # if not at the end of the row or column keep iterating

    # assign category axis marks, text and grid locations
    count = 0
    for m in parameters.caxismarkslocation:
        if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
            lst.append(set_geometry_MARKX_top(parameters, m))
            lst.append(set_geometry_MARKX_bottom(parameters, m))
            lst.append(set_geometry_TEXTX_top(parameters, m, count))
            lst.append(set_geometry_TEXTX_bottom(parameters, m, count))
            lst.append(set_geometry_GRIDX(parameters, m))
        elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
            lst.append(set_geometry_MARKY_left(parameters, m))
            lst.append(set_geometry_MARKY_right(parameters, m))
            lst.append(set_geometry_TEXTY_left(parameters, m, count))
            lst.append(set_geometry_TEXTY_right(parameters, m, count))            
            lst.append(set_geometry_GRIDY(parameters, m))
        count += 1
  
    # assign value axis marks, text and grid locations
    count = 0
    for m in parameters.vaxismarkslocation:
        if parameters.originaxis == defines_for_datavalues.HORIZONTAL_AXIS:
            lst.append(set_geometry_MARKY_right(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_MARKY_left(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_TEXTY_left(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_TEXTY_right(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_GRIDY(parameters, parameters.vaxismarkslocation[count]))
        elif parameters.originaxis == defines_for_datavalues.VERTICAL_AXIS:
            lst.append(set_geometry_MARKX_top(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_MARKX_bottom(parameters, parameters.vaxismarkslocation[count]))
            lst.append(set_geometry_TEXTX_top(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_TEXTX_bottom(parameters, 
                                              parameters.vaxismarkslocation[count], 
                                              parameters.magmarkslocation[count]))
            lst.append(set_geometry_GRIDX(parameters, parameters.vaxismarkslocation[count]))
        count += 1
    
    return lst

# sets values based on table_type
def set_childtables_values(table, parameters):

    if parameters.table_type == defines_for_table.TABLE_STACKEDBAR:
        return set_childtables_values_STACKEDBAR(table, parameters)
    
    elif parameters.table_type == defines_for_table.TABLE_LINE:
        return set_childtables_values_LINE(table, parameters)
    
    elif parameters.table_type == defines_for_table.TABLE_PIE:
        return set_childtables_values_PIE(table, parameters)




def runscratchpie(f, in_table_type):
    
    # BUG: bezier curve value for plots greater than PI is incorrect
    

    for v in [0,1,2,3]:
            
        sdict = {}
        
        if v == 0:
            for i in range(0,2):#range(0, 8):
                s = None
                s = pd.Series((randint(0,100)),[0])
                sdict[i] = s
                
        elif v == 1:
            for i in range(0, 1):
                s = None
                s = pd.Series((randint(0,100),randint(0,100),randint(0,100),randint(0,100),
                               randint(0,100),randint(0,100),randint(0,100),randint(0,100)), [0,1,2,3,4,5,6,7])
                sdict[i] = s
        
        elif v == 2 or v == 3:
            for i in range(0, 8):
                s = None
                #s = pd.Series((randint(0,100), randint(0,100), randint(0,100), randint(0,100),randint(0,100)), 
                #              [0,1,2,3,4])
                s = pd.Series((randint(0,100),randint(0,100),randint(0,100),randint(0,100),
                               randint(0,100),randint(0,100),randint(0,100),randint(0,100),), [0,1,2,3,4,5,6,7])
                sdict[i] = s

        df = pd.DataFrame(sdict)
        t = table()
        t.table_type = in_table_type
                    
        if v == 0 or v == 2: 
            table.datavalues_properties.orientation = defines_for_datavalues.COLUMN_WISE
        elif v == 1 or v == 3: 
            table.datavalues_properties.orientation = defines_for_datavalues.ROW_WISE
        
        t.df = df
        if SCRATCH_DEBUG_PRINT: print(t.df)
        p = calculate_parameters(t)
        if SCRATCH_DEBUG_PRINT: print(p)
                
        lst = [] 
        lst = set_childtables_values(t, p)
         
        f.write('<svg width="1000" height="1000">\n')
        f.write('<rect width="1000" height="1000" style="fill:rgb(14,17,14);"></rect>\n')
         
        for i in lst:
            f.write(i)
            f.write('\n')
        f.write('</svg><br>~<br>')
                 

    
    

def runscratch(f, in_table_type):

    
    
    
    for v in range(0,8):

        for d in range(0,2):
            
            sdict = {}
            for i in range(0, 8):
                s = None
    
                if d == 0:
    
                    if v == 0 or v == 2 or v == 4 or v == 6:
                        if i % 2 == 0:
                            s = pd.Series((randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100)), [0,1,2,3,4])
                        else:
                            s = pd.Series((randint(-100,0),randint(-100,0),randint(-100,0),randint(-100,0),randint(-100,0)),[0,1,2,3,4])                                
                    
                    elif v == 1 or v == 3 or v == 5 or v == 7:
                        s = pd.Series((randint(0,100),randint(-100,0),randint(0,100),randint(-100,0),randint(0,100)), [0,1,2,3,4])
                
                elif d == 1:
                    if v == 0 or v == 1 or v == 2 or v == 3:
                        s = pd.Series((randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100)), [0,1,2,3,4])
                    elif v == 4 or v == 5 or v == 6 or v == 7:
                        s = pd.Series((randint(-100,0),randint(-100,0),randint(-100,0),randint(-100,0),randint(-100,0)),[0,1,2,3,4])
                
                sdict[i] = s
    
            df = pd.DataFrame(sdict)
            t = table()
            t.table_type = in_table_type
            
            if v == 0 or v == 1 or v == 4 or v == 5: 
                table.datavalues_properties.originaxis = defines_for_datavalues.HORIZONTAL_AXIS
            elif v == 2 or v == 3 or v == 6 or v == 7: 
                table.datavalues_properties.originaxis = defines_for_datavalues.VERTICAL_AXIS
            
            if v == 0 or v == 2 or v == 4 or v == 6: 
                table.datavalues_properties.orientation = defines_for_datavalues.COLUMN_WISE
            elif v == 1 or v == 3 or v == 5 or v == 7: 
                table.datavalues_properties.orientation = defines_for_datavalues.ROW_WISE
            
            t.df = df
            p = calculate_parameters(t)
            if SCRATCH_DEBUG_PRINT: print(t.df)
            if SCRATCH_DEBUG_PRINT: print(p)
                         
            lst = set_childtables_values(t, p)
                          
            f.write('<svg width="1000" height="1000">\n')
            f.write('<rect width="1000" height="1000" style="fill:rgb(14,17,14);"></rect>\n')
             
            for i in lst:
                f.write(i)
                f.write('\n')
            f.write('</svg><br>~<br>')
                 
    

    
    

SCRATCH_DEBUG_PRINT = False
    
f = open('./brandon_tardio_python_coding_sample.html', 'w')
f.write('<html><head><title></title></head><body>\n')    

runscratchpie(f, defines_for_table.TABLE_PIE)
runscratch(f, defines_for_table.TABLE_LINE)
runscratch(f, defines_for_table.TABLE_STACKEDBAR)

f.write('</body></html>')

f.close()



