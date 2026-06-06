%%% DATA %%%

% Events with years
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

% Prerequisites: event E requires event R
prereq(fall_of_rome, ancient_knowledge).
prereq(dark_ages, fall_of_rome).
prereq(renaissance, dark_ages).
prereq(age_of_sail, renaissance).
prereq(age_of_steam, renaissance).
prereq(discovery_of_new_world, age_of_sail).
prereq(global_trade_routes, age_of_sail).
prereq(industrial_revolution, age_of_steam).
prereq(information_age, industrial_revolution).
prereq(digital_renaissance, alternate_industrial_revolution).

% Pivot groups
pivot_group("paradigm", age_of_sail).
pivot_group("paradigm", age_of_steam).

% Conditional prerequisites: event E requires event R UNLESS event U occurs
cond_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Interventions: prevent these events in alternate timeline
intervention(age_of_sail).

%%% DOMAIN %%%

% All events
event(E) :- event(E, _).
year(E, Y) :- event(E, Y).

%%% ORIGINAL TIMELINE %%%

% Choice: which events occur in original timeline
{ occurs_original(E) } :- event(E).

% Prerequisite enforcement for original
:- occurs_original(E), prereq(E, R), not occurs_original(R).

% Pivot exclusivity: at most one per group
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, occurs_original(E1), occurs_original(E2).

% Pivot selection: if any event in a pivot group is possible (prerequisites met), exactly one must be chosen
% An event is possible if all its prerequisites occur
possible_original(E) :- event(E), prereq(E, R) : occurs_original(R).
% Events with no prerequisites are always possible
possible_original(E) :- event(E), not prereq(E, _).

% For each pivot group, if at least one event is possible, exactly one must occur
:- pivot_group(G, _), #count{ E : pivot_group(G, E), possible_original(E) } >= 1, #count{ E : pivot_group(G, E), occurs_original(E) } = 0.
:- pivot_group(G, _), #count{ E : pivot_group(G, E), possible_original(E) } >= 1, #count{ E : pivot_group(G, E), occurs_original(E) } > 1.

% Original timeline pivot rule: when multiple pivot events are possible, choose the one with the earliest year
% We need to enforce that if both age_of_sail and age_of_steam are possible, we pick the earliest (age_of_sail has year 1400, age_of_steam has 1700)
% So: if age_of_sail is possible, it must occur (since it's earliest)
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, possible_original(E1), possible_original(E2), year(E1, Y1), year(E2, Y2), Y1 < Y2, not occurs_original(E1).

% Conditional prerequisite logic for original
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
:- occurs_original(E), cond_prereq(E, R, U), not occurs_original(U), not occurs_original(R).

%%% ALTERNATE TIMELINE %%%

% Choice: which events occur in alternate timeline
{ occurs_alternate(E) } :- event(E).

% Prerequisite enforcement for alternate
:- occurs_alternate(E), prereq(E, R), not occurs_alternate(R).

% Pivot exclusivity for alternate
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, occurs_alternate(E1), occurs_alternate(E2).

% Pivot selection for alternate: if any event in a pivot group is possible, exactly one must be chosen
possible_alternate(E) :- event(E), prereq(E, R) : occurs_alternate(R).
possible_alternate(E) :- event(E), not prereq(E, _).

:- pivot_group(G, _), #count{ E : pivot_group(G, E), possible_alternate(E) } >= 1, #count{ E : pivot_group(G, E), occurs_alternate(E) } = 0.
:- pivot_group(G, _), #count{ E : pivot_group(G, E), possible_alternate(E) } >= 1, #count{ E : pivot_group(G, E), occurs_alternate(E) } > 1.

% Intervention enforcement: prevented events cannot occur in alternate timeline
:- intervention(E), occurs_alternate(E).

% Conditional prerequisite logic for alternate
:- occurs_alternate(E), cond_prereq(E, R, U), not occurs_alternate(U), not occurs_alternate(R).

%%% OUTPUT %%%

% Original timeline events sorted by year
original_event(E) :- occurs_original(E).

% Alternate timeline events sorted by year
alternate_event(E) :- occurs_alternate(E).

% Prevented: occurred in original but not alternate
prevented(E) :- occurs_original(E), not occurs_alternate(E).

% Activated: occurred in alternate but not original
activated(E) :- occurs_alternate(E), not occurs_original(E).

% Paradox detection: check for logical impossibilities
% A paradox occurs if the constraints cannot be simultaneously satisfied
% Since we're modeling both timelines together, if unsat we detect paradox
paradox("unsatisfiable_constraints") :- false.

#show original_event/1.
#show alternate_event/1.
#show prevented/1.
#show activated/1.
#show paradox/1.