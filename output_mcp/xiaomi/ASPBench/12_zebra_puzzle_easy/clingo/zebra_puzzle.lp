% Zebra Puzzle (Einstein's Riddle) in Clingo ASP

% Domain definitions
house(1..5).

% Attribute domains
color(red). color(green). color(white). color(yellow). color(blue).
nationality(brit). nationality(swede). nationality(dane). nationality(norwegian). nationality(german).
drink(tea). drink(coffee). drink(milk). drink(beer). drink(water).
cigarette(pall_mall). cigarette(dunhill). cigarette(blends). cigarette(blue_master). cigarette(prince).
pet(dog). pet(birds). pet(cats). pet(horse). pet(zebra).

% Each house has exactly one of each attribute
1 { color(H, C) : color(C) } 1 :- house(H).
1 { nationality(H, N) : nationality(N) } 1 :- house(H).
1 { drink(H, D) : drink(D) } 1 :- house(H).
1 { cigarette(H, Cig) : cigarette(Cig) } 1 :- house(H).
1 { pet(H, P) : pet(P) } 1 :- house(H).

% Each attribute value appears exactly once across all houses
1 { color(H, C) : house(H) } 1 :- color(C).
1 { nationality(H, N) : house(H) } 1 :- nationality(N).
1 { drink(H, D) : house(H) } 1 :- drink(D).
1 { cigarette(H, Cig) : house(H) } 1 :- cigarette(Cig).
1 { pet(H, P) : house(H) } 1 :- pet(P).

% Constraint 1: The Brit lives in the red house
:- nationality(H, brit), not color(H, red).
:- color(H, red), not nationality(H, brit).

% Constraint 2: The Swede keeps dogs as pets
:- nationality(H, swede), not pet(H, dog).
:- pet(H, dog), not nationality(H, swede).

% Constraint 3: The Dane drinks tea
:- nationality(H, dane), not drink(H, tea).
:- drink(H, tea), not nationality(H, dane).

% Constraint 4: The green house is on the left of the white house (directly adjacent)
:- color(H1, green), color(H2, white), H2 != H1+1.

% Constraint 5: The green house's owner drinks coffee
:- color(H, green), not drink(H, coffee).
:- drink(H, coffee), not color(H, green).

% Constraint 6: The person who smokes Pall Mall rears birds
:- cigarette(H, pall_mall), not pet(H, birds).
:- pet(H, birds), not cigarette(H, pall_mall).

% Constraint 7: The owner of the yellow house smokes Dunhill
:- color(H, yellow), not cigarette(H, dunhill).
:- cigarette(H, dunhill), not color(H, yellow).

% Constraint 8: The person living in the center house (house 3) drinks milk
:- not drink(3, milk).

% Constraint 9: The Norwegian lives in the first house (house 1)
:- not nationality(1, norwegian).

% Constraint 10: The person who smokes Blends lives next to the one who keeps cats
:- cigarette(H1, blends), pet(H2, cats), |H1-H2| != 1.

% Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
:- pet(H1, horse), cigarette(H2, dunhill), |H1-H2| != 1.

% Constraint 12: The owner who smokes Blue Master drinks beer
:- cigarette(H, blue_master), not drink(H, beer).
:- drink(H, beer), not cigarette(H, blue_master).

% Constraint 13: The German smokes Prince
:- nationality(H, german), not cigarette(H, prince).
:- cigarette(H, prince), not nationality(H, german).

% Constraint 14: The Norwegian lives next to the blue house
:- nationality(H1, norwegian), color(H2, blue), |H1-H2| != 1.

% Constraint 15: The person who smokes Blends has a neighbor who drinks water
:- cigarette(H1, blends), not drink(H1-1, water), not drink(H1+1, water).
% Need to handle boundary conditions
:- cigarette(1, blends), not drink(2, water).
:- cigarette(5, blends), not drink(4, water).
:- cigarette(H, blends), H != 1, H != 5, not drink(H-1, water), not drink(H+1, water).

% Show the solution
#show color/2.
#show nationality/2.
#show drink/2.
#show cigarette/2.
#show pet/2.