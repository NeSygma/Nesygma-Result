% --- Domain ---
time(0..100).

% --- Tasks ---
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

% --- Durations and Resources ---
duration(prep_chicken, 15). resource(prep_chicken, prep_area).
duration(bake_chicken, 50). resource(bake_chicken, oven).
duration(rest_chicken, 10). resource(rest_chicken, prep_area).
duration(chop_veg_soup, 20). resource(chop_veg_soup, prep_area).
duration(simmer_stock, 30). resource(simmer_stock, stove).
duration(chop_onion, 5). resource(chop_onion, prep_area).
duration(cook_risotto, 25). resource(cook_risotto, stove).
duration(wash_greens, 5). resource(wash_greens, prep_area).
duration(mix_dressing, 10). resource(mix_dressing, prep_area).
duration(preheat_oven, 10). resource(preheat_oven, oven).

% --- Precedences ---
precedence(prep_chicken, bake_chicken).
precedence(bake_chicken, rest_chicken).
precedence(chop_veg_soup, simmer_stock).
precedence(chop_onion, cook_risotto).
precedence(wash_greens, mix_dressing).
precedence(simmer_stock, cook_risotto).
precedence(preheat_oven, bake_chicken).

% --- Scheduling ---
1 { start(Task, T) : time(T) } 1 :- task(Task).
end(Task, E) :- start(Task, S), duration(Task, D), E = S + D.

% --- Constraints ---
% 1. Precedence
:- precedence(T1, T2), end(T1, E1), start(T2, S2), S2 < E1.

% 2. Resource Capacity
% prep_area: 2
:- time(T), #count { Task : resource(Task, prep_area), start(Task, S), end(Task, E), S <= T, T < E } > 2.
% oven: 1
:- time(T), #count { Task : resource(Task, oven), start(Task, S), end(Task, E), S <= T, T < E } > 1.
% stove: 1
:- time(T), #count { Task : resource(Task, stove), start(Task, S), end(Task, E), S <= T, T < E } > 1.

% 3. Makespan
makespan(M) :- M = #max { E : end(Task, E) }.
#minimize { M : makespan(M) }.

% --- Output ---
#show start/2.
#show end/2.
#show makespan/1.