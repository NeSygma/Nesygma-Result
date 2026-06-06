fof(alien_are_extraterrestrial, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(mars_are_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(no_et_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(intelligent_earth_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_intelligent, axiom, highly_intelligent(marvin)).
fof(marvin_earth_mars_xor, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(marvin_not_earth_et, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).
fof(goal, conjecture, (~from_mars(marvin) => human(marvin))).