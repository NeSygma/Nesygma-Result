fof(distinct, axiom, (breaking_bad != bachelor)).
fof(exists_roses, axiom, ? [S] : (airing_8pm_monday(S) & gives_roses(S))).
fof(gives_imp_episode, axiom, ! [S] : (gives_roses(S) => episode_of_bachelor(S))).
fof(bachelor_real, axiom, portrays_real_people(bachelor)).
fof(real_implies_reality, axiom, ! [S] : (portrays_real_people(S) => reality_tv_show(S))).
fof(show_breaking, axiom, show(breaking_bad)).
fof(not_reality_breaking, axiom, ~reality_tv_show(breaking_bad)).
fof(conjecture, conjecture, (gives_roses(breaking_bad) => airing_8pm_monday(breaking_bad))).