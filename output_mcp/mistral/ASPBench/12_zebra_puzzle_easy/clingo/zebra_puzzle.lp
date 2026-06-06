% Zebra Puzzle (Einstein's Riddle) ASP Encoding

% Domains

% Houses are numbered 1 to 5
{house(1..5)}.

% Attributes and their possible values
color(red; green; white; yellow; blue).
nationality(brit; swede; dane; norwegian; german).
drink(tea; coffee; milk; beer; water).
cigarette(pall_mall; dunhill; blends; blue_master; prince).
pet(dog; birds; cats; horse; zebra).

% Each house has exactly one of each attribute
1 { house_color(H, C) : color(C) } 1 :- house(H).
1 { house_nationality(H, N) : nationality(N) } 1 :- house(H).
1 { house_drink(H, D) : drink(D) } 1 :- house(H).
1 { house_cigarette(H, S) : cigarette(S) } 1 :- house(H).
1 { house_pet(H, P) : pet(P) } 1 :- house(H).

% Uniqueness constraints: each attribute value appears exactly once per category
:- color(C), house(H1), house(H2), H1 != H2, house_color(H1, C), house_color(H2, C).
:- nationality(N), house(H1), house(H2), H1 != H2, house_nationality(H1, N), house_nationality(H2, N).
:- drink(D), house(H1), house(H2), H1 != H2, house_drink(H1, D), house_drink(H2, D).
:- cigarette(S), house(H1), house(H2), H1 != H2, house_cigarette(H1, S), house_cigarette(H2, S).
:- pet(P), house(H1), house(H2), H1 != H2, house_pet(H1, P), house_pet(H2, P).

% Adjacency and ordering predicates
next_to(H1, H2) :- H1 = H2 - 1, house(H1), house(H2).
next_to(H1, H2) :- H1 = H2 + 1, house(H1), house(H2).

left_of(H1, H2) :- H2 = H1 + 1, house(H1), house(H2).

% Constraint 1: The Brit lives in the red house
:- house_nationality(H, brit), not house_color(H, red).

% Constraint 2: The Swede keeps dogs as pets
:- house_nationality(H, swede), not house_pet(H, dog).

% Constraint 3: The Dane drinks tea
:- house_nationality(H, dane), not house_drink(H, tea).

% Constraint 4: The green house is on the left of the white house (directly adjacent)
:- house_color(H, green), not left_of(H, H2), house(H2), house_color(H2, white).

% Constraint 5: The green house's owner drinks coffee
:- house_color(H, green), not house_drink(H, coffee).

% Constraint 6: The person who smokes Pall Mall rears birds
:- house_cigarette(H, pall_mall), not house_pet(H, birds).

% Constraint 7: The owner of the yellow house smokes Dunhill
:- house_color(H, yellow), not house_cigarette(H, dunhill).

% Constraint 8: The person living in the center house (house 3) drinks milk
:- not house_drink(3, milk).

% Constraint 9: The Norwegian lives in the first house (house 1)
:- not house_nationality(1, norwegian).

% Constraint 10: The person who smokes Blends lives next to the one who keeps cats
:- house_cigarette(H1, blends), not next_to(H1, H2), house_pet(H2, cats).

% Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
:- house_pet(H1, horse), not next_to(H1, H2), house_cigarette(H2, dunhill).

% Constraint 12: The owner who smokes Blue Master drinks beer
:- house_cigarette(H, blue_master), not house_drink(H, beer).

% Constraint 13: The German smokes Prince
:- house_nationality(H, german), not house_cigarette(H, prince).

% Constraint 14: The Norwegian lives next to the blue house
% Since Norwegian is in house 1 (constraint 9), house 2 must be blue
:- house_nationality(1, norwegian), not house_color(2, blue).

% Constraint 15: The person who smokes Blends has a neighbor who drinks water
:- house_cigarette(H1, blends), not next_to(H1, H2), house_drink(H2, water).

% Identify the zebra owner
zebra_owner(N) :- house_nationality(H, N), house_pet(H, zebra).

% Show the solution
#show house_color/2.
#show house_nationality/2.
#show house_drink/2.
#show house_cigarette/2.
#show house_pet/2.
#show zebra_owner/1.