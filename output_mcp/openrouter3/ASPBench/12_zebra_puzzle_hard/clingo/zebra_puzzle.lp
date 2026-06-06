% Zebra Puzzle with 8 International Strategists

% Domain declarations
suite(1..8).

nationality(american). nationality(brazilian). nationality(canadian). nationality(dutch).
nationality(egyptian). nationality(french). nationality(german). nationality(hungarian).

profession(architect). profession(biologist). profession(chemist). profession(doctor).
profession(engineer). profession(lawyer). profession(musician). profession(pilot).

car(audi). car(bmw). car(ford). car(honda). car(mercedes). car(nissan). car(toyota). car(volvo).

drink(coffee). drink(juice). drink(milk). drink(soda). drink(tea). drink(water). drink(wine). drink(whiskey).

music(blues). music(classical). music(folk). music(jazz). music(pop). music(rap). music(reggae). music(rock).

pet(cat). pet(dog). pet(fish). pet(hamster). pet(lizard). pet(parrot). pet(rabbit). pet(snake).

destination(bali). destination(dubai). destination(london). destination(newyork). destination(paris). destination(rome). destination(sydney). destination(tokyo).

% Each suite has exactly one of each attribute
1 { nationality(P, N) : nationality(N) } 1 :- suite(P).
1 { profession(P, Prof) : profession(Prof) } 1 :- suite(P).
1 { car(P, Car) : car(Car) } 1 :- suite(P).
1 { drink(P, Drink) : drink(Drink) } 1 :- suite(P).
1 { music(P, Music) : music(Music) } 1 :- suite(P).
1 { pet(P, Pet) : pet(Pet) } 1 :- suite(P).
1 { destination(P, Dest) : destination(Dest) } 1 :- suite(P).

% Each attribute value appears exactly once across all suites
{ nationality(P, N) : suite(P) } 1 :- nationality(N).
{ profession(P, Prof) : suite(P) } 1 :- profession(Prof).
{ car(P, Car) : suite(P) } 1 :- car(Car).
{ drink(P, Drink) : suite(P) } 1 :- drink(Drink).
{ music(P, Music) : suite(P) } 1 :- music(Music).
{ pet(P, Pet) : suite(P) } 1 :- pet(Pet).
{ destination(P, Dest) : suite(P) } 1 :- destination(Dest).

% Constraint 1: Suite 4 drinks Milk
drink(4, milk).

% Constraint 2: Hungarian in suite 4
nationality(4, hungarian).

% Constraint 3: American is Lawyer
profession(P, lawyer) :- nationality(P, american).

% Constraint 4: BMW driver is Biologist
profession(P, biologist) :- car(P, bmw).

% Constraint 5: Canadian owns Snake
pet(P, snake) :- nationality(P, canadian).

% Constraint 6: Classical music listener drives Audi
car(P, audi) :- music(P, classical).

% Constraint 7: German drinks Coffee
drink(P, coffee) :- nationality(P, german).

% Constraint 8: Tokyo visitor is Chemist
profession(P, chemist) :- destination(P, tokyo).

% Constraint 9: Engineer is immediately left of Lawyer
% Engineer in suite P, Lawyer in suite P+1
:- suite(P), suite(P+1), profession(P, engineer), not profession(P+1, lawyer).
:- suite(P), suite(P+1), profession(P+1, lawyer), not profession(P, engineer).

% Constraint 10: Dog owner lives next to Volvo driver
% Dog owner in P, Volvo driver in P+1 or P-1
neighbor(P, Q) :- suite(P), suite(Q), P = Q+1.
neighbor(P, Q) :- suite(P), suite(Q), P = Q-1.
:- suite(P), pet(P, dog), not neighbor(P, Q), car(Q, volvo).

% Constraint 11: Rock listener lives next to Pop listener
% Rock in P, Pop in P+1 or P-1
:- suite(P), music(P, rock), not neighbor(P, Q), music(Q, pop).

% Constraint 12: Paris visitor lives next to Fish owner
% Paris in P, Fish in P+1 or P-1
:- suite(P), destination(P, paris), not neighbor(P, Q), pet(Q, fish).

% Constraint 13: Pilot lives in even-numbered suite
% Suite numbers are 1..8, even means 2,4,6,8
:- suite(P), profession(P, pilot), P != 2, P != 4, P != 6, P != 8.

% Constraint 14: Wine drinker is right of Coffee drinker
% Wine in P, Coffee in Q where P > Q
:- suite(P), drink(P, wine), not (suite(Q), drink(Q, coffee), P > Q).

% Constraint 15: Ford driver has neighbor who drinks Tea
% Ford in P, Tea in P+1 or P-1
:- suite(P), car(P, ford), not neighbor(P, Q), drink(Q, tea).

% Constraint 16: Nissan driver not in suite 1 or 8
:- car(1, nissan).
:- car(8, nissan).

% Constraint 17: Jazz listener suite number < Blues listener suite number
:- suite(P), music(P, jazz), suite(Q), music(Q, blues), P >= Q.

% Constraint 18: Dutch person in suite 1
nationality(1, dutch).

% Show solution
#show nationality/2.
#show profession/2.
#show car/2.
#show drink/2.
#show music/2.
#show pet/2.
#show destination/2.

% Find lizard owner nationality
lizard_owner(N) :- suite(P), pet(P, lizard), nationality(P, N).
#show lizard_owner/1.