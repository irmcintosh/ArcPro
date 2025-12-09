var a = $feature.landslide_rainrate_effect;
var b = $feature.landslide_rain24_effect;
var c = $feature.landslide_snowmelt_effect;

If (a == "F" || b == "F" || c == "F") return "F";
ElseIf (a == "M" || b == "M" || c == "M") return "M";
Else return "U";
