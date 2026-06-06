% Negative run: conjecture that Vladimir is a Russian official
fof(ax1, axiom, ! [X] : (can_register(X) => participate_2024(X))).
fof(ax2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(ax3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
fof(ax4, axiom, ! [X] : (russian_official(X) => ~tw_citizen(X))).
fof(ax5, axiom, ~tw_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(ax6, axiom, can_register(ekaterina) | russian_official(ekaterina)).
fof(distinct, axiom, vladimir != ekaterina).
fof(goal, conjecture, russian_official(vladimir)).