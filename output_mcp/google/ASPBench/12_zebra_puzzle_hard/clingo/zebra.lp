% --- Domains ---
suite(1..8).
nationality(american; brazilian; canadian; dutch; egyptian; french; german; hungarian).
profession(architect; biologist; chemist; doctor; engineer; lawyer; musician; pilot).
car(audi; bmw; ford; honda; mercedes; nissan; toyota; volvo).
drink(coffee; juice; milk; soda; tea; water; wine; whiskey).
music(blues; classical; folk; jazz; pop; rap; reggae; rock).
pet(cat; dog; fish; hamster; lizard; parrot; rabbit; snake).
destination(bali; dubai; london; new_york; paris; rome; sydney; tokyo).

% --- Assignment ---
1 { assigned(nationality, V, S) : suite(S) } 1 :- nationality(V).
1 { assigned(profession, V, S) : suite(S) } 1 :- profession(V).
1 { assigned(car, V, S) : suite(S) } 1 :- car(V).
1 { assigned(drink, V, S) : suite(S) } 1 :- drink(V).
1 { assigned(music, V, S) : suite(S) } 1 :- music(V).
1 { assigned(pet, V, S) : suite(S) } 1 :- pet(V).
1 { assigned(destination, V, S) : suite(S) } 1 :- destination(V).

1 { assigned(nationality, V, S) : nationality(V) } 1 :- suite(S).
1 { assigned(profession, V, S) : profession(V) } 1 :- suite(S).
1 { assigned(car, V, S) : car(V) } 1 :- suite(S).
1 { assigned(drink, V, S) : drink(V) } 1 :- suite(S).
1 { assigned(music, V, S) : music(V) } 1 :- suite(S).
1 { assigned(pet, V, S) : pet(V) } 1 :- suite(S).
1 { assigned(destination, V, S) : destination(V) } 1 :- suite(S).

% --- Constraints ---
assigned(drink, milk, 4).
assigned(nationality, hungarian, 4).

% 3. The American is a Lawyer
assigned(nationality, american, S) :- assigned(profession, lawyer, S).
assigned(profession, lawyer, S) :- assigned(nationality, american, S).

% 4. The person who drives a BMW is a Biologist
assigned(car, bmw, S) :- assigned(profession, biologist, S).
assigned(profession, biologist, S) :- assigned(car, bmw, S).

% 5. The Canadian owns a Snake
assigned(nationality, canadian, S) :- assigned(pet, snake, S).
assigned(pet, snake, S) :- assigned(nationality, canadian, S).

% 6. The person who listens to Classical music drives an Audi
assigned(music, classical, S) :- assigned(car, audi, S).
assigned(car, audi, S) :- assigned(music, classical, S).

% 7. The German drinks Coffee
assigned(nationality, german, S) :- assigned(drink, coffee, S).
assigned(drink, coffee, S) :- assigned(nationality, german, S).

% 8. The person going to Tokyo is a Chemist
assigned(destination, tokyo, S) :- assigned(profession, chemist, S).
assigned(profession, chemist, S) :- assigned(destination, tokyo, S).

% 9. The Engineer's suite is immediately to the left of the Lawyer's suite
assigned(profession, engineer, S) :- assigned(profession, lawyer, S+1), suite(S).

% 10. The Dog owner lives next to the Volvo driver
neighbor(S1, S2) :- suite(S1), suite(S2), S2 = S1 + 1.
neighbor(S1, S2) :- suite(S1), suite(S2), S1 = S2 + 1.
:- assigned(pet, dog, S1), assigned(car, volvo, S2), not neighbor(S1, S2).

% 11. The Rock music listener lives next to the Pop music listener
:- assigned(music, rock, S1), assigned(music, pop, S2), not neighbor(S1, S2).

% 12. The person going to Paris lives next to the Fish owner
:- assigned(destination, paris, S1), assigned(pet, fish, S2), not neighbor(S1, S2).

% 13. The Pilot lives in an even-numbered suite
assigned(profession, pilot, S) :- suite(S), S \ 2 = 0.

% 14. The Wine drinker's suite is to the right of the Coffee drinker's suite
% "to the right of" means S_wine > S_coffee
:- assigned(drink, wine, S1), assigned(drink, coffee, S2), S1 < S2.

% 15. The Ford driver has a neighbor who drinks Tea
% This means there exists a neighbor S2 such that drink(tea, S2)
has_tea_neighbor(S1) :- assigned(car, ford, S1), neighbor(S1, S2), assigned(drink, tea, S2).
:- assigned(car, ford, S1), not has_tea_neighbor(S1).

% 16. The Nissan driver does not live in suite #1 or #8
:- assigned(car, nissan, 1).
:- assigned(car, nissan, 8).

% 17. The Jazz listener's suite number is less than the Blues listener's suite number
:- assigned(music, jazz, S1), assigned(music, blues, S2), S1 >= S2.

% 18. The Dutch person lives in suite #1
assigned(nationality, dutch, 1).

% --- Objective ---
lizard_owner(N) :- assigned(pet, lizard, S), assigned(nationality, N, S).

#show lizard_owner/1.