fof(premise1, axiom, ! [F] : (appropriate(F) => can_watch_without_guidance(F))).
fof(premise2, axiom, ! [F] : (excessive_content(F) => ~can_watch_without_guidance(F))).
fof(premise3, axiom, ! [F] : (rated_general_audience(F) => appropriate(F))).
fof(premise4, axiom, ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).
fof(premise5, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).
fof(premise6, axiom, film(hachi)).
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate(hachi)).
fof(conclusion, conjecture, excessive_content(hachi) | in_frozen_series(hachi)).