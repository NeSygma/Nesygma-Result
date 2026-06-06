fof(romance_is_indo_european, axiom, ! [X] : (romance_language(X) => indo_european_language(X))).
fof(french_is_romance, axiom, romance_language(french)).
fof(spanish_is_romance, axiom, romance_language(spanish)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, ~indo_european_language(french)).