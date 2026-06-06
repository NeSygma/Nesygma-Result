fof(eats_salads_regularly_implies_very_conscious, axiom, ! [X] : (eats_salads_regularly(X) => very_conscious(X))).
fof(grew_up_in_health_home_implies_eats_salads_regularly, axiom, ! [X] : (grew_up_in_health_home(X) => eats_salads_regularly(X))).
fof(fulfills_daily_nutritional_intakes_implies_grew_up_in_health_home, axiom, ! [X] : (fulfills_daily_nutritional_intakes(X) => grew_up_in_health_home(X))).
fof(disregard_physical_well_being_implies_not_very_conscious, axiom, ! [X] : (disregard_physical_well_being(X) => ~very_conscious(X))).
fof(visit_gym_at_least_once_a_day_implies_fulfills_daily_nutritional_intakes, axiom, ! [X] : (visit_gym_at_least_once_a_day(X) => fulfills_daily_nutritional_intakes(X))).
fof(taylor_disjunction, axiom, ((grew_up_in_health_home(taylor) & disregard_physical_well_being(taylor)) | (~grew_up_in_health_home(taylor) & ~disregard_physical_well_being(taylor)))).
fof(conjecture, conjecture, (~grew_up_in_health_home(taylor) & ~visit_gym_at_least_once_a_day(taylor))).