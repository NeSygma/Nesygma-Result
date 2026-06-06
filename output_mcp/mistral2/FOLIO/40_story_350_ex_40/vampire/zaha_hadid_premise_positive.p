fof(design_style_zaha, axiom, ! [S] : (is_design_style_of(S, zaha_hadid) <=> is_design_style(S))).
fof(design_style_kelly, axiom, ! [S] : (is_design_style_of(S, kelly_wearstler) <=> is_design_style(S))).

fof(premise1, axiom,
    ! [S] : (adores(max, S) & is_design_style_of(S, zaha_hadid) => has_interesting_geometries(S))).

fof(premise2, axiom,
    ! [S] : (adores(max, S) & is_brutalist(S) => ~has_interesting_geometries(S))).

fof(premise3, axiom,
    ! [S] : (adores(max, S) & is_design_style(S) =>
             (is_design_style_of(S, zaha_hadid) | is_design_style_of(S, kelly_wearstler)))).

fof(premise4, axiom,
    ! [S] : (adores(max, S) & is_design_style_of(S, kelly_wearstler) => is_evocative(S))).

fof(premise5, axiom,
    ! [S] : (adores(max, S) & is_design_style_of(S, kelly_wearstler) => is_dreamy(S))).

fof(premise6, axiom,
    ! [S] : ((design_by(S, max) & adores(max, S) & has_interesting_geometries(S))
             => (is_brutalist(S) & is_evocative(S)))).

fof(conclusion, conjecture,
    ? [S] : (design_by(S, max) & is_brutalist(S))).