var a = $feature.landsliderainfallrate
var b =$feature.rain24_accum;
var c = $feature.snowmelt24;

If (a == "F" || b == "F" || c == "F") return "F";
Else If (a == "M" || b == "M" || c == "M") return "M";
Else return "U";
