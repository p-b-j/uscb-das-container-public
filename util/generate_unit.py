import pandas as pd

unit_fields = ['RTYPE', 'MAFID', 'BCUSTATEFP', 'VERSION', 'FINAL_POP', 'HHLDRAGE', 'HHSPAN', 'HHLDRACE', 'HHRACE', 'TEN', 'TEN_A', 'TEN_R', 'VACS', 'QGQTYP', 'GQSEX', 'OIDTB', 'HHT', 'HHT2', 'CPLT', 'UPART', 'MULTG', 'PAOC', 'P18', 'P60', 'P65', 'P75', 'PAC', 'HHSEX']

unit_df = pd.DataFrame(columns=unit_fields)

new_row = {
    "RTYPE"         : '2', # record type - CHAR(1) - 2 = Housing unit; 4 = Group quarters
    "MAFID"         : '899999999', # maybe household id ???
    "BCUSTATEFP"    : '53', # State FIPS code ?
    "VERSION"       : '12345', # ???
    "FINAL_POP"     : '4', # count of people in this unit ???
    "HHLDRAGE"      : '25', # Age of Householder - CHAR(1) - 0 = NIU; 1 = 15-24; etc
    "HHSPAN"        : '1', # Hispanic Householder - CHAR(1) - 0 = NIU; 1 = Not Hispanic; 2 = Hispanic
    "HHLDRACE"      : '1', # Race of Householder - CHAR(2) - 00 = NIU; 01 = White Along; etc ???
    "HHRACE"        : '11', # Race of Householder - CHAR(2) - 00 = NIU; 01 = White Along; etc ???
    "TEN"           : '2', # Tenure - CHAR(1) - 0 = NIU; 9 = Occupied
    "TEN_A"         : '2', # ???
    "TEN_R"         : '2', # ???
    "VACS"          : '0', # Vacancy States - CHAR(1) - 0 = NIU; 9 = Vacant
    "QGQTYP"        : '   ', # Group quarters facility type - CHAR(3) - 000 = NIU; 101 = Federal detention centers; etc.
    "GQSEX"         : '1', # ???
    "OIDTB"         : '27659836057514', # ???  maybe this is the unique key to join against the grf file
    "HHT"           : '5', # Household/Family Type - CHAR(1) - 0 = NIU; 1 = Married couple; etc.
    "HHT2"          : '12', # Household/Family Type (Includes Cohabitating) - CHAR(2) - 00 = NIU; ...
    "CPLT"          : '0', # Couple Type - CHAR(1) - 0 = NIU; etc
    "UPART"         : '0', # Presence and Type of Unmarried Partner Household - CHAR(1) - 0 = NIU; etc
    "MULTG"         : '1', # Multigenerational Household - CHAR(1) - 0 = NIU; 1 = Not Multi; 2 = Multi
    "PAOC"          : '4', # Presence and Age of Own Children Under 18 - CHAR(1) - 0 = NIU; ...
    "P18"           : '0', # Presence of People Under 18 Years in Household - CHAR(1) - 9 = Not reported
    "P60"           : '0', # Presence of People 60 Years and Over in Household - CHAR(1) - 0 = NIU; 1 = one or more
    "P65"           : '0', # Presence of People 65 Years and Over in Household - CHAR(1) - 0 = NIU; 1 = one or more
    "P75"           : '0', # Presence of People 75 Years and Over in Household - CHAR(1) - 0 = NIU; 1 = one or more
    "PAC"           : '4', # Presence and Age of Children Under 18 - CHAR(1) - 9 = Not reported
    "HHSEX"         : '1', # Sex of Householder - CHAR(1) - 0 = NIU; 1 = Male; 2 = Female
}

unit_df = unit_df.append(new_row, ignore_index=True)

unit_df.to_csv('seattle_arboretum_unit.cef', sep='|', index=False, header=False)
