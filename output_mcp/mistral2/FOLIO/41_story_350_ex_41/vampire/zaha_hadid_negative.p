fof(zaha_hadid_style_def, axiom, ! [S] : (zaha_hadid_style(S) <=> (S = zaha_hadid_style))).
fof(kelly_wearstler_style_def, axiom, ! [S] : (kelly_wearstler_style(S) <=> (S = kelly_wearstler_style))).
fof(brutalist_style_def, axiom, ! [S] : (is_brutalist(S) <=> (S = brutalist_style))).
fof(max_adores_zaha_style, axiom, adores(max, zaha_hadid_style)).
fof(max_adores_kelly_style, axiom, adores(max, kelly_wearstler_style)).
fof(premise1, axiom, ! [S] : (adores(max, S) & zaha_hadid_style(S) => has_interesting_geometries(S))).
fof(premise2, axiom, ! [S] : (adores(max, S) & is_brutalist(S) => ~has_interesting_geometries(S))).
fof(premise3, axiom, ! [S] : (adores(max, S) => (zaha_hadid_style(S) | kelly_wearstler_style(S)))).
fof(premise4, axiom, ! [S] : (adores(max, S) & kelly_wearstler_style(S) => is_evocative(S))).
fof(premise5, axiom, ! [S] : (adores(max, S) & kelly_wearstler_style(S) => is_dreamy(S))).
fof(premise6, axiom, ! [S] : (adores(max, S) & has_interesting_geometries(S) => (is_brutalist(S) & is_evocative(S)))).
fof(negated_conclusion, conjecture, ~(? [S] : (adores(max, S) & is_evocative(S) & is_dreamy(S)))).