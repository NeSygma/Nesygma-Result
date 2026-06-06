% Axioms
fof(axiom_eat_salad_conscious, axiom, ! [X] : (eat_salad_regularly(X) => conscious(X))).
fof(axiom_grew_up_eat_salad, axiom, ! [X] : (grew_up_in_health_conscious_childhood_home(X) => eat_salad_regularly(X))).
fof(axiom_fulfill_grew_up, axiom, ! [X] : (fulfill_daily_nutritional_intake(X) => grew_up_in_health_conscious_childhood_home(X))).
fof(axiom_disregard_not_conscious, axiom, ! [X] : (disregard_physical_wellbeing(X) => ~conscious(X))).
fof(axiom_gym_fulfill, axiom, ! [X] : (gym(X) => fulfill_daily_nutritional_intake(X))).
fof(taylor_condition, axiom, (grew_up_in_health_conscious_childhood_home(taylor) & disregard_physical_wellbeing(taylor)) | (~grew_up_in_health_conscious_childhood_home(taylor) & ~disregard_physical_wellbeing(taylor))).

% Negated conjecture
fof(conjecture_neg, conjecture, grew_up_in_health_conscious_childhood_home(taylor) | gym(taylor)).