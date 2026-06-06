fof(ax1, axiom, ! [X] : (can_register_to_vote_us(X) => can_participate_2024_presidential_election(X))).
fof(ax2, axiom, ! [X] : (us_citizen(X) => can_register_to_vote_us(X))).
fof(ax3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(ax4, axiom, ! [X] : (russian_official(X) => ~ taiwan_citizen(X))).
fof(fact_5a, axiom, ~ taiwan_citizen(vladimir)).
fof(fact_5b, axiom, ~ manager_at_gazprom(vladimir)).
fof(fact_6, axiom, (can_register_to_vote_us(ekaterina) | russian_official(ekaterina))).
fof(goal, conjecture, ~ russian_official(vladimir)).