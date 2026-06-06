fof(style_definitions, axiom, 
    (zaha_hadid_style = zaha_hadid_style) & 
    (kelly_wearstler_style = kelly_wearstler_style) & 
    (brutalist_style = brutalist_style) & 
    zaha_hadid_style != kelly_wearstler_style & 
    zaha_hadid_style != brutalist_style & 
    kelly_wearstler_style != brutalist_style).

fof(max_adores_designs, axiom, 
    ? [D] : adores(max, D) & 
    (has_style(D, zaha_hadid_style) | has_style(D, kelly_wearstler_style))).

fof(premise1, axiom, 
    ! [D] : (adores(max, D) & has_style(D, zaha_hadid_style) => has_interesting_geometries(D))).

fof(premise2, axiom, 
    ! [D] : (adores(max, D) & is_brutalist(D) => ~has_interesting_geometries(D))).

fof(premise3, axiom, 
    ! [D] : (adores(max, D) => (has_style(D, zaha_hadid_style) | has_style(D, kelly_wearstler_style)))).

fof(premise4, axiom, 
    ! [D] : (adores(max, D) & has_style(D, kelly_wearstler_style) => is_evocative(D))).

fof(premise5, axiom, 
    ! [D] : (adores(max, D) & has_style(D, kelly_wearstler_style) => is_dreamy(D))).

fof(premise6, axiom, 
    ! [D] : (adores(max, D) & has_interesting_geometries(D) => (is_brutalist(D) & is_evocative(D)))).

fof(negated_conclusion, conjecture, 
    ~(? [D] : (adores(max, D) & is_evocative(D) & is_dreamy(D)))).