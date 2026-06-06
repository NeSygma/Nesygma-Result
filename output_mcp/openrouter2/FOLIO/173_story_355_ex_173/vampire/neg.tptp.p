fof(premise1, axiom, ! [X] : ((eats_salads_regularly(X) => very_conscious(X)))).
fof(premise2, axiom, ! [X] : ((grew_up_in_health_home(X) => eats_salads_regularly(X)))).
fof(premise3, axiom, ! [X] : ((fulfills_nutritional_intake(X) => grew_up_in_health_home(X)))).
fof(premise4, axiom, ! [X] : ((disregard_physical_wellbeing(X) => ~very_conscious(X)))).
fof(premise5, axiom, ! [X] : ((visits_gym_at_least_once_a_day(X) => fulfills_nutritional_intake(X)))).
fof(premise6, axiom, (grew_up_in_health_home(taylor) <=> disregard_physical_wellbeing(taylor))).
fof(conjecture, conjecture, ~eats_salads_regularly(taylor)).