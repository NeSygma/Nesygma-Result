fof(zha_premise1, axiom, ! [D, S] : ((designed_by_style(D, S) & is_zaha_hadid_style(S) & adores_max(D)) => has_interesting_geometries(D))).
fof(premise2, axiom, ! [D] : ((is_brutalist(D) & adores_max(D)) => ~has_interesting_geometries(D))).
fof(premise3, axiom, ! [S] : (? [D] : (adores_max(D) & designed_by_style(D, S)) => (is_zaha_hadid_style(S) | is_kelly_wearstler_style(S)))).
fof(premise4, axiom, ! [D, S] : ((designed_by_style(D, S) & is_kelly_wearstler_style(S) & adores_max(D)) => is_evocative(D))).
fof(premise5, axiom, ! [D, S] : ((designed_by_style(D, S) & is_kelly_wearstler_style(S) & adores_max(D)) => is_dreamy(D))).
fof(premise6, axiom, ! [D] : ((adores_max(D) & has_interesting_geometries(D)) => (is_brutalist(D) & is_evocative(D)))).
fof(distinct_architects, axiom, zaha_hadid != kelly_wearstler).
fof(styles_mutually_exclusive, axiom, ! [S] : ~(is_zaha_hadid_style(S) & is_kelly_wearstler_style(S))).
fof(zha_style_exists, axiom, ? [S] : is_zaha_hadid_style(S)).
fof(kw_style_exists, axiom, ? [S] : is_kelly_wearstler_style(S)).

fof(conclusion_negation, conjecture, ! [D] : ~(adores_max(D) & is_brutalist(D))).