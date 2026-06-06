% Define recipes and steps
recipe(pasta).
recipe(salad).
recipe(bread).

% Steps: recipe, step_name, duration, resource
step(pasta, prep, 10, prep_area).
step(pasta, boil, 15, stove).
step(pasta, serve, 5, prep_area).

step(salad, chop, 15, prep_area).
step(salad, mix, 5, prep_area).

step(bread, bake, 30, oven).

% Precedence constraints within recipes
precedes(pasta, prep, boil).
precedes(pasta, boil, serve).
precedes(salad, chop, mix).

% Resources
resource(oven).
resource(stove).
resource(prep_area).

% Time horizon - we'll bound it to a reasonable value
% Since the expected optimal is 35, let's use 0..40
% This gives enough room for the solver to find the optimal solution
time(0..40).

% Choice rule: assign start times to steps
{ start(R, S, T) : time(T) } = 1 :- step(R, S, _, _).

% Derive end times
end(R, S, T + D) :- step(R, S, D, _), start(R, S, T), time(T), time(T + D).

% All steps must be scheduled (ensured by the choice rule with = 1)

% Precedence constraints: if S1 precedes S2 in recipe R, then end(R, S1, E1) <= start(R, S2, T2)
:- precedes(R, S1, S2),
   end(R, S1, E1),
   start(R, S2, T2),
   E1 > T2.

% Resource usage: a step uses a resource
uses_resource(R, S, Rsrc) :- step(R, S, _, Rsrc).

% No overlapping resource usage: for any resource, two steps cannot overlap in time
:- uses_resource(R1, S1, Rsrc), uses_resource(R2, S2, Rsrc),
   R1 != R2,
   start(R1, S1, T1), end(R1, S1, E1),
   start(R2, S2, T2), end(R2, S2, E2),
   T1 < E2, T2 < E1.

% Define total_time as the maximum end time across all steps
total_time(T) :- T = #max { E : end(_, _, E) }.

% Minimize the total_time
#minimize { T : total_time(T) }.

% Show the schedule and resource usage
% Helper to show schedule: recipe, step, start_time, end_time, resource
schedule(R, S, T, E, Rsrc) :-
    step(R, S, _, Rsrc),
    start(R, S, T),
    end(R, S, E).

% Helper to show resource usage: resource, start, end, recipe
resource_usage(Rsrc, T, E, R) :-
    uses_resource(R, S, Rsrc),
    start(R, S, T),
    end(R, S, E).

#show schedule/5.
#show resource_usage/4.
#show total_time/1.