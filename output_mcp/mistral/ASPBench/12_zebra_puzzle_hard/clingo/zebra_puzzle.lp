% Define the 8 suites
suite(1..8).

% Define all possible values for each attribute category
nationality(american; brazilian; canadian; dutch; egyptian; french; german; hungarian).
profession(architect; biologist; chemist; doctor; engineer; lawyer; musician; pilot).
car_brand(audi; bmw; ford; honda; mercedes; nissan; toyota; volvo).
drink(coffee; juice; milk; soda; tea; water; wine; whiskey).
music_genre(blues; classical; folk; jazz; pop; rap; reggae; rock).
pets(cat; dog; fish; hamster; lizard; parrot; rabbit; snake).
destination(bali; dubai; london; new_york; paris; rome; sydney; tokyo).

% Assign attributes to suites using choice rules
% Each suite gets exactly one value for each attribute
1 { has_nationality(S, N) : nationality(N) } 1 :- suite(S).
1 { has_profession(S, P) : profession(P) } 1 :- suite(S).
1 { has_car_brand(S, C) : car_brand(C) } 1 :- suite(S).
1 { has_drink(S, D) : drink(D) } 1 :- suite(S).
1 { has_music_genre(S, M) : music_genre(M) } 1 :- suite(S).
1 { has_pet(S, P) : pets(P) } 1 :- suite(S).
1 { has_destination(S, D) : destination(D) } 1 :- suite(S).

% Uniqueness constraints within each category
% Nationality uniqueness
:- suite(S1), suite(S2), S1 != S2, has_nationality(S1, N), has_nationality(S2, N).
% Profession uniqueness
:- suite(S1), suite(S2), S1 != S2, has_profession(S1, P), has_profession(S2, P).
% Car brand uniqueness
:- suite(S1), suite(S2), S1 != S2, has_car_brand(S1, C), has_car_brand(S2, C).
% Drink uniqueness
:- suite(S1), suite(S2), S1 != S2, has_drink(S1, D), has_drink(S2, D).
% Music genre uniqueness
:- suite(S1), suite(S2), S1 != S2, has_music_genre(S1, M), has_music_genre(S2, M).
% Pet uniqueness
:- suite(S1), suite(S2), S1 != S2, has_pet(S1, P), has_pet(S2, P).
% Destination uniqueness
:- suite(S1), suite(S2), S1 != S2, has_destination(S1, D), has_destination(S2, D).

% Constraint 1: Suite #4 drinks Milk
:- has_drink(4, D), D != milk.

% Constraint 2: Hungarian lives in suite #4
:- has_nationality(4, N), N != hungarian.

% Constraint 3: American is a Lawyer
:- has_nationality(S, american), not has_profession(S, lawyer).
:- has_profession(S, lawyer), not has_nationality(S, american).

% Constraint 4: BMW driver is a Biologist
:- has_car_brand(S, bmw), not has_profession(S, biologist).
:- has_profession(S, biologist), not has_car_brand(S, bmw).

% Constraint 5: Canadian owns a Snake
:- has_nationality(S, canadian), not has_pet(S, snake).
:- has_pet(S, snake), not has_nationality(S, canadian).

% Constraint 6: Classical music listener drives an Audi
:- has_music_genre(S, classical), not has_car_brand(S, audi).
:- has_car_brand(S, audi), not has_music_genre(S, classical).

% Constraint 7: German drinks Coffee
:- has_nationality(S, german), not has_drink(S, coffee).
:- has_drink(S, coffee), not has_nationality(S, german).

% Constraint 8: Tokyo destination is a Chemist
:- has_destination(S, tokyo), not has_profession(S, chemist).
:- has_profession(S, chemist), not has_destination(S, tokyo).

% Constraint 9: Engineer's suite is immediately to the left of Lawyer's suite
:- has_profession(S1, engineer), has_profession(S2, lawyer), S2 != S1 + 1.
:- has_profession(S, engineer), S + 1 <= 8, not has_profession(S + 1, lawyer).

% Constraint 10: Dog owner lives next to Volvo driver
% Define neighbor relationship explicitly
neighbor(S, S1) :- suite(S), suite(S1), S1 = S + 1.
neighbor(S, S1) :- suite(S), suite(S1), S1 = S - 1.

% Helper predicates for constraint 10
has_dog_neighbor_volvo(S) :- has_pet(S, dog), neighbor(S, S1), has_car_brand(S1, volvo).
has_volvo_neighbor_dog(S) :- has_car_brand(S, volvo), neighbor(S, S1), has_pet(S1, dog).
:- has_pet(S, dog), not has_dog_neighbor_volvo(S).
:- has_car_brand(S, volvo), not has_volvo_neighbor_dog(S).

% Constraint 11: Rock music listener lives next to Pop music listener
% Helper predicates for constraint 11
has_rock_neighbor_pop(S) :- has_music_genre(S, rock), neighbor(S, S1), has_music_genre(S1, pop).
has_pop_neighbor_rock(S) :- has_music_genre(S, pop), neighbor(S, S1), has_music_genre(S1, rock).
:- has_music_genre(S, rock), not has_rock_neighbor_pop(S).
:- has_music_genre(S, pop), not has_pop_neighbor_rock(S).

% Constraint 12: Paris destination lives next to Fish owner
% Helper predicates for constraint 12
has_paris_neighbor_fish(S) :- has_destination(S, paris), neighbor(S, S1), has_pet(S1, fish).
has_fish_neighbor_paris(S) :- has_pet(S, fish), neighbor(S, S1), has_destination(S1, paris).
:- has_destination(S, paris), not has_paris_neighbor_fish(S).
:- has_pet(S, fish), not has_fish_neighbor_paris(S).

% Constraint 13: Pilot lives in even-numbered suite
:- has_profession(S, pilot), S mod 2 != 0.

% Constraint 14: Wine drinker's suite is to the right of Coffee drinker's suite
:- has_drink(S1, coffee), has_drink(S2, wine), S2 =< S1.

% Constraint 15: Ford driver has neighbor who drinks Tea
% Helper predicates for constraint 15
has_ford_neighbor_tea(S) :- has_car_brand(S, ford), neighbor(S, S1), has_drink(S1, tea).
:- has_car_brand(S, ford), not has_ford_neighbor_tea(S).

% Constraint 16: Nissan driver does not live in suite #1 or #8
:- has_car_brand(1, nissan).
:- has_car_brand(8, nissan).

% Constraint 17: Jazz listener's suite number is less than Blues listener's suite number
:- has_music_genre(S1, jazz), has_music_genre(S2, blues), S1 >= S2.

% Constraint 18: Dutch person lives in suite #1
:- has_nationality(1, N), N != dutch.

% Derive the lizard owner
lizard_owner(N) :- has_pet(S, lizard), has_nationality(S, N).

% Show the solution
#show has_nationality/2.
#show has_profession/2.
#show has_car_brand/2.
#show has_drink/2.
#show has_music_genre/2.
#show has_pet/2.
#show has_destination/2.
#show lizard_owner/1.