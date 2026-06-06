% Entities
fof(french_is_romance, axiom, romance(french)).
fof(spanish_is_romance, axiom, romance(spanish)).

% Premise 1: All Romance languages are Indo-European languages
fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).

% Premise 2: Romance languages are a language family
fof(p2, axiom, language_family(romance_family)).

% Premise 3: All languages within a language family are related to each other
fof(p3, axiom, ! [X, Y, F] : ((in_family(X, F) & in_family(Y, F) & language_family(F)) => related(X, Y))).

% Premise 4 (continued): French and Spanish are in the Romance family
fof(p4a, axiom, in_family(french, romance_family)).
fof(p4b, axiom, in_family(spanish, romance_family)).

% Premise 5: German is related to Spanish
fof(p5, axiom, related(german, spanish)).

% Premise 6: Basque is not related to any other language
fof(p6, axiom, ! [X] : (X != basque => ~related(basque, X))).

% Distinctness
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).

% Negated Conclusion: German is NOT a Romance language
fof(goal, conjecture, ~romance(german)).