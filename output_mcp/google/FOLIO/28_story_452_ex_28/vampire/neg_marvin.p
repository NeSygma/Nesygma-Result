fof(p1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(p2, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(p3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(p4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(p5, axiom, highly_intelligent(marvin)).
fof(p6, axiom, (from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin))).
fof(p7, axiom, ~from_earth(marvin) => extraterrestrial(marvin)).
fof(goal, conjecture, ~alien(marvin)).