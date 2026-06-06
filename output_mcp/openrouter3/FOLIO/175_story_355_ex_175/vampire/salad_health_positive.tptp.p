% Positive version: Taylor neither grew up in a health-conscious childhood home nor visits the gym daily
fof(premise_1, axiom, ! [X] : (eats_salads_regularly(X) => conscious_about_health(X))).
fof(premise_2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads_regularly(X))).
fof(premise_3, axiom, ! [X] : (fulfills_nutritional_intakes(X) => grew_up_health_conscious(X))).
fof(premise_4, axiom, ! [X] : (disregards_physical_wellbeing(X) => ~conscious_about_health(X))).
fof(premise_5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutritional_intakes(X))).
fof(premise_6, axiom, (grew_up_health_conscious(taylor) & disregards_physical_wellbeing(taylor)) | (~grew_up_health_conscious(taylor) & ~disregards_physical_wellbeing(taylor))).
fof(goal, conjecture, ~grew_up_health_conscious(taylor) & ~visits_gym_daily(taylor)).