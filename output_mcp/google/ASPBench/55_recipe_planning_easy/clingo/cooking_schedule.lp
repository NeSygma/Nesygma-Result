% --- Data ---
recipe(pasta). recipe(salad). recipe(bread).

% step(Recipe, StepName, Duration, Resource)
step(pasta, prep, 10, prep_area).
step(pasta, boil, 15, stove).
step(pasta, serve, 5, prep_area).
step(salad, chop, 15, prep_area).
step(salad, mix, 5, prep_area).
step(bread, bake, 30, oven).

% precedence(Recipe, Step1, Step2)
precedence(pasta, prep, boil).
precedence(pasta, boil, serve).
precedence(salad, chop, mix).

% --- Time Horizon ---
time(0..40).

% --- Generation ---
% Every step must be scheduled exactly once
1 { start(R, S, T) : time(T) } 1 :- step(R, S, _, _).

% Calculate end times
end(R, S, T + D) :- start(R, S, T), step(R, S, D, _).

% --- Constraints ---
% 1. Precedence constraints
:- precedence(R, S1, S2), start(R, S1, T1), end(R, S1, E1), start(R, S2, T2), T2 < E1.

% 2. No resource conflicts
% Two steps using the same resource cannot overlap
:- step(R1, S1, _, Res), step(R2, S2, _, Res),
   start(R1, S1, T1), end(R1, S1, E1),
   start(R2, S2, T2), end(R2, S2, E2),
   (R1, S1) < (R2, S2),
   T1 < E2, T2 < E1.

% 3. Ensure all steps finish within time horizon
:- end(R, S, E), E > 40.

% --- Objective ---
total_time(M) :- M = #max { E : end(_, _, E) }.
#minimize { M : total_time(M) }.

% --- Output ---
#show start/3.
#show end/3.
#show total_time/1.