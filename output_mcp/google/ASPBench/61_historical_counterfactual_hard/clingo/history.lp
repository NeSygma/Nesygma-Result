% --- Events and Data ---
event(ancient_knowledge, 100).
event(fall_of_rome, 476).
event(dark_ages, 500).
event(renaissance, 1300).
event(age_of_sail, 1400).
event(age_of_steam, 1700).
event(discovery_of_new_world, 1492).
event(global_trade_routes, 1550).
event(industrial_revolution, 1760).
event(information_age, 1970).
event(alternate_industrial_revolution, 1780).
event(digital_renaissance, 1980).

requires(fall_of_rome, ancient_knowledge).
requires(dark_ages, fall_of_rome).
requires(renaissance, dark_ages).
requires(age_of_sail, renaissance).
requires(age_of_steam, renaissance).
requires(discovery_of_new_world, age_of_sail).
requires(global_trade_routes, age_of_sail).
requires(industrial_revolution, age_of_steam).
requires(information_age, industrial_revolution).
requires(digital_renaissance, alternate_industrial_revolution).

pivot(paradigm, age_of_sail).
pivot(paradigm, age_of_steam).

conditional_requires(alternate_industrial_revolution, global_trade_routes, age_of_steam).

intervention(age_of_sail).

timeline(original).
timeline(alternate).

% --- Logic ---
% Every event can potentially occur
{ occurs(T, E) } :- timeline(T), event(E, _).

% Prerequisite enforcement
:- occurs(T, E), requires(E, P), not occurs(T, P).
:- occurs(T, E), conditional_requires(E, P, U), not occurs(T, P), not occurs(T, U).

% Pivot exclusivity
:- occurs(T, E1), occurs(T, E2), pivot(G, E1), pivot(G, E2), E1 != E2.

% Pivot selection: If any event in a pivot group is possible, exactly one must be chosen
% An event is possible if its prerequisites are met
possible(T, E) :- timeline(T), event(E, _), 
                  not requires(E, _), 
                  not conditional_requires(E, _, _).
possible(T, E) :- timeline(T), event(E, _), 
                  requires(E, _),
                  { requires(E, P) : not occurs(T, P) } = 0.
possible(T, E) :- timeline(T), event(E, _), 
                  conditional_requires(E, _, _),
                  { conditional_requires(E, P, U) : not occurs(T, P), not occurs(T, U) } = 0.

pivot_possible(T, G) :- pivot(G, E), possible(T, E).
1 { occurs(T, E) : pivot(G, E) } 1 :- pivot_possible(T, G).

% Original timeline: Deterministic pivot selection (earliest year)
:- timeline(original), pivot(G, E1), pivot(G, E2), E1 != E2, 
   possible(original, E1), possible(original, E2), 
   event(E1, Y1), event(E2, Y2), Y1 < Y2, occurs(original, E2).

% Intervention enforcement
:- timeline(alternate), intervention(E), occurs(alternate, E).

% --- Output ---
prevented(E) :- occurs(original, E), not occurs(alternate, E).
activated(E) :- occurs(alternate, E), not occurs(original, E).

#show occurs/2.
#show prevented/1.
#show activated/1.