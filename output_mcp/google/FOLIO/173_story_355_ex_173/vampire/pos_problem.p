fof(p1, axiom, ! [X] : (eats_salads(X) => health_conscious(X))).
fof(p2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads(X))).
fof(p3, axiom, ! [X] : (fulfills_nutritional_intake(X) => grew_up_health_conscious(X))).
fof(p4, axiom, ! [X] : (disregards_well_being(X) => ~health_conscious(X))).
fof(p5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutritional_intake(X))).
fof(p6, axiom, (grew_up_health_conscious(taylor) & disregards_well_being(taylor)) | (~grew_up_health_conscious(taylor) & ~disregards_well_being(taylor))).
fof(goal, conjecture, eats_salads(taylor)).