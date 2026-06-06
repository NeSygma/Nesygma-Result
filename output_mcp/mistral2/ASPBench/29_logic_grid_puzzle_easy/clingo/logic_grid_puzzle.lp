% Domains
person(alice; bob; carol; dave).
color(red; blue; green; yellow).
pets(cat; dog; bird; fish).
house(1; 2; 3; 4).

% Assignments
1 { lives_in(P, H) : house(H) } 1 :- person(P).
1 { lives_in(P, H) : person(P) } 1 :- house(H).

1 { has_color(P, C) : color(C) } 1 :- person(P).
1 { has_color(P, C) : person(P) } 1 :- color(C).

1 { has_pet(P, Pt) : pets(Pt) } 1 :- person(P).
1 { has_pet(P, Pt) : person(P) } 1 :- pets(Pt).

% Constraints
lives_in(alice, 1).
lives_in(P, 2) :- has_color(P, red).
has_pet(bob, cat).
has_color(carol, blue).
has_pet(P, fish) :- has_color(P, yellow).
lives_in(P, 4) :- has_color(P, green).
has_pet(dave, dog).
:- has_pet(alice, bird).

% Show the solution
#show lives_in/2.
#show has_color/2.
#show has_pet/2.