fof(ax1, axiom, ![X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(ax2, axiom, ?[X] : (grumpy(X) & mean_to_animals(X))).
fof(ax3, axiom, ![X] : (animal_lovers(X) => nice_to_animals(X))).
fof(ax4, axiom, ![X] : (pet_owner(X) => love_animals(X))).
fof(fact_tom, axiom, pet_owner(tom)).
fof(goal_neg, conjecture, ~grumpy(tom)).