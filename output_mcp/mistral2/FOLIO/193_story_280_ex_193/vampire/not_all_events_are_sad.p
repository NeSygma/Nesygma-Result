fof(events_are_happy_or_sad, axiom, ! [E] : (event(E) => (happy(E) | sad(E)))).
fof(at_least_one_happy, axiom, ? [E] : (event(E) & happy(E))).
fof(not_all_events_are_sad, conjecture, ? [E] : (event(E) & ~sad(E))).