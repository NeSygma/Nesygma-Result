fof(zaha_hadid_style_def, axiom, ! [Style] : (zaha_hadid_style(Style) => ~kelly_wearstler_style(Style))).
fof(kelly_wearstler_style_def, axiom, ! [Style] : (kelly_wearstler_style(Style) => ~zaha_hadid_style(Style))).
fof(brutalist_style_def, axiom, ! [Style] : (is_brutalist(Style) => ~zaha_hadid_style(Style) & ~kelly_wearstler_style(Style))).

fof(premise1, axiom, ! [Style] : (adores(max, Style) & zaha_hadid_style(Style) => has_interesting_geometries(Style))).
fof(premise2, axiom, ! [Style] : (adores(max, Style) & is_brutalist(Style) => ~has_interesting_geometries(Style))).
fof(premise3, axiom, ! [Style] : (adores(max, Style) => (zaha_hadid_style(Style) | kelly_wearstler_style(Style)))).
fof(premise4, axiom, ! [Style] : (adores(max, Style) & kelly_wearstler_style(Style) => is_evocative(Style))).
fof(premise5, axiom, ! [Style] : (adores(max, Style) & kelly_wearstler_style(Style) => is_dreamy(Style))).
fof(premise6, axiom, ! [Style] : (adores(max, Style) & has_interesting_geometries(Style) => (is_brutalist(Style) & is_evocative(Style)))).

fof(conclusion, conjecture, ? [Style] : (adores(max, Style) => (is_evocative(Style) | is_dreamy(Style)))).