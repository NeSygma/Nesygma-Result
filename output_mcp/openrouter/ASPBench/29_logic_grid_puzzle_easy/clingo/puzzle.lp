% Entities
person(alice). person(bob). person(carol). person(dave).
color(red). color(blue). color(green). color(yellow).
pet(cat). pet(dog). pet(bird). pet(fish).
house(1). house(2). house(3). house(4).

% Choice rules for assignments
1 { has_color(P,C) : color(C) } 1 :- person(P).
1 { has_pet(P,T) : pet(T) } 1 :- person(P).
1 { lives(P,H) : house(H) } 1 :- person(P).

% Bijectivity constraints
:- has_color(P1,C), has_color(P2,C), P1 != P2.
:- has_pet(P1,T), has_pet(P2,T), P1 != P2.
:- lives(P1,H), lives(P2,H), P1 != P2.

% Given clues
lives(alice,1).
has_color(P,red) :- lives(P,2).
has_pet(bob,cat).
has_color(carol,blue).
has_pet(P,fish) :- has_color(P,yellow).
has_color(P,green) :- lives(P,4).
has_pet(dave,dog).
:- has_pet(alice,bird).

#show has_color/2.
#show has_pet/2.
#show lives/2.