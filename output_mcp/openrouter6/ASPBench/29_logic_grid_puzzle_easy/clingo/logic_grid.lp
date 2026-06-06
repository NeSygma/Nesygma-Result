% Logic Grid Puzzle: Four people, colors, pets, houses

% Domains
person(alice). person(bob). person(carol). person(dave).
color(red). color(blue). color(green). color(yellow).
pet(cat). pet(dog). pet(bird). pet(fish).
house(1). house(2). house(3). house(4).

% Assignments: each person gets exactly one color, one pet, one house
% Each color assigned to exactly one person
1 { has_color(P, C) : color(C) } 1 :- person(P).
1 { has_color(P, C) : person(P) } 1 :- color(C).

% Each pet assigned to exactly one person
1 { has_pet(P, Pet) : pet(Pet) } 1 :- person(P).
1 { has_pet(P, Pet) : person(P) } 1 :- pet(Pet).

% Each house assigned to exactly one person
1 { lives_in(P, H) : house(H) } 1 :- person(P).
1 { lives_in(P, H) : person(P) } 1 :- house(H).

% Constraints
% 4. Alice must live in house 1
lives_in(alice, 1).

% 5. The person with the red color must live in house 2
lives_in(P, 2) :- has_color(P, red).

% 6. Bob must have a cat
has_pet(bob, cat).

% 7. Carol's favorite color must be blue
has_color(carol, blue).

% 8. The person with the yellow color must have a fish
has_pet(P, fish) :- has_color(P, yellow).

% 9. The person with the green color must live in house 4
lives_in(P, 4) :- has_color(P, green).

% 10. Dave must have the dog
has_pet(dave, dog).

% 11. Alice cannot have the bird
:- has_pet(alice, bird).

% Show the solution
#show has_color/2.
#show has_pet/2.
#show lives_in/2.