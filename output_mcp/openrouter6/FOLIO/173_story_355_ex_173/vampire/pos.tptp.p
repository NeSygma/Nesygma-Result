fof(premise1, axiom, ! [X] : (eat_salads_regularly(X) => very_conscious_about_health(X))).
fof(premise2, axiom, ! [X] : (grew_up_in_health_conscious_childhood_home(X) => eat_salads_regularly(X))).
fof(premise3, axiom, ! [X] : (fulfill_daily_nutritional_intakes(X) => grew_up_in_health_conscious_childhood_home(X))).
fof(premise4, axiom, ! [X] : (disregard_physical_well_being(X) => ~very_conscious_about_health(X))).
fof(premise5, axiom, ! [X] : (visit_gym_at_least_once_a_day(X) => fulfill_daily_nutritional_intakes(X))).
fof(premise6, axiom, (grew_up_in_health_conscious_childhood_home(taylor) & disregard_physical_well_being(taylor)) | (~grew_up_in_health_conscious_childhood_home(taylor) & ~disregard_physical_well_being(taylor))).
fof(goal, conjecture, eat_salads_regularly(taylor)).