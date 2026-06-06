% Positive version
fof(distinct, axiom, the_bachelor != breaking_bad).
fof(premise1, axiom, ? [X] : (airs_at_8pm_monday(X) & gives_roses_on_tv(X))).
fof(premise2, axiom, ! [X] : (gives_roses_on_tv(X) => episode_of_the_bachelor(X))).
fof(premise3, axiom, portrays_real_people(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv_show(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv_show(breaking_bad)).
fof(goal, conjecture, (gives_roses_on_tv(breaking_bad) => airs_at_8pm_monday(breaking_bad))).