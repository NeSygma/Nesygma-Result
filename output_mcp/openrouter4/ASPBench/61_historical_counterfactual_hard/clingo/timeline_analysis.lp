% ==========================================
% PROBLEM DATA
% ==========================================
% Events with their years
event(ancient_knowledge; fall_of_rome; dark_ages; renaissance; age_of_sail; age_of_steam; discovery_of_new_world; global_trade_routes; industrial_revolution; information_age; alternate_industrial_revolution; digital_renaissance).

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

% Prerequisites: event E requires prerequisite P
prerequisite(fall_of_rome, ancient_knowledge).
prerequisite(dark_ages, fall_of_rome).
prerequisite(renaissance, dark_ages).
prerequisite(age_of_sail, renaissance).
prerequisite(age_of_steam, renaissance).
prerequisite(discovery_of_new_world, age_of_sail).
prerequisite(global_trade_routes, age_of_sail).
prerequisite(industrial_revolution, age_of_steam).
prerequisite(information_age, industrial_revolution).
prerequisite(digital_renaissance, alternate_industrial_revolution).

% Pivot groups: mutually exclusive events
pivot_group("paradigm", age_of_sail).
pivot_group("paradigm", age_of_steam).

% Conditional prerequisites: E requires Req UNLESS UnlessCond occurs
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam
cond_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Intervention: prevent age_of_sail
intervention(prevent, age_of_sail).

% ==========================================
% ORIGINAL TIMELINE MODELING
% ==========================================
% Use choice rules to determine which events occur
{ occurs_orig(E) } :- event(E).

% Constraint 1: Prerequisite enforcement - if E occurs, all its regular prerequisites must occur
:- occurs_orig(E), prerequisite(E, P), not occurs_orig(P).

% Constraint 2: Pivot exclusivity - at most one per pivot group
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, occurs_orig(E1), occurs_orig(E2).

% Helper: an event's regular prerequisites are all met
prereqs_met_orig(E) :- 
    event(E),
    #count { P : prerequisite(E, P), not occurs_orig(P) } = 0.

% Constraint 3: Pivot selection - if any event in a pivot group has prerequisites met, exactly one must be chosen
% If at least one event in the group is possible, at least one must occur
:- pivot_group(G, _), 
   #count { E : pivot_group(G, E), prereqs_met_orig(E) } > 0,
   #count { E : pivot_group(G, E), occurs_orig(E) } = 0.

% If at least one event in the group is possible, at most one can occur (already enforced by constraint 2)

% Constraint 4: Earliest year pivot rule - when multiple pivot events are possible, choose the one with earliest year
% If E1 (earlier) and E2 (later) are both possible, E2 cannot be chosen
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   prereqs_met_orig(E1), prereqs_met_orig(E2),
   year(E1, Y1), year(E2, Y2), Y1 < Y2,
   occurs_orig(E2).

% Constraint 5: Conditional prerequisite enforcement
% If E occurs and the UNLESS condition is NOT met, then the required event must also occur
:- occurs_orig(E), cond_prereq(E, Req, Unless), 
   not occurs_orig(Unless), not occurs_orig(Req).

% If an event's prerequisites are met and it's not a pivot-excluded event, it must occur
% (to ensure events don't randomly not occur when they should)
occurs_orig(E) :- prereqs_met_orig(E), not pivot_excluded_orig(E).
pivot_excluded_orig(E) :- pivot_group(G, E), pivot_group(G, E2), E != E2, occurs_orig(E2).

% ==========================================
% ALTERNATE TIMELINE MODELING
% ==========================================
{ occurs_alt(E) } :- event(E).

% Constraint 1: Prerequisite enforcement
:- occurs_alt(E), prerequisite(E, P), not occurs_alt(P).

% Constraint 2: Pivot exclusivity
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, occurs_alt(E1), occurs_alt(E2).

% Helper: prerequisites met
prereqs_met_alt(E) :- 
    event(E),
    #count { P : prerequisite(E, P), not occurs_alt(P) } = 0.

% Constraint 3: Pivot selection
:- pivot_group(G, _), 
   #count { E : pivot_group(G, E), prereqs_met_alt(E) } > 0,
   #count { E : pivot_group(G, E), occurs_alt(E) } = 0.

% Constraint 4: Earliest year pivot rule
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   prereqs_met_alt(E1), prereqs_met_alt(E2),
   year(E1, Y1), year(E2, Y2), Y1 < Y2,
   occurs_alt(E2).

% Constraint 5: Conditional prerequisite enforcement
:- occurs_alt(E), cond_prereq(E, Req, Unless), 
   not occurs_alt(Unless), not occurs_alt(Req).

% Constraint 6: Intervention - prevented events cannot occur
:- intervention(prevent, E), occurs_alt(E).

% Must-occur rule for alternate
occurs_alt(E) :- prereqs_met_alt(E), not pivot_excluded_alt(E).
pivot_excluded_alt(E) :- pivot_group(G, E), pivot_group(G, E2), E != E2, occurs_alt(E2).

% ==========================================
% ANALYSIS
% ==========================================
% Prevented: occurred in original but not in alternate
prevented(E) :- occurs_orig(E), not occurs_alt(E).

% Activated: occurred in alternate but not in original
activated(E) :- occurs_alt(E), not occurs_orig(E).

% ==========================================
% OUTPUT
% ==========================================
#show occurs_orig/1.
#show occurs_alt/1.
#show prevented/1.
#show activated/1.