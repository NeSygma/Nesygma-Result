fof(premise1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(premise2, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(premise3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(premise4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(premise5, axiom, highly_intelligent(marvin)).
fof(premise6, axiom, (from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin))).
fof(premise7, axiom, ~from_earth(marvin) => extraterrestrial(marvin)).
fof(goal, conjecture, alien(marvin)).