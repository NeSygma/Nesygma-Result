% Domain definitions
suite(1..8).

nationality(american).
nationality(brazilian).
nationality(canadian).
nationality(dutch).
nationality(egyptian).
nationality(french).
nationality(german).
nationality(hungarian).

profession(architect).
profession(biologist).
profession(chemist).
profession(doctor).
profession(engineer).
profession(lawyer).
profession(musician).
profession(pilot).

car(audi).
car(bmw).
car(ford).
car(honda).
car(mercedes).
car(nissan).
car(toyota).
car(volvo).

drink(coffee).
drink(juice).
drink(milk).
drink(soda).
drink(tea).
drink(water).
drink(wine).
drink(whiskey).

music(blues).
music(classical).
music(folk).
music(jazz).
music(pop).
music(rap).
music(reggae).
music(rock).

pet(cat).
pet(dog).
pet(fish).
pet(hamster).
pet(lizard).
pet(parrot).
pet(rabbit).
pet(snake).

destination(bali).
destination(dubai).
destination(london).
destination(new_york).
destination(paris).
destination(rome).
destination(sydney).
destination(tokyo).

% Each suite has exactly one of each attribute
1 { has_nationality(S, N) : nationality(N) } 1 :- suite(S).
1 { has_profession(S, P) : profession(P) } 1 :- suite(S).
1 { has_car(S, C) : car(C) } 1 :- suite(S).
1 { has_drink(S, D) : drink(D) } 1 :- suite(S).
1 { has_music(S, M) : music(M) } 1 :- suite(S).
1 { has_pet(S, Pt) : pet(Pt) } 1 :- suite(S).
1 { has_destination(S, Dt) : destination(Dt) } 1 :- suite(S).

% Each attribute value appears exactly once across all suites
1 { has_nationality(S, N) : suite(S) } 1 :- nationality(N).
1 { has_profession(S, P) : suite(S) } 1 :- profession(P).
1 { has_car(S, C) : suite(S) } 1 :- car(C).
1 { has_drink(S, D) : suite(S) } 1 :- drink(D).
1 { has_music(S, M) : suite(S) } 1 :- music(M).
1 { has_pet(S, Pt) : suite(S) } 1 :- pet(Pt).
1 { has_destination(S, Dt) : suite(S) } 1 :- destination(Dt).

% Constraint 1: The person in suite #4 drinks Milk
has_drink(4, milk).

% Constraint 2: The Hungarian lives in suite #4
has_nationality(4, hungarian).

% Constraint 3: The American is a Lawyer
has_profession(S, lawyer) :- has_nationality(S, american).
has_nationality(S, american) :- has_profession(S, lawyer).

% Constraint 4: The person who drives a BMW is a Biologist
has_profession(S, biologist) :- has_car(S, bmw).
has_car(S, bmw) :- has_profession(S, biologist).

% Constraint 5: The Canadian owns a Snake
has_pet(S, snake) :- has_nationality(S, canadian).
has_nationality(S, canadian) :- has_pet(S, snake).

% Constraint 6: The person who listens to Classical music drives an Audi
has_car(S, audi) :- has_music(S, classical).
has_music(S, classical) :- has_car(S, audi).

% Constraint 7: The German drinks Coffee
has_drink(S, coffee) :- has_nationality(S, german).
has_nationality(S, german) :- has_drink(S, coffee).

% Constraint 8: The person going to Tokyo is a Chemist
has_profession(S, chemist) :- has_destination(S, tokyo).
has_destination(S, tokyo) :- has_profession(S, chemist).

% Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
has_profession(S+1, lawyer) :- has_profession(S, engineer), suite(S), suite(S+1).
has_profession(S-1, engineer) :- has_profession(S, lawyer), suite(S), suite(S-1).

% Constraint 10: The Dog owner lives next to the Volvo driver
has_car(S+1, volvo) :- has_pet(S, dog), suite(S), suite(S+1).
has_car(S-1, volvo) :- has_pet(S, dog), suite(S), suite(S-1).
has_pet(S+1, dog) :- has_car(S, volvo), suite(S), suite(S+1).
has_pet(S-1, dog) :- has_car(S, volvo), suite(S), suite(S-1).

% Constraint 11: The Rock music listener lives next to the Pop music listener
has_music(S+1, pop) :- has_music(S, rock), suite(S), suite(S+1).
has_music(S-1, pop) :- has_music(S, rock), suite(S), suite(S-1).
has_music(S+1, rock) :- has_music(S, pop), suite(S), suite(S+1).
has_music(S-1, rock) :- has_music(S, pop), suite(S), suite(S-1).

% Constraint 12: The person going to Paris lives next to the Fish owner
has_pet(S+1, fish) :- has_destination(S, paris), suite(S), suite(S+1).
has_pet(S-1, fish) :- has_destination(S, paris), suite(S), suite(S-1).
has_destination(S+1, paris) :- has_pet(S, fish), suite(S), suite(S+1).
has_destination(S-1, paris) :- has_pet(S, fish), suite(S), suite(S-1).

% Constraint 13: The Pilot lives in an even-numbered suite
has_profession(S, pilot) :- suite(S), S = 2.
has_profession(S, pilot) :- suite(S), S = 4.
has_profession(S, pilot) :- suite(S), S = 6.
has_profession(S, pilot) :- suite(S), S = 8.

% Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
has_drink(S2, wine) :- has_drink(S1, coffee), suite(S1), suite(S2), S2 > S1.

% Constraint 15: The Ford driver has a neighbor who drinks Tea
has_drink(S+1, tea) :- has_car(S, ford), suite(S), suite(S+1).
has_drink(S-1, tea) :- has_car(S, ford), suite(S), suite(S-1).
has_car(S+1, ford) :- has_drink(S, tea), suite(S), suite(S+1).
has_car(S-1, ford) :- has_drink(S, tea), suite(S), suite(S-1).

% Constraint 16: The Nissan driver does not live in suite #1 or #8
:- has_car(1, nissan).
:- has_car(8, nissan).

% Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
has_music(S2, blues) :- has_music(S1, jazz), suite(S1), suite(S2), S2 > S1.

% Constraint 18: The Dutch person lives in suite #1
has_nationality(1, dutch).

% Helper predicates for output
lizard_owner(N) :- has_pet(S, lizard), has_nationality(S, N).

% Show all assignments
#show has_nationality/2.
#show has_profession/2.
#show has_car/2.
#show has_drink/2.
#show has_music/2.
#show has_pet/2.
#show has_destination/2.
#show lizard_owner/1.