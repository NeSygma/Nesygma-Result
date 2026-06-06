% --- Domains ---
house(1..5).
color(red; green; white; yellow; blue).
nationality(brit; swede; dane; norwegian; german).
drink(tea; coffee; milk; beer; water).
cigarette(pall_mall; dunhill; blends; blue_master; prince).
pet(dog; birds; cats; horse; zebra).

% --- Choice rules for assignments ---
1 { color(H, C) : color(C) } 1 :- house(H).
1 { nationality(H, N) : nationality(N) } 1 :- house(H).
1 { drink(H, D) : drink(D) } 1 :- house(H).
1 { cigarette(H, S) : cigarette(S) } 1 :- house(H).
1 { pet(H, P) : pet(P) } 1 :- house(H).

% --- Helper predicates ---
next_to(H1, H2) :- house(H1), house(H2), H2 = H1 + 1.
left_of(H1, H2) :- house(H1), house(H2), H1 = H2 - 1.

% --- Constraints ---
% 1. Brit lives in the red house
:- nationality(H, brit), not color(H, red).

% 2. Swede keeps dogs
:- nationality(H, swede), not pet(H, dog).

% 3. Dane drinks tea
:- nationality(H, dane), not drink(H, tea).

% 4. Green house is immediately left of white house
:- color(H1, green), color(H2, white), not left_of(H1, H2).

% 5. Green house's owner drinks coffee
:- color(H, green), not drink(H, coffee).

% 6. Pall Mall smoker rears birds
:- cigarette(H, pall_mall), not pet(H, birds).

% 7. Yellow house smoker smokes Dunhill
:- color(H, yellow), not cigarette(H, dunhill).

% 8. House 3 drinks milk
drink(3, milk).

% 9. Norwegian lives in house 1
nationality(1, norwegian).

% 10. Blends smoker lives next to cats
:- cigarette(H1, blends), pet(H2, cats), not next_to(H1, H2).

% 11. Horse owner lives next to Dunhill smoker
:- pet(H1, horse), cigarette(H2, dunhill), not next_to(H1, H2).

% 12. Blue Master smoker drinks beer
:- cigarette(H, blue_master), not drink(H, beer).

% 13. German smokes Prince
:- nationality(H, german), not cigarette(H, prince).

% 14. Norwegian lives next to blue house
:- nationality(1, norwegian), not next_to(1, H), not color(H, blue).

% 15. Blends smoker has neighbor who drinks water
:- cigarette(H1, blends), drink(H2, water), not next_to(H1, H2).

% --- Zebra owner ---
zebra_owner(N) :- nationality(H, N), pet(H, zebra).

% --- Show directives ---
#show color/2.
#show nationality/2.
#show drink/2.
#show cigarette/2.
#show pet/2.
#show zebra_owner/1.