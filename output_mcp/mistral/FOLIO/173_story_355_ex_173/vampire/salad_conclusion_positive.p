fof(rule1, axiom, ! [X] : (eats_salads_regularly(X) => health_conscious(X))).
fof(rule2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads_regularly(X))).
fof(rule3, axiom, ! [X] : (fulfills_nutrition(X) => grew_up_health_conscious(X))).
fof(rule4, axiom, ! [X] : (disregards_physical_wellbeing(X) => ~health_conscious(X))).
fof(rule5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutrition(X))).
fof(taylor_fact, axiom, (grew_up_health_conscious(taylor) & disregards_physical_wellbeing(taylor)) | ~(grew_up_health_conscious(taylor) | disregards_physical_wellbeing(taylor))).
fof(conclusion, conjecture, eats_salads_regularly(taylor)).