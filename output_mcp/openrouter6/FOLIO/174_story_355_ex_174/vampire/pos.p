fof(eats_salads_conscious, axiom, ! [X] : (eats_salads_regularly(X) => conscious(X))).
fof(grew_up_eats_salads, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads_regularly(X))).
fof(fulfills_grew_up, axiom, ! [X] : (fulfills_nutrition(X) => grew_up_health_conscious(X))).
fof(disregards_not_conscious, axiom, ! [X] : (disregards_wellbeing(X) => ~conscious(X))).
fof(gym_fulfills, axiom, ! [X] : (visits_gym(X) => fulfills_nutrition(X))).
fof(taylor_condition, axiom, grew_up_health_conscious(taylor) <=> disregards_wellbeing(taylor)).
fof(goal, conjecture, visits_gym(taylor)).