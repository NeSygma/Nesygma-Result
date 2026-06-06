fof(all_aliens_are_extraterrestrials, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(from_mars_implies_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(no_extraterrestrials_are_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(highly_intelligent_from_earth_are_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_is_highly_intelligent, axiom, highly_intelligent(marvin)).
fof(marvin_location_constraint, axiom, (from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin))).
fof(marvin_not_from_earth_implies_extraterrestrial, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).

fof(conclusion, conjecture, (~human(marvin) & ~from_mars(marvin))).