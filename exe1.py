#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlsxwriter

workbook = xlsxwriter.Workbook("xlsx_test.xlsx")

worksheet1 = workbook.add_worksheet("ID")

worksheet2 = workbook.add_worksheet("姓名")

worksheet1.set_column("A:A",20)
worksheet1.set_column("B:B",10)

worksheet1.write(0,0,"hello world!")

workbook.close()