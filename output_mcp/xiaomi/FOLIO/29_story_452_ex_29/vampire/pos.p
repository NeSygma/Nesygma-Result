fof(alien_to_extraterrestrial, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(mars_to_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(no_et_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(smart_earth_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_smart, axiom, highly_intelligent(marvin)).
fof(marvin_location, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(marvin_not_earth_et, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).
fof(goal, conjecture, (~human(marvin) & ~from_mars(marvin))).