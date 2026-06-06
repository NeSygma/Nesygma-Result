% ==========================================
% PROBLEM DATA
% ==========================================
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

% Prerequisites
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

% Pivot groups
pivot_group("paradigm", age_of_sail).
pivot_group("paradigm", age_of_steam).

% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam
cond_prereq(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Intervention
intervention(prevent, age_of_sail).

% ==========================================
% ORIGINAL TIMELINE - Direct deterministic rules
% ==========================================
% Base event has no prerequisites
occurs_orig(ancient_knowledge).

% Direct prerequisite chains (excluding pivot events which need special handling)
occurs_orig(fall_of_rome) :- occurs_orig(ancient_knowledge).
occurs_orig(dark_ages) :- occurs_orig(fall_of_rome).
occurs_orig(renaissance) :- occurs_orig(dark_ages).

% Pivot group: age_of_sail (1400) and age_of_steam (1700) both require renaissance
% In original timeline, choose earliest year: age_of_sail
occurs_orig(age_of_sail) :- occurs_orig(renaissance).

% age_of_steam does NOT occur in original (pivot exclusivity - sail is chosen)

% Events requiring age_of_sail
occurs_orig(discovery_of_new_world) :- occurs_orig(age_of_sail).
occurs_orig(global_trade_routes) :- occurs_orig(age_of_sail).

% Events requiring age_of_steam - don't occur in original
% industrial_revolution requires age_of_steam -> doesn't occur
% information_age requires industrial_revolution -> doesn't occur

% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam
% In original, age_of_steam does NOT occur, so global_trade_routes IS required
occurs_orig(alternate_industrial_revolution) :- occurs_orig(global_trade_routes).

% digital_renaissance requires alternate_industrial_revolution
occurs_orig(digital_renaissance) :- occurs_orig(alternate_industrial_revolution).

% ==========================================
% ALTERNATE TIMELINE - Direct deterministic rules
% ==========================================
occurs_alt(ancient_knowledge).
occurs_alt(fall_of_rome) :- occurs_alt(ancient_knowledge).
occurs_alt(dark_ages) :- occurs_alt(fall_of_rome).
occurs_alt(renaissance) :- occurs_alt(dark_ages).

% Intervention prevents age_of_sail - so it does NOT occur in alternate

% Pivot: age_of_sail is prevented, so age_of_steam must be chosen
occurs_alt(age_of_steam) :- occurs_alt(renaissance).

% discovery_of_new_world and global_trade_routes require age_of_sail - don't occur

% industrial_revolution requires age_of_steam
occurs_alt(industrial_revolution) :- occurs_alt(age_of_steam).

% Conditional: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam
% age_of_steam OCCURS in alternate, so UNLESS applies - requirement is waived
% alternate_industrial_revolution has no other prerequisites, so it can occur
occurs_alt(alternate_industrial_revolution) :- occurs_alt(age_of_steam).

% information_age requires industrial_revolution
occurs_alt(information_age) :- occurs_alt(industrial_revolution).

% digital_renaissance requires alternate_industrial_revolution
occurs_alt(digital_renaissance) :- occurs_alt(alternate_industrial_revolution).

% ==========================================
% CONSISTENCY CONSTRAINTS
% ==========================================
% Ensure pivot exclusivity in original
:- occurs_orig(age_of_sail), occurs_orig(age_of_steam).

% Ensure pivot exclusivity in alternate
:- occurs_alt(age_of_sail), occurs_alt(age_of_steam).

% Ensure intervention is enforced in alternate
:- intervention(prevent, E), occurs_alt(E).

% ==========================================
% ANALYSIS
% ==========================================
prevented(E) :- occurs_orig(E), not occurs_alt(E).
activated(E) :- occurs_alt(E), not occurs_orig(E).

% ==========================================
% OUTPUT
% ==========================================
#show occurs_orig/1.
#show occurs_alt/1.
#show prevented/1.
#show activated/1.