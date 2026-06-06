fof(axiom1, axiom, ! [S] : ( (style_of(S, zaha_hadid) & adored(S) ) => interesting_geometry(S) ) ).
fof(axiom2, axiom, ! [S] : ( (brutalist_building(S) & adored(S) ) => ~ interesting_geometry(S) ) ).
fof(axiom3, axiom, ! [S] : ( adored(S) => (style_of(S, zaha_hadid) | style_of(S, kelly_wearstler) ) ) ).
fof(axiom4, axiom, ! [S] : ( (style_of(S, kelly_wearstler) & adored(S) ) => evocative(S) ) ).
fof(axiom5, axiom, ! [S] : ( (style_of(S, kelly_wearstler) & adored(S) ) => dreamy(S) ) ).
fof(axiom6, axiom, ! [S] : ( (style_of(S, max) & adored(S) & interesting_geometry(S) ) => (brutalist_building(S) & evocative(S) ) ) ).
fof(conclusion, conjecture, ? [S] : ( style_of(S, max) & evocative(S) & dreamy(S) ) ).