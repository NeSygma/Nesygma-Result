% ============================================================
% ALTERNATIVE HISTORY SCENARIO ANALYZER
% ============================================================

% --- Domain: Events and their years ---
event(ancient_knowledge).
event(fall_of_rome).
event(dark_ages).
event(renaissance).
event(age_of_sail).
event(age_of_steam).
event(discovery_of_new_world).
event(global_trade_routes).
event(industrial_revolution).
event(information_age).
event(alternate_industrial_revolution).
event(digital_renaissance).

year(ancient_knowledge, 100).
year(fall_of_rome, 476).
year(dark_ages, 500).
year(renaissance, 1300).
year(age_of_sail, 1400).
year(age_of_steam, 1700).
year(discovery_of_new_world, 1492).
year(global_trade_routes, 1550).
year(industrial_revolution, 1760).
year(information_age, 1970).
year(alternate_industrial_revolution, 1780).
year(digital_renaissance, 1980).

% --- Prerequisites (standard) ---
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

% --- Pivot Groups (mutually exclusive) ---
pivot_group(age_of_sail, paradigm).
pivot_group(age_of_steam, paradigm).

% --- Conditional Prerequisites ---
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
cond_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% --- Interventions ---
prevented(age_of_sail).

% ============================================================
% ORIGINAL TIMELINE (deterministic pivot selection by earliest year)
% ============================================================

% An event is possible in original timeline if all its standard prereqs are met
% and all its conditional prereqs are met (unless condition)
possible_original(E) :- event(E),
    prereq(E, _),
    not prereq_missing_original(E).
possible_original(E) :- event(E),
    not prereq(E, _),
    not cond_prereq(E, _, _).
possible_original(E) :- event(E),
    cond_prereq(E, _, _),
    not prereq(E, _),
    not cond_prereq_missing_original(E).

% Check if any standard prereq is missing
prereq_missing_original(E) :- prereq(E, P), not occurs_original(P).

% Check if conditional prereq is missing
cond_prereq_missing_original(E) :- cond_prereq(E, P, U), not occurs_original(P), not occurs_original(U).

% An event occurs in original if it has no prerequisites at all
occurs_original(E) :- event(E), not prereq(E, _), not cond_prereq(E, _, _).

% An event occurs if all its standard prereqs are met and it's not in a pivot group
occurs_original(E) :- event(E), prereq(E, _), not pivot_group(E, _),
    not prereq_missing_original(E),
    not cond_prereq_missing_original(E).

% An event with only conditional prereqs (no standard prereqs) occurs if cond prereq met
occurs_original(E) :- event(E), cond_prereq(E, _, _), not prereq(E, _),
    not cond_prereq_missing_original(E).

% --- Pivot Selection for Original Timeline ---
% Count how many pivot events in each group are possible
possible_pivot_original(G, E) :- pivot_group(E, G), possible_original(E).

% Select the earliest possible pivot event
% We need to ground Y from the event being considered
selected_pivot_original(E) :- pivot_group(E, G), possible_pivot_original(G, E),
    year(E, Y),
    not earlier_pivot_original(G, E, Y).

earlier_pivot_original(G, E1, Y1) :- pivot_group(E1, G), possible_pivot_original(G, E1),
    year(E1, Y1),
    pivot_group(E2, G), possible_pivot_original(G, E2),
    year(E2, Y2), Y2 < Y1, E1 != E2.

% Pivot event occurs if selected
occurs_original(E) :- selected_pivot_original(E).

% Non-selected pivot events do not occur
:- pivot_group(E, G), possible_pivot_original(G, E), not selected_pivot_original(E), occurs_original(E).

% ============================================================
% ALTERNATE TIMELINE (after interventions)
% ============================================================

% An event is possible in alternate timeline if all its standard prereqs are met
possible_alternate(E) :- event(E),
    prereq(E, _),
    not prereq_missing_alternate(E).
possible_alternate(E) :- event(E),
    not prereq(E, _),
    not cond_prereq(E, _, _).
possible_alternate(E) :- event(E),
    cond_prereq(E, _, _),
    not prereq(E, _),
    not cond_prereq_missing_alternate(E).

% Check if any standard prereq is missing in alternate
prereq_missing_alternate(E) :- prereq(E, P), not occurs_alternate(P).

% Check if conditional prereq is missing in alternate
cond_prereq_missing_alternate(E) :- cond_prereq(E, P, U), not occurs_alternate(P), not occurs_alternate(U).

% An event occurs in alternate if it has no prerequisites and is not prevented
occurs_alternate(E) :- event(E), not prereq(E, _), not cond_prereq(E, _, _), not prevented(E).

% An event occurs if all its standard prereqs are met, not in pivot group, not prevented
occurs_alternate(E) :- event(E), prereq(E, _), not pivot_group(E, _),
    not prereq_missing_alternate(E),
    not cond_prereq_missing_alternate(E),
    not prevented(E).

% An event with only conditional prereqs occurs if cond prereq met and not prevented
occurs_alternate(E) :- event(E), cond_prereq(E, _, _), not prereq(E, _),
    not cond_prereq_missing_alternate(E),
    not prevented(E).

% --- Pivot Selection for Alternate Timeline ---
possible_pivot_alternate(G, E) :- pivot_group(E, G), possible_alternate(E), not prevented(E).

% Select the earliest possible pivot event in alternate
selected_pivot_alternate(E) :- pivot_group(E, G), possible_pivot_alternate(G, E),
    year(E, Y),
    not earlier_pivot_alternate(G, E, Y).

earlier_pivot_alternate(G, E1, Y1) :- pivot_group(E1, G), possible_pivot_alternate(G, E1),
    year(E1, Y1),
    pivot_group(E2, G), possible_pivot_alternate(G, E2),
    year(E2, Y2), Y2 < Y1, E1 != E2.

% Pivot event occurs if selected and not prevented
occurs_alternate(E) :- selected_pivot_alternate(E), not prevented(E).

% Non-selected pivot events do not occur in alternate
:- pivot_group(E, G), possible_pivot_alternate(G, E), not selected_pivot_alternate(E), occurs_alternate(E).

% Prevented events cannot occur in alternate
:- prevented(E), occurs_alternate(E).

% ============================================================
% PARADOX DETECTION
% ============================================================

% A paradox occurs if a prevented event is required by a non-prevented event
% and there's no alternative path
paradox(required_event_prevented(E, P)) :- prevented(P), prereq(E, P), not prevented(E), occurs_alternate(E).

% A paradox occurs if a conditional prereq creates an impossible chain
paradox(cond_prereq_impossible(E)) :- cond_prereq(E, P, U), prevented(P), prevented(U), not prevented(E).

% ============================================================
% TIMELINE DIFFERENCES
% ============================================================

prevented_event(E) :- occurs_original(E), not occurs_alternate(E).
activated_event(E) :- occurs_alternate(E), not occurs_original(E).

% ============================================================
% OUTPUT
% ============================================================

#show occurs_original/1.
#show occurs_alternate/1.
#show prevented_event/1.
#show activated_event/1.
#show paradox/1.
#show selected_pivot_original/1.
#show selected_pivot_alternate/1.