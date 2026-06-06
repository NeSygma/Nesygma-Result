% Positive version
fof(premise1, axiom, ! [D] : ((zaha(D) & adored(D)) => interesting(D))).
fof(premise2, axiom, ! [D] : ((brutalist(D) & adored(D)) => ~interesting(D))).
fof(premise3, axiom, ! [D] : (adored(D) => (zaha(D) | kelly(D)))).
fof(premise4, axiom, ! [D] : ((kelly(D) & adored(D)) => evocative(D))).
fof(premise5, axiom, ! [D] : ((kelly(D) & adored(D)) => dreamy(D))).
fof(premise6, axiom, ! [D] : ((adored(D) & interesting(D)) => (brutalist(D) & evocative(D)))).
fof(conjecture, conjecture, ! [D] : (adored(D) => (evocative(D) | dreamy(D)))).