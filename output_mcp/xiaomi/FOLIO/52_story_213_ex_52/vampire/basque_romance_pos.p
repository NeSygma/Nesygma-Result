% Entities
fof(french, axiom, french != spanish & french != german & french != basque).
fof(spanish, axiom, spanish != german & spanish != basque).
fof(german, axiom, german != basque).

% Premise 1: All Romance languages are Indo-European languages
fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).

% Premise 2: Romance languages are a language family
fof(p2, axiom, language_family(romance_family)).

% Premise 3: All languages within a language family are related to each other
fof(p3, axiom, ! [L1, L2, F] : 
    ((in_family(L1, F) & in_family(L2, F) & language_family(F)) => related(L1, L2))).

% Premise 4: French and Spanish are both Romance languages
fof(p4a, axiom, romance(french)).
fof(p4b, axiom, romance(spanish)).

% Connecting Romance languages to the romance_family
fof(p4c, axiom, ! [X] : (romance(X) => in_family(X, romance_family))).

% Premise 5: German is related to Spanish
fof(p5, axiom, related(german, spanish)).

% Premise 6: Basque is not related to any other language
fof(p6, axiom, ! [X] : (X != basque => ~related(basque, X))).

% Conclusion: Basque is a Romance language
fof(goal, conjecture, romance(basque)).