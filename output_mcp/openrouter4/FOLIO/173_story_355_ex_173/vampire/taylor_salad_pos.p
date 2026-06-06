% Positive: Is "Taylor eats salads regularly" entailed?
fof(distinct, axiom, $true).  % No multiple entities needing distinctness

% Premise 1: All people who eat salads regularly are health-conscious
fof(p1, axiom, ! [X] : (eats_salads(X) => health_conscious(X))).

% Premise 2: All people who grew up healthy eat salads regularly
fof(p2, axiom, ! [X] : (grew_up_healthy(X) => eats_salads(X))).

% Premise 3: All people who fulfill nutrition grew up healthy
fof(p3, axiom, ! [X] : (fulfills_nutrition(X) => grew_up_healthy(X))).

% Premise 4: All people who disregard wellbeing are NOT health-conscious
fof(p4, axiom, ! [X] : (disregards_wellbeing(X) => ~health_conscious(X))).

% Premise 5: If people visit gym daily, they fulfill nutrition
fof(p5, axiom, ! [X] : (visits_gym(X) => fulfills_nutrition(X))).

% Premise 6: Taylor either (grew_up_healthy AND disregards_wellbeing) OR (neither)
fof(p6, axiom, 
    ( (grew_up_healthy(taylor) & disregards_wellbeing(taylor)) 
    | (~grew_up_healthy(taylor) & ~disregards_wellbeing(taylor)) )).

% Conclusion: Taylor eats salads regularly
fof(goal, conjecture, eats_salads(taylor)).