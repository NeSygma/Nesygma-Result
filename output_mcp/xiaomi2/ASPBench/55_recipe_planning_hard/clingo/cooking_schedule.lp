% Constants
#const max_time = 200.

% Time horizon
time(0..max_time).

% Tasks
task(preheat_oven).
task(prep_chicken). task(bake_chicken). task(rest_chicken).
task(chop_veg_soup). task(simmer_stock).
task(chop_onion). task(cook_risotto).
task(wash_greens). task(mix_dressing).

% Recipes
recipe(roast_chicken). recipe(veg_soup). recipe(risotto). recipe(side_salad).

% Task-recipe membership (preheat_oven is a special task, not in any recipe)
belongs(prep_chicken, roast_chicken). belongs(bake_chicken, roast_chicken). belongs(rest_chicken, roast_chicken).
belongs(chop_veg_soup, veg_soup). belongs(simmer_stock, veg_soup).
belongs(chop_onion, risotto). belongs(cook_risotto, risotto).
belongs(wash_greens, side_salad). belongs(mix_dressing, side_salad).

% Helper: task belongs to some recipe
has_recipe(T) :- belongs(T, _).

% Resources
resource(prep_area). resource(oven). resource(stove).

% Durations (in minutes)
duration(preheat_oven, 10).
duration(prep_chicken, 15). duration(bake_chicken, 50). duration(rest_chicken, 10).
duration(chop_veg_soup, 20). duration(simmer_stock, 30).
duration(chop_onion, 5). duration(cook_risotto, 25).
duration(wash_greens, 5). duration(mix_dressing, 10).

% Resource usage
uses(preheat_oven, oven).
uses(prep_chicken, prep_area). uses(bake_chicken, oven). uses(rest_chicken, prep_area).
uses(chop_veg_soup, prep_area). uses(simmer_stock, stove).
uses(chop_onion, prep_area). uses(cook_risotto, stove).
uses(wash_greens, prep_area). uses(mix_dressing, prep_area).

% Resource capacities
capacity(prep_area, 2).
capacity(oven, 1).
capacity(stove, 1).

% Precedences (within recipes and inter-recipe)
precedes(preheat_oven, bake_chicken).    % oven preheat before baking
precedes(prep_chicken, bake_chicken).    % roast chicken: prep -> bake
precedes(bake_chicken, rest_chicken).    % roast chicken: bake -> rest
precedes(chop_veg_soup, simmer_stock).   % veg soup: chop -> simmer
precedes(chop_onion, cook_risotto).      % risotto: chop -> cook
precedes(simmer_stock, cook_risotto).    % inter-recipe: simmer_stock produces veggie_stock needed by cook_risotto
precedes(wash_greens, mix_dressing).     % side salad: wash -> mix

%%%% Decision Variables %%%%

% Each task starts at exactly one time point
1 { start(T, S) : time(S) } 1 :- task(T).

% All tasks must end within the time horizon
:- start(T, S), duration(T, D), S + D > max_time.

%%%% Derived Predicates %%%%

% End time of each task
end(T, E) :- start(T, S), duration(T, D), E = S + D, task(T).

%%%% Constraints %%%%

% Precedence: successor must start no earlier than predecessor's end
:- start(T1, S1), start(T2, S2), precedes(T1, T2), duration(T1, D1), S2 < S1 + D1.

% Track which tasks are active at each time point on each resource
active(T, Res, Tm) :- start(T, S), duration(T, D), uses(T, Res), time(Tm), Tm >= S, Tm < S + D.

% Resource capacity: at any time point, active tasks on a resource must not exceed its capacity
res_time(Res, Tm) :- active(_, Res, Tm).
:- res_time(Res, Tm), capacity(Res, Cap), #count { T : active(T, Res, Tm) } > Cap.

%%%% Optimization %%%%

% Makespan is the latest end time across all tasks
makespan(M) :- M = #max { E : end(_, E) }.

% Minimize the makespan
#minimize { M : makespan(M) }.

%%%% Output %%%%

feasible.

% Schedule for recipe tasks: (recipe, step, start, end, resource)
recipe_schedule(R, T, S, E, Res) :- start(T, S), end(T, E), uses(T, Res), belongs(T, R).

% Schedule for special tasks: (task, start, end, resource)
special_schedule(T, S, E, Res) :- start(T, S), end(T, E), uses(T, Res), not has_recipe(T).

#show start/2.
#show end/2.
#show recipe_schedule/5.
#show special_schedule/5.
#show makespan/1.
#show feasible.