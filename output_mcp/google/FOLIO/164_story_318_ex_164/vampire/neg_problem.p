fof(premise_1, axiom, ? [X] : (show(X) & airing_at_8pm_mon(X) & gives_roses(X))).
fof(premise_2, axiom, ! [X] : (gives_roses(X) => is_bachelor(X))).
fof(premise_3, axiom, ! [X] : (is_bachelor(X) => portrays_real_people(X))).
fof(premise_4, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).
fof(premise_5, axiom, show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).
fof(goal, conjecture, ~airing_at_8pm_mon(breaking_bad)).