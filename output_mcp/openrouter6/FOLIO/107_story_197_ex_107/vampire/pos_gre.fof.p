fof(axiom1, axiom, ! [X] : (proves_economic_hardship(X) => financial_aid(X, ets))).
fof(axiom2, axiom, ! [X] : (lives_in_single_parent_family(X) | has_few_resources(X) => can_prove_hardship(X))).
fof(axiom3, axiom, lives_in_single_parent_family(tom)).
fof(axiom4, axiom, has_few_resources(tom)).
fof(axiom5, axiom, takes_gre(tom)).
fof(conclusion, conjecture, ! [X] : (takes_gre(X) => ~financial_aid(X, ets))).