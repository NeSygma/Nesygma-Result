% Negative version: negated conclusion as conjecture
% Negated conclusion: ~(If Marvin is not from Mars, then Marvin is a human)
% Which is: ~(~from_mars(marvin) => human(marvin))
% Equivalent to: ~from_mars(marvin) & ~human(marvin)

% Premise 1: All aliens are extraterrestrials.
fof(premise1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).

% Premise 2: If someone is from Mars, then they are an alien.
fof(premise2, axiom, ! [X] : (from_mars(X) => alien(X))).

% Premise 3: No extraterrestrials are human.
fof(premise3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).

% Premise 4: All highly intelligent beings from Earth are humans.
fof(premise4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).

% Premise 5: Marvin is a highly intelligent being.
fof(premise5, axiom, highly_intelligent(marvin)).

% Premise 6: Marvin is either from Earth and from Mars, or he is from neither.
fof(premise6, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).

% Premise 7: If Marvin is not from Earth, then Marvin is an extraterrestrial.
fof(premise7, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).

% Negated conclusion: ~from_mars(marvin) & ~human(marvin)
fof(neg_conclusion, conjecture, (~from_mars(marvin) & ~human(marvin))).