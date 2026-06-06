% Negative version: negated conclusion as conjecture
% Predicates:
%   eats_salad_regularly(X)
%   health_conscious(X)
%   grew_up_health_conscious(X)
%   fulfills_nutrition(X)
%   disregards_wellbeing(X)
%   visits_gym_daily(X)

fof(premise1, axiom, ! [X] : (eats_salad_regularly(X) => health_conscious(X))).
fof(premise2, axiom, ! [X] : (grew_up_health_conscious(X) => eats_salad_regularly(X))).
fof(premise3, axiom, ! [X] : (fulfills_nutrition(X) => grew_up_health_conscious(X))).
fof(premise4, axiom, ! [X] : (disregards_wellbeing(X) => ~health_conscious(X))).
fof(premise5, axiom, ! [X] : (visits_gym_daily(X) => fulfills_nutrition(X))).
fof(premise6, axiom, 
    ( (grew_up_health_conscious(taylor) & disregards_wellbeing(taylor)) 
    | (~grew_up_health_conscious(taylor) & ~disregards_wellbeing(taylor)) )).

% Negated conclusion: It is NOT the case that Taylor neither grew up health-conscious nor visits gym daily.
% i.e., grew_up_health_conscious(taylor) | visits_gym_daily(taylor)
fof(negated_conclusion, conjecture, (grew_up_health_conscious(taylor) | visits_gym_daily(taylor))).