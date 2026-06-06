% Domains
suite(1..8).

nationality(american; brazilian; canadian; dutch; egyptian; french; german; hungarian).
profession(architect; biologist; chemist; doctor; engineer; lawyer; musician; pilot).
car(audi; bmw; ford; honda; mercedes; nissan; toyota; volvo).
drink(coffee; juice; milk; soda; tea; water; wine; whiskey).
music(blues; classical; folk; jazz; pop; rap; reggae; rock).
pet(cat; dog; fish; hamster; lizard; parrot; rabbit; snake).
destination(bali; dubai; london; new_york; paris; rome; sydney; tokyo).

% Assign attributes to suites
1 { nationality(S, Nat) : nationality(Nat) } 1 :- suite(S).
1 { profession(S, Prof) : profession(Prof) } 1 :- suite(S).
1 { car(S, Car) : car(Car) } 1 :- suite(S).
1 { drink(S, Drk) : drink(Drk) } 1 :- suite(S).
1 { music(S, Mus) : music(Mus) } 1 :- suite(S).
1 { pet(S, Pet) : pet(Pet) } 1 :- suite(S).
1 { destination(S, Dest) : destination(Dest) } 1 :- suite(S).

% Uniqueness constraints
:- nationality(S1, Nat), nationality(S2, Nat), S1 != S2.
:- profession(S1, Prof), profession(S2, Prof), S1 != S2.
:- car(S1, Car), car(S2, Car), S1 != S2.
:- drink(S1, Drk), drink(S2, Drk), S1 != S2.
:- music(S1, Mus), music(S2, Mus), S1 != S2.
:- pet(S1, Pet), pet(S2, Pet), S1 != S2.
:- destination(S1, Dest), destination(S2, Dest), S1 != S2.

% Given constraints
:- not drink(4, milk).
:- not nationality(4, hungarian).
:- not nationality(S, american), profession(S, lawyer).
:- not car(S, bmw), profession(S, biologist).
:- not nationality(S, canadian), pet(S, snake).
:- not music(S, classical), car(S, audi).
:- not nationality(S, german), drink(S, coffee).
:- not destination(S, tokyo), profession(S, chemist).
:- not profession(S, engineer), profession(S+1, lawyer), suite(S+1).
:- not pet(S, dog), car(S+1, volvo), suite(S+1).
:- not pet(S, dog), car(S-1, volvo), suite(S-1).
:- not music(S, rock), music(S+1, pop), suite(S+1).
:- not music(S, rock), music(S-1, pop), suite(S-1).
:- not destination(S, paris), pet(S+1, fish), suite(S+1).
:- not destination(S, paris), pet(S-1, fish), suite(S-1).
:- not profession(S, pilot), suite(S), S = 2..8, S mod 2 = 0.
:- not drink(S1, coffee), drink(S2, wine), S1 < S2.
:- not car(S, ford), drink(S-1, tea), suite(S-1).
:- not car(S, ford), drink(S+1, tea), suite(S+1).
:- not car(S, nissan), suite(S), S != 1, S != 8.
:- not music(S1, jazz), music(S2, blues), S1 < S2.
:- not nationality(1, dutch).

% Identify the lizard owner
lizard_owner(Nat) :- nationality(S, Nat), pet(S, lizard).

% Show the solution and the lizard owner
#show nationality/2.
#show profession/2.
#show car/2.
#show drink/2.
#show music/2.
#show pet/2.
#show destination/2.
#show lizard_owner/1.