% Logic Grid Puzzle: Four People with Colors, Pets, Houses

% Domain declarations
person(alice). person(bob). person(carol). person(dave).
color(red). color(blue). color(green). color(yellow).
pet(cat). pet(dog). pet(bird). pet(fish).
house(1). house(2). house(3). house(4).

% Choice rules for assignments
{lives_in(P, H) : house(H)} 1 :- person(P).
{has_color(P, C) : color(C)} 1 :- person(P).
{has_pet(P, P2) : pet(P2)} 1 :- person(P).

% Exactly one person per house
1 {lives_in(P, H) : person(P)} 1 :- house(H).

% Exactly one color per person (already enforced by choice rule)
% Exactly one person per color
1 {has_color(P, C) : person(P)} 1 :- color(C).

% Exactly one pet per person (already enforced by choice rule)
% Exactly one person per pet
1 {has_pet(P, P2) : person(P)} 1 :- pet(P2).

% Constraint 4: Alice must live in house 1
lives_in(alice, 1).

% Constraint 5: The person with red color must live in house 2
% We need to find who has red color, then that person lives in house 2
:- has_color(P, red), lives_in(P, H), H != 2.

% Constraint 6: Bob must have a cat
has_pet(bob, cat).

% Constraint 7: Carol's favorite color must be blue
has_color(carol, blue).

% Constraint 8: The person with yellow color must have a fish
:- has_color(P, yellow), has_pet(P, P2), P2 != fish.

% Constraint 9: The person with green color must live in house 4
:- has_color(P, green), lives_in(P, H), H != 4.

% Constraint 10: Dave must have the dog
has_pet(dave, dog).

% Constraint 11: Alice cannot have the bird
:- has_pet(alice, bird).

% Show the solution
#show lives_in/2.
#show has_color/2.
#show has_pet/2.