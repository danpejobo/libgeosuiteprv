from os.path import splitext, basename
from itertools import count
import numpy as np
import datetime
import time
import pandas as pd
import warnings
import zipfile
import codecs
import os
import io
import logging

logger = logging.getLogger(__name__)


def parse(input_filename, borehole_id=None):
    if borehole_id is None:
        if isinstance(input_filename, str):
            borehole_id = input_filename.split("/")[-1].split(".", 1)[0]

    df = pd.DataFrame()
    comment_list = []
    if isinstance(input_filename, str):
        with open(input_filename, 'r', encoding='iso8859_10') as f:
            lines = f.readlines()
    else:
        lines = codecs.getreader('utf8')(input_filename, errors='ignore').readlines()

    firstline_list = lines[0][:-1].split()

    main = [{'date': pd.to_datetime(firstline_list[2], format='%d.%m.%Y') if firstline_list[2] != "-" else np.nan,
             "method_code": "core_sampling",
             "investigation_point": borehole_id
    }]
    rows = []
    for l in lines[2:-1]:
        values = l[:-1].split()
        if '?' in values:
            index = values.index('?')
            values[index] = 0
        if l[0]=='*':
            break
        tube = values[0]
        data_str = values[1:12]
        data_num = np.array(data_str, dtype=np.float64)
        row = pd.Series([tube] + list(data_num))
        rows.append(row)
        comment_list.append(' '.join(values[12:]))
    df = pd.concat([r.to_frame().T for r in rows], ignore_index=True)

    df = df.replace(0,np.nan).rename(columns={
        0:'tube',
        2:'depth',
        3:'water_content_%',
        8:'cu_kpa_undrained_shear_strength',
        10:'unit_weight_kn_m3',
        4:'plastic_limit',
        5:'liquid_limit',
        6:'cufc',
        7:'curfc',
    })

    return [{"main": main,
             "data": df}]
