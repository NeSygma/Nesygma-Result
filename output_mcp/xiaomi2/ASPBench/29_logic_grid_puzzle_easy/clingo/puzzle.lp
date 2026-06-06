% Domains
person(alice; bob; carol; dave).
color(red; blue; green; yellow).
pet(cat; dog; bird; fish).
house(1; 2; 3; 4).

% Each person gets exactly one color, pet, and house
1 { has_color(P, C) : color(C) } 1 :- person(P).
1 { has_pet(P, Pet) : pet(Pet) } 1 :- person(P).
1 { lives_in(P, H) : house(H) } 1 :- person(P).

% Each color, pet, and house is assigned to exactly one person
1 { has_color(P, C) : person(P) } 1 :- color(C).
1 { has_pet(P, Pet) : person(P) } 1 :- pet(Pet).
1 { lives_in(P, H) : person(P) } 1 :- house(H).

% Constraint 4: Alice lives in house 1
lives_in(alice, 1).

% Constraint 5: Red color person lives in house 2
lives_in(P, 2) :- has_color(P, red).

% Constraint 6: Bob has a cat
has_pet(bob, cat).

% Constraint 7: Carol's color is blue
has_color(carol, blue).

% Constraint 8: Yellow color person has a fish
has_pet(P, fish) :- has_color(P, yellow).

% Constraint 9: Green color person lives in house 4
lives_in(P, 4) :- has_color(P, green).

% Constraint 10: Dave has the dog
has_pet(dave, dog).

% Constraint 11: Alice cannot have the bird
:- has_pet(alice, bird).

% Show assignments
#show has_color/2.
#show has_pet/2.
#show lives_in/2.