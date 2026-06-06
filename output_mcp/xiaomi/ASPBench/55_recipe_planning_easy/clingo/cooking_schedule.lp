% Domain: Recipes
recipe(pasta). recipe(salad). recipe(bread).

% Steps within each recipe
step(pasta, prep). step(pasta, boil). step(pasta, serve).
step(salad, chop). step(salad, mix).
step(bread, bake).

% Resources used by each step
resource(pasta, prep, prep_area).
resource(pasta, boil, stove).
resource(pasta, serve, prep_area).
resource(salad, chop, prep_area).
resource(salad, mix, prep_area).
resource(bread, bake, oven).

% Durations (in minutes)
duration(pasta, prep, 10).
duration(pasta, boil, 15).
duration(pasta, serve, 5).
duration(salad, chop, 15).
duration(salad, mix, 5).
duration(bread, bake, 30).

% Precedence constraints within recipes
precedes(pasta, prep, boil).
precedes(pasta, boil, serve).
precedes(salad, chop, mix).

% Time horizon: 0 to 40 minutes (sufficient for optimal solution)
time(0..40).

% Decision variables: assign start time to each step
{ start(R, S, T) : time(T) } 1 :- step(R, S).

% End time is start + duration
end(R, S, T + D) :- start(R, S, T), duration(R, S, D).

% Constraint 1: Precedence constraints within recipes
:- precedes(R, S1, S2), start(R, S1, T1), end(R, S2, T2), T2 <= T1.

% Constraint 2: No resource conflicts - same resource cannot be used at overlapping times
% Two steps using same resource cannot overlap
:- resource(R1, S1, Res), resource(R2, S2, Res), 
   start(R1, S1, T1), end(R1, S1, E1),
   start(R2, S2, T2), end(R2, S2, E2),
   (R1, S1) != (R2, S2),
   T1 < E2, T2 < E1.

% Constraint 3: All times must be non-negative (already ensured by time(0..40))

% Compute total completion time (maximum end time)
total_time(T) :- T = #max{ E : end(_, _, E) }.

% Optimization: minimize total completion time
#minimize { T : total_time(T) }.

% Output formatting
#show start/3.
#show end/3.
#show total_time/1.