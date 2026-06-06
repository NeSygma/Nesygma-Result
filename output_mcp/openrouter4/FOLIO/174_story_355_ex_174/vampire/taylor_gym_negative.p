% Negative version: claim is "Taylor does NOT visit the gym at least once a day"
fof(p1, axiom, ! [X] : (salad_regular(X) => health_conscious(X))).
fof(p2, axiom, ! [X] : (grew_up_healthy(X) => salad_regular(X))).
fof(p3, axiom, ! [X] : (fulfill_nutrition(X) => grew_up_healthy(X))).
fof(p4, axiom, ! [X] : (disregard_health(X) => ~health_conscious(X))).
fof(p5, axiom, ! [X] : (gym_daily(X) => fulfill_nutrition(X))).
fof(p6, axiom, (grew_up_healthy(taylor) & disregard_health(taylor)) | (~grew_up_healthy(taylor) & ~disregard_health(taylor))).
fof(goal, conjecture, ~gym_daily(taylor)).