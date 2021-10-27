import pandas as pd

per_fields = ['RTYPE', 'MAFID', 'CUF_PNC', 'BCUSTATEFP', 'VERSION', 'QSEX', 'QAGE', 'QDB', 'QDOB_MONTH', 'QDOB_DAY', 'QDOB_YEAR', 'QSPAN', 'QSPANX', 'CENHISP', 'QRACE1', 'QRACE2', 'QRACE3', 'QRACE4', 'QRACE5', 'QRACE6', 'QRACE7', 'QRACE8', 'QRACEX', 'CENRACE', 'RACE2010', 'RELSHIP', 'QGQTYP', 'LIVE_ALONE']
per_df = pd.DataFrame(columns=per_fields)

new_row_template = {
    "RTYPE"         : '3', # Record Type - 3 = person in housing unit; 5 = person in group quarters
    "MAFID"         : '899999999', # 9-digit Person Number ?? or maybe household id??? 999999999 = Not reported
    "CUF_PNC"       : '12345',  # ???
    "BCUSTATEFP"    : '53',  # State FIPS code ?
    "VERSION"       : '12345',  # ???
    "QSEX"          : '1',  # Edited Sex - CHAR(1) - 1 = male; 2 = female
    "QAGE"          : '25', # Edited Age - INT(3) - 0-115
    "QDB"           : '19960101',  # Date of birth - INT(8) ? - YYYMMDD 
    "QDOB_MONTH"    : '1',  # Month of birth - INT(2) ?
    "QDOB_DAY"      : '1',  # Day of birth - INT(2) ??
    "QDOB_YEAR"     : '1996',  # Year of birth - INT(4) ??
    "QSPAN"         : '1000',  # Hispanic origin code - CHAR(3) ??
    "QSPANX"        : '1',  # Hispanic Origin Edit/Allocation Group - CHAR(1) ??
    "CENHISP"       : '1',  # Hispanic Origin - CHAR(1) - 1 = not Hispanic; 2 = Hispanic
    "QRACE1"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE2"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE3"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE4"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE5"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE6"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE7"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACE8"        : '1000', # race code - CHAR(3) - 100 = White; 200 = Black; 300 = AIAN; ???
    "QRACEX"        : '1', # Race Edit/Allocation Group - CHAR(1) - 
    "CENRACE"       : '11', # Census Race - CHAR(2) - 01 to 63, coding all combinations of one or more races
    "RACE2010"      : '11', # ???
    "RELSHIP"       : '21', # Edited relationship - CHAR(2) - 99 = not reported
    "QGQTYP"        : '   ', # Group Quarters Facilities Type - CHAR(3) - 000 = NIU, 101, 201, 301, etc listed in TDA docs
    "LIVE_ALONE"    : '0', # Person living alone - CHAR(1) - 9 = not reported
}

for age in [25, 26, 27, 28]:
    new_row_template["CUF_PNC"] = '123' + str(age)
    new_row_template["QAGE"] = str(age)
    birthyear = 2021 - age
    new_row_template["QDB"] = str(birthyear) + '0101'
    new_row_template["QDOB_YEAR"] = str(birthyear)
    if age != 28:
        new_row_template["RELSHIP"] = '35'

    per_df = per_df.append(new_row_template, ignore_index=True)

per_df.to_csv('seattle_arboretum_per.cef', sep='|', index=False, header=False)
