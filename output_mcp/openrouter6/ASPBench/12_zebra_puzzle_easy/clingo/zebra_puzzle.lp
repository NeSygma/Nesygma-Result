% Zebra Puzzle in Clingo ASP

% Domains
house(1..5).
color(red; green; white; yellow; blue).
nationality(brit; swede; dane; norwegian; german).
drink(tea; coffee; milk; beer; water).
cigarette(pall_mall; dunhill; blends; blue_master; prince).
pet(dog; birds; cats; horse; zebra).

% Each house has exactly one of each attribute
1 { color(H, C) : color(C) } 1 :- house(H).
1 { nationality(H, N) : nationality(N) } 1 :- house(H).
1 { drink(H, D) : drink(D) } 1 :- house(H).
1 { cigarette(H, C) : cigarette(C) } 1 :- house(H).
1 { pet(H, P) : pet(P) } 1 :- house(H).

% Each attribute value appears exactly once across houses
1 { color(H, C) : house(H) } 1 :- color(C).
1 { nationality(H, N) : house(H) } 1 :- nationality(N).
1 { drink(H, D) : house(H) } 1 :- drink(D).
1 { cigarette(H, C) : house(H) } 1 :- cigarette(C).
1 { pet(H, P) : house(H) } 1 :- pet(P).

% Adjacency definition
adjacent(H1, H2) :- house(H1), house(H2), H1 != H2, H1 = H2+1.
adjacent(H1, H2) :- house(H1), house(H2), H1 != H2, H2 = H1+1.

% Constraints
% 1. The Brit lives in the red house
color(H, red) :- nationality(H, brit).

% 2. The Swede keeps dogs as pets
pet(H, dog) :- nationality(H, swede).

% 3. The Dane drinks tea
drink(H, tea) :- nationality(H, dane).

% 4. The green house is on the left of the white house (directly adjacent)
green_left_of_white :- color(H, green), color(H+1, white), H < 5.
:- not green_left_of_white.

% 5. The green house's owner drinks coffee
drink(H, coffee) :- color(H, green).

% 6. The person who smokes Pall Mall rears birds
pet(H, birds) :- cigarette(H, pall_mall).

% 7. The owner of the yellow house smokes Dunhill
cigarette(H, dunhill) :- color(H, yellow).

% 8. The person living in the center house (house 3) drinks milk
drink(3, milk).

% 9. The Norwegian lives in the first house (house 1)
nationality(1, norwegian).

% 10. The person who smokes Blends lives next to the one who keeps cats
blends_next_to_cats :- cigarette(H1, blends), pet(H2, cats), adjacent(H1, H2).
:- not blends_next_to_cats.

% 11. The person who keeps a horse lives next to the person who smokes Dunhill
horse_next_to_dunhill :- pet(H1, horse), cigarette(H2, dunhill), adjacent(H1, H2).
:- not horse_next_to_dunhill.

% 12. The owner who smokes Blue Master drinks beer
drink(H, beer) :- cigarette(H, blue_master).

% 13. The German smokes Prince
cigarette(H, prince) :- nationality(H, german).

% 14. The Norwegian lives next to the blue house
norwegian_next_to_blue :- nationality(H1, norwegian), color(H2, blue), adjacent(H1, H2).
:- not norwegian_next_to_blue.

% 15. The person who smokes Blends has a neighbor who drinks water
blends_next_to_water :- cigarette(H1, blends), drink(H2, water), adjacent(H1, H2).
:- not blends_next_to_water.

% Output solution
#show house/1.
#show color/2.
#show nationality/2.
#show drink/2.
#show cigarette/2.
#show pet/2.

% Find zebra owner
zebra_owner(N) :- pet(H, zebra), nationality(H, N).
#show zebra_owner/1.