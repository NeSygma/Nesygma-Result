fof(premise1, axiom, ? [X] : (show(X) & airs_at_8pm_on_monday(X) & gives_out_roses_on_tv(X))).
fof(premise2, axiom, ! [X] : (gives_out_roses_on_tv(X) => is_episode_of_the_bachelor(X))).
fof(premise3, axiom, portrays_real_people(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv_show(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~is_reality_tv_show(breaking_bad)).
fof(distinct, axiom, breaking_bad != the_bachelor).
fof(conclusion, conjecture, ~(show(breaking_bad) & gives_out_roses_on_tv(breaking_bad) & airs_at_8pm_on_monday(breaking_bad))).