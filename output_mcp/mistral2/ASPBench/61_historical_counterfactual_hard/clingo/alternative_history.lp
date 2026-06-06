% --- Facts ---
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

% Prerequisites
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

% Pivot groups
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

% Conditional prerequisites
conditional_requires(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Prevented events
prevented(age_of_sail).

% --- Helper Predicates ---
% Possible events: all prerequisites are met
possible(E) :-
    event(E, _),
    not prevented(E),
    not impossible(E).

% Impossible events: prerequisites not met
impossible(E) :-
    event(E, _),
    requires(E, R),
    not occurs_original(R).

% Occurs in original timeline (choice)
{ occurs_original(E) : event(E, _) }.

% Occurs in alternate timeline (choice)
{ occurs_alternate(E) : event(E, _) }.

% --- Prerequisite Enforcement ---
% All prerequisites must occur
:- occurs_original(E), requires(E, R), not occurs_original(R).
:- occurs_alternate(E), requires(E, R), not occurs_alternate(R).

% --- Conditional Prerequisites ---
% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes unless age_of_steam occurs
:- occurs_original(alternate_industrial_revolution),
   not occurs_original(global_trade_routes),
   not occurs_original(age_of_steam).
:- occurs_alternate(alternate_industrial_revolution),
   not occurs_alternate(global_trade_routes),
   not occurs_alternate(age_of_steam).

% --- Pivot Group Logic ---
% At most one event per pivot group
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   occurs_original(E1), occurs_original(E2).
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   occurs_alternate(E1), occurs_alternate(E2).

% If any event in a pivot group is possible, exactly one must be chosen
:- pivot_group(G, E), possible(E),
   not occurs_original(E),
   not (pivot_group(G, E1), E1 < E, possible(E1), occurs_original(E1)).
:- pivot_group(G, E), possible(E),
   not occurs_alternate(E),
   not (pivot_group(G, E1), E1 < E, possible(E1), occurs_alternate(E1)).

% --- Original Timeline Pivot Rule: Choose earliest year if multiple are possible ---
% For pivot groups, choose the event with the earliest year if multiple are possible
chosen_pivot(G, E) :-
    pivot_group(G, E),
    occurs_original(E),
    possible(E),
    not (pivot_group(G, E1), E1 != E, possible(E1), occurs_original(E1), event(E1, Y1), event(E, Y), Y1 < Y).

% --- Interventions: Prevented events cannot occur in alternate timeline ---
:- occurs_alternate(E), prevented(E).

% --- Paradox Detection ---
% Paradox: An event is both possible and impossible
paradox(impossible_possible, E) :-
    possible(E),
    impossible(E).

% Paradox: A prevented event occurs in the alternate timeline
paradox(prevented_occurs, E) :-
    occurs_alternate(E),
    prevented(E).

% Paradox: A pivot group has no chosen event but has possible events
paradox(no_pivot_choice, G) :-
    pivot_group(G, _),
    possible(E) : pivot_group(G, E),
    not occurs_original(E),
    not occurs_alternate(E).

% --- Timelines ---
% Original timeline: events that occur and are not prevented
original_timeline(E) :- occurs_original(E), not prevented(E).

% Alternate timeline: events that occur and are not prevented
alternate_timeline(E) :- occurs_alternate(E), not prevented(E).

% --- Prevented Events ---
% Events in original_timeline but not in alternate_timeline
prevented_event(E) :-
    original_timeline(E),
    not alternate_timeline(E).

% --- Activated Events ---
% Events in alternate_timeline but not in original_timeline
activated_event(E) :-
    alternate_timeline(E),
    not original_timeline(E).

% --- Output ---
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_event/1.
#show activated_event/1.
#show paradox/2.