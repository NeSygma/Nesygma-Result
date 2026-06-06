fof(premise1, axiom, ! [X] : (eat_salads_regularly(X) => very_conscious(X))).
fof(premise2, axiom, ! [X] : (grew_up_health_conscious(X) => eat_salads_regularly(X))).
fof(premise3, axiom, ! [X] : (fulfill_nutritional_intakes(X) => grew_up_health_conscious(X))).
fof(premise4, axiom, ! [X] : (disregard_physical_wellbeing(X) => ~very_conscious(X))).
fof(premise5, axiom, ! [X] : (visit_gym_daily(X) => fulfill_nutritional_intakes(X))).
fof(premise6, axiom, (grew_up_health_conscious(taylor) & disregard_physical_wellbeing(taylor)) | (~grew_up_health_conscious(taylor) & ~disregard_physical_wellbeing(taylor))).
fof(neg_conclusion, conjecture, grew_up_health_conscious(taylor) | visit_gym_daily(taylor)).