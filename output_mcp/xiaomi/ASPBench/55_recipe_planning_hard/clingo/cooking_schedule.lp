% ============================================
% Cooking Schedule Optimization - ASP Model
% ============================================

% --- Time Horizon ---
time(0..100).

% --- Recipes ---
recipe(roast_chicken).
recipe(veg_soup).
recipe(risotto).
recipe(side_salad).

% --- Tasks (Recipe Steps) ---
task(prep_chicken).
task(bake_chicken).
task(rest_chicken).
task(chop_veg_soup).
task(simmer_stock).
task(chop_onion).
task(cook_risotto).
task(wash_greens).
task(mix_dressing).
task(preheat_oven).

% --- Task-Recipe Mapping ---
task_recipe(prep_chicken, roast_chicken).
task_recipe(bake_chicken, roast_chicken).
task_recipe(rest_chicken, roast_chicken).
task_recipe(chop_veg_soup, veg_soup).
task_recipe(simmer_stock, veg_soup).
task_recipe(chop_onion, risotto).
task_recipe(cook_risotto, risotto).
task_recipe(wash_greens, side_salad).
task_recipe(mix_dressing, side_salad).

% Special task (no recipe)
is_special(preheat_oven).

% --- Durations ---
duration(prep_chicken, 15).
duration(bake_chicken, 50).
duration(rest_chicken, 10).
duration(chop_veg_soup, 20).
duration(simmer_stock, 30).
duration(chop_onion, 5).
duration(cook_risotto, 25).
duration(wash_greens, 5).
duration(mix_dressing, 10).
duration(preheat_oven, 10).

% --- Resource Requirements ---
resource(prep_chicken, prep_area).
resource(bake_chicken, oven).
resource(rest_chicken, prep_area).
resource(chop_veg_soup, prep_area).
resource(simmer_stock, stove).
resource(chop_onion, prep_area).
resource(cook_risotto, stove).
resource(wash_greens, prep_area).
resource(mix_dressing, prep_area).
resource(preheat_oven, oven).

% --- Resource Capacities ---
capacity(prep_area, 2).
capacity(oven, 1).
capacity(stove, 1).

% --- Precedence Constraints (within recipes) ---
precedence(prep_chicken, bake_chicken).
precedence(bake_chicken, rest_chicken).
precedence(chop_veg_soup, simmer_stock).
precedence(chop_onion, cook_risotto).
precedence(wash_greens, mix_dressing).

% --- Inter-Recipe Dependency ---
precedence(simmer_stock, cook_risotto).

% --- Special: preheat_oven must finish before bake_chicken ---
precedence(preheat_oven, bake_chicken).

% ============================================
% Decision Variables
% ============================================

% Assign a start time to each task
1 { start(T, S) : time(S) } 1 :- task(T).

% Compute end time
end(T, E) :- start(T, S), duration(T, D), E = S + D.

% ============================================
% Constraints
% ============================================

% 1. Precedence: T1 must finish before T2 starts
:- precedence(T1, T2), start(T1, S1), end(T1, E1), start(T2, S2), S2 < E1.

% 2. Resource capacity constraints
% For each resource, at any time point, the number of tasks using it must not exceed capacity
% A task uses a resource from its start time to end time - 1
uses_resource_at(Res, T, P) :- task(T), resource(T, Res), start(T, S), end(T, E), time(P), P >= S, P < E.

:- time(P), resource(Res, _), capacity(Res, Cap), 
   #count { T : uses_resource_at(Res, T, P) } > Cap.

% ============================================
% Objective: Minimize Makespan
% ============================================

makespan(M) :- M = #max { E : end(_, E) }.

#minimize { M : makespan(M) }.

% ============================================
% Output
% ============================================

#show start/2.
#show end/2.
#show makespan/1.