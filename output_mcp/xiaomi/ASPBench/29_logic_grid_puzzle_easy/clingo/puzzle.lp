% Domain facts
person(alice). person(bob). person(carol). person(dave).
color(red). color(blue). color(green). color(yellow).
pet(cat). pet(dog). pet(bird). pet(fish).
house(1). house(2). house(3). house(4).

% Choice rules: assign exactly one house, one color, one pet to each person
1 { lives_in(P, H) : house(H) } 1 :- person(P).
1 { has_color(P, C) : color(C) } 1 :- person(P).
1 { has_pet(P, Pt) : pet(Pt) } 1 :- person(P).

% Each house has exactly one person
1 { lives_in(P, H) : person(P) } 1 :- house(H).

% Each color assigned to exactly one person
1 { has_color(P, C) : person(P) } 1 :- color(C).

% Each pet assigned to exactly one person
1 { has_pet(P, Pt) : person(P) } 1 :- pet(Pt).

% Constraint 4: Alice lives in house 1
lives_in(alice, 1).

% Constraint 5: Red color person lives in house 2
lives_in(P, 2) :- has_color(P, red).

% Constraint 6: Bob has cat
has_pet(bob, cat).

% Constraint 7: Carol has blue
has_color(carol, blue).

% Constraint 8: Yellow color person has fish
has_pet(P, fish) :- has_color(P, yellow).

% Constraint 9: Green color person lives in house 4
lives_in(P, 4) :- has_color(P, green).

% Constraint 10: Dave has dog
has_pet(dave, dog).

% Constraint 11: Alice cannot have bird
:- has_pet(alice, bird).

% Show the assignments
#show lives_in/2.
#show has_color/2.
#show has_pet/2.