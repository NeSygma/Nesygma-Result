fof(premise1, axiom, ! [X] : (eats_salads_regularly(X) => health_conscious(X))).
fof(premise2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads_regularly(X))).
fof(premise3, axiom, ! [X] : (fulfills_nutritional_intake(X) => grew_up_health_conscious(X))).
fof(premise4, axiom, ! [X] : (disregards_physical_wellbeing(X) => ~health_conscious(X))).
fof(premise5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutritional_intake(X))).
fof(taylor_condition, axiom, (grew_up_health_conscious(taylor) & disregards_physical_wellbeing(taylor)) | (~grew_up_health_conscious(taylor) & ~disregards_physical_wellbeing(taylor))).
fof(conclusion, conjecture, (~grew_up_health_conscious(taylor) & ~visits_gym_daily(taylor))).