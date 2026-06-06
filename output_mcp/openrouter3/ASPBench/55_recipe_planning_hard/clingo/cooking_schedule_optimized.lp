% Cooking Schedule Optimization Problem

% ===== DOMAIN DEFINITIONS =====
% Recipes
recipe(roast_chicken).
recipe(vegetable_soup).
recipe(risotto).
recipe(side_salad).

% Steps per recipe
step(roast_chicken, prep_chicken).
step(roast_chicken, bake_chicken).
step(roast_chicken, rest_chicken).

step(vegetable_soup, chop_veg_soup).
step(vegetable_soup, simmer_stock).

step(risotto, chop_onion).
step(risotto, cook_risotto).

step(side_salad, wash_greens).
step(side_salad, mix_dressing).

% Special task
task(preheat_oven).

% Resources
resource(prep_area).
resource(oven).
resource(stove).

% ===== DURATIONS AND RESOURCES =====
% Roast Chicken
duration(roast_chicken, prep_chicken, 15).
resource(roast_chicken, prep_chicken, prep_area).
duration(roast_chicken, bake_chicken, 50).
resource(roast_chicken, bake_chicken, oven).
duration(roast_chicken, rest_chicken, 10).
resource(roast_chicken, rest_chicken, prep_area).

% Vegetable Soup
duration(vegetable_soup, chop_veg_soup, 20).
resource(vegetable_soup, chop_veg_soup, prep_area).
duration(vegetable_soup, simmer_stock, 30).
resource(vegetable_soup, simmer_stock, stove).

% Risotto
duration(risotto, chop_onion, 5).
resource(risotto, chop_onion, prep_area).
duration(risotto, cook_risotto, 25).
resource(risotto, cook_risotto, stove).

% Side Salad
duration(side_salad, wash_greens, 5).
resource(side_salad, wash_greens, prep_area).
duration(side_salad, mix_dressing, 10).
resource(side_salad, mix_dressing, prep_area).

% Special task - preheat_oven
duration(preheat_oven, 10).
resource(preheat_oven, oven).

% ===== PRECEDENCES =====
% Within recipes
precedes(roast_chicken, prep_chicken, bake_chicken).
precedes(roast_chicken, bake_chicken, rest_chicken).

precedes(vegetable_soup, chop_veg_soup, simmer_stock).

precedes(risotto, chop_onion, cook_risotto).

precedes(side_salad, wash_greens, mix_dressing).

% Inter-recipe dependency
inter_dep(simmer_stock, cook_risotto).

% ===== TIME DOMAIN =====
% Use a smaller, more reasonable time horizon
time(0..80).  % Based on expected optimal 75

% ===== TASK SCHEDULING =====
% Generate start times for all tasks
{ start_time(T, T0) : time(T0) } 1 :- task(T).
{ start_time(R, S, T0) : time(T0) } 1 :- recipe(R), step(R, S).

% Calculate end times
end_time(T, T0 + D) :- start_time(T, T0), duration(T, D).
end_time(R, S, T0 + D) :- start_time(R, S, T0), duration(R, S, D).

% ===== RESOURCE CAPACITY CONSTRAINTS =====
% Capacity definitions
capacity(prep_area, 2).
capacity(oven, 1).
capacity(stove, 1).

% Helper: task uses resource
uses(T, Res) :- resource(T, Res).
uses(R, S, Res) :- resource(R, S, Res).

% Resource capacity constraint: at any time, number of concurrent tasks using resource <= capacity
% For special tasks
:- time(T), capacity(Res, C),
   #count{ T1 : start_time(T1, S1), end_time(T1, E1), S1 <= T, T < E1, uses(T1, Res) } > C.

% For recipe steps
:- time(T), capacity(Res, C),
   #count{ R, S : start_time(R, S, S1), end_time(R, S, E1), S1 <= T, T < E1, uses(R, S, Res) } > C.

% ===== PRECEDENCE CONSTRAINTS =====
% Within recipes
:- start_time(R, S1, T1), start_time(R, S2, T2), 
   precedes(R, S1, S2), T2 < T1 + D1, duration(R, S1, D1).

% Inter-recipe dependency
:- start_time(vegetable_soup, simmer_stock, T1), start_time(risotto, cook_risotto, T2),
   T2 < T1 + 30.  % simmer_stock duration is 30

% Oven preheat constraint
:- start_time(roast_chicken, bake_chicken, T_bake), start_time(preheat_oven, T_pre),
   T_bake < T_pre + 10.  % preheat_oven duration is 10

% ===== OBJECTIVE: MINIMIZE MAKESPAN =====
% Calculate makespan as maximum end time across all tasks
total_time(M) :- M = #max{ E : end_time(T, E) }, task(T).
total_time(M) :- M = #max{ E : end_time(R, S, E) }, recipe(R), step(R, S).

% Minimize makespan
#minimize { M@1 : total_time(M) }.

% ===== FEASIBILITY =====
feasible :- total_time(_).

% ===== SHOW DIRECTIVES =====
#show total_time/1.
#show feasible/0.
#show start_time/3.
#show end_time/3.
#show resource/3.
#show recipe/1.
#show step/2.