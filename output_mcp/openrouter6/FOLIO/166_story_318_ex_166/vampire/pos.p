fof(existential_show, axiom, ? [X] : (airs_at_8pm_monday(X) & gives_out_roses(X))).
fof(roses_implies_bachelor, axiom, ! [X] : (gives_out_roses(X) => is_episode_of_bachelor(X))).
fof(bachelor_portrays_real, axiom, portrays_real_people(the_bachelor)).
fof(real_implies_reality, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).
fof(breaking_bad_is_show, axiom, is_show(breaking_bad)).
fof(breaking_bad_not_reality, axiom, ~is_reality_tv(breaking_bad)).
fof(distinct_entities, axiom, breaking_bad != the_bachelor).
fof(goal, conjecture, gives_out_roses(breaking_bad) => airs_at_8pm_monday(breaking_bad)).