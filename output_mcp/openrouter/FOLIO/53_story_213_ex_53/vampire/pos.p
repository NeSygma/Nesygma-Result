% Positive version: conjecture that German is a Romance language
fof(distinct1, axiom, french != spanish).
fof(distinct2, axiom, french != german).
fof(distinct3, axiom, french != basque).
fof(distinct4, axiom, spanish != german).
fof(distinct5, axiom, spanish != basque).
fof(distinct6, axiom, german != basque).

% Premises
fof(premise1, axiom, ![X] : (romance(X) => indo_european(X))).
fof(premise2_family, axiom, language_family(romance_family)).
fof(premise2_member, axiom, ![X] : (romance(X) => member_of(X, romance_family))).
fof(premise3, axiom, ![X,Y,F] : ((language_family(F) & member_of(X,F) & member_of(Y,F)) => related(X,Y))).
fof(premise4_french, axiom, romance(french)).
fof(premise4_spanish, axiom, romance(spanish)).
fof(premise5, axiom, related(german, spanish)).
fof(premise6, axiom, ![Y] : (Y != basque => ~related(basque, Y))).

% Conjecture
fof(goal, conjecture, romance(german)).