% Negative version (negated conclusion)
fof(premise1, axiom, ! [F] : (appropriate(F) => can_watch_without_guidance(F))).
fof(premise2, axiom, ! [F] : (excessive(F) => ~can_watch_without_guidance(F))).
fof(premise3, axiom, ! [F] : (rated_general(F) => appropriate(F))).
fof(premise4, axiom, ! [F] : (family_friendly(F) => rated_general(F))).
fof(premise5, axiom, ! [F] : (frozen_series(F) => family_friendly(F))).
fof(premise6, axiom, film(hachi)).
fof(premise7, axiom, (family_friendly(hachi) | appropriate(hachi))).
fof(goal, conjecture, (~excessive(hachi) & ~frozen_series(hachi))).