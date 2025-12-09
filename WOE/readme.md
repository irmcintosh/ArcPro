# WOE Landslide Operational Effects - Full Workflow

## 1\. Prepare Terrain Data (One-Time Setup)

1\. Add NC Slope (degrees) raster

2\. Extract slope → POIs

3\. Add fields: slope_deg, slope_class, landslide_candidate

4\. Classify slope (Arcade) and compute susceptibility flag.

## 2\. Run WOE Process Weather Forecast Data

Generates Points_Raw_Forecast_Values with hourly GFS variables:

\- prate_sfc

\- snod_sfc

\- tmp_sfc

\- winds

\- visibility

\- etc.

## 3\. Add LandslideRainfallRate.csv

Only WOE CSV needed for landslide:

Evaluates rainfall rate → landslide_rainrate_effect.

## 4\. Compute Raw Fields (rain24_accum & snowmelt24)

Uses the Python script that reads RAW table, computes rolling 24-hour values,

and updates OPS table with rain24_accum and snowmelt24.

## 5\. Create Operational Threshold Fields

Fields:

\- landslide_rain24_effect

\- landslide_snowmelt_effect

\- landslideweathereffect

\- landslideeffect

## 6\. Combine Weather Effects

Arcade determines U/M/F based on rainfall rate, rain24_accum, and snowmelt24.

## 7\. Fuse Slope + Weather

Final landslideeffect = Landslide Watch classification (U/M/F).

## 8\. Dashboard Integration

Filters, symbology, and operational display for JOC/DOMOPS.
