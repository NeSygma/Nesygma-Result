fof(premise_1, axiom, ! [X] : (eats_salads_regularly(X) => health_conscious(X))).
fof(premise_2, axiom, ! [X] : (health_conscious_home(X) => eats_salads_regularly(X))).
fof(premise_3, axiom, ! [X] : (fulfills_nutrition(X) => health_conscious_home(X))).
fof(premise_4, axiom, ! [X] : (disregards_wellbeing(X) => ~health_conscious(X))).
fof(premise_5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutrition(X))).
fof(premise_6, axiom, 
    ((health_conscious_home(taylor) & disregards_wellbeing(taylor)) | 
     (~health_conscious_home(taylor) & ~disregards_wellbeing(taylor)))).
fof(goal, conjecture, ~health_conscious_home(taylor) & ~visits_gym_daily(taylor)).