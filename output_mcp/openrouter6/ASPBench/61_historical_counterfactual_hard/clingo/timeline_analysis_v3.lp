% Timeline Analysis with Pivot Events and Conditional Prerequisites

% =====================
% 1. EVENT DATA
% =====================
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

% =====================
% 2. PREREQUISITES
% =====================
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

% =====================
% 3. PIVOT GROUPS
% =====================
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

% =====================
% 4. CONDITIONAL PREREQUISITES
% =====================
conditional_requires(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% =====================
% 5. INTERVENTIONS
% =====================
prevented(age_of_sail).  % For alternate timeline

% =====================
% 6. ORIGINAL TIMELINE
% =====================

% Helper: Check if unconditional prerequisites are satisfied
prereq_missing_original(E, R) :- requires(E, R), not occurs_original(R).

% Helper: Check if conditional prerequisites are satisfied
conditional_missing_original(E, R, U) :- 
    conditional_requires(E, R, U),
    not occurs_original(U),
    not occurs_original(R).

% Possible event: all prerequisites satisfied
possible_original(E) :-
    not prereq_missing_original(E, _),
    not conditional_missing_original(E, _, _).

% Non-pivot events occur if possible
occurs_original(E) :- not pivot_group(_, E), possible_original(E).

% Pivot events: define which are possible
pivot_possible_original(G, E) :- pivot_group(G, E), possible_original(E).

% Helper: Check if an earlier pivot exists in the same group
earlier_pivot_exists_original(G, E) :-
    pivot_possible_original(G, E),
    year(E, Y),
    pivot_possible_original(G, F),
    year(F, Z),
    Z < Y.

% Determine earliest pivot event in each group
earliest_pivot_original(G, E) :-
    pivot_possible_original(G, E),
    not earlier_pivot_exists_original(G, E).

% Exactly one pivot event per group if any are possible: choose earliest
occurs_original(E) :- earliest_pivot_original(G, E), pivot_group(G, E).

% =====================
% 7. ALTERNATE TIMELINE
% =====================

% Helper: Check if unconditional prerequisites are satisfied (alternate)
prereq_missing_alternate(E, R) :- requires(E, R), not occurs_alternate(R).

% Helper: Check if conditional prerequisites are satisfied (alternate)
conditional_missing_alternate(E, R, U) :- 
    conditional_requires(E, R, U),
    not occurs_alternate(U),
    not occurs_alternate(R).

% Possible event: all prerequisites satisfied (alternate)
possible_alternate(E) :-
    not prereq_missing_alternate(E, _),
    not conditional_missing_alternate(E, _, _).

% Non-pivot events occur if possible (alternate)
occurs_alternate(E) :- not pivot_group(_, E), possible_alternate(E).

% Pivot events: define which are possible (alternate)
pivot_possible_alternate(G, E) :- pivot_group(G, E), possible_alternate(E).

% Helper: Check if an earlier pivot exists in the same group (alternate)
earlier_pivot_exists_alternate(G, E) :-
    pivot_possible_alternate(G, E),
    year(E, Y),
    pivot_possible_alternate(G, F),
    year(F, Z),
    Z < Y.

% Determine earliest pivot event in each group (alternate)
earliest_pivot_alternate(G, E) :-
    pivot_possible_alternate(G, E),
    not earlier_pivot_exists_alternate(G, E).

% Exactly one pivot event per group if any are possible: choose earliest (alternate)
occurs_alternate(E) :- earliest_pivot_alternate(G, E), pivot_group(G, E).

% Intervention enforcement: prevented events cannot occur in alternate timeline
:- occurs_alternate(E), prevented(E).

% =====================
% 8. OUTPUT PREDICATES
% =====================

% Original timeline events
original_timeline(E) :- occurs_original(E).

% Alternate timeline events
alternate_timeline(E) :- occurs_alternate(E).

% Prevented events (in original but not alternate)
prevented_events(E) :- original_timeline(E), not alternate_timeline(E).

% Activated events (in alternate but not original)
activated_events(E) :- alternate_timeline(E), not original_timeline(E).

% Paradoxes: none in this solution
paradox(E) :- false.

% =====================
% 9. ORDERED OUTPUT (for sorting)
% =====================

% Helper: Count of events with smaller year for original timeline
original_timeline_count_smaller(E, Count) :-
    original_timeline(E),
    year(E, Y),
    Count = #count{ F : original_timeline(F), year(F, Y2), Y2 < Y }.

% Original timeline sorted by year
original_timeline_ordered(I, E) :-
    original_timeline(E),
    original_timeline_count_smaller(E, Count),
    I = 1 + Count.

% Helper: Count of events with smaller year for alternate timeline
alternate_timeline_count_smaller(E, Count) :-
    alternate_timeline(E),
    year(E, Y),
    Count = #count{ F : alternate_timeline(F), year(F, Y2), Y2 < Y }.

% Alternate timeline sorted by year
alternate_timeline_ordered(I, E) :-
    alternate_timeline(E),
    alternate_timeline_count_smaller(E, Count),
    I = 1 + Count.

% Helper: Count of prevented events with smaller alphabetical order
prevented_events_count_smaller(E, Count) :-
    prevented_events(E),
    Count = #count{ F : prevented_events(F), F < E }.

% Prevented events sorted alphabetically (by symbol order)
prevented_events_ordered(I, E) :-
    prevented_events(E),
    prevented_events_count_smaller(E, Count),
    I = 1 + Count.

% Helper: Count of activated events with smaller alphabetical order
activated_events_count_smaller(E, Count) :-
    activated_events(E),
    Count = #count{ F : activated_events(F), F < E }.

% Activated events sorted alphabetically (by symbol order)
activated_events_ordered(I, E) :-
    activated_events(E),
    activated_events_count_smaller(E, Count),
    I = 1 + Count.

% =====================
% 10. SHOW DIRECTIVES
% =====================
#show original_timeline_ordered/2.
#show alternate_timeline_ordered/2.
#show prevented_events_ordered/2.
#show activated_events_ordered/2.
#show paradox/1.