event(discovery_of_america,1492).
event(columbian_exchange,1500).
event(spanish_empire,1520).
event(industrial_revolution,1750).
event(world_wars,1914).

prereq(columbian_exchange, discovery_of_america).
prereq(spanish_empire, discovery_of_america).
prereq(industrial_revolution, spanish_empire).
prereq(world_wars, industrial_revolution).

% intervention
prevented_by_intervention(discovery_of_america).

% propagation
prevented(E) :- prevented_by_intervention(E).
prevented(E) :- prereq(E, P), prevented(P).

% direct effects
causal_analysis_direct_effects(E) :- prereq(E, P), prevented_by_intervention(P).

% cascade effects
causal_analysis_cascade_effects(E) :- prevented(E), not causal_analysis_direct_effects(E), not prevented_by_intervention(E).

% preserved events
causal_analysis_preserved_events(E) :- event(E,_), not prevented(E).

% alternate timeline
alternate_timeline(E) :- causal_analysis_preserved_events(E).

% original timeline
original_timeline(E) :- event(E,_).

% intervention events
causal_analysis_intervention_events(E) :- prevented_by_intervention(E).

% prevented events list
prevented_events(E) :- prevented(E).

#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show causal_analysis_direct_effects/1.
#show causal_analysis_cascade_effects/1.
#show causal_analysis_preserved_events/1.
#show causal_analysis_intervention_events/1.