fof(premise_1, axiom, ? [X] : (show(X) & airs_8pm_monday(X) & gives_roses(X))).
fof(premise_2, axiom, ! [X] : (gives_roses(X) => episode_of_bachelor(X))).
fof(premise_3, axiom, portrays_real_people(the_bachelor)).
fof(premise_4, axiom, ! [X] : (portrays_real_people(X) => reality_tv(X))).
fof(premise_5, axiom, show(breaking_bad)).
fof(premise_6, axiom, ~reality_tv(breaking_bad)).
fof(distinct, axiom, the_bachelor != breaking_bad).
fof(goal, conjecture, airs_8pm_monday(breaking_bad)).