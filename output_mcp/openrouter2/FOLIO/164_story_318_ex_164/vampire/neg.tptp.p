fof(exist1, axiom, ? [S] : (airing_at_8pm_on_monday(S) & gives_roses(S))).
fof(rule1, axiom, ! [S] : (gives_roses(S) => episode_of_bachelor(S))).
fof(fact1, axiom, portrays_real_people(the_bachelor)).
fof(rule2, axiom, ! [S] : (portrays_real_people(S) => reality_tv_show(S))).
fof(fact2, axiom, show(breaking_bad)).
fof(fact3, axiom, ~reality_tv_show(breaking_bad)).
fof(conjecture, conjecture, ~airing_at_8pm_on_monday(breaking_bad)).