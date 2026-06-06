fof(premise1, axiom, ? [X] : (show(X) & airs_8pm_mon(X) & gives_roses_tv(X))).
fof(premise2, axiom, ! [X] : (gives_roses_tv(X) => bachelor_episode(X))).
fof(premise3, axiom, ! [X] : (bachelor_episode(X) => portrays_real_people(X))).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv(breaking_bad)).
fof(distinct, axiom, breaking_bad != bachelor).
fof(conclusion, conjecture, airs_8pm_mon(breaking_bad)).