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

class defines_for_cell():
    
    #DATA_DATE = 'dd'
    #DATA_DATETIME = 'dt'
    #DATA_STRING = 'ds'    
    DATA_CHAR = 'dc'
    #DATA_BIGINTEGER = 'db'
    #DATA_INTEGER = 'di'
    #DATA_DECIMAL = 'dl'
    DATA_FLOAT = 'df'
    
    DATA_TYPE_CHOICES = (#(DATA_DATE, 'Date'),
                         #(DATA_DATETIME, 'Date and Time'),
                         (DATA_CHAR, 'Text String'),
                         #(DATA_STRING, 'Big Text String'),
                         #(DATA_INTEGER, 'Integer'),
                         #(DATA_BIGINTEGER, 'Big Integer'),
                         (DATA_FLOAT, 'Decimal'),
                         #(DATA_DECIMAL, 'Big Decimal'),
                         )
    
    # circle : cx cy r
    CIRC_CX = 'ccx'
    CIRC_CY = 'ccy'
    CIRC_R = 'cr'

    # ellipse : cx cy rx ry
    ELLI_CX = 'ecx'
    ELLI_CY = 'ecy'
    ELLI_RX = 'erx'
    ELLI_RY = 'ery'
        
    # transform : a b c d e f
    FORM_A = 'fa'
    FORM_B = 'fb'
    FORM_C = 'fc'
    FORM_D = 'fd'
    FORM_E = 'fe'
    FORM_F = 'ff'

    # polygon : points
    GON_POINTS = 'np'

    # grid : d pathLength
    GRID_D = 'Gd'
    GRID_PATHLENGTH = 'Gpl'

    # gridx : x1 x2 y1 y2
    GRIDX_X1 = 'gx1'
    GRIDX_Y1 = 'gy1'
    GRIDX_X2 = 'gx2'
    GRIDX_Y2 = 'gy2'

    # gridy : x1 x2 y1 y2
    GRIDY_X1 = 'ix1'
    GRIDY_Y1 = 'iy1'
    GRIDY_X2 = 'ix2'
    GRIDY_Y2 = 'iy2'

    # line : x1 x2 y1 y2
    LINE_X1 = 'lx1'
    LINE_Y1 = 'ly1'
    LINE_X2 = 'lx2'
    LINE_Y2 = 'ly2'

    # axis tick marks : x1 x2 y1 y2
    MARK_X1 = 'Mx1'
    MARK_Y1 = 'My1'
    MARK_X2 = 'Mx2'
    MARK_Y2 = 'My2'

    # xaxis ticks : x1 x2 y1 y2
    MARKX_X1 = 'kx1'
    MARKX_Y1 = 'ky1'
    MARKX_X2 = 'kx2'
    MARKX_Y2 = 'ky2'

    # yaxis ticks : x1 x2 y1 y2
    MARKY_X1 = 'ax1'
    MARKY_Y1 = 'ay1'
    MARKY_X2 = 'ax2'
    MARKY_Y2 = 'ay2'
        
    # mouse over style : stroke fill strokeopacity fillopacity strokewidth fontsize fontfamily fontweight 
    # letterspacing wordspacing appearance(shape)
    MOVERS_STROKE = 'ms'
    MOVERS_FILL = 'mf'
    MOVERS_STROKEOPACITY = 'mso'
    MOVERS_FILLOPACITY = 'mfo'
    MOVERS_STROKEWIDTH = 'msw'
    MOVERS_FONTSIZE = 'mfs'
    MOVERS_FONTFAMILY = 'mff'
    MOVERS_FONTWEIGHT = 'mfw'
    MOVERS_LETTERSPACING = 'mls'
    MOVERS_WORDSPACING = 'mws'
    MOVERS_APPEARANCE = 'ma'

    # polyline : points
    OLYL_POINTS = 'op'
        
    # path : d pathLength
    PATH_D = 'pd'
    PATH_PATHLENGTH = 'ppl'

    # plotpoint circ
    PLOTCIRC_CX = 'vcx'
    PLOTCIRC_CY = 'vcy'
    PLOTCIRC_R = 'vr'

    # plotpoint polygon
    PLOTOLYL_POINTS = 'wp'
    
    # plotpoint rect
    PLOTRECT_X = 'qx'
    PLOTRECT_Y = 'qy'
    PLOTRECT_H = 'qh'
    PLOTRECT_W = 'qw'
    PLOTRECT_RX = 'qrx'
    PLOTRECT_RY = 'qry'

    # rect : x y width height rx ry
    RECT_X = 'rx'
    RECT_Y = 'ry'
    RECT_H = 'rh'
    RECT_W = 'rw'
    RECT_RX = 'rrx'
    RECT_RY = 'rry'

    # style : stroke fill strokeopacity fillopacity strokewidth fontsize fontfamily fontweight letterspacing
    #         wordspacing appearance(shape)
    STYLE_STROKE = 'ss'
    STYLE_FILL = 'sf'
    STYLE_STROKEOPACITY = 'sso'
    STYLE_FILLOPACITY = 'sfo'
    STYLE_STROKEWIDTH = 'ssw'
    STYLE_FONTSIZE = 'sfs'
    STYLE_FONTFAMILY = 'sff'
    STYLE_FONTWEIGHT = 'sfw'
    STYLE_LETTERSPACING = 'sls'
    STYLE_WORDSPACING = 'sws'
    STYLE_APPEARANCE = 'sa'

    # main table, parent-less table
    TABLE_STACKEDBAR = 'ub'
    TABLE_LINE = 'ul'
    TABLE_PIE = 'ud'

    # text : x y dx dy text-anchor rotate textLength lengthAdjust
    TEXT_X = 'Tx'
    TEXT_Y = 'Ty'
    TEXT_INNERHTML = 'Tih'
    TEXT_DX = 'Tdx'
    TEXT_DY = 'Tdy'
    TEXT_TEXTANCHOR = 'Tta'
    TEXT_ROTATE = 'Tr'
    TEXT_LENGTH = 'Tl'
    TEXT_LENGTHADJUST = 'Tla'
    
    # textx xaxis text : x y dx dy text-anchor rotate textLength lengthAdjust
    TEXTX_X = 'hx'
    TEXTX_Y = 'hy'
    TEXTX_INNERHTML = 'hih'
    TEXTX_DX = 'hdx'
    TEXTX_DY = 'hdy'
    TEXTX_TEXTANCHOR = 'hta'
    TEXTX_ROTATE = 'hr'
    TEXTX_LENGTH = 'hl'
    TEXTX_LENGTHADJUST = 'hla'

    # texty yaxis text : x y dx dy text-anchor rotate textLength lengthAdjust
    TEXTY_X = 'jx'
    TEXTY_Y = 'jy'
    TEXTY_INNERHTML = 'jih'
    TEXTY_DX = 'jdx'
    TEXTY_DY = 'jdy'
    TEXTY_TEXTANCHOR = 'jta'
    TEXTY_ROTATE = 'jr'
    TEXTY_LENGTH = 'jl'
    TEXTY_LENGTHADJUST = 'jla'
        
    # maps the cell type choice to a svg attribute
    CELL_TYPE_SVG_DICT = {
                     CIRC_CX: 'cx', 
                     CIRC_CY: 'cy',
                     CIRC_R: 'r',
                     ELLI_CX: 'cx', 
                     ELLI_CY: 'cx', 
                     ELLI_RX: 'rx', 
                     ELLI_RY: 'ry',
                     GON_POINTS: 'points',
                     GRID_D: 'd',
                     GRID_PATHLENGTH: 'pathLength', 
                     GRIDX_X1: 'x1',
                     GRIDX_Y1: 'y1', 
                     GRIDX_X2: 'x2',
                     GRIDX_Y2: 'y2',
                     GRIDY_X1: 'x1', 
                     GRIDY_Y1: 'y1', 
                     GRIDY_X2: 'x2',
                     GRIDY_Y2: 'y2',
                     LINE_X1: 'x1',
                     LINE_Y1: 'y1',
                     LINE_X2: 'x2',
                     LINE_Y2: 'y2',
                     MARK_X1: 'x1',
                     MARK_Y1: 'y1',
                     MARK_X2: 'x2',
                     MARK_Y2: 'y2',
                     MARKX_X1: 'x1',
                     MARKX_Y1: 'y1',
                     MARKX_X2: 'x2',
                     MARKX_Y2: 'y2',
                     MARKY_X1: 'x1',
                     MARKY_Y1: 'y1',
                     MARKY_X2: 'x2',
                     MARKY_Y2: 'y2',
                     OLYL_POINTS: 'points',
                     PATH_D: 'd',
                     PATH_PATHLENGTH: 'pathLength',
                     PLOTCIRC_CX: 'cx',
                     PLOTCIRC_CY: 'cy',
                     PLOTCIRC_R: 'r',
                     PLOTOLYL_POINTS: 'points',
                     PLOTRECT_X: 'x',
                     PLOTRECT_Y: 'y',
                     PLOTRECT_H: 'height',
                     PLOTRECT_W: 'width',
                     PLOTRECT_RX: 'rx',
                     PLOTRECT_RY: 'ry',
                     RECT_X: 'x',
                     RECT_Y: 'y',
                     RECT_H: 'height',
                     RECT_W: 'width',
                     RECT_RX: 'rx',
                     RECT_RY: 'ry',
                     TEXT_X: 'x', 
                     TEXT_Y: 'y',
                     TEXT_DX: 'dx',
                     TEXT_DY: 'dy',
                     TEXT_TEXTANCHOR: 'text-anchor', 
                     TEXT_ROTATE: 'rotate',
                     TEXT_LENGTH: 'textLength',
                     TEXT_LENGTHADJUST: 'lengthAdjust',
                     TEXTX_X: 'x', 
                     TEXTX_Y: 'y',
                     TEXTX_DX: 'dx',
                     TEXTX_DY: 'dy',
                     TEXTX_TEXTANCHOR: 'text-anchor', 
                     TEXTX_ROTATE: 'rotate',
                     TEXTX_LENGTH: 'textLength',
                     TEXTX_LENGTHADJUST: 'lengthAdjust',
                     TEXTY_X: 'x', 
                     TEXTY_Y: 'y',
                     TEXTY_DX: 'dx',
                     TEXTY_DY: 'dy',
                     TEXTY_TEXTANCHOR: 'text-anchor', 
                     TEXTY_ROTATE: 'rotate',
                     TEXTY_LENGTH: 'textLength',
                     TEXTY_LENGTHADJUST: 'lengthAdjust',
                    }

    # maps the cell type choice to f or c attribute
    CELL_TYPE_DATA_TYPE_DICT = {
                     CIRC_CX: 'f', 
                     CIRC_CY: 'f',
                     CIRC_R: 'f',
                     ELLI_CX: 'f', 
                     ELLI_CY: 'f', 
                     ELLI_RX: 'f', 
                     ELLI_RY: 'f',
                     GON_POINTS: 'c',
                     GRID_D: 'c',
                     GRID_PATHLENGTH: 'f', 
                     GRIDX_X1: 'f',
                     GRIDX_Y1: 'f', 
                     GRIDX_X2: 'f',
                     GRIDX_Y2: 'f',
                     GRIDY_X1: 'f', 
                     GRIDY_Y1: 'f', 
                     GRIDY_X2: 'f',
                     GRIDY_Y2: 'f',
                     LINE_X1: 'f',
                     LINE_Y1: 'f',
                     LINE_X2: 'f',
                     LINE_Y2: 'f',
                     MARK_X1: 'f',
                     MARK_Y1: 'f',
                     MARK_X2: 'f',
                     MARK_Y2: 'f',
                     MARKX_X1: 'f',
                     MARKX_Y1: 'f',
                     MARKX_X2: 'f',
                     MARKX_Y2: 'f',
                     MARKY_X1: 'f',
                     MARKY_Y1: 'f',
                     MARKY_X2: 'f',
                     MARKY_Y2: 'f',
                     OLYL_POINTS: 'c',
                     PATH_D: 'c',
                     PATH_PATHLENGTH: 'f',
                     PLOTCIRC_CX: 'f',
                     PLOTCIRC_CY: 'f',
                     PLOTCIRC_R: 'f',
                     PLOTOLYL_POINTS: 'c',
                     PLOTRECT_X: 'f',
                     PLOTRECT_Y: 'f',
                     PLOTRECT_H: 'f',
                     PLOTRECT_W: 'f',
                     PLOTRECT_RX: 'f',
                     PLOTRECT_RY: 'f',
                     RECT_X: 'f',
                     RECT_Y: 'f',
                     RECT_H: 'f',
                     RECT_W: 'f',
                     RECT_RX: 'f',
                     RECT_RY: 'f',
                     TEXT_X: 'f', 
                     TEXT_Y: 'f',
                     TEXT_DX: 'f',
                     TEXT_DY: 'f',
                     TEXT_TEXTANCHOR: 'c', 
                     TEXT_ROTATE: 'f',
                     TEXT_LENGTH: 'f',
                     TEXT_LENGTHADJUST: 'f',
                     TEXT_INNERHTML: 'c',
                     TEXTX_X: 'f', 
                     TEXTX_Y: 'f',
                     TEXTX_DX: 'f',
                     TEXTX_DY: 'f',
                     TEXTX_TEXTANCHOR: 'c', 
                     TEXTX_ROTATE: 'f',
                     TEXTX_LENGTH: 'f',
                     TEXTX_LENGTHADJUST: 'f',
                     TEXTX_INNERHTML: 'c',
                     TEXTY_X: 'f', 
                     TEXTY_Y: 'f',
                     TEXTY_DX: 'f',
                     TEXTY_DY: 'f',
                     TEXTY_TEXTANCHOR: 'c', 
                     TEXTY_ROTATE: 'f',
                     TEXTY_LENGTH: 'f',
                     TEXTY_LENGTHADJUST: 'f',
                     TEXTY_INNERHTML: 'c',
                    }

    CELL_TYPE_CHOICES = (
                         (CIRC_CX, 'Circle Center X'), 
                         (CIRC_CY, 'Circle Center Y'), 
                         (CIRC_R, 'Circle Radius'),
                         (ELLI_CX, 'Ellipse Center X'), 
                         (ELLI_CY, 'Ellipse Center Y'), 
                         (ELLI_RX, 'Ellipse RX'), 
                         (ELLI_RY, 'Ellipse RY'),
                         (FORM_A, 'Transform [0][0]'), 
                         (FORM_B, 'Transform [0][1]'), 
                         (FORM_C, 'Transform [1][0]'), 
                         (FORM_D, 'Transform [1][1]'),
                         (FORM_E, 'Transform [2][0]'), 
                         (FORM_F, 'Transform [2][1]'),
                         (GON_POINTS, 'Polygon Points'),
                         (GRID_D, 'Grid Directives'), 
                         (GRID_PATHLENGTH, 'Grid Path Length'), 
                         (GRIDX_X1, 'GridX X1 Coordinate'), 
                         (GRIDX_Y1, 'GridX Y1 Coordinate'), 
                         (GRIDX_X2, 'GridX X2 Coordinate'),
                         (GRIDX_Y2, 'GridX Y2 Coordinate'),
                         (GRIDY_X1, 'GridY X1 Coordinate'), 
                         (GRIDY_Y1, 'GridY Y1 Coordinate'), 
                         (GRIDY_X2, 'GridY X2 Coordinate'),
                         (GRIDY_Y2, 'GridY Y2 Coordinate'),
                         (LINE_X1, 'Line X1'),  
                         (LINE_Y2, 'Line Y1'), 
                         (LINE_X2, 'Line X2'),
                         (LINE_Y2, 'Line Y2'),
                         (MARK_X1, 'Axis Mark X1 Coordinate'), 
                         (MARK_Y1, 'Axis Mark Y1 Coordinate'), 
                         (MARK_X2, 'Axis Mark X2 Coordinate'),
                         (MARK_Y2, 'Axis Mark Y2 Coordinate'),
                         (MARKX_X1, 'XAxis Mark X1 Coordinate'), 
                         (MARKX_Y1, 'XAxis Mark Y1 Coordinate'), 
                         (MARKX_X2, 'XAxis Mark X2 Coordinate'),
                         (MARKX_Y2, 'XAxis Mark Y2 Coordinate'),
                         (MARKY_X1, 'YAxis Mark X1 Coordinate'), 
                         (MARKY_Y1, 'YAxis Mark Y1 Coordinate'),
                         (MARKY_X2, 'YAxis Mark X2 Coordinate'), 
                         (MARKY_Y2, 'YAxis Mark Y2 Coordinate'),
                         (MOVERS_STROKE, 'Stroke Color'), 
                         (MOVERS_FILL, 'Fill Color'), 
                         (MOVERS_STROKEOPACITY, 'Stroke Opacity'),
                         (MOVERS_FILLOPACITY, 'Fill Opacity'), 
                         (MOVERS_STROKEWIDTH, 'Stroke Width'), 
                         (MOVERS_FONTSIZE, 'Font Size'),
                         (MOVERS_FONTFAMILY, 'Font Family'), 
                         (MOVERS_FONTWEIGHT, 'Font Weight'), 
                         (MOVERS_LETTERSPACING, 'Letter Spacing'), 
                         (MOVERS_WORDSPACING, 'Word Spacing'),
                         (MOVERS_APPEARANCE, 'Plot Point Appearance'),
                         (OLYL_POINTS, 'Polyline Points'),
                         (PATH_D, 'Path Directives'), 
                         (PATH_PATHLENGTH, 'Path Length'),
                         (PLOTCIRC_CX, 'Plot Point Circle Center X'), 
                         (PLOTCIRC_CY, 'Plot Point Circle Center Y'), 
                         (PLOTCIRC_R, 'Plot Point Circle Radius'),
                         (PLOTOLYL_POINTS, 'Plot Point Polyline Points'),
                         (PLOTRECT_X, 'Plot Point Rectangle X'), 
                         (PLOTRECT_Y, 'Plot Point Rectangle Y'), 
                         (PLOTRECT_H, 'Plot Point Rectangle H'), 
                         (PLOTRECT_W, 'Plot Point Rectangle W'), 
                         (PLOTRECT_RX, 'Plot Point Rectangle RX'), 
                         (PLOTRECT_RY, 'Plot Point Rectangle RY'),
                         (RECT_X, 'Rectangle X'), 
                         (RECT_Y, 'Rectangle Y'), 
                         (RECT_H, 'Rectangle H'), 
                         (RECT_W, 'Rectangle W'), 
                         (RECT_RX, 'Rectangle RX'), 
                         (RECT_RY, 'Rectangle RY'),
                         (STYLE_STROKE, 'Stroke Color'), 
                         (STYLE_FILL, 'Fill Color'), 
                         (STYLE_STROKEOPACITY, 'Stroke Opacity'), 
                         (STYLE_FILLOPACITY, 'Fill Opacity'), 
                         (STYLE_STROKEWIDTH, 'Stroke Width'), 
                         (STYLE_FONTSIZE, 'Font Size'),
                         (STYLE_FONTFAMILY, 'Font Family'), 
                         (STYLE_FONTWEIGHT, 'Font Weight'), 
                         (STYLE_LETTERSPACING, 'Letter Spacing'), 
                         (STYLE_WORDSPACING, 'Word Spacing'),
                         (STYLE_APPEARANCE, 'Plot Point Appearance'),
                         (TABLE_STACKEDBAR, 'Table Stacked Bar'),
                         (TABLE_LINE, 'Table Line'),
                         (TABLE_PIE, 'Table Pie'),
                         (TEXT_X, 'Text X'), 
                         (TEXT_Y, 'Text Y'), 
                         (TEXT_INNERHTML, 'Text Inner HTML'),
                         (TEXT_DX, 'Text Adjust x'), 
                         (TEXT_DY, 'Text Adjust y'),
                         (TEXT_TEXTANCHOR, 'Text Anchor'), 
                         (TEXT_ROTATE, 'Text Rotate'),
                         (TEXT_LENGTH, 'Text Length'), 
                         (TEXT_LENGTHADJUST, 'Text Length Adjust'),
                         (TEXTX_X, 'XAxis Text X'), 
                         (TEXTX_Y, 'XAxis Text Y'), 
                         (TEXTX_INNERHTML, 'XAxis Text Inner HTML'),
                         (TEXTX_DX, 'XAxis Text Adjust x'), 
                         (TEXTX_DY, 'XAxis Text Adjust y'),
                         (TEXTX_TEXTANCHOR, 'XAxis Text Anchor'), 
                         (TEXTX_ROTATE, 'XAxis Text Rotate'),
                         (TEXTX_LENGTH, 'XAxis Text Length'), 
                         (TEXTX_LENGTHADJUST, 'XAxis Text Length Adjust'),
                         (TEXTY_X, 'YAxis Text X'), 
                         (TEXTY_Y, 'YAxis Text Y'), 
                         (TEXTY_INNERHTML, 'YAxis Text Inner HTML'),
                         (TEXTY_DX, 'YAxis Text Adjust x'), 
                         (TEXTY_DY, 'YAxis Text Adjust y'),
                         (TEXTY_TEXTANCHOR, 'YAxis Text Anchor'), 
                         (TEXTY_ROTATE, 'YAxis Text Rotate'),
                         (TEXTY_LENGTH, 'YAxis Text Length'), 
                         (TEXTY_LENGTHADJUST, 'YAxis Text Length Adjust'),)

class defines_for_column(defines_for_cell):

    COLUMN_TYPE_CHOICES = defines_for_cell.CELL_TYPE_CHOICES
    
class defines_for_row():
    
    CIRC = 'c'
    ELLI = 'e'
    FORM = 'f'
    GON = 'n'
    GRID = 'G'
    GRIDX = 'g'
    GRIDY = 'i'
    LINE = 'l'
    MARK = 'M'
    MARKX = 'k'
    MARKY = 'a'
    MOVERS = 'm'
    OLYL = 'o'
    PATH = 'p'
    PLOTCIRC = 'v'
    PLOTOLYL = 'w'
    PLOTRECT = 'q'
    RECT = 'r'
    STYLE = 's'
    TABLE_STACKEDBAR = 'b'
    TABLE_LINE = 'n'
    TABLE_PIE = 'd'
    TEXT = 'T'
    TEXTX = 'h'
    TEXTY = 'j'
    
    ROW_TYPE_CHOICES = (
                        (CIRC, 'Circle'),
                        (ELLI, 'Ellipse'), 
                        (FORM, 'Transform'), 
                        (GON, 'Polygon'),
                        (GRID, 'Grid'),
                        (GRIDX, 'XAxis Grid'),
                        (GRIDY, 'YAxis Grid'),
                        (LINE, 'Line'), 
                        (MARK, 'Mark'),
                        (MARKX, 'XAxis Mark'), 
                        (MARKY, 'YAxis Mark'), 
                        (MOVERS, 'Mouse Over Style'),
                        (OLYL, 'Polyline'), 
                        (PATH, 'Path'), 
                        (PLOTCIRC, 'Plot Point Circle'),
                        (PLOTOLYL, 'Plot Point Polyline'),
                        (PLOTRECT, 'Plot Point Rect'),
                        (RECT, 'Rectangle'), 
                        (STYLE, 'Style'), 
                        (TABLE_STACKEDBAR, 'Table Stacked Bar'),
                        (TABLE_LINE, 'Table Line'),
                        (TABLE_PIE, 'Table Pie'),
                        (TEXT, 'Text'), 
                        (TEXTX, 'XAxis Text'),
                        (TEXTY, 'YAxis Text'),)

    ROW_TYPE_SVG_DICT = {
                            CIRC: 'circle',
                            ELLI: 'ellipse',
                            GON: 'polygon',
                            GRID: 'path',
                            GRIDX: 'line',
                            GRIDY: 'line',
                            LINE: 'line',
                            MARK: 'line',
                            MARKX: 'line',
                            MARKY: 'line',
                            OLYL: 'polyline',
                            PATH: 'path',
                            PLOTCIRC: 'circle',
                            PLOTOLYL: 'polyline',
                            PLOTRECT: 'rect',
                            RECT: 'rect',
                            TEXT: 'text',
                            TEXTX: 'text',
                            TEXTY: 'text',
                         }

    
class defines_for_table():
    
    GEO = 'g'
    GEO_CIRC = 'gc'
    GEO_ELLI = 'ge'
    GEO_GON = 'gn'
    GEO_LINE = 'gl'
    GEO_OLYL = 'go'
    GEO_PATH = 'gp'
    GEO_RECT = 'gr'
    
    OPT = 'o'
    OPT_FORM = 'of'
    OPT_MOVERS = 'om'
    OPT_STYLE = 'os'
    
    PLOT = 'p'
    PLOT_CIRC = 'pv'
    PLOT_OLYL = 'pw'
    PLOT_RECT = 'pq'
    
    STRUC = 's'
    STRUC_GRID = 'sG'
    STRUC_GRIDX = 'sg'
    STRUC_GRIDY = 'si'
    STRUC_MARK = 'sM'
    STRUC_MARKX = 'sk'
    STRUC_MARKY = 'sa'
    STRUC_TEXT = 'sT'
    STRUC_TEXTX = 'sh'
    STRUC_TEXTY = 'sj'

    TABLE = 'u'
    TABLE_LINE = 'ul'
    TABLE_STACKEDBAR = 'ub'
    TABLE_PIE = 'ud'

    columncountfortype = {GEO_RECT: 6,
                          GEO_LINE: 4,
                          GEO_CIRC: 3,
                          GEO_ELLI: 4,
                          GEO_PATH: 2, 
                          GEO_GON: 1,
                          GEO_OLYL: 1,
                          OPT_FORM: 6,
                          OPT_STYLE: 11,
                          OPT_MOVERS: 11,
                          PLOT_CIRC: 3,
                          PLOT_OLYL: 1,
                          PLOT_RECT: 6,
                          STRUC_MARK: 4,
                          STRUC_MARKX: 4,
                          STRUC_MARKY: 4,
                          STRUC_GRID: 2,
                          STRUC_GRIDX: 4,
                          STRUC_GRIDY: 4,
                          STRUC_TEXT: 9,
                          STRUC_TEXTX: 9,
                          STRUC_TEXTY: 9}

    TABLE_TYPE_CHOICES = (
                          (GEO_RECT, 'Rectangle'), 
                          (GEO_LINE, 'Line'), 
                          (GEO_CIRC, 'Circle'),
                          (GEO_ELLI, 'Ellipse'),  
                          (GEO_PATH, 'Path'),
                          (GEO_GON, 'Polygon'), 
                          (GEO_OLYL, 'Polyline'), 
                          (OPT_FORM, 'Transform'), 
                          (OPT_STYLE, 'Style'), 
                          (OPT_MOVERS, 'Mouse Over Style'),
                          (PLOT_CIRC, 'Plot Point Circle'),
                          (PLOT_OLYL, 'Plot Point Polyline'),
                          (PLOT_RECT, 'Plot Point Rectangle'),
                          (STRUC_MARK, 'Axis Mark'),
                          (STRUC_MARKX, 'XAxis Mark'),
                          (STRUC_MARKY, 'YAxis Mark'),
                          (STRUC_GRID, 'Axis Grid'),
                          (STRUC_GRIDX, 'XAxis Grid'),
                          (STRUC_GRIDY, 'YAxis Grid'),
                          (STRUC_TEXT, 'Axis Text'),
                          (STRUC_TEXTX, 'XAxis Text'),
                          (STRUC_TEXTY, 'YAxis Text'),
                          (TABLE_STACKEDBAR, 'Stacked Bar Table'), 
                          (TABLE_LINE, 'Line Table'),
                          (TABLE_PIE, 'Pie Table'))
    
    
    
    
    
    
class defines_for_datavalues():
    
    COLUMN_WISE = 'cw'
    ROW_WISE = 'rw'
    ORIENTATION_CHOICES = ((COLUMN_WISE, 'Column Orientation'),
                           (ROW_WISE, 'Row Orientation'))
    
    HORIZONTAL_AXIS = 'ha'
    VERTICAL_AXIS = 'va'
    ORIGIN_AXIS_CHOICES = ((HORIZONTAL_AXIS, 'Inverse Sign Equadistance to Horizontal X Axis.'),
                           (VERTICAL_AXIS, 'Inverse Sign Equadistance to Vertical Y Axis.'))
    
    # label text-anchor
    ANCHOR_START = 'as'
    ANCHOR_MIDDLE = 'am'
    ANCHOR_END = 'ae'
    ANCHOR_TYPE_SVG_DICT = {ANCHOR_START: 'start', ANCHOR_MIDDLE: 'middle', ANCHOR_END: 'end'}
    
    # defines the number of markings on the y-axis
    NUMBER_MARKS_CHOICES = ((5, '5'),
                            (10, '10'),
                            (15, '15'),
                            (20, '20'),
                            (25, '25'),
                            (30, '30'),
                            (35, '35'),
                            (40, '40'),
                            (45, '45'),
                            (50, '50'),
                            (55, '55'),
                            (60, '60'),
                            (65, '65'),
                            (70, '70'),
                            (75, '75'),
                            (80, '80'),
                            (85, '85'),
                            (90, '90'),
                            (95, '95'),
                            (100, '100'))

    
class defines_for_optionals():


    SERIF = 's'
    SANSSERIF = 'a'
    MONOSPACE = 'm'
    CURSIVE = 'c'
    FANTASY = 'f'

    TEXT_FAMILY_CHOICES = ((SERIF, 'Serif'),
                           (SANSSERIF, 'Sans-Serif'),
                           (MONOSPACE, 'Monospace'),
                           (CURSIVE, 'Cursive'),
                           (FANTASY, 'Fantasy'))    

    TEXT_FAMILY_DICT = {
                        SERIF: 'serif',
                        SANSSERIF: 'sans-serif',
                        MONOSPACE: 'monospace',
                        CURSIVE: 'cursive',
                        FANTASY: 'fantasy',
                        }    


    
    SQUARE = 's'
    CIRCLE = 'c'
    DIAMOND = 'd'
    STAR = 't'
    
    PLOTPOINT_SHAPE_CHOICES = ((SQUARE, 'Square'), (CIRCLE, 'Circle'), (DIAMOND, 'Diamond'), (STAR, 'Star'))

    
    
    