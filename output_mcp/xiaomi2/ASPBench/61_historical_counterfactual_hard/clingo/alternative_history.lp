% =============================================
% Alternative History Scenario Analysis
% =============================================

% === Timelines ===
timeline(original).
timeline(alternate).

% === Events and Years ===
event(ancient_knowledge). year(ancient_knowledge, 100).
event(fall_of_rome). year(fall_of_rome, 476).
event(dark_ages). year(dark_ages, 500).
event(renaissance). year(renaissance, 1300).
event(age_of_sail). year(age_of_sail, 1400).
event(age_of_steam). year(age_of_steam, 1700).
event(discovery_of_new_world). year(discovery_of_new_world, 1492).
event(global_trade_routes). year(global_trade_routes, 1550).
event(industrial_revolution). year(industrial_revolution, 1760).
event(information_age). year(information_age, 1970).
event(alternate_industrial_revolution). year(alternate_industrial_revolution, 1780).
event(digital_renaissance). year(digital_renaissance, 1980).

% === Regular Prerequisites ===
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

% === Pivot Groups (mutually exclusive) ===
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

% === Conditional Prerequisites ===
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
cond_requires(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% === Interventions ===
prevented(age_of_sail).

% === Intervention Enforcement: prevented events blocked in alternate timeline ===
prevented_in(E, alternate) :- prevented(E).

% =============================================
% Prerequisite Logic
% =============================================

% A regular prerequisite is unmet if the required event does not occur
has_unmet_regular(E, T) :- requires(E, P), timeline(T), not occurs(P, T).

% A conditional prerequisite is met if the "unless" event occurs
cond_prereq_met(E, T) :- cond_requires(E, _, U), occurs(U, T), timeline(T).
% A conditional prerequisite is also met if the required event occurs
cond_prereq_met(E, T) :- cond_requires(E, P, _), occurs(P, T), timeline(T).

% A conditional prerequisite is unmet if neither condition holds
has_unmet_conditional(E, T) :- cond_requires(E, _, _), timeline(T), not cond_prereq_met(E, T).

% All prerequisites are met for an event in a timeline
prereqs_met(E, T) :- event(E), timeline(T),
    not has_unmet_regular(E, T),
    not has_unmet_conditional(E, T).

% =============================================
% Event Possibility
% =============================================

% An event is possible if prerequisites are met and it is not prevented
possible(E, T) :- prereqs_met(E, T), not prevented_in(E, T).

% =============================================
% Pivot Group Logic
% =============================================

% A pivot group needs selection if any event in it has prerequisites met
group_needs_selection(G, T) :- pivot_group(G, E), prereqs_met(E, T), timeline(T).

% If a pivot group needs selection, exactly one possible event must be chosen
1 { occurs(E, T) : pivot_group(G, E), possible(E, T) } 1 :- group_needs_selection(G, T).

% Pivot exclusivity: at most one event from each pivot group per timeline
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   occurs(E1, T), occurs(E2, T).

% =============================================
% Non-Pivot Events
% =============================================

% Non-pivot events occur automatically if they are possible
occurs(E, T) :- event(E), timeline(T),
    not pivot_group(_, E),
    possible(E, T).

% =============================================
% Integrity Constraints
% =============================================

% An event cannot occur if its prerequisites are not met
:- occurs(E, T), not prereqs_met(E, T).

% An event cannot occur if it is prevented in that timeline
:- occurs(E, T), prevented_in(E, T).

% =============================================
% Original Timeline: Deterministic Pivot Selection
% =============================================

% In the original timeline, when multiple pivot events are possible,
% the one with the earliest year is chosen.
% (If E1 has earlier year than E2, both possible, E2 cannot occur in original.)
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   year(E1, Y1), year(E2, Y2), Y1 < Y2,
   possible(E1, original), possible(E2, original),
   occurs(E2, original).

% =============================================
% Output Predicates
% =============================================

original_event(E) :- occurs(E, original).
alternate_event(E) :- occurs(E, alternate).
prevented_event(E) :- occurs(E, original), not occurs(E, alternate).
activated_event(E) :- occurs(E, alternate), not occurs(E, original).

#show original_event/1.
#show alternate_event/1.
#show prevented_event/1.
#show activated_event/1.