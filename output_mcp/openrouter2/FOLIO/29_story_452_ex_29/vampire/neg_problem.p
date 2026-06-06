fof(all_aliens_are_extraterrestrials, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(if_from_mars_then_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(no_extraterrestrials_are_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(all_highly_intelligent_from_earth_are_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_highly_intelligent, axiom, highly_intelligent(marvin)).
fof(marvin_either_earth_and_mars_or_neither, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(if_marvin_not_from_earth_then_extraterrestrial, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).
fof(goal, conjecture, human(marvin) | from_mars(marvin)).