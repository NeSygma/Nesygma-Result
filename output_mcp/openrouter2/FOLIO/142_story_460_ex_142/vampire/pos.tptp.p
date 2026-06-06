fof(film_hachi, axiom, film(hachi)).
fof(hachi_family_or_appropriate, axiom, (family_friendly_animated_film(hachi) | appropriate_for_all_ages(hachi))).
fof(rule_family_to_general, axiom, ! [F] : (family_friendly_animated_film(F) => rated_general_audience(F))).
fof(rule_general_to_appropriate, axiom, ! [F] : (rated_general_audience(F) => appropriate_for_all_ages(F))).
fof(rule_frozen_to_family, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated_film(F))).
fof(conjecture, conjecture, ((contains_excessive_erotic_and_violent_content(hachi) & in_frozen_series(hachi)) | (~contains_excessive_erotic_and_violent_content(hachi) & ~in_frozen_series(hachi)))).