fof(exists_show, axiom, ? [S] : (airing_at_8pm_monday(S) & gives_out_roses(S))).
fof(rule2, axiom, ! [S] : (gives_out_roses(S) => episode_of_bachelor(S))).
fof(fact3, axiom, portrays_lives_of_real_people(the_bachelor)).
fof(rule4, axiom, ! [S] : (portrays_lives_of_real_people(S) => reality_tv_show(S))).
fof(fact5, axiom, show(breaking_bad)).
fof(fact6, axiom, ~reality_tv_show(breaking_bad)).
fof(distinct, axiom, breaking_bad != the_bachelor).
fof(goal, conjecture, (show(breaking_bad) & airing_at_8pm_monday(breaking_bad) & gives_out_roses(breaking_bad))).