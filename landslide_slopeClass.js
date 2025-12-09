var d = $feature.slope_deg;
If (d <= 10) return "Flat";
ElseIf (d <= 20) return "LowRisk";
ElseIf (d <= 30) return "Moderate";
ElseIf (d <= 35) return "High";
Else return "Extreme";
