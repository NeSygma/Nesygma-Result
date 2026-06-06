% Zebra Puzzle - Einstein's Riddle

% Domain definitions
house(1..5).
color(red; green; white; yellow; blue).
nationality(brit; swede; dane; norwegian; german).
drink(tea; coffee; milk; beer; water).
cigarette(pall_mall; dunhill; blends; blue_master; prince).
pet(dog; birds; cats; horse; zebra).

% Choice rules: exactly one of each attribute per house
1 { color(H, C) : color(C) } 1 :- house(H).
1 { nationality(H, N) : nationality(N) } 1 :- house(H).
1 { drink(H, D) : drink(D) } 1 :- house(H).
1 { cigarette(H, C) : cigarette(C) } 1 :- house(H).
1 { pet(H, P) : pet(P) } 1 :- house(H).

% Helper: adjacency (next to)
adjacent(H1, H2) :- house(H1), house(H2), H1 = H2 - 1.
adjacent(H1, H2) :- house(H1), house(H2), H1 = H2 + 1.

% Constraint 1: The Brit lives in the red house
:- nationality(H, brit), color(H, C), C != red.

% Constraint 2: The Swede keeps dogs as pets
:- nationality(H, swede), pet(H, P), P != dog.

% Constraint 3: The Dane drinks tea
:- nationality(H, dane), drink(H, D), D != tea.

% Constraint 4: The green house is on the left of the white house (directly adjacent)
:- color(H1, green), color(H2, white), not adjacent(H1, H2).

% Constraint 5: The green house's owner drinks coffee
:- color(H, green), drink(H, D), D != coffee.

% Constraint 6: The person who smokes Pall Mall rears birds
:- cigarette(H, pall_mall), pet(H, P), P != birds.

% Constraint 7: The owner of the yellow house smokes Dunhill
:- color(H, yellow), cigarette(H, C), C != dunhill.

% Constraint 8: The person living in the center house (house 3) drinks milk
:- drink(3, D), D != milk.

% Constraint 9: The Norwegian lives in the first house (house 1)
:- nationality(1, N), N != norwegian.

% Constraint 10: The person who smokes Blends lives next to the one who keeps cats
:- cigarette(H1, blends), not (adjacent(H1, H2), pet(H2, cats)).

% Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
:- pet(H1, horse), not (adjacent(H1, H2), cigarette(H2, dunhill)).

% Constraint 12: The owner who smokes Blue Master drinks beer
:- cigarette(H, blue_master), drink(H, D), D != beer.

% Constraint 13: The German smokes Prince
:- nationality(H, german), cigarette(H, C), C != prince.

% Constraint 14: The Norwegian lives next to the blue house
:- nationality(H, norwegian), not (adjacent(H, H2), color(H2, blue)).

% Constraint 15: The person who smokes Blends has a neighbor who drinks water
:- cigarette(H1, blends), not (adjacent(H1, H2), drink(H2, water)).

% Show the solution
#show color/2.
#show nationality/2.
#show drink/2.
#show cigarette/2.
#show pet/2.

% Find who owns the zebra
zebra_owner(N) :- nationality(H, N), pet(H, zebra).
#show zebra_owner/1.