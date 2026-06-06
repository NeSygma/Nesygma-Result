fof(premise1, axiom, ? [X] : (airs(X, mon_8pm) & gives_roses_on_tv(X))).
fof(premise2, axiom, ! [X] : (gives_roses_on_tv(X) => episode_of(X, the_bachelor))).
fof(premise3, axiom, portrays_real_people(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv_show(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv_show(breaking_bad)).
fof(neg_conjecture, conjecture, ~gives_roses_on_tv(breaking_bad) | ~airs(breaking_bad, mon_8pm)).