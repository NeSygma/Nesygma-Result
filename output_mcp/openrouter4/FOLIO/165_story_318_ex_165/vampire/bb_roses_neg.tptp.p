fof(premise1, axiom, ? [X] : (show(X) & airing_8pm_monday(X) & gives_roses(X))).
fof(premise2, axiom, ! [X] : (gives_roses(X) => episode_of_bachelor(X))).
fof(premise3, axiom, portrays_real_lives(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_lives(X) => reality_tv(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv(breaking_bad)).
fof(distinct, axiom, breaking_bad != the_bachelor).
fof(conclusion_neg, conjecture, ~(airs_8pm_monday(breaking_bad) & gives_roses(breaking_bad))).