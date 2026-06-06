fof(p1, axiom, ! [X] : (eats_salads_regularly(X) => health_conscious(X))).
fof(p2, axiom, ! [X] : (health_conscious_home(X) => eats_salads_regularly(X))).
fof(p3, axiom, ! [X] : (fulfills_nutrition(X) => health_conscious_home(X))).
fof(p4, axiom, ! [X] : (disregards_wellbeing(X) => ~health_conscious(X))).
fof(p5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutrition(X))).
fof(p6, axiom, ((health_conscious_home(taylor) & disregards_wellbeing(taylor)) | (~health_conscious_home(taylor) & ~disregards_wellbeing(taylor)))).
fof(goal, conjecture, ~eats_salads_regularly(taylor)).