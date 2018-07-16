# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:39:25 2018

@author: jackr
"""

import pandas as pd
import json

with open('json/fpl.json') as f:
    d = f.read()

d = json.loads(d)
print(pd.DataFrame.from_records(d))