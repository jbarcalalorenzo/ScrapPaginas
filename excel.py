__author__ = 'Javier'

from pyExcelerator import *

class Excel(object):
    def __init__(self, name_space='0'):
        self.column = 0
        self.row = 0
        self.workbook = Workbook()
        self.worksheet = self.workbook.add_sheet(name_space)

    def write_row(self, content):
        self.column = 0
        for i in content:
            self.worksheet.write(self.row, self.column, i)
            self.column += 1
        self.row += 1

    def write_with_format(self, content, bold=False, name='Arial', colour_index=4):
        font = Font()
        font.name = name
        font.colour_index = colour_index
        font.bold = bold
        style = XFStyle()
        style.font = font
        self.column = 0
        for i in content:
            self.worksheet.write(self.row, self.column, i, style)
            self.column += 1
        self.row += 1

    def save(self, filename='empresas.xls'):
        self.workbook.save(filename)