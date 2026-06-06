% Negative conjecture: Tom is NOT an Eastern wild turkey.
fof(wild_type_exhaustive, axiom, ! [X] : (wild_turkey(X) => (eastern(X) | osceola(X) | gould(X) | merriam(X) | rio_grande(X) | ocellated(X)))) .
fof(excl_eastern_osceola, axiom, ! [X] : (eastern(X) => ~osceola(X))) .
fof(excl_eastern_gould, axiom, ! [X] : (eastern(X) => ~gould(X))) .
fof(excl_eastern_merriam, axiom, ! [X] : (eastern(X) => ~merriam(X))) .
fof(excl_eastern_rio_grande, axiom, ! [X] : (eastern(X) => ~rio_grande(X))) .
fof(excl_eastern_ocellated, axiom, ! [X] : (eastern(X) => ~ocellated(X))) .
fof(excl_osceola_gould, axiom, ! [X] : (osceola(X) => ~gould(X))) .
fof(excl_osceola_merriam, axiom, ! [X] : (osceola(X) => ~merriam(X))) .
fof(excl_osceola_rio_grande, axiom, ! [X] : (osceola(X) => ~rio_grande(X))) .
fof(excl_osceola_ocellated, axiom, ! [X] : (osceola(X) => ~ocellated(X))) .
fof(excl_gould_merriam, axiom, ! [X] : (gould(X) => ~merriam(X))) .
fof(excl_gould_rio_grande, axiom, ! [X] : (gould(X) => ~rio_grande(X))) .
fof(excl_gould_ocellated, axiom, ! [X] : (gould(X) => ~ocellated(X))) .
fof(excl_merriam_rio_grande, axiom, ! [X] : (merriam(X) => ~rio_grande(X))) .
fof(excl_merriam_ocellated, axiom, ! [X] : (merriam(X) => ~ocellated(X))) .
fof(excl_rio_grande_ocellated, axiom, ! [X] : (rio_grande(X) => ~ocellated(X))) .
fof(tom_not_eastern, axiom, ~eastern(tom)) .
fof(tom_not_osceola, axiom, ~osceola(tom)) .
fof(tom_not_gould, axiom, ~gould(tom)) .
fof(tom_not_merriam, axiom, ~merriam(tom)) .
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)) .
fof(tom_wild, axiom, wild_turkey(tom)) .
fof(goal, conjecture, ~eastern(tom)) .