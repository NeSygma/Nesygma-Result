% Define the domain of people
person(michael).
person(peter).
person(windy).

% Define who is a man
man(michael).
man(peter).
man(windy).

% Michael is taller than Peter and Windy
taller(michael, peter).
taller(michael, windy).

% Peter is taller than Michael
taller(peter, michael).

% Transitivity of taller relation
taller(X, Z) :- taller(X, Y), taller(Y, Z).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting
% This is a general rule that applies to all men
can_block(Taller, Shorter) :- taller(Taller, Shorter), man(Taller), man(Shorter).

% Premise 5: Michael can block any shooting from a person as long as the person does not jump when shooting
% This is a specific rule about Michael's blocking ability
can_block(michael, Person) :- man(Person), Person != windy, not can_jump(Person).

% Premise 6: Michael cannot block Windy's shooting
% This is a specific exception
:- can_block(michael, windy).

% Define can_jump as an open relation (can be true or false for each person)
{ can_jump(X) : person(X) }.

% Premise 7: Every shooter who can jump when shooting is a great shooter
shooter(X) :- person(X).
great_shooter(X) :- shooter(X), can_jump(X).

% Define the conclusion
conclusion_true :- great_shooter(windy).
conclusion_false :- not great_shooter(windy).
conclusion_uncertain :- not conclusion_true, not conclusion_false.

answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- conclusion_uncertain.

#show answer/1.