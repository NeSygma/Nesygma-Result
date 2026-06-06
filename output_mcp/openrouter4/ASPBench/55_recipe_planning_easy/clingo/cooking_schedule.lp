% Cooking schedule optimization

% Constants - set horizon just above expected optimal (35)
#const max_time = 40.

% Time domain
time(0..max_time).

% Steps: step(id, recipe, step_name, duration, resource)
step(1, pasta, prep, 10, prep_area).
step(2, pasta, boil, 15, stove).
step(3, pasta, serve, 5, prep_area).
step(4, salad, chop, 15, prep_area).
step(5, salad, mix, 5, prep_area).
step(6, bread, bake, 30, oven).

% Precedence constraints within recipes: prec(before_id, after_id)
prec(1, 2).  % pasta: prep before boil
prec(2, 3).  % pasta: boil before serve
prec(4, 5).  % salad: chop before mix

% Assignment: each step gets exactly one start time
{ start(SID, T) : time(T), T + Dur <= max_time } = 1 :- step(SID, _, _, Dur, _).

% End time derived from start time and duration
end(SID, T + Dur) :- start(SID, T), step(SID, _, _, Dur, _).

% Precedence constraints: before step must finish before after step starts
:- prec(SID1, SID2), end(SID1, E), start(SID2, S), E > S.

% Resource conflict: no two steps using the same resource may overlap
:- step(SID1, _, _, _, Res), step(SID2, _, _, _, Res), SID1 < SID2,
   start(SID1, S1), end(SID1, E1), start(SID2, S2), end(SID2, E2),
   S1 < E2, S2 < E1.

% Makespan: maximum end time across all steps
makespan(M) :- M = #max{ E : end(_, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

% Display results
#show start/2.
#show end/2.
#show makespan/1.

% For readable output, derive schedule facts
schedule(SID, Recipe, Step, St, En, Res) :-
    start(SID, St), end(SID, En), step(SID, Recipe, Step, _, Res).

#show schedule/6.