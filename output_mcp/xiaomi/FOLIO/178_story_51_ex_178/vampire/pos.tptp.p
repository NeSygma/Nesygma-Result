fof(premise_1, axiom, sporting_event(summer_olympics)).
fof(premise_2, axiom, held_in(last_summer_olympics, tokyo)).
fof(premise_3, axiom, won_most_medals_in(united_states, tokyo)).
fof(distinct_entities, axiom, (
    summer_olympics != tokyo &
    summer_olympics != united_states &
    summer_olympics != last_summer_olympics &
    tokyo != united_states &
    tokyo != last_summer_olympics &
    united_states != last_summer_olympics
)).
fof(bridge, axiom, ! [Event, Place, Country] :
    ((held_in(Event, Place) & won_most_medals_in(Country, Place))
     => won_most_medals_in(Country, Event))).
fof(goal, conjecture, won_most_medals_in(united_states, last_summer_olympics)).