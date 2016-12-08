# -*- coding: utf-8 -*-
from PyQt5 import uic

class UiConvert:
    def __init__(self, in_name, out_name):
        self.f_in = open(in_name, 'r', encoding='utf-8')
        self.f_out = open(out_name, 'w', encoding='utf-8')
        uic.compileUi(self.f_in, self.f_out, execute=False)
        self.f_in.close()
        self.f_out.close()
