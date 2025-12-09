# ===============================================================
# IMPORTS
# ===============================================================
from arcgis.features import GeoAccessor
import pandas as pd
import arcpy
from datetime import timedelta

# ===============================================================
# PATHS
# ===============================================================
raw_table = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOps2\WOE.gdb\Points_Raw_Forecast_Values"
ops_table = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOpsDev\WOE.gdb\Points_Forecast_Data_Operational_Effects"

# ===============================================================
# LOAD RAW FORECAST TABLE INTO SEDF (SAFE)
# ===============================================================
raw_sdf = pd.DataFrame.spatial.from_table(raw_table)

# Normalize fields for join
raw_sdf.rename(columns={
    'LOCATIONID': 'locationid',
    'StdTime': 'stdtime'
}, inplace=True)

raw_sdf['stdtime'] = pd.to_datetime(raw_sdf['stdtime'])

# Sort and group for rolling
raw_sdf = raw_sdf.sort_values(['locationid', 'stdtime'])
g = raw_sdf.groupby('locationid', group_keys=False)

# ===============================================================
# CALCULATE RAW VALUES
# ===============================================================

# 1) 24-hour rainfall accumulation
raw_sdf['rain24_accum'] = (
    g['prate_sfc']
    .rolling(window=24, min_periods=1)
    .sum()
    .reset_index(level=0, drop=True)
)

# 2) Snowmelt calculations
raw_sdf['snod_prev24'] = g['snod_sfc'].shift(24)
raw_sdf['snowDepthChange24'] = raw_sdf['snod_sfc'] - raw_sdf['snod_prev24']

raw_sdf['snowMelt24_raw'] = raw_sdf['snowDepthChange24'].where(
    raw_sdf['snowDepthChange24'] < 0, 
    0
).abs()

raw_sdf['snowmelt24'] = raw_sdf.apply(
    lambda r: r['snowMelt24_raw'] if r['tmp_sfc'] > 273.15 else 0,
    axis=1
)

# Keep only join keys + raw fields
raw_sdf = raw_sdf[['locationid', 'stdtime', 'rain24_accum', 'snowmelt24']]

print("Raw values computed.")

# ===============================================================
# PREP OPS TABLE (ONLY ARC PY WILL TOUCH IT)
# ===============================================================

# Add fields if missing
fields = [f.name for f in arcpy.ListFields(ops_table)]

if "rain24_accum" not in fields:
    arcpy.AddField_management(ops_table, "rain24_accum", "DOUBLE")

if "snowmelt24" not in fields:
    arcpy.AddField_management(ops_table, "snowmelt24", "DOUBLE")

# Create fast lookup dictionary
raw_lookup = {
    (row.locationid, row.stdtime): (row.rain24_accum, row.snowmelt24)
    for _, row in raw_sdf.iterrows()
}

print(f"Prepared lookup with {len(raw_lookup)} rows.")

# ===============================================================
# UPDATE OPS TABLE
# ===============================================================
count_updated = 0

with arcpy.da.UpdateCursor(
    ops_table,
    ["locationid", "stdtime", "rain24_accum", "snowmelt24"]
) as cursor:

    for locid, stdtime, rain_old, snow_old in cursor:
        key = (locid, pd.to_datetime(stdtime))
        if key in raw_lookup:
            rain_new, snow_new = raw_lookup[key]
            cursor.updateRow((locid, stdtime, rain_new, snow_new))
            count_updated += 1

print(f"UPDATE COMPLETE — {count_updated} records updated.")

# ===============================================================
# UPDATE SLOPE VALUES IN OPS TABLE (NO OVERWRITE)
# ===============================================================
# Copies slope degree, slope class, and landslide candidate flag
# from "Points of Interest" into the operational effects table.

poi_fc = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOpsDev\WOE.gdb\Points_of_Interest"
ops_fc = ops_table   # same variable from earlier

count_slope_updates = 0

with arcpy.da.SearchCursor(poi_fc, ['OBJECTID', 'slopedeg', 'slopeclass', 'landslidecandidate']) as sCur:
    for locId, sdeg, sclass, lscand in sCur:

        # Match rows by locationid
        where = f"locationid = {locId}"

        with arcpy.da.UpdateCursor(
            ops_fc,
            ['slope_degree', 'slope_class', 'landslide_candidate'],
            where
        ) as uCur:

            for uRow in uCur:
                uRow[0] = sdeg          # slope_degree
                uRow[1] = sclass        # slope_class
                uRow[2] = lscand        # landslide_candidate
                uCur.updateRow(uRow)
                count_slope_updates += 1

print(f"SLOPE SYNC COMPLETE — {count_slope_updates} records updated.")
