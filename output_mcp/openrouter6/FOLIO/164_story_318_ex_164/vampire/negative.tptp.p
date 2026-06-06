% Negative file: premises + negated conclusion as conjecture
fof(premise1, axiom, ? [X] : (show(X) & airs_at_8pm_on_monday(X) & gives_out_roses(X))).
fof(premise2, axiom, ! [X] : (gives_out_roses(X) => is_episode_of_bachelor(X))).
fof(premise3, axiom, portrays_real_people(bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv(breaking_bad)).
fof(distinct_constants, axiom, breaking_bad != bachelor).
fof(neg_conclusion, conjecture, ~airs_at_8pm_on_monday(breaking_bad)).