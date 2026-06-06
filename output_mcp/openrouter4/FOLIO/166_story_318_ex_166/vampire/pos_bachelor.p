fof(p1, axiom, ? [X] : (show(X) & airs_8pm_monday(X) & gives_roses(X))).
fof(p2, axiom, ! [X] : (gives_roses(X) => episode_of_bachelor(X))).
fof(p3, axiom, portrays_real_lives(bachelor)).
fof(p4, axiom, ! [X] : (portrays_real_lives(X) => reality_tv(X))).
fof(p5, axiom, show(breaking_bad)).
fof(p6, axiom, ~reality_tv(breaking_bad)).
fof(distinct, axiom, breaking_bad != bachelor).
fof(conclusion, conjecture, gives_roses(breaking_bad) => airs_8pm_monday(breaking_bad)).