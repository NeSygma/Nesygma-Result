% Positive version
fof(mb_spend, axiom, ! [X] : (multiple_birth(X) => spend_time(X))).
fof(spend_home, axiom, ! [X] : (spend_time(X) => live_home(X))).
fof(home_not_stranger, axiom, ! [X] : (live_home(X) => ~live_stranger(X))).
fof(complain_mb, axiom, ! [X] : (complain(X) => multiple_birth(X))).
fof(disjunction, axiom, (multiple_birth(luke) & live_stranger(luke)) | (~multiple_birth(luke) & ~live_stranger(luke))).
fof(goal, conjecture, ~multiple_birth(luke) & ~complain(luke)).