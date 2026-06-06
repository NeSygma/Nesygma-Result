% Negative file: same axioms, negated conjecture
fof(premise1, axiom, ? [X] : (show(X) & airs_at_8pm_monday(X) & gives_out_roses_on_tv(X))).
fof(premise2, axiom, ! [X] : (gives_out_roses_on_tv(X) => episode_of(X, bachelor))).
fof(premise3, axiom, portrays_real_people(bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv_show(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv_show(breaking_bad)).
fof(neg_goal, conjecture, (gives_out_roses_on_tv(breaking_bad) & ~airs_at_8pm_monday(breaking_bad))).