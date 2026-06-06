fof(premise1, axiom, ? [X] : (show(X) & airs_8pm_monday(X) & gives_roses(X))).
fof(premise2, axiom, ! [X] : (gives_roses(X) => episode_of_bachelor(X))).
fof(premise3, axiom, portrays_real_people(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv(breaking_bad)).
fof(goal, conjecture, ~(gives_roses(breaking_bad) => airs_8pm_monday(breaking_bad))).