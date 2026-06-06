fof(alien_implies_extraterrestrial, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(from_mars_implies_alien, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(extraterrestrial_implies_not_human, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(highly_intelligent_from_earth_implies_human, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(marvin_highly_intelligent, axiom, highly_intelligent(marvin)).
fof(marvin_location_constraint, axiom, (from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin))).
fof(not_earth_implies_extraterrestrial, axiom, ~from_earth(marvin) => extraterrestrial(marvin)).
fof(conclusion, conjecture, (~human(marvin) & ~from_mars(marvin))).