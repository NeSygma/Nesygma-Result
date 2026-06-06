% Historical Timeline Analysis with Pivot Events and Conditional Prerequisites

% ==================== DOMAIN DEFINITIONS ====================
% Events with their years
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

% Pivot groups
pivot_group("paradigm", age_of_sail).
pivot_group("paradigm", age_of_steam).

% Simple prerequisites
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

% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
% This means: alternate_industrial_revolution can occur if global_trade_routes occurs AND age_of_steam does NOT occur
% OR if age_of_steam occurs (then the global_trade_routes requirement is waived)

% ==================== TIMELINE DEFINITIONS ====================
% We need to model two timelines: original and alternate
% For each timeline, we need to determine which events occur

% Original timeline events (to be determined)
{ occurred_original(E) } :- event(E, _).

% Alternate timeline events (to be determined)
{ occurred_alternate(E) } :- event(E, _).

% ==================== PREREQUISITE ENFORCEMENT ====================
% An event can only occur if all its required events have occurred
:- occurred_original(E), requires(E, R), not occurred_original(R).
:- occurred_alternate(E), requires(E, R), not occurred_alternate(R).

% ==================== CONDITIONAL PREREQUISITE LOGIC ====================
% alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
% This means: if age_of_steam occurs, then alternate_industrial_revolution can occur regardless of global_trade_routes
% If age_of_steam does NOT occur, then alternate_industrial_revolution requires global_trade_routes

% For original timeline
:- occurred_original(alternate_industrial_revolution), 
   not occurred_original(age_of_steam), 
   not occurred_original(global_trade_routes).

% For alternate timeline
:- occurred_alternate(alternate_industrial_revolution), 
   not occurred_alternate(age_of_steam), 
   not occurred_alternate(global_trade_routes).

% ==================== PIVOT EXCLUSIVITY ====================
% At most one event from each pivot group can occur in each timeline
% Group "paradigm": age_of_sail, age_of_steam
:- occurred_original(age_of_sail), occurred_original(age_of_steam).
:- occurred_alternate(age_of_sail), occurred_alternate(age_of_steam).

% ==================== PIVOT SELECTION RULE ====================
% If any event in a pivot group is possible (prerequisites met), exactly one must be chosen
% For original timeline: choose the one with earliest year (deterministic)
% For alternate timeline: we'll need to consider interventions

% Helper: check if a pivot event is possible (prerequisites met)
possible_original(E) :- event(E, _), 
                         not (requires(E, R), not occurred_original(R)).

possible_alternate(E) :- event(E, _), 
                         not (requires(E, R), not occurred_alternate(R)).

% Original timeline: if a pivot event is possible, exactly one must be chosen
% For group "paradigm": if either age_of_sail or age_of_steam is possible, exactly one occurs
% Since we want earliest year, we'll enforce that if both are possible, age_of_sail (earlier) occurs
% But we need to handle the case where only one is possible

% For original timeline: if age_of_sail is possible, it must occur (earliest year)
% If age_of_sail is not possible but age_of_steam is possible, then age_of_steam must occur
% This ensures exactly one occurs when at least one is possible

% Rule: if age_of_sail is possible, it must occur in original timeline
% But we need to be careful: this might conflict with other constraints

% Let's think differently: we want exactly one pivot event when at least one is possible
% For original timeline, we choose the earliest possible one

% First, determine which pivot events are possible in original timeline
possible_pivot_original(age_of_sail) :- possible_original(age_of_sail).
possible_pivot_original(age_of_steam) :- possible_original(age_of_steam).

% If at least one pivot is possible, exactly one must occur
% For original timeline: choose the earliest year
% age_of_sail (1400) is earlier than age_of_steam (1700)
% So if age_of_sail is possible, it must occur
% If age_of_sail is not possible but age_of_steam is possible, then age_of_steam must occur

% Rule: if age_of_sail is possible, it must occur in original timeline
% But this might be too strong - what if we want to test alternatives?

% Actually, for original timeline, we want deterministic selection by earliest year
% So: if age_of_sail is possible, it occurs; otherwise if age_of_steam is possible, it occurs

% But we need to ensure exactly one occurs when at least one is possible
% Let's use a different approach: define which pivot occurs based on possibilities

% For original timeline:
% If age_of_sail is possible, then age_of_sail occurs (and age_of_steam does not)
% If age_of_sail is not possible but age_of_steam is possible, then age_of_steam occurs
% If neither is possible, neither occurs

% This ensures at most one occurs, and exactly one occurs when at least one is possible

% ==================== INTERVENTION ENFORCEMENT ====================
% Prevent age_of_sail in alternate timeline
:- occurred_alternate(age_of_sail).

% ==================== ORIGINAL TIMELINE DETERMINISTIC SELECTION ====================
% For original timeline, we need to enforce the pivot selection rule
% If age_of_sail is possible, it must occur (earliest year)
% If age_of_sail is not possible but age_of_steam is possible, then age_of_steam must occur

% First, determine if age_of_sail is possible in original timeline
possible_age_of_sail_original :- possible_original(age_of_sail).

% If age_of_sail is possible, it must occur in original timeline
occurred_original(age_of_sail) :- possible_age_of_sail_original.

% If age_of_sail is not possible but age_of_steam is possible, then age_of_steam must occur
possible_age_of_steam_original :- possible_original(age_of_steam), not possible_age_of_sail_original.
occurred_original(age_of_steam) :- possible_age_of_steam_original.

% ==================== ALTERNATE TIMELINE SELECTION ====================
% For alternate timeline, we need to consider the intervention (prevent age_of_sail)
% So age_of_sail cannot occur in alternate timeline
% If age_of_steam is possible, it must occur (since age_of_sail is prevented)
% If neither is possible, neither occurs

% Determine if age_of_steam is possible in alternate timeline
possible_age_of_steam_alternate :- possible_alternate(age_of_steam).

% If age_of_steam is possible, it must occur in alternate timeline
occurred_alternate(age_of_steam) :- possible_age_of_steam_alternate.

% ==================== FRAME AXIOMS (PERSISTENCE) ====================
% Events that occur in original timeline but not in alternate timeline are "prevented"
% Events that occur in alternate timeline but not in original timeline are "activated"

% ==================== PARADOX DETECTION ====================
% A paradox occurs if the constraints cannot be satisfied
% We'll detect paradoxes by checking if the timeline generation fails

% For original timeline: check if pivot selection is consistent
% If both age_of_sail and age_of_steam are possible, we choose age_of_sail (earliest)
% This should always be consistent

% For alternate timeline: check if the intervention creates a paradox
% If age_of_sail is required for some event but prevented, that might create a paradox

% Check for paradoxes in alternate timeline
% If an event requires age_of_sail but age_of_sail is prevented, and there's no alternative
% For example: discovery_of_new_world requires age_of_sail
% If age_of_sail is prevented, then discovery_of_new_world cannot occur
% This is not a paradox, just a consequence of the intervention

% A paradox would be if the constraints are contradictory
% For example, if we required both age_of_sail and not age_of_sail

% Let's check for logical impossibilities:
% 1. If an event requires age_of_sail but age_of_sail is prevented, and the event is required for something else
% 2. If the pivot selection rule cannot be satisfied

% For now, we'll assume no paradoxes unless we find contradictory constraints

% ==================== OUTPUT DEFINITIONS ====================
% Original timeline: list of events that occurred, sorted by year
original_timeline(E) :- occurred_original(E).

% Alternate timeline: list of events that occurred, sorted by year
alternate_timeline(E) :- occurred_alternate(E).

% Prevented events: in original but not in alternate
prevented_events(E) :- occurred_original(E), not occurred_alternate(E).

% Activated events: in alternate but not in original
activated_events(E) :- occurred_alternate(E), not occurred_original(E).

% Paradoxes: list of logical impossibilities (empty if solution is valid)
% We'll define a paradox if we find contradictory constraints
% For now, we'll leave this empty and add detection rules if needed

% ==================== SHOW DIRECTIVES ====================
#show occurred_original/1.
#show occurred_alternate/1.
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show activated_events/1.
#show possible_original/1.
#show possible_alternate/1.