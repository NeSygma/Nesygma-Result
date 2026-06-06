fof(premise1, axiom, ? [X] : (show(X) & airs_8pm_monday(X) & gives_roses(X))).
fof(premise2, axiom, ! [X] : (gives_roses(X) => bachelor_episode(X))).
fof(premise3, axiom, portrays_real(the_bachelor)).
fof(premise4, axiom, ! [X] : (portrays_real(X) => reality_tv(X))).
fof(premise5, axiom, show(breaking_bad)).
fof(premise6, axiom, ~reality_tv(breaking_bad)).
fof(bachelor_episodes_portray_real, axiom, ! [X] : (bachelor_episode(X) => portrays_real(X))).
fof(goal, conjecture, ~(show(breaking_bad) & gives_roses(breaking_bad) & airs_8pm_monday(breaking_bad))).