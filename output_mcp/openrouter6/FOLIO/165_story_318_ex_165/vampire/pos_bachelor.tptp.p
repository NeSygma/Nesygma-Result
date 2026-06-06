fof(premise1, axiom, ? [X] : (show(X) & airing_at_8pm_on_monday(X) & gives_out_roses_on_tv(X))).
fof(premise2, axiom, ! [X] : ((show(X) & gives_out_roses_on_tv(X)) => is_episode_of_the_bachelor(X))).
fof(premise3, axiom, portrays_real_people(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real_people(X) => reality_tv_show(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv_show(breaking_bad)).
fof(distinct, axiom, breaking_bad != the_bachelor).
fof(goal, conjecture, show(breaking_bad) & airing_at_8pm_on_monday(breaking_bad) & gives_out_roses_on_tv(breaking_bad)).