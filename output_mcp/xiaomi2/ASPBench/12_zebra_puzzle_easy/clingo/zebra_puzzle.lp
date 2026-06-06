% ===== DOMAINS =====
house(1..5).
color(red; green; white; yellow; blue).
nationality(brit; swede; dane; norwegian; german).
drink(tea; coffee; milk; beer; water).
cigarette(pall_mall; dunhill; blends; blue_master; prince).
pet(dog; birds; cats; horse; zebra).

% ===== ASSIGNMENT: Each house gets exactly one of each attribute =====
1 { color(H, C) : color(C) } 1 :- house(H).
1 { nationality(H, N) : nationality(N) } 1 :- house(H).
1 { drink(H, D) : drink(D) } 1 :- house(H).
1 { cigarette(H, Cig) : cigarette(Cig) } 1 :- house(H).
1 { pet(H, P) : pet(P) } 1 :- house(H).

% ===== UNIQUENESS: Each attribute value used exactly once =====
1 { color(H, C) : house(H) } 1 :- color(C).
1 { nationality(H, N) : house(H) } 1 :- nationality(N).
1 { drink(H, D) : house(H) } 1 :- drink(D).
1 { cigarette(H, Cig) : house(H) } 1 :- cigarette(Cig).
1 { pet(H, P) : house(H) } 1 :- pet(P).

% ===== ADJACENCY HELPER =====
adjacent(H1, H2) :- house(H1), house(H2), H2 = H1 + 1.
adjacent(H1, H2) :- house(H1), house(H2), H2 = H1 - 1.

% ===== CONSTRAINTS =====

% 1. The Brit lives in the red house
color(H, red) :- nationality(H, brit).

% 2. The Swede keeps dogs as pets
pet(H, dog) :- nationality(H, swede).

% 3. The Dane drinks tea
drink(H, tea) :- nationality(H, dane).

% 4. The green house is directly to the left of the white house
:- color(H1, green), color(H2, white), H2 != H1 + 1.

% 5. The green house's owner drinks coffee
drink(H, coffee) :- color(H, green).

% 6. The person who smokes Pall Mall rears birds
pet(H, birds) :- cigarette(H, pall_mall).

% 7. The owner of the yellow house smokes Dunhill
cigarette(H, dunhill) :- color(H, yellow).

% 8. The person in house 3 drinks milk
drink(3, milk).

% 9. The Norwegian lives in house 1
nationality(1, norwegian).

% 10. The Blends smoker lives next to the cat keeper
:- cigarette(H1, blends), pet(H2, cats), not adjacent(H1, H2).

% 11. The horse keeper lives next to the Dunhill smoker
:- pet(H1, horse), cigarette(H2, dunhill), not adjacent(H1, H2).

% 12. The Blue Master smoker drinks beer
drink(H, beer) :- cigarette(H, blue_master).

% 13. The German smokes Prince
cigarette(H, prince) :- nationality(H, german).

% 14. The Norwegian lives next to the blue house
:- nationality(H, norwegian), color(H2, blue), not adjacent(H, H2).

% 15. The Blends smoker has a neighbor who drinks water
:- cigarette(H1, blends), not has_water_neighbor(H1).
has_water_neighbor(H1) :- cigarette(H1, blends), drink(H2, water), adjacent(H1, H2).

% ===== DERIVE ZEBRA OWNER =====
zebra_owner(N) :- nationality(H, N), pet(H, zebra).

% ===== OUTPUT =====
#show color/2.
#show nationality/2.
#show drink/2.
#show cigarette/2.
#show pet/2.
#show zebra_owner/1.