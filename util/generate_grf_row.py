
import pandas as pd


grfc_fields = ['TABBLKST', 'TABBLKCOU', 'TABTRACTCE', 'TABBLK', 'TABBLKSUFX1', 'TABBLKSUFX2', 'TABBLKGRPCE', 'POPDEC', 'HOUSING', 'CURSTATE', 'CURCOUNTY', 'CURTRACTCE', 'CURBLKGRPCE', 'REGIONCE', 'DIVISIONCE', 'STATENS', 'COUNTYNS', 'COUNTYFS', 'COUSUBFP', 'COUSUBNS', 'COUSUBFS', 'SUBMCDFP', 'SUBMCDNS', 'ESTATEFP', 'ESTATENS', 'CONCITFP', 'CONCITNS', 'PLACEFP', 'PLACENS', 'PLACEFS', 'AIANNHFP', 'AIANNHCE', 'AIANNHNS', 'AIHHTLI', 'TRIBALSUBFP', 'TRIBALSUBCE', 'TRIBALSUBNS', 'TTRACTCE', 'TBLKGRPCE', 'ANRCFP', 'ANRCNS', 'UACE', 'UATYP', 'UR', 'CD116FP', 'CDCURFP', 'VTDST', 'SLDUST', 'SLDLST', 'ZCTA5CE', 'SDELMLEA', 'SDSECLEA', 'SDUNILEA', 'UGACE', 'PUMA', 'LWBLKTYP', 'INTPTLAT', 'INTPTLON', 'AREALAND', 'AREAWATER', 'AREAWATERINLD', 'AREAWATERCSTL', 'AREAWATERGRLK', 'AREAWATERTSEA', 'CSAFP', 'CBSAFP', 'METDIVFP', 'PCICBSA', 'CNECTAFP', 'NECTAFP', 'NECTADIVFP', 'PCINECTA', 'ACT', 'MEMI', 'NMEMI', 'OIDTABBLK']

grfc_df = pd.DataFrame(columns=grfc_fields)

new_row = {
    "TABBLKST"      : '53',
    "TABBLKCOU"     : '033',
    "TABTRACTCE"    : '006400',
    "TABBLK"        : '1006',
    "TABBLKSUFX1"   : '',
    "TABBLKSUFX2"   : '',
    "TABBLKGRPCE"   : '1',
    "POPDEC"        : '4',
    "HOUSING"       : '1',
    "CURSTATE"      : '',
    "CURCOUNTY"     : '',
    "CURTRACTCE"    : '',
    "CURBLKGRPCE"   : '',
    "REGIONCE"      : '4',
    "DIVISIONCE"    : '9',
    "STATENS"       : '53',
    "COUNTYNS"      : '033',
    "COUNTYFS"      : 'S',
    "COUSUBFP"      : '92928',
    "COUSUBNS"      : '01939621',
    "COUSUBFS"      : 'S',
    "SUBMCDFP"      : '92928',
    "SUBMCDNS"      : '01939621',
    "ESTATEFP"      : '92928', #TODO
    "ESTATENS"      : '01939621', #TODO
    "CONCITFP"      : '', #TODO
    "CONCITNS"      : '', #TODO
    "PLACEFP"       : '63000',
    "PLACENS"       : '02411856',
    "PLACEFS"       : 'S',
    "AIANNHFP"      : '99999',
    "AIANNHCE"      : '9999',
    "AIANNHNS"      : '99999999',
    "AIHHTLI"       : '9',
    "TRIBALSUBFP"   : '99999',
    "TRIBALSUBCE"   : '999',
    "TRIBALSUBNS"   : '99999999',
    "TTRACTCE"      : '999999',
    "TBLKGRPCE"     : '9',
    "ANRCFP"        : '99999',
    "ANRCNS"        : '99999999',
    "UACE"          : '80389',
    "UATYP"         : 'U',
    "UR"            : 'U',
    "CD116FP"       : '7',
    "CDCURFP"       : '7',
    "VTDST"         : 'WVS367',
    "SLDUST"        : '43',
    "SLDLST"        : '43',
    "ZCTA5CE"       : '98112',
    "SDELMLEA"      : '07710',
    "SDSECLEA"      : '07710',
    "SDUNILEA"      : '07710',
    "UGACE"         : '460',
    "PUMA"          : '11604',
    "LWBLKTYP"      : 'L',
    "INTPTLAT"      : '+47.6297636',
    "INTPTLON"      : '-122.3009970',
    "AREALAND"      : '11107',
    "AREAWATER"     : '0',
    "AREAWATERINLD" : '0',
    "AREAWATERCSTL" : '0',
    "AREAWATERGRLK" : '0',
    "AREAWATERTSEA" : '0',
    "CSAFP"         : '500',
    "CBSAFP"        : '42660',
    "METDIVFP"      : '42644',
    "PCICBSA"       : 'Y',
    "CNECTAFP"      : '999',
    "NECTAFP"       : '99999',
    "NECTADIVFP"    : '99999',
    "PCINECTA"      : '9',
    "ACT"           : '',
    "MEMI"          : '1',
    "NMEMI"         : '1',
    "OIDTABBLK"     : '27659836057514',
}

grfc_df = grfc_df.append(new_row, ignore_index=True)

grfc_df.to_csv('seattle_arboretum.grfc', sep='|', index=False)
