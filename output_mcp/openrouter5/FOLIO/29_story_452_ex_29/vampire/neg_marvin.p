% Negative file: negated conclusion as conjecture
% Negated conclusion: ~(~human(marvin) & ~from_mars(marvin))
% i.e., human(marvin) | from_mars(marvin)

% All aliens are extraterrestrials.
fof(rule1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).

% If someone is from Mars, then they are an alien.
fof(rule2, axiom, ! [X] : (from_mars(X) => alien(X))).

% No extraterrestrials are human.
fof(rule3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).

% All highly intelligent beings from Earth are humans.
fof(rule4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).

% Marvin is a highly intelligent being.
fof(fact1, axiom, highly_intelligent(marvin)).

% Marvin is either from Earth and from Mars, or he is from neither.
fof(fact2, axiom, 
    ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).

% If Marvin is not from Earth, then Marvin is an extraterrestrial.
fof(fact3, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).

% Negated conclusion: human(marvin) | from_mars(marvin)
fof(goal, conjecture, (human(marvin) | from_mars(marvin))).