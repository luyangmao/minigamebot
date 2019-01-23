# -*- coding: UTF-8 -*-
import os;

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text