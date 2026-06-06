% Zebra Puzzle with 8 strategists

% Domains
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

% Assign exactly one attribute per suite
1 { nationality(S, Nat) : nationality(Nat) } 1 :- suite(S).
1 { profession(S, Prof) : profession(Prof) } 1 :- suite(S).
1 { car(S, Car) : car(Car) } 1 :- suite(S).
1 { drink(S, Drink) : drink(Drink) } 1 :- suite(S).
1 { music(S, Music) : music(Music) } 1 :- suite(S).
1 { pet(S, Pet) : pet(Pet) } 1 :- suite(S).
1 { destination(S, Dest) : destination(Dest) } 1 :- suite(S).

% Each value used exactly once across suites
1 { nationality(S, Nat) : suite(S) } 1 :- nationality(Nat).
1 { profession(S, Prof) : suite(S) } 1 :- profession(Prof).
1 { car(S, Car) : suite(S) } 1 :- car(Car).
1 { drink(S, Drink) : suite(S) } 1 :- drink(Drink).
1 { music(S, Music) : suite(S) } 1 :- music(Music).
1 { pet(S, Pet) : suite(S) } 1 :- pet(Pet).
1 { destination(S, Dest) : suite(S) } 1 :- destination(Dest).

% Helper: adjacent suites
adjacent(S, T) :- S = T-1; S = T+1.

% Constraints
% 1. The person in suite #4 drinks Milk
drink(4, milk).

% 2. The Hungarian lives in suite #4
nationality(4, hungarian).

% 3. The American is a Lawyer
profession(S, lawyer) :- nationality(S, american).

% 4. The person who drives a BMW is a Biologist
profession(S, biologist) :- car(S, bmw).

% 5. The Canadian owns a Snake
pet(S, snake) :- nationality(S, canadian).

% 6. The person who listens to Classical music drives an Audi
car(S, audi) :- music(S, classical).

% 7. The German drinks Coffee
drink(S, coffee) :- nationality(S, german).

% 8. The person going to Tokyo is a Chemist
profession(S, chemist) :- destination(S, tokyo).

% 9. The Engineer's suite is immediately to the left of the Lawyer's suite
:- profession(S, engineer), profession(T, lawyer), T != S+1.

% 10. The Dog owner lives next to the Volvo driver
:- pet(S, dog), car(T, volvo), S != T, not adjacent(S, T).

% 11. The Rock music listener lives next to the Pop music listener
:- music(S, rock), music(T, pop), S != T, not adjacent(S, T).

% 12. The person going to Paris lives next to the Fish owner
:- destination(S, paris), pet(T, fish), S != T, not adjacent(S, T).

% 13. The Pilot lives in an even-numbered suite
:- profession(S, pilot), S mod 2 = 1.

% 14. The Wine drinker's suite is to the right of the Coffee drinker's suite
:- drink(S, wine), drink(T, coffee), S <= T.

% 15. The Ford driver has a neighbor who drinks Tea
% Helper: has_tea_neighbor(S) if car(S, ford) and there exists neighbor T with drink(T, tea)
has_tea_neighbor(S) :- car(S, ford), drink(T, tea), adjacent(S, T).
:- car(S, ford), not has_tea_neighbor(S).

% 16. The Nissan driver does not live in suite #1 or #8
:- car(S, nissan), S = 1.
:- car(S, nissan), S = 8.

% 17. The Jazz listener's suite number is less than the Blues listener's suite number
:- music(S, jazz), music(T, blues), S >= T.

% 18. The Dutch person lives in suite #1
nationality(1, dutch).

% Solution output
solution(S, Nat, Prof, Car, Drink, Music, Pet, Dest) :-
    nationality(S, Nat), profession(S, Prof), car(S, Car),
    drink(S, Drink), music(S, Music), pet(S, Pet), destination(S, Dest).

lizard_owner(Nat) :- pet(S, lizard), nationality(S, Nat).

#show solution/8.
#show lizard_owner/1.