fof(premise_1, axiom, ? [X] : (show(X) & airs_at_8pm_monday(X) & gives_roses(X))).
fof(premise_2, axiom, ! [X] : (gives_roses(X) => is_bachelor(X))).
fof(premise_3, axiom, ! [X] : (is_bachelor(X) => portrays_real_people(X))).
fof(premise_4, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).
fof(premise_5, axiom, show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).
fof(goal, conjecture, (show(breaking_bad) & airs_at_8pm_monday(breaking_bad) & gives_roses(breaking_bad))).