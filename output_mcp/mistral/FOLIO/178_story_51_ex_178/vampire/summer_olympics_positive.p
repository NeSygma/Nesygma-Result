fof(summer_olympic_is_sporting_event, axiom,
    sporting_event(last_summer_olympic_games)).

fof(last_summer_olympic_in_tokyo, axiom,
    held_in(last_summer_olympic_games, tokyo)).

fof(usa_won_most_medals, axiom,
    won_most_medals(united_states, last_summer_olympic_games)).

fof(distinct_constants, axiom,
    ( tokyo != united_states
    & tokyo != last_summer_olympic_games
    & united_states != last_summer_olympic_games )).

fof(conclusion, conjecture,
    won_most_medals(united_states, last_summer_olympic_games)).