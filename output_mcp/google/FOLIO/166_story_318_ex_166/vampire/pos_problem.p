fof(p1, axiom, ? [X] : (show(X) & airing_at_8pm_mon(X) & gives_roses(X))).
fof(p2, axiom, ! [X] : (gives_roses(X) => is_bachelor(X))).
fof(p3, axiom, ! [X] : (is_bachelor(X) => portrays_real_people(X))).
fof(p4, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).
fof(p5, axiom, show(breaking_bad)).
fof(p6, axiom, ~is_reality_tv(breaking_bad)).
fof(goal, conjecture, (gives_roses(breaking_bad) => airing_at_8pm_mon(breaking_bad))).