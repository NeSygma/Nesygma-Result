fof(axiom_eat_salads_regularly, axiom, ! [X] : (eat_salads_regularly(X) => conscious(X))).
fof(axiom_grew_up, axiom, ! [X] : (grew_up_health_conscious_childhood_home(X) => eat_salads_regularly(X))).
fof(axiom_fulfills, axiom, ! [X] : (fulfills_daily_nutritional_intake(X) => grew_up_health_conscious_childhood_home(X))).
fof(axiom_disregard, axiom, ! [X] : (disregard_physical_wellbeing(X) => ~conscious(X))).
fof(axiom_gym, axiom, ! [X] : (visits_gym_at_least_once_a_day(X) => fulfills_daily_nutritional_intake(X))).
fof(taylor_case, axiom, (grew_up_health_conscious_childhood_home(taylor) & disregard_physical_wellbeing(taylor)) | (~grew_up_health_conscious_childhood_home(taylor) & ~disregard_physical_wellbeing(taylor))).
fof(neg_goal, conjecture, ~visits_gym_at_least_once_a_day(taylor)).