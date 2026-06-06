% Cooking Schedule Planning Problem

% ==================== DOMAIN DECLARATIONS ====================
% Recipes
recipe(pasta).
recipe(salad).
recipe(bread).

% Steps per recipe
step(pasta, prep).
step(pasta, boil).
step(pasta, serve).
step(salad, chop).
step(salad, mix).
step(bread, bake).

% Resources
resource(oven).
resource(stove).
resource(prep_area).

% ==================== INSTANCE DATA ====================
% Step durations (recipe, step, duration)
step_duration(pasta, prep, 10).
step_duration(pasta, boil, 15).
step_duration(pasta, serve, 5).
step_duration(salad, chop, 15).
step_duration(salad, mix, 5).
step_duration(bread, bake, 30).

% Step resources (recipe, step, resource)
step_resource(pasta, prep, prep_area).
step_resource(pasta, boil, stove).
step_resource(pasta, serve, prep_area).
step_resource(salad, chop, prep_area).
step_resource(salad, mix, prep_area).
step_resource(bread, bake, oven).

% ==================== PRECEDENCE CONSTRAINTS ====================
% Pasta: prep -> boil -> serve
precedence(pasta, prep, boil, 1).
precedence(pasta, boil, serve, 2).

% Salad: chop -> mix
precedence(salad, chop, mix, 1).

% Bread: no internal dependencies

% ==================== TIME DOMAIN ====================
% Define time horizon (0 to 100 minutes should be sufficient)
time(0..100).

% ==================== SCHEDULING VARIABLES ====================
% Start time for each step (integer)
1 { start_time(R, S, T) : time(T) } 1 :- step(R, S).

% End time for each step
end_time(R, S, T + D) :- start_time(R, S, T), step_duration(R, S, D).

% ==================== PRECEDENCE CONSTRAINTS ====================
% Steps must occur in order
:- precedence(R, S1, S2, _), end_time(R, S1, T1), start_time(R, S2, T2), T1 > T2.

% ==================== RESOURCE CONFLICTS ====================
% No overlapping usage of same resource
% Use helper predicate to avoid complex inequality
conflict(R1, S1, R2, S2) :-
    step_resource(R1, S1, Res),
    step_resource(R2, S2, Res),
    start_time(R1, S1, T1),
    end_time(R1, S1, E1),
    start_time(R2, S2, T2),
    end_time(R2, S2, E2),
    T1 < E2,
    T2 < E1,
    (R1 != R2 ; S1 != S2).

:- conflict(R1, S1, R2, S2).

% ==================== NON-NEGATIVE TIMES ====================
:- start_time(R, S, T), T < 0.

% ==================== TOTAL TIME CALCULATION ====================
% Maximum end time across all steps
total_time(T) :- T = #max { E, R, S : end_time(R, S, E) }.

% ==================== OPTIMIZATION ====================
% Minimize total completion time
#minimize { T : total_time(T) }.

% ==================== OUTPUT ====================
% Show the schedule
#show start_time/3.
#show end_time/3.
#show total_time/1.

% Helper for resource usage summary
resource_usage(Res, R, S, T) :- 
    step_resource(R, S, Res),
    start_time(R, S, T1),
    end_time(R, S, T2),
    T >= T1, T < T2.

#show resource_usage/4.