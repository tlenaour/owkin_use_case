import re
import math


def curate_pack_years(pack_years_value):
    if isinstance(pack_years_value, str):
        match = re.match(r'\b\d+\b', pack_years_value)
        if match:
            return int(match.group())
        else:
            return -1
    elif math.isnan(pack_years_value):
        return -1
    else:
        return pack_years_value


