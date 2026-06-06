fof(p1, axiom, ! [X] : (eats_salads_regularly(X) => health_conscious(X))).
fof(p2, axiom, ! [X] : (grew_up_health_conscious_home(X) => eats_salads_regularly(X))).
fof(p3, axiom, ! [X] : (fulfills_daily_nutrition(X) => grew_up_health_conscious_home(X))).
fof(p4, axiom, ! [X] : (disregards_physical_wellbeing(X) => ~health_conscious(X))).
fof(p5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_daily_nutrition(X))).
fof(p6, axiom, ((grew_up_health_conscious_home(taylor) & disregards_physical_wellbeing(taylor)) | (~grew_up_health_conscious_home(taylor) & ~disregards_physical_wellbeing(taylor)))).
fof(goal, conjecture, ~visits_gym_daily(taylor)).