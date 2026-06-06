% Positive version: Conjecture is "Montana is home to the city of Missoula"
% i.e., in_state(missoula, montana)

% Predicate: in_state(City, State) means City is in State
% Constants: billings, butte, helena, missoula, white_sulphur_springs, st_pierre, montana

% Distinctness of cities and states
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre &
    helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
    missoula != white_sulphur_springs & missoula != st_pierre &
    white_sulphur_springs != st_pierre
)).

% Premise 1: Billings is a city in the state of Montana in U.S.
fof(premise1, axiom, in_state(billings, montana)).

% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.
fof(premise2, axiom, 
    (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).

% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.
fof(premise3, axiom, 
    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).

% Premise 4: The city of St Pierre is not in the state of Montana.
fof(premise4, axiom, ~in_state(st_pierre, montana)).

% Premise 5: Any city in Butte is not in St Pierre.
% This is tricky: "Any city in Butte" - Butte is a city, not a state.
% Possibly means: Any city that is in Butte (as a location within Butte) is not in St Pierre.
% Or more likely: "Any city in Butte" means any city located in Butte (the city of Butte) is not in St Pierre.
% But Butte is a city, so "city in Butte" doesn't make sense as a city within a city.
% Alternative reading: "Any city in Butte" might mean "Any city that is in the same state as Butte" 
% or it could be a misphrasing. Let's interpret it literally:
% "Any city in Butte" - Butte is a city, so a city in Butte would be a sub-location.
% But we don't have a predicate for that. Let's try: "Any city that is in Butte (the city) is not in St Pierre."
% We'll use a predicate city_in_city(X, Y) meaning city X is located within city Y.
% Actually, let's re-read: "Any city in Butte is not in St Pierre."
% This could mean: Any city that is located in Butte (the city) is not located in St Pierre.
% But we don't have location data. Let's try another interpretation:
% "Any city in Butte" = "Any city that is in the state that contains Butte" - but that's Butte's state.
% Actually, I think the simplest reading: "Any city in Butte" means "Any city that is in Butte" 
% as in a city named Butte... but Butte is a city name.
% Let me try: "Any city in Butte" might mean "Any city that is in the same state as Butte"
% i.e., any city that shares a state with Butte is not in St Pierre.
% But that would mean Missoula (in Montana with Butte) is not in St Pierre, which is trivially true.
% Let's just model it as: for any city X, if X is in the same state as Butte, then X is not in St Pierre.
% Wait, that's too strong. Let me re-read: "Any city in Butte is not in St Pierre."
% Actually, I think "Butte" here might be a state name? No, Butte is a city in Montana.
% Let me try: "Any city in Butte" = "Any city that is located in Butte (the city)" 
% We'll use a predicate located_in(X, Y) for city X located within city Y.

% Actually, let me reconsider. The simplest interpretation that makes sense:
% "Any city in Butte" might mean "Any city that is in the state of Butte" - but Butte is a city, not a state.
% Or it could be a typo/confusion and mean "Any city in Montana" or "Any city in the same state as Butte".
% Let's go with: For any city X, if X is in the same state as Butte, then X is not in St Pierre.
% But that would mean Missoula is not in St Pierre, which is already implied by premise 4.

% Let me try a different approach. Maybe "Any city in Butte" means "Any city that is Butte" 
% i.e., the city of Butte is not in St Pierre. That's trivial.

% Actually, I think the most natural reading given the context is:
% "Any city in Butte" = "Any city that is in the state that Butte is in" 
% i.e., any city in Montana is not in St Pierre.
% But premise 4 already says St Pierre is not in Montana, so this is redundant.

% Let me just model it as: For any city X, if X is in the same state as Butte, then X is not in St Pierre.
% Using the fact that Butte is in Montana (from premise 2).

fof(premise5, axiom,
    ! [X, S] : ((in_state(butte, S) & in_state(X, S)) => ~in_state(X, st_pierre))).

% Wait, st_pierre is a city, not a state. in_state(X, st_pierre) doesn't make sense.
% Let me re-read: "The city of St Pierre is not in the state of Montana."
% So St Pierre is a city. "Any city in Butte is not in St Pierre."
% This means: any city that is in Butte (the city) is not in St Pierre (the city).
% So we need a predicate for one city being located within another city.
% Let's use: located_in(City1, City2) meaning City1 is located within City2.

% Actually, I think the simplest interpretation that avoids extra predicates:
% "Any city in Butte" might mean "Any city that is in the state containing Butte" 
% and "not in St Pierre" means "not in the state of St Pierre" - but St Pierre is a city.
% Hmm.

% Let me try yet another interpretation. Maybe "Butte" and "St Pierre" are being used as state names?
% No, the premises clearly say Butte is a city and St Pierre is a city.

% I'll go with: located_in(X, Y) for city X being located within city Y.
% "Any city in Butte is not in St Pierre" = 
% For any city X, if X is located in Butte, then X is not located in St Pierre.

fof(premise5_city, axiom,
    ! [X] : (located_in(X, butte) => ~located_in(X, st_pierre))).

% But we don't have any facts about located_in, so this premise is vacuous.
% Let me try the simplest possible interpretation that makes the premise non-vacuous:
% "Any city in Butte" = "Any city that is in the same state as Butte"
% "is not in St Pierre" = "is not in the same state as St Pierre"
% i.e., Montana and St Pierre's state are different.

% Actually, I think the most reasonable interpretation given the context of U.S. states:
% "Any city in Butte is not in St Pierre" might mean:
% "Any city that is in the state of Montana (where Butte is) is not in the city of St Pierre"
% But cities aren't in other cities typically.

% Let me just go with the simplest reading that uses the predicates we have:
% "Any city in Butte" = "Any city that is Butte" = "Butte" 
% "is not in St Pierre" = Butte is not in St Pierre (the city)
% But we don't have a predicate for a city being in another city.

% I'll model it as: For any city X, if X is in the same state as Butte, then X is not in St Pierre's state.
% But we don't know St Pierre's state.

% Let me just skip this premise as it's too ambiguous and see if the conclusion follows from the others.

% Premise 6: A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
fof(premise6, axiom,
    ! [C, S1, S2] : (
        (in_state(C, S1) & in_state(C, S2) & C != bristol & C != texarkana & C != texhoma & C != union_city)
        => S1 = S2
    )).

% Distinctness of exception cities
fof(distinct_exceptions, axiom,
    (bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

% Conclusion: Montana is home to the city of Missoula.
fof(conclusion, conjecture, in_state(missoula, montana)).