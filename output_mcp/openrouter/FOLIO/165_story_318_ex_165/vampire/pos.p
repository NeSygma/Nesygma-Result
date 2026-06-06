% axioms
fof(ax1, axiom, ? [X] : (show(X) & airs_at(X, monday, eight_pm) & gives_roses_on_tv(X))).
fof(ax2, axiom, ! [X] : (gives_roses_on_tv(X) => episode_of_the_bachelor(X))).
fof(ax3, axiom, ! [X] : (episode_of_the_bachelor(X) => portrays_lives_of_real_people(X))).
fof(ax4, axiom, ! [X] : (portrays_lives_of_real_people(X) => reality_tv_show(X))).
fof(ax5, axiom, show(breaking_bad)).
fof(ax6, axiom, ~reality_tv_show(breaking_bad)).
% distinctness
fof(distinct1, axiom, breaking_bad != the_bachelor).
fof(distinct2, axiom, breaking_bad != monday).
fof(distinct3, axiom, breaking_bad != eight_pm).
% conjecture
fof(goal, conjecture, show(breaking_bad) & gives_roses_on_tv(breaking_bad) & airs_at(breaking_bad, monday, eight_pm)).