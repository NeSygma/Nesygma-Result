%%% Domains %%%
suite(1..8).

nationality(american; brazilian; canadian; dutch; egyptian; french; german; hungarian).
profession(architect; biologist; chemist; doctor; engineer; lawyer; musician; pilot).
car(audi; bmw; ford; honda; mercedes; nissan; toyota; volvo).
drink(coffee; juice; milk; soda; tea; water; wine; whiskey).
music(blues; classical; folk; jazz; pop; rap; reggae; rock).
pet(cat; dog; fish; hamster; lizard; parrot; rabbit; snake).
destination(bali; dubai; london; new_york; paris; rome; sydney; tokyo).

%%% Each suite gets exactly one of each attribute %%%
1 { nationality(Pos, Nat) : nationality(Nat) } 1 :- suite(Pos).
1 { profession(Pos, Prof) : profession(Prof) } 1 :- suite(Pos).
1 { car(Pos, Brand) : car(Brand) } 1 :- suite(Pos).
1 { drink(Pos, Bev) : drink(Bev) } 1 :- suite(Pos).
1 { music(Pos, Genre) : music(Genre) } 1 :- suite(Pos).
1 { pet(Pos, Animal) : pet(Animal) } 1 :- suite(Pos).
1 { destination(Pos, Dest) : destination(Dest) } 1 :- suite(Pos).

%%% Each value is used exactly once %%%
:- nationality(Pos1, Nat), nationality(Pos2, Nat), Pos1 != Pos2.
:- profession(Pos1, Prof), profession(Pos2, Prof), Pos1 != Pos2.
:- car(Pos1, Brand), car(Pos2, Brand), Pos1 != Pos2.
:- drink(Pos1, Bev), drink(Pos2, Bev), Pos1 != Pos2.
:- music(Pos1, Genre), music(Pos2, Genre), Pos1 != Pos2.
:- pet(Pos1, Animal), pet(Pos2, Animal), Pos1 != Pos2.
:- destination(Pos1, Dest), destination(Pos2, Dest), Pos1 != Pos2.

%%% Helper: even-numbered suites %%%
even(2;4;6;8).

%%% Constraint 1: Suite #4 drinks Milk %%%
drink(4, milk).

%%% Constraint 2: Hungarian lives in suite #4 %%%
nationality(4, hungarian).

%%% Constraint 3: The American is a Lawyer %%%
profession(Pos, lawyer) :- nationality(Pos, american).

%%% Constraint 4: The BMW driver is a Biologist %%%
profession(Pos, biologist) :- car(Pos, bmw).

%%% Constraint 5: The Canadian owns a Snake %%%
pet(Pos, snake) :- nationality(Pos, canadian).

%%% Constraint 6: Classical music listener drives an Audi %%%
car(Pos, audi) :- music(Pos, classical).

%%% Constraint 7: The German drinks Coffee %%%
drink(Pos, coffee) :- nationality(Pos, german).

%%% Constraint 8: The person going to Tokyo is a Chemist %%%
profession(Pos, chemist) :- destination(Pos, tokyo).

%%% Constraint 9: Engineer is immediately to the left of Lawyer %%%
:- profession(Pos1, engineer), profession(Pos2, lawyer), Pos1 + 1 != Pos2.

%%% Constraint 10: Dog owner lives next to Volvo driver %%%
:- pet(Pos1, dog), car(Pos2, volvo), Pos1 != Pos2 + 1, Pos1 != Pos2 - 1.

%%% Constraint 11: Rock listener lives next to Pop listener %%%
:- music(Pos1, rock), music(Pos2, pop), Pos1 != Pos2 + 1, Pos1 != Pos2 - 1.

%%% Constraint 12: Person going to Paris lives next to Fish owner %%%
:- destination(Pos1, paris), pet(Pos2, fish), Pos1 != Pos2 + 1, Pos1 != Pos2 - 1.

%%% Constraint 13: Pilot lives in an even-numbered suite %%%
:- profession(Pos, pilot), not even(Pos).

%%% Constraint 14: Wine drinker's suite is to the right of Coffee drinker's suite %%%
:- drink(Pos1, coffee), drink(Pos2, wine), Pos2 <= Pos1.

%%% Constraint 15: Ford driver has a neighbor who drinks Tea %%%
has_tea_neighbor(Pos) :- car(Pos, ford), drink(Pos + 1, tea), suite(Pos + 1).
has_tea_neighbor(Pos) :- car(Pos, ford), drink(Pos - 1, tea), suite(Pos - 1).
:- car(Pos, ford), not has_tea_neighbor(Pos).

%%% Constraint 16: Nissan driver does not live in suite #1 or #8 %%%
:- car(1, nissan).
:- car(8, nissan).

%%% Constraint 17: Jazz listener's suite number < Blues listener's suite number %%%
:- music(Pos1, jazz), music(Pos2, blues), Pos1 >= Pos2.

%%% Constraint 18: Dutch person lives in suite #1 %%%
nationality(1, dutch).

%%% Objective: Find the nationality of the Lizard owner %%%
lizard_owner(Nat) :- pet(Pos, lizard), nationality(Pos, Nat).

%%% Output all attributes per suite %%%
#show nationality/2.
#show profession/2.
#show car/2.
#show drink/2.
#show music/2.
#show pet/2.
#show destination/2.
#show lizard_owner/1.