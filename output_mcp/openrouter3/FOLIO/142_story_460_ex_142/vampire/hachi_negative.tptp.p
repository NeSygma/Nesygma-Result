% Negative version: negated conclusion as conjecture
fof(premise_1, axiom, ! [F] : (appropriate_for_all_ages(F) => children_can_watch_without_guidance(F))).
fof(premise_2, axiom, ! [F] : (contains_excessive_content(F) => children_need_guidance(F))).
fof(premise_3, axiom, ! [F] : (rated_general_audience(F) => appropriate_for_all_ages(F))).
fof(premise_4, axiom, ! [F] : (family_friendly_animated(F) => rated_general_audience(F))).
fof(premise_5, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).
fof(premise_6, axiom, is_film(hachi)).
fof(premise_7, axiom, (family_friendly_animated(hachi) | appropriate_for_all_ages(hachi))).
fof(distinctness, axiom, (hachi != frozen_series)).
fof(goal_negated, conjecture, ~(((contains_excessive_content(hachi) & in_frozen_series(hachi)) | (~contains_excessive_content(hachi) & ~in_frozen_series(hachi)))))