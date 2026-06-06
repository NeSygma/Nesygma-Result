% Domains
pos(1..8).

% Attribute sets
nationality(american). nationality(brazilian). nationality(canadian). nationality(dutch). nationality(egyptian). nationality(french). nationality(german). nationality(hungarian).
profession(architect). profession(biologist). profession(chemist). profession(doctor). profession(engineer). profession(lawyer). profession(musician). profession(pilot).
car(audi). car(bmw). car(ford). car(honda). car(mercedes). car(nissan). car(toyota). car(volvo).
drink(coffee). drink(juice). drink(milk). drink(soda). drink(tea). drink(water). drink(wine). drink(whiskey).
music(blues). music(classical). music(folk). music(jazz). music(pop). music(rap). music(reggae). music(rock).
pet(cat). pet(dog). pet(fish). pet(hamster). pet(lizard). pet(parrot). pet(rabbit). pet(snake).
destination(bali). destination(dubai). destination(london). destination(new_york). destination(paris). destination(rome). destination(sydney). destination(tokyo).

% Exactly one attribute per position
1 { nat(N,Pos) : nationality(N) } 1 :- pos(Pos).
1 { prof(P,Pos) : profession(P) } 1 :- pos(Pos).
1 { car(C,Pos) : car(C) } 1 :- pos(Pos).
1 { drink(D,Pos) : drink(D) } 1 :- pos(Pos).
1 { music(M,Pos) : music(M) } 1 :- pos(Pos).
1 { pet(Pet,Pos) : pet(Pet) } 1 :- pos(Pos).
1 { dest(Dest,Pos) : destination(Dest) } 1 :- pos(Pos).

% Uniqueness of each attribute across positions
:- nat(N,Pos1), nat(N,Pos2), Pos1 != Pos2.
:- prof(P,Pos1), prof(P,Pos2), Pos1 != Pos2.
:- car(C,Pos1), car(C,Pos2), Pos1 != Pos2.
:- drink(D,Pos1), drink(D,Pos2), Pos1 != Pos2.
:- music(M,Pos1), music(M,Pos2), Pos1 != Pos2.
:- pet(Pet,Pos1), pet(Pet,Pos2), Pos1 != Pos2.
:- dest(Dest,Pos1), dest(Dest,Pos2), Pos1 != Pos2.

% Helper for odd positions (pilot must be even)
odd(1). odd(3). odd(5). odd(7).

% Constraints
% 1. suite #4 drinks Milk
drink(milk,4).
% 2. Hungarian lives in suite #4
nat(hungarian,4).
% 3. American is a Lawyer
prof(lawyer,Pos) :- nat(american,Pos).
% 4. BMW driver is a Biologist
prof(biologist,Pos) :- car(bmw,Pos).
% 5. Canadian owns a Snake
pet(snake,Pos) :- nat(canadian,Pos).
% 6. Classical music listener drives an Audi
car(audi,Pos) :- music(classical,Pos).
% 7. German drinks Coffee
drink(coffee,Pos) :- nat(german,Pos).
% 8. Person going to Tokyo is a Chemist
prof(chemist,Pos) :- dest(tokyo,Pos).
% 9. Engineer's suite is immediately to the left of Lawyer's suite
:- prof(engineer,PosE), prof(lawyer,PosL), PosE+1 != PosL.
% 10. Dog owner lives next to Volvo driver
:- pet(dog,PosD), car(volvo,PosV), PosD != PosV+1, PosD != PosV-1.
% 11. Rock music listener lives next to Pop music listener
:- music(rock,PosR), music(pop,PosP), PosR != PosP+1, PosR != PosP-1.
% 12. Person going to Paris lives next to Fish owner
:- dest(paris,PosPar), pet(fish,PosF), PosPar != PosF+1, PosPar != PosF-1.
% 13. Pilot lives in an even-numbered suite
:- prof(pilot,Pos), odd(Pos).
% 14. Wine drinker's suite is to the right of Coffee drinker's suite
:- drink(wine,PosW), drink(coffee,PosC), PosW <= PosC.
% 15. Ford driver has a neighbor who drinks Tea
:- car(ford,PosF), not drink(tea,PosF+1), not drink(tea,PosF-1).
% 16. Nissan driver does not live in suite #1 or #8
:- car(nissan,1).
:- car(nissan,8).
% 17. Jazz listener's suite number is less than Blues listener's suite number
:- music(jazz,PosJ), music(blues,PosB), PosJ >= PosB.
% 18. Dutch person lives in suite #1
nat(dutch,1).

% Derive lizard owner nationality
lizard_owner(N) :- pet(lizard,Pos), nat(N,Pos).

% Show all attributes and lizard owner
#show nat/2.
#show prof/2.
#show car/2.
#show drink/2.
#show music/2.
#show pet/2.
#show dest/2.
#show lizard_owner/1.