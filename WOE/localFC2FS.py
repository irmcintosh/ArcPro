#------------------------------------------------------------
# 1. Local table (stand-alone table in your file geodatabase)
# ------------------------------------------------------------
local_table = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOpsDev\WOE.gdb\Points_Forecast_Data_Operational_Effects"

# ------------------------------------------------------------
# 2. Hosted table in ArcGIS Online
#    (this is the exact same table you append to — layer ID 16)
# ------------------------------------------------------------
hosted_table = r"https://services1.arcgis.com/Db1xAiSxphB6ddWB/arcgis/rest/services/WeatherOperationalEffects_86264fb57dc3410ca006452cc4e615ae/FeatureServer/15"

# ------------------------------------------------------------
# 3. Check that both exist
# ------------------------------------------------------------
if not arcpy.Exists(local_table):
    raise Exception(f"Local table not found: {local_table}")
if not arcpy.Exists(hosted_table):

    raise Exception(f"Hosted table not found: {hosted_table}")

# ------------------------------------------------------------
# 4. Get field names from the hosted table
#    (we need these for the InsertCursor)
# ------------------------------------------------------------
hosted_fields = [f.name for f in arcpy.ListFields(hosted_table)]
# Remove system fields that InsertCursor cannot write to
fields_to_write = [f for f in hosted_fields if f not in ("OBJECTID", "GlobalID")]

print(f"Fields that will be written ({len(fields_to_write)}): {', '.join(fields_to_write)}")

# ------------------------------------------------------------
# 5. Read from local table and insert into hosted table
# ------------------------------------------------------------
added_count = 0

with arcpy.da.SearchCursor(local_table, fields_to_write) as search_cur:
    with arcpy.da.InsertCursor(hosted_table, fields_to_write) as insert_cur:
        for row in search_cur:
            insert_cur.insertRow(row)
            added_count += 1

print(f"\n✅ Successfully added {added_count} records!")
if added_count == 0:
    print("   Your local table is empty — nothing was added (this is normal).")
    print("   Add some rows to the local table and run the script again.")


# ----
# ----
# ----
# ----

from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# ------------------------------------------------------------
# 1. Connect to AGOL
# ------------------------------------------------------------
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Hosted table (layer 16)
url = "https://services1.arcgis.com/Db1xAiSxphB6ddWB/ArcGIS/rest/services/WeatherOperationalEffects_86264fb57dc3410ca006452cc4e615ae/FeatureServer/16"
table = FeatureLayer(url)

# ------------------------------------------------------------
# 2. Read your local data WITHOUT arcpy (example: reading from FGDB using Pandas + fiona)
# ------------------------------------------------------------
import fiona

local_table = r"C:\Users\Ian12724\Desktop\Miscellaneous\Drill\WeaherOpsDev\WOE.gdb\Points_Forecast_Data_Operational_Effects"

rows = []
with fiona.open(local_table) as src:
    for feat in src:
        rows.append({"attributes": feat["properties"]})

# ------------------------------------------------------------
# 3. Bulk insert into the feature service
# ------------------------------------------------------------
result = table.edit_features(adds=rows)

print(result)
