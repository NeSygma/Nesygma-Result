% Define the recipes
recipe(roast_chicken).
recipe(vegetable_soup).
recipe(risotto).
recipe(side_salad).

% Define steps for each recipe with duration and resource
% Format: step(StepName, Recipe, Duration, Resource)
step(prep_chicken, roast_chicken, 15, prep_area).
step(bake_chicken, roast_chicken, 50, oven).
step(rest_chicken, roast_chicken, 10, prep_area).

step(chop_veg_soup, vegetable_soup, 20, prep_area).
step(simmer_stock, vegetable_soup, 30, stove).

step(chop_onion, risotto, 5, prep_area).
step(cook_risotto, risotto, 25, stove).

step(wash_greens, side_salad, 5, prep_area).
step(mix_dressing, side_salad, 10, prep_area).

% Special task: preheat oven
special_task(preheat_oven, 10, oven).

% Define all tasks (steps + special tasks)
task(T, D, Res) :- step(T, _, D, Res).
task(T, D, Res) :- special_task(T, D, Res).

% Define precedences within each recipe
% Format: precedence(Step1, Step2, Recipe)
precedence(prep_chicken, bake_chicken, roast_chicken).
precedence(bake_chicken, rest_chicken, roast_chicken).

precedence(chop_veg_soup, simmer_stock, vegetable_soup).

precedence(chop_onion, cook_risotto, risotto).

precedence(wash_greens, mix_dressing, side_salad).

% Inter-recipe dependency: simmer_stock must finish before cook_risotto starts
% Format: inter_dep(Step1, Recipe1, Step2, Recipe2)
inter_dep(simmer_stock, vegetable_soup, cook_risotto, risotto).

% Define resources and their capacities
resource(prep_area, 2).
resource(oven, 1).
resource(stove, 1).

% Time horizon (upper bound for makespan)
time(0..100).

% Choice rule: assign a start time to each task
{ start(T, Time) : time(Time) } = 1 :- task(T, _, _).

% Derive end time from start time and duration
end(T, End) :- start(T, Start), task(T, Duration, _), End = Start + Duration.

% Enforce precedences within recipes
:- precedence(S1, S2, _), end(S1, End1), start(S2, Start2), End1 > Start2.

% Enforce inter-recipe dependencies
:- inter_dep(S1, _, S2, _), end(S1, End1), start(S2, Start2), End1 > Start2.

% Helper predicate: preheat_done_by(StartBake) is true if preheat_oven has ended by StartBake
preheat_done_by(StartBake) :- start(bake_chicken, StartBake), end(preheat_oven, EndPreheat), EndPreheat =< StartBake.

% Enforce oven preheating before any baking
:- step(bake_chicken, roast_chicken, _, oven), start(bake_chicken, StartBake), not preheat_done_by(StartBake).

% Resource capacity constraints
% For each resource and time point, at most Cap tasks can be using it
:- resource(Res, Cap),
   time(T),
   #count { Task : start(Task, Start), end(Task, End), uses(Res, Task), Start =< T, T < End } > Cap.

% Define which tasks use which resources
uses(Res, T) :- step(T, _, _, Res).
uses(Res, T) :- special_task(T, _, Res).

% Ensure all steps are completed (no choice for steps)
:- step(S, _, _, _), not end(S, _).

% Ensure special tasks are completed
:- special_task(T, _, _), not end(T, _).

% Define makespan as the maximum end time
makespan(M) :- M = #max { End : end(_, End) }.

% Objective: minimize makespan
#minimize { M : makespan(M) }.

% Show the schedule
#show start/2.
#show end/2.
#show makespan/1.
#show feasible.

% Helper to indicate feasibility (always true if constraints are satisfied)
feasible :- makespan(_).
#show feasible/0.