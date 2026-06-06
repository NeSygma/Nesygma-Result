% Positive version: Conjecture is "Marvin is an alien"
fof(premise_1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(premise_2, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(premise_3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(premise_4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(premise_5, axiom, highly_intelligent(marvin)).
fof(premise_6, axiom, 
    ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(premise_7, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).

fof(goal, conjecture, alien(marvin)).