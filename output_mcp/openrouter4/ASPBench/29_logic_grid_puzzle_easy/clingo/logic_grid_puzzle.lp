% Domains
person(alice; bob; carol; dave).
color(red; blue; green; yellow).
pet(cat; dog; bird; fish).
house(1..4).

% Each person has exactly one house
1 { assigned_house(P, H) : house(H) } 1 :- person(P).

% Each house has exactly one person
1 { assigned_house(P, H) : person(P) } 1 :- house(H).

% Each person has exactly one color
1 { assigned_color(P, C) : color(C) } 1 :- person(P).

% Each color is assigned to exactly one person
1 { assigned_color(P, C) : person(P) } 1 :- color(C).

% Each person has exactly one pet
1 { assigned_pet(P, Y) : pet(Y) } 1 :- person(P).

% Each pet is assigned to exactly one person
1 { assigned_pet(P, Y) : person(P) } 1 :- pet(Y).

% Constraint 4: Alice must live in house 1
assigned_house(alice, 1).

% Constraint 5: The person with the red color must live in house 2
:- assigned_color(P, red), not assigned_house(P, 2).
:- assigned_house(P, 2), not assigned_color(P, red).

% Constraint 6: Bob must have a cat
assigned_pet(bob, cat).

% Constraint 7: Carol's favorite color must be blue
assigned_color(carol, blue).

% Constraint 8: The person with the yellow color must have a fish
:- assigned_color(P, yellow), not assigned_pet(P, fish).
:- assigned_pet(P, fish), not assigned_color(P, yellow).

% Constraint 9: The person with the green color must live in house 4
:- assigned_color(P, green), not assigned_house(P, 4).
:- assigned_house(P, 4), not assigned_color(P, green).

% Constraint 10: Dave must have the dog
assigned_pet(dave, dog).

% Constraint 11: Alice cannot have the bird
:- assigned_pet(alice, bird).

% Show the solution
#show assigned_house/2.
#show assigned_color/2.
#show assigned_pet/2.