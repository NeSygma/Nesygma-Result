% Domains
person(alice; bob; carol; dave).
color(red; blue; green; yellow).
pets(cat; dog; bird; fish).
house(1; 2; 3; 4).

% Each person lives in exactly one house
1 { house(P, H) : house(H) } 1 :- person(P).

% Each house has exactly one person
:- house(P1, H), house(P2, H), P1 != P2.

% Each person has exactly one color
1 { color(P, C) : color(C) } 1 :- person(P).

% Each color is assigned to exactly one person
:- color(P1, C), color(P2, C), P1 != P2.

% Each person has exactly one pet
1 { pet(P, Pt) : pets(Pt) } 1 :- person(P).

% Each pet belongs to exactly one person
:- pet(P1, Pt), pet(P2, Pt), P1 != P2.

% Constraints
% 4. Alice must live in house 1
house(alice, 1).

% 5. The person with the red color must live in house 2
:- color(P, red), not house(P, 2).

% 6. Bob must have a cat
pet(bob, cat).

% 7. Carol's favorite color must be blue
color(carol, blue).

% 8. The person with the yellow color must have a fish
:- color(P, yellow), pet(P, Pt), Pt != fish.

% 9. The person with the green color must live in house 4
:- color(P, green), not house(P, 4).

% 10. Dave must have the dog
pet(dave, dog).

% 11. Alice cannot have the bird
:- pet(alice, bird).

% Show the solution
#show house/2.
#show color/2.
#show pet/2.