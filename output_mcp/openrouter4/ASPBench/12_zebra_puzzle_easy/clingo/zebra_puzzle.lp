% The Zebra Puzzle (Einstein's Riddle)
% Houses numbered 1 to 5 from left to right

% ---------- DOMAINS ----------
house(1..5).

% Colors
color(red; green; white; yellow; blue).

% Nationalities
nationality(brit; swede; dane; norwegian; german).

% Drinks
drink(tea; coffee; milk; beer; water).

% Cigarettes
cigarette(pall_mall; dunhill; blends; blue_master; prince).

% Pets
pet(dog; birds; cats; horse; zebra).

% ---------- ASSIGNMENT CHOICE RULES ----------
% Each house gets exactly one color
1 { house_color(H, C) : color(C) } 1 :- house(H).

% Each house gets exactly one nationality
1 { house_nationality(H, N) : nationality(N) } 1 :- house(H).

% Each house gets exactly one drink
1 { house_drink(H, D) : drink(D) } 1 :- house(H).

% Each house gets exactly one cigarette
1 { house_cigarette(H, C) : cigarette(C) } 1 :- house(H).

% Each house gets exactly one pet
1 { house_pet(H, P) : pet(P) } 1 :- house(H).

% ---------- UNIQUENESS (each value used exactly once) ----------
:- color(C), #count { H : house_color(H, C) } != 1.
:- nationality(N), #count { H : house_nationality(H, N) } != 1.
:- drink(D), #count { H : house_drink(H, D) } != 1.
:- cigarette(C), #count { H : house_cigarette(H, C) } != 1.
:- pet(P), #count { H : house_pet(H, P) } != 1.

% ---------- ADJACENCY HELPER ----------
next_to(H1, H2) :- house(H1), house(H2), |H1 - H2| = 1.

% Directly left (strict adjacency, green left of white)
left_adjacent(H1, H2) :- house(H1), house(H2), H1 + 1 = H2.

% ---------- CONSTRAINTS ----------

% 1. The Brit lives in the red house
:- house_nationality(H, brit), not house_color(H, red).

% 2. The Swede keeps dogs as pets
:- house_nationality(H, swede), not house_pet(H, dog).

% 3. The Dane drinks tea
:- house_nationality(H, dane), not house_drink(H, tea).

% 4. The green house is on the left of the white house (directly adjacent)
:- house_color(H1, green), house_color(H2, white), not left_adjacent(H1, H2).

% 5. The green house's owner drinks coffee
:- house_color(H, green), not house_drink(H, coffee).

% 6. The person who smokes Pall Mall rears birds
:- house_cigarette(H, pall_mall), not house_pet(H, birds).

% 7. The owner of the yellow house smokes Dunhill
:- house_color(H, yellow), not house_cigarette(H, dunhill).

% 8. The person living in the center house (house 3) drinks milk
:- house_drink(3, D), D != milk.

% 9. The Norwegian lives in the first house (house 1)
:- house_nationality(1, N), N != norwegian.

% 10. The person who smokes Blends lives next to the one who keeps cats
:- house_cigarette(H, blends), not { house_pet(H2, cats) : next_to(H, H2) }.

% 11. The person who keeps a horse lives next to the person who smokes Dunhill
:- house_pet(H, horse), not { house_cigarette(H2, dunhill) : next_to(H, H2) }.

% 12. The owner who smokes Blue Master drinks beer
:- house_cigarette(H, blue_master), not house_drink(H, beer).

% 13. The German smokes Prince
:- house_nationality(H, german), not house_cigarette(H, prince).

% 14. The Norwegian lives next to the blue house
:- house_nationality(H, norwegian), not { house_color(H2, blue) : next_to(H, H2) }.

% 15. The person who smokes Blends has a neighbor who drinks water
:- house_cigarette(H, blends), not { house_drink(H2, water) : next_to(H, H2) }.

% ---------- OUTPUT ----------
% Show the complete assignment for each house
#show house_color/2.
#show house_nationality/2.
#show house_drink/2.
#show house_cigarette/2.
#show house_pet/2.