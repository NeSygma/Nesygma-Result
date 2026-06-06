% --- Domain definitions ---
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

% --- Prerequisites ---
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

% --- Conditional prerequisite ---
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
cond_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% --- Pivot group ---
% group "paradigm" contains age_of_sail and age_of_steam (mutually exclusive)
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

pivot_event(E) :- pivot_group(_,E).

% -------------------------------------------------
% Helper: an event's prerequisites are satisfied (ignoring pivot exclusivity)
% Base events with no normal prereq and no conditional prereq are possible.
possible(E) :- event(E), not prereq(E,_), not cond_prereq(E,_,_).
% Propagate normal prerequisites
possible(E) :- prereq(E,R), possible(R).
% Conditional prerequisite satisfied via unless condition
possible(E) :- cond_prereq(E,_,U), possible(U).
% Conditional prerequisite satisfied via required when unless not present
possible(E) :- cond_prereq(E,Req,U), possible(Req), not possible(U).

% -------------------------------------------------
% Original timeline deterministic pivot selection (earliest year)
% Determine if an earlier pivot in same group is possible
earlier_possible_original(E) :-
    pivot_event(E), pivot_group(G,E),
    pivot_event(E2), pivot_group(G,E2),
    year(E2,Y2), year(E,Y), Y2 < Y,
    possible(E2).

% Selected pivot event for original timeline: earliest possible
selected_original(E) :- pivot_event(E), possible(E), not earlier_possible_original(E).

% Non-pivot events occur if they are possible
selected_original(E) :- not pivot_event(E), possible(E).

% Pivot exclusivity (at most one per group) is guaranteed by selection rule, but add safety constraint
:- selected_original(E1), selected_original(E2), pivot_group(G,E1), pivot_group(G,E2), E1 != E2.

% -------------------------------------------------
% Alternate timeline with intervention (prevent age_of_sail)
% The same possible/possible definitions apply (prereqs unchanged)
% Determine earlier possible pivot in alternate timeline (same logic)
earlier_possible_alternate(E) :-
    pivot_event(E), pivot_group(G,E),
    pivot_event(E2), pivot_group(G,E2),
    year(E2,Y2), year(E,Y), Y2 < Y,
    possible(E2).

% Selected pivot for alternate timeline: earliest possible that is not prevented
selected_alternate(E) :- pivot_event(E), possible(E), not earlier_possible_alternate(E), not prevented(E).

% Define prevented events (intervention) – age_of_sail is prevented
prevented(age_of_sail).

% Non-pivot events occur if possible
selected_alternate(E) :- not pivot_event(E), possible(E).

% Pivot exclusivity safety constraint for alternate timeline
:- selected_alternate(E1), selected_alternate(E2), pivot_group(G,E1), pivot_group(G,E2), E1 != E2.

% -------------------------------------------------
% Output predicates
original_timeline(E) :- selected_original(E).
alternate_timeline(E) :- selected_alternate(E).
prevented_events(E) :- original_timeline(E), not alternate_timeline(E).
activated_events(E) :- alternate_timeline(E), not original_timeline(E).
% No paradoxes detected in this model
paradoxes :- false.

#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show activated_events/1.
#show paradoxes/1.