import numpy as np
import pandas as pd
import codecs
import logging
from dateutil import parser as dateparser

logger = logging.getLogger(__name__)


def parse_date(v):
    try:
        if len(v) >= 8:
            return dateparser.isoparse(v).date()
    except ValueError as exception:
        logger.debug("Unable to parse date as ISO: %s (%s)", v, exception)
    try:
        return dateparser.parse(v, parserinfo=dateparser.parserinfo(dayfirst=True)).date()
    except Exception as e:
        logger.debug("Unable to parse date: %s (%s)", v, e)
        return np.nan

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

    main = [{'date': parse_date(firstline_list[2]),
             "method_code": "core_sampling",
             "investigation_point": borehole_id
    }]
    rows = []
    for l in lines[2:-1]:
        values = l[:-1].split()
        cleaned = [np.nan if v == '?' else v for v in values[1:12]]
        try:
            if l[0]=='*':
                break
        except IndexError:
            logger.warning(f"Encountered empty or malformed line while checking for '*': '{l.strip()}'")
            continue
        try:
            tube = values[0]
            data_num = np.array(cleaned, dtype=np.float64)
            row = pd.Series([tube] + list(data_num))
            rows.append(row)
            comment_list.append(' '.join(values[12:]))
        except Exception as e:
            logger.warning(f"Failed to parse line: {l.strip()} — {e}")
    df = pd.concat([r.to_frame().T for r in rows], ignore_index=True)

    df = df.rename(columns={
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
