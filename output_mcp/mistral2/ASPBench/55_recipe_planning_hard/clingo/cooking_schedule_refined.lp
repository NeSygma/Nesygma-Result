% --- DOMAINS ---
time(0..200). % Increased horizon
recipe(roast_chicken; vegetable_soup; risotto; side_salad).
step(prep_chicken; bake_chicken; rest_chicken;
     chop_veg_soup; simmer_stock;
     chop_onion; cook_risotto;
     wash_greens; mix_dressing;
     preheat_oven).

resource(prep_area; oven; stove).

% --- FACTS ---
% Step durations
step_duration(prep_chicken, 15).
step_duration(bake_chicken, 50).
step_duration(rest_chicken, 10).
step_duration(chop_veg_soup, 20).
step_duration(simmer_stock, 30).
step_duration(chop_onion, 5).
step_duration(cook_risotto, 25).
step_duration(wash_greens, 5).
step_duration(mix_dressing, 10).
step_duration(preheat_oven, 10).

% Step resources
step_resource(prep_chicken, prep_area).
step_resource(bake_chicken, oven).
step_resource(rest_chicken, prep_area).
step_resource(chop_veg_soup, prep_area).
step_resource(simmer_stock, stove).
step_resource(chop_onion, prep_area).
step_resource(cook_risotto, stove).
step_resource(wash_greens, prep_area).
step_resource(mix_dressing, prep_area).
step_resource(preheat_oven, oven).

% Step recipes
step_recipe(prep_chicken, roast_chicken).
step_recipe(bake_chicken, roast_chicken).
step_recipe(rest_chicken, roast_chicken).
step_recipe(chop_veg_soup, vegetable_soup).
step_recipe(simmer_stock, vegetable_soup).
step_recipe(chop_onion, risotto).
step_recipe(cook_risotto, risotto).
step_recipe(wash_greens, side_salad).
step_recipe(mix_dressing, side_salad).
step_recipe(preheat_oven, special).

% Precedences within recipes
precedes(prep_chicken, bake_chicken).
precedes(bake_chicken, rest_chicken).
precedes(chop_veg_soup, simmer_stock).
precedes(chop_onion, cook_risotto).
precedes(wash_greens, mix_dressing).

% Inter-recipe dependency: simmer_stock must finish before cook_risotto starts
inter_recipe_dependency(simmer_stock, cook_risotto).

% Resource capacities
resource_capacity(prep_area, 2).
resource_capacity(oven, 1).
resource_capacity(stove, 1).

% --- CHOICE RULES ---
% Schedule all steps (including preheat_oven)
{ task(Step, Start, End, Resource) :
    step(Step),
    step_resource(Step, Resource),
    time(Start),
    time(End),
    End = Start + Duration,
    step_duration(Step, Duration)
} = 1.

% --- CONSTRAINTS ---
% All steps must be scheduled
:- step(Step), not scheduled(Step).
scheduled(Step) :- task(Step, _, _, _).

% Precedences within recipes (strict: End1 < Start2)
:- task(Step1, Start1, End1, _),
   task(Step2, Start2, End2, _),
   precedes(Step1, Step2),
   End1 >= Start2.

% Inter-recipe dependency (strict: End1 < Start2)
:- task(DepStep, Start1, End1, _),
   task(ReqStep, Start2, End2, _),
   inter_recipe_dependency(DepStep, ReqStep),
   End1 >= Start2.

% Resource capacity constraints
:- resource_capacity(Resource, Capacity),
   time(T),
   #count { Start, End : task(_, Start, End, Resource), T >= Start, T < End } > Capacity.

% Oven preheating: preheat_oven must finish before bake_chicken starts (strict)
:- task(preheat_oven, Start1, End1, oven),
   task(bake_chicken, Start2, End2, oven),
   End1 >= Start2.

% --- OPTIMIZATION ---
% Minimize total_time (makespan)
total_time(T) :- T = #max { End : task(_, _, End, _) }.
#minimize { T : total_time(T) }.

% --- SHOW ---
#show task/4.
#show total_time/1.