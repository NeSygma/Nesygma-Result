% --- Instance Data ---
% Recipes
recipe(pasta; salad; bread).

% Steps for each recipe
step(pasta, prep).
step(pasta, boil).
step(pasta, serve).
step(salad, chop).
step(salad, mix).
step(bread, bake).

% Resources
resource(oven; stove; prep_area).

% Precedence constraints
precedes(pasta, prep, boil).
precedes(pasta, boil, serve).
precedes(salad, chop, mix).

% Durations
duration(pasta, prep, 10).
duration(pasta, boil, 15).
duration(pasta, serve, 5).
duration(salad, chop, 15).
duration(salad, mix, 5).
duration(bread, bake, 30).

% Resource usage per step
uses(pasta, prep, prep_area).
uses(pasta, boil, stove).
uses(pasta, serve, prep_area).
uses(salad, chop, prep_area).
uses(salad, mix, prep_area).
uses(bread, bake, oven).

% --- Time Horizon ---
max_time(100).
time(0..T) :- max_time(T).

% --- Schedule Assignment ---
% Each step must be scheduled exactly once
1 { start(R, S, T) : time(T) } 1 :- step(R, S).

% Derive end times from start times and durations
end(R, S, T + D) :- start(R, S, T), duration(R, S, D), time(T), time(T+D).

% --- Constraints ---
% Precedence constraints
:- precedes(R, S1, S2), end(R, S1, E1), start(R, S2, S2T), E1 > S2T.

% Resource usage intervals
resource_usage(Res, R, S, Start, End) :-
    uses(R, S, Res),
    start(R, S, Start),
    end(R, S, End),
    time(Start),
    time(End).

% No resource conflicts: no two steps using the same resource can overlap
:- resource_usage(Res, R1, S1, Start1, End1),
     resource_usage(Res, R2, S2, Start2, End2),
     Res = Res,
     (R1 < R2 ; (R1 = R2, S1 < S2)),
     Start1 < End2,
     Start2 < End1.

% --- Objective: Minimize total completion time ---
% Compute the maximum end time
max_end_time(T) :- T = #max { E : end(_, _, E) }.

% Minimize the maximum end time
#minimize { T : max_end_time(T) }.

% --- Show the schedule and resource usage ---
#show start/3.
#show end/3.
#show resource_usage/4.
#show max_end_time/1.