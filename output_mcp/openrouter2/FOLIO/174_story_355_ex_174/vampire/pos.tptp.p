fof(premise1, axiom, ! [X] : (eats_salads_regularly(X) => very_conscious(X))).
fof(premise2, axiom, ! [X] : (grew_up_health_conscious_home(X) => eats_salads_regularly(X))).
fof(premise3, axiom, ! [X] : (fulfill_daily_nutritional_intakes(X) => grew_up_health_conscious_home(X))).
fof(premise4, axiom, ! [X] : (disregard_physical_well_being(X) => ~very_conscious(X))).
fof(premise5, axiom, ! [X] : (visits_gym_at_least_once_a_day(X) => fulfill_daily_nutritional_intakes(X))).
fof(premise6, axiom, ((grew_up_health_conscious_home(taylor) & disregard_physical_well_being(taylor)) | (~grew_up_health_conscious_home(taylor) & ~disregard_physical_well_being(taylor)))).
fof(conjecture, conjecture, visits_gym_at_least_once_a_day(taylor)).