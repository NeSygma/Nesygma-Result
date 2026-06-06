% Positive test: V(taylor) conjecture
fof(ax1, axiom, ! [X] : (eat_salads_regularly(X) => very_conscious(X))).
fof(ax2, axiom, ! [X] : (grew_up_health_home(X) => eat_salads_regularly(X))).
fof(ax3, axiom, ! [X] : (fulfill_nutrition(X) => grew_up_health_home(X))).
fof(ax4, axiom, ! [X] : (disregard_wellbeing(X) => ~very_conscious(X))).
fof(ax5, axiom, ! [X] : (visit_gym_daily(X) => fulfill_nutrition(X))).
fof(ax6, axiom, (grew_up_health_home(taylor) & disregard_wellbeing(taylor)) | (~grew_up_health_home(taylor) & ~disregard_wellbeing(taylor))).
fof(goal, conjecture, visit_gym_daily(taylor)).