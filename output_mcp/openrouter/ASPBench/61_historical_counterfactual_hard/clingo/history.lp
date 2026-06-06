% Events and years
event(ancient_knowledge). year(ancient_knowledge,100).

event(fall_of_rome). year(fall_of_rome,476).

event(dark_ages). year(dark_ages,500).

event(renaissance). year(renaissance,1300).

event(age_of_sail). year(age_of_sail,1400).

event(age_of_steam). year(age_of_steam,1700).

event(discovery_of_new_world). year(discovery_of_new_world,1492).

event(global_trade_routes). year(global_trade_routes,1550).

event(industrial_revolution). year(industrial_revolution,1760).

event(information_age). year(information_age,1970).

event(alternate_industrial_revolution). year(alternate_industrial_revolution,1780).

event(digital_renaissance). year(digital_renaissance,1980).

% Prerequisites (normal)
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

% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
conditional_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Pivot group (mutually exclusive)
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

pivot_event(E) :- pivot_group(_,E).

% ---------- Original timeline ----------
% Base case: events with no normal prerequisites and no conditional prerequisite
all_prereqs_satisfied_original(E) :- event(E), not prereq(E,_), not conditional_prereq(E,_,_).

% Normal prerequisites satisfied (all required events selected)
all_prereqs_satisfied_original(E) :-
    event(E),
    #count{R : prereq(E,R)} = N,
    #count{R : prereq(E,R), selected_original(R)} = N,
    not conditional_prereq(E,_,_).

% Conditional prerequisite satisfied (two alternatives)
all_prereqs_satisfied_original(E) :-
    conditional_prereq(E,Req,Unless),
    selected_original(Unless).
all_prereqs_satisfied_original(E) :-
    conditional_prereq(E,Req,Unless),
    selected_original(Req), not selected_original(Unless).

% Selection for non‑pivot events
selected_original(E) :-
    event(E),
    not pivot_event(E),
    all_prereqs_satisfied_original(E).

% Helper: earlier possible pivot event in the same group
earlier_possible_original(E) :-
    pivot_event(E),
    pivot_group(G,E),
    pivot_event(E2),
    pivot_group(G,E2),
    year(E2,Y2), year(E,Y), Y2 < Y,
    all_prereqs_satisfied_original(E2).

% Selection for pivot events (deterministic earliest‑year rule)
selected_original(E) :-
    pivot_event(E),
    all_prereqs_satisfied_original(E),
    not earlier_possible_original(E).

% Pivot exclusivity (at most one per group)
:- selected_original(E1), selected_original(E2), pivot_group(G,E1), pivot_group(G,E2), E1 != E2.

% ---------- Alternate timeline (with intervention) ----------
% Base case for alternate timeline
all_prereqs_satisfied_alternate(E) :- event(E), not prereq(E,_), not conditional_prereq(E,_,_).

% Normal prerequisites satisfied (using alternate selections)
all_prereqs_satisfied_alternate(E) :-
    event(E),
    #count{R : prereq(E,R)} = N,
    #count{R : prereq(E,R), selected_alternate(R)} = N,
    not conditional_prereq(E,_,_).

% Conditional prerequisite satisfied (two alternatives)
all_prereqs_satisfied_alternate(E) :-
    conditional_prereq(E,Req,Unless),
    selected_alternate(Unless).
all_prereqs_satisfied_alternate(E) :-
    conditional_prereq(E,Req,Unless),
    selected_alternate(Req), not selected_alternate(Unless).

% Selection for non‑pivot events in alternate timeline
selected_alternate(E) :-
    event(E),
    not pivot_event(E),
    all_prereqs_satisfied_alternate(E).

% Helper: earlier possible pivot event in the same group (alternate)
earlier_possible_alternate(E) :-
    pivot_event(E),
    pivot_group(G,E),
    pivot_event(E2),
    pivot_group(G,E2),
    year(E2,Y2), year(E,Y), Y2 < Y,
    all_prereqs_satisfied_alternate(E2).

% Selection for pivot events (deterministic earliest‑year rule)
selected_alternate(E) :-
    pivot_event(E),
    all_prereqs_satisfied_alternate(E),
    not earlier_possible_alternate(E).

% Pivot exclusivity for alternate timeline
:- selected_alternate(E1), selected_alternate(E2), pivot_group(G,E1), pivot_group(G,E2), E1 != E2.

% Intervention: prevent age_of_sail in alternate timeline
:- selected_alternate(age_of_sail).

% ---------- Output predicates ----------
original_timeline(E) :- selected_original(E).
alternate_timeline(E) :- selected_alternate(E).
prevented_events(E) :- original_timeline(E), not alternate_timeline(E).
activated_events(E) :- alternate_timeline(E), not original_timeline(E).
% No paradoxes expected; define none
% paradoxes/1 left empty

#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show activated_events/1.
#show paradoxes/1.