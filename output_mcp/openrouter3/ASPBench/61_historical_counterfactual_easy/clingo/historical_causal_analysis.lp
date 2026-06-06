% Historical Causal Analysis with Intervention
% ================================================

% --- Domain Declaration ---
event(discovery_of_america, 1492).
event(columbian_exchange, 1500).
event(spanish_empire, 1520).
event(industrial_revolution, 1750).
event(world_wars, 1914).

% --- Causal Dependencies ---
enables(discovery_of_america, columbian_exchange).
enables(discovery_of_america, spanish_empire).
enables(spanish_empire, industrial_revolution).
enables(industrial_revolution, world_wars).

% --- Intervention ---
% The intervention prevents discovery_of_america
intervention_event(discovery_of_america).

% --- Original Timeline (All events occur with all prerequisites satisfied) ---
original_occurs(Event) :- event(Event, _).

% --- Prevented Events Logic ---
% An event is prevented if:
% 1. It is directly prevented by intervention, OR
% 2. Any of its prerequisites is prevented
prevented(Event) :- intervention_event(Event).
prevented(Event) :- enables(Prerequisite, Event), prevented(Prerequisite).

% --- Alternate Timeline ---
% An event occurs in the alternate timeline if:
% 1. It is not prevented, AND
% 2. All its prerequisites occur in the alternate timeline
occurs(Event) :- event(Event, _), not prevented(Event), 
                #count{Prerequisite : enables(Prerequisite, Event), not occurs(Prerequisite)} = 0.

% --- Causal Analysis ---
% Direct effects: Events immediately enabled by the prevented event
direct_effect(Event) :- enables(intervention_event, Event).

% Cascade effects: Events prevented through dependency chains (but not direct effects)
cascade_effect(Event) :- prevented(Event), not direct_effect(Event), Event != intervention_event.

% Preserved events: Events that remain in the alternate timeline
preserved_event(Event) :- occurs(Event).

% --- Output Formatting ---
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show causal_analysis_direct_effects/1.
#show causal_analysis_cascade_effects/1.
#show causal_analysis_preserved_events/1.
#show causal_analysis_intervention_events/1.

% Helper predicates for output
original_timeline(Event) :- original_occurs(Event).
alternate_timeline(Event) :- occurs(Event).
prevented_events(Event) :- prevented(Event).
causal_analysis_direct_effects(Event) :- direct_effect(Event).
causal_analysis_cascade_effects(Event) :- cascade_effect(Event).
causal_analysis_preserved_events(Event) :- preserved_event(Event).
causal_analysis_intervention_events(Event) :- intervention_event(Event).