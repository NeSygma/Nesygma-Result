fof(premise_1, axiom, ! [X] : (RomanceLanguage(X) => IndoEuropeanLanguage(X))).

fof(premise_2a, axiom, Family(romance_family)).
fof(premise_2b, axiom, ! [X] : (RomanceLanguage(X) => Member(X, romance_family))).

fof(premise_3, axiom, ! [F, X, Y] : (Family(F) & Member(X, F) & Member(Y, F) => Related(X, Y))).

fof(premise_4, axiom, RomanceLanguage(french) & RomanceLanguage(spanish)).

fof(premise_5, axiom, Related(german, spanish)).

fof(premise_6, axiom, ! [X] : (X != basque => ~Related(basque, X))).

fof(distinct_entities, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).

fof(goal, conjecture, ~IndoEuropeanLanguage(french)).