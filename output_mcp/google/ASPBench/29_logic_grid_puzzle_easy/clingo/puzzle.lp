% Domains
person(alice; bob; carol; dave).
color(red; blue; green; yellow).
pet(cat; dog; bird; fish).
house(1; 2; 3; 4).

% Each person has exactly one color, one pet, and one house
1 { has_color(P, C) : color(C) } 1 :- person(P).
1 { has_pet(P, PT) : pet(PT) } 1 :- person(P).
1 { lives_in(P, H) : house(H) } 1 :- person(P).

% Each color, pet, and house is assigned to exactly one person
:- color(C), not 1 { has_color(P, C) : person(P) } 1.
:- pet(PT), not 1 { has_pet(P, PT) : person(P) } 1.
:- house(H), not 1 { lives_in(P, H) : person(P) } 1.

% Constraints
% 4. Alice must live in house 1
lives_in(alice, 1).

% 5. The person with the red color must live in house 2
has_color(P, red) :- lives_in(P, 2).
lives_in(P, 2) :- has_color(P, red).

% 6. Bob must have a cat
has_pet(bob, cat).

% 7. Carol's favorite color must be blue
has_color(carol, blue).

% 8. The person with the yellow color must have a fish
has_color(P, yellow) :- has_pet(P, fish).
has_pet(P, fish) :- has_color(P, yellow).

% 9. The person with the green color must live in house 4
has_color(P, green) :- lives_in(P, 4).
lives_in(P, 4) :- has_color(P, green).

% 10. Dave must have the dog
has_pet(dave, dog).

% 11. Alice cannot have the bird
:- has_pet(alice, bird).

#show has_color/2.
#show has_pet/2.
#show lives_in/2.