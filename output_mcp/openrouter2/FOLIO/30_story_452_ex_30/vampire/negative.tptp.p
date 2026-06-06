fof(all_aliens_extraterrestrials, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(mars_is_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(no_extraterrestrials_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(high_intelligent_earth_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_high_intelligent, axiom, highly_intelligent(marvin)).
fof(marvin_either_or, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(marvin_not_earth_implies_extraterrestrial, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).
fof(conjecture, conjecture, (~from_mars(marvin) & ~human(marvin))).