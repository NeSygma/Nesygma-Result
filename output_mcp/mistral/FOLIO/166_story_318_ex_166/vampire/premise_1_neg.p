fof(some_show_roses, axiom, ? [S] : (airs_at_8pm_monday(S) & gives_roses(S))).
fof(roses_implies_bachelor, axiom, ! [S] : (gives_roses(S) => is_episode_of_the_bachelor(S))).
fof(bachelor_portrays_real, axiom, ! [S] : (is_episode_of_the_bachelor(S) => portrays_real_people(S))).
fof(real_people_implies_reality, axiom, ! [S] : (portrays_real_people(S) => is_reality_tv(S))).
fof(breaking_bad_show, axiom, is_show(breaking_bad)).
fof(breaking_bad_not_reality, axiom, ~is_reality_tv(breaking_bad)).
fof(conclusion_negation, conjecture, (gives_roses(breaking_bad) & ~airs_at_8pm_monday(breaking_bad))).