%%% Domain Definitions %%%

% Steps with (recipe, step, duration, resource)
step("pasta", "prep", 10, "prep_area").
step("pasta", "boil", 15, "stove").
step("pasta", "serve", 5, "prep_area").
step("salad", "chop", 15, "prep_area").
step("salad", "mix", 5, "prep_area").
step("bread", "bake", 30, "oven").

% Precedence: (recipe, step_before, step_after)
precedence("pasta", "prep", "boil").
precedence("pasta", "boil", "serve").
precedence("salad", "chop", "mix").

% Resources
resource("oven"; "stove"; "prep_area").

% Time horizon - upper bound for scheduling
% Sum of all durations = 10+15+5+15+5+30 = 80, but optimal is 35
% Use a generous upper bound
time(0..80).

%%% Decision Variables %%%

% Each step gets a start time
{ start_time(Recipe, Step, T) : time(T) } 1 :- step(Recipe, Step, Dur, Res).

%%% Derived: end time %%%
end_time(Recipe, Step, T+Dur) :- start_time(Recipe, Step, T), step(Recipe, Step, Dur, Res).

%%% Constraints %%%

% 1. All steps must be scheduled (already enforced by choice rule with 1)

% 2. No resource conflicts - same resource cannot be used at overlapping times
% Two steps conflict if they use the same resource and their intervals overlap
:- step(R1, S1, D1, Res), step(R2, S2, D2, Res),
   R1 != R2,
   start_time(R1, S1, T1), start_time(R2, S2, T2),
   T1 < T2 + D2, T2 < T1 + D1.

% Also handle same recipe different steps using same resource (e.g., pasta prep and serve both use prep_area)
:- step(R, S1, D1, Res), step(R, S2, D2, Res),
   S1 != S2,
   start_time(R, S1, T1), start_time(R, S2, T2),
   T1 < T2 + D2, T2 < T1 + D1.

% 3. Precedence constraints - within each recipe, steps must complete in order
:- precedence(R, S_before, S_after),
   step(R, S_before, D_before, _), step(R, S_after, D_after, _),
   start_time(R, S_before, T_before), start_time(R, S_after, T_after),
   T_before + D_before > T_after.

% 4. Correct durations - enforced by end_time derivation

% 5. Non-negative times - enforced by time(0..80)

%%% Objective: minimize makespan %%%

% Makespan is the maximum end time across all steps
makespan(M) :- M = #max{ E : end_time(_, _, E) }.

#minimize { M@1 : makespan(M) }.

%%% Output %%%

#show start_time/3.
#show end_time/3.
#show makespan/1.