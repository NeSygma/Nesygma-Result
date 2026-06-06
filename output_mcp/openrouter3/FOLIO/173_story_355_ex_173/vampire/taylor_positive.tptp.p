% Taylor Salad Problem - Positive Version
% Premises
fof(premise_1, axiom, ! [X] : (eats_salads_regularly(X) => very_conscious(X))).
fof(premise_2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salads_regularly(X))).
fof(premise_3, axiom, ! [X] : (fulfills_nutritional_intakes(X) => grew_up_health_conscious(X))).
fof(premise_4, axiom, ! [X] : (disregards_physical_wellbeing(X) => ~very_conscious(X))).
fof(premise_5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutritional_intakes(X))).
fof(premise_6, axiom, (grew_up_health_conscious(taylor) & disregards_physical_wellbeing(taylor)) | (~grew_up_health_conscious(taylor) & ~disregards_physical_wellbeing(taylor))).

% Conclusion
fof(goal, conjecture, eats_salads_regularly(taylor)).