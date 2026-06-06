fof(premise1, axiom, ! [P] : (eats_salads_regularly(P) => health_conscious(P))).
fof(premise2, axiom, ! [P] : (grew_up_health_conscious(P) => eats_salads_regularly(P))).
fof(premise3, axiom, ! [P] : (fulfills_nutritional_intakes(P) => grew_up_health_conscious(P))).
fof(premise4, axiom, ! [P] : (disregards_physical_wellbeing(P) => ~health_conscious(P))).
fof(premise5, axiom, ! [P] : (visits_gym_daily(P) => fulfills_nutritional_intakes(P))).
fof(premise6_taylor, axiom, (grew_up_health_conscious(taylor) & disregards_physical_wellbeing(taylor)) | (~grew_up_health_conscious(taylor) & ~disregards_physical_wellbeing(taylor))).
fof(goal, conjecture, ~visits_gym_daily(taylor)).