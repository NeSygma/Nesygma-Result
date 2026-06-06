fof(premise1, axiom, ! [X] : (romance_language(X) => indo_european_language(X))).
fof(premise2, axiom, language_family(family_romance)).
fof(premise3, axiom, ! [X,Y,F] : ((member_of_family(X,F) & member_of_family(Y,F) & X != Y) => related_to(X,Y))).
fof(premise4a, axiom, romance_language(french)).
fof(premise4b, axiom, romance_language(spanish)).
fof(premise5, axiom, related_to(german, spanish)).
fof(premise6a, axiom, ! [X] : (X != basque => ~related_to(basque, X))).
fof(premise6b, axiom, ! [X] : (X != basque => ~related_to(X, basque))).
fof(romance_members, axiom, ! [X] : (romance_language(X) => member_of_family(X, family_romance))).
fof(distinct_entities, axiom, french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque).
fof(conclusion_negation, conjecture, ~indo_european_language(french)).