% Define all tasks with (ID, Recipe, Step, Duration, Resource)
task(1, "roast_chicken", "prep_chicken", 15, "prep_area").
task(2, "roast_chicken", "bake_chicken", 50, "oven").
task(3, "roast_chicken", "rest_chicken", 10, "prep_area").
task(4, "special", "preheat_oven", 10, "oven").
task(5, "vegetable_soup", "chop_veg_soup", 20, "prep_area").
task(6, "vegetable_soup", "simmer_stock", 30, "stove").
task(7, "risotto", "chop_onion", 5, "prep_area").
task(8, "risotto", "cook_risotto", 25, "stove").
task(9, "side_salad", "wash_greens", 5, "prep_area").
task(10, "side_salad", "mix_dressing", 10, "prep_area").

% Precedence constraints (within recipes)
prec(1, 2).  % prep_chicken -> bake_chicken
prec(2, 3).  % bake_chicken -> rest_chicken
prec(5, 6).  % chop_veg_soup -> simmer_stock
prec(7, 8).  % chop_onion -> cook_risotto
prec(9, 10). % wash_greens -> mix_dressing

% Inter-recipe dependency: simmer_stock (6) before cook_risotto (8)
prec(6, 8).

% Oven preheating: preheat_oven (4) before bake_chicken (2)
prec(4, 2).

% Resource capacities
resource("prep_area", 2).
resource("oven", 1).
resource("stove", 1).

% Time horizon (sufficiently large upper bound)
time(0..120).

% Each task must start at exactly one valid time point
1 { start(Task, S) : time(S), S + Dur <= 120 } 1 :- task(Task, _, _, Dur, _).

% Derive end time from start time and duration
end(Task, S + Dur) :- start(Task, S), task(Task, _, _, Dur, _).

% Precedence constraints: predecessor must finish before successor starts
:- prec(Pre, Post), end(Pre, E), start(Post, S), S < E.

% Resource capacity constraints
% For each time point and each resource, number of concurrent tasks <= capacity
:- resource(Res, Cap), time(T),
    #count { Task : task(Task, _, _, Dur, Res), start(Task, S), S <= T, T < S + Dur } > Cap.

% Makespan = maximum end time across all tasks
makespan(M) :- M = #max { E : end(_, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

#show start/2.
#show end/2.
#show makespan/1.