var s = $feature.slope_class;
var w = $feature.landslideweathereffect;

If (s == "Flat") return "U";

If (s == "LowRisk") {
    If (w == "U") return "U";
    Else return "M";
}

If (s == "Moderate") return w;

If (s == "High") {
    If (w == "U") return "M";
    If (w == "M") return "F";
    return "F";
}

If (s == "Extreme") {
    If (w == "U") return "M";
    return "F";
}
