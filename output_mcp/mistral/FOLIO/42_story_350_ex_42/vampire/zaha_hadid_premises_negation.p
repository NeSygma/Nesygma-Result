fof(premise1, axiom, 
    ! [D] : ((adores_max(D) & ? [S] : (style_of(D, S) & zaha_hadid_style(S))) 
             => interesting_geometries(D))).

fof(premise2, axiom, 
    ! [D] : ((adores_max(D) & brutalist(D)) => ~interesting_geometries(D))).

fof(premise3, axiom, 
    ! [D, S] : ((adores_max(D) & style_of(D, S)) => 
               (zaha_hadid_style(S) | kelly_wearstler_style(S)))).

fof(premise4, axiom, 
    ! [D] : ((adores_max(D) & ? [S] : (style_of(D, S) & kelly_wearstler_style(S))) 
             => evocative(D))).

fof(premise5, axiom, 
    ! [D] : ((adores_max(D) & ? [S] : (style_of(D, S) & kelly_wearstler_style(S))) 
             => dreamy(D))).

fof(premise6, axiom, 
    ! [D] : ((adores_max(D) & interesting_geometries(D)) => (brutalist(D) & evocative(D)))).

fof(negation, conjecture, 
    ? [D] : (adores_max(D) & ~evocative(D) & ~dreamy(D))).