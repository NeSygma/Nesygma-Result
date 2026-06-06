% Rockie Animals Problem
% ========================

% Domain: Animals that can be spotted near campus
animal(rockie).
animal(rabbit1).
animal(turtle1).
animal(squirrel1).

% Rockie facts from premise 6
spotted_near_campus(rockie).
calm(rockie).

% Some turtle spotted near campus (premise 2)
spotted_near_campus(turtle1).
turtle(turtle1).

% Open relations for animal types (we don't know Rockie's type)
{ rabbit(X) } :- animal(X).
{ turtle(X) } :- animal(X).
{ squirrel(X) } :- animal(X).

% Premise 1: All rabbits that can be spotted near campus are cute
cute(X) :- rabbit(X), spotted_near_campus(X).

% Premise 3 constraint: Only rabbits and squirrels spotted near campus
% If spotted_near_campus(X), then X must be rabbit or squirrel
:- spotted_near_campus(X), not rabbit(X), not squirrel(X).

% Premise 4: If skittish then not calm
:- skittish(X), calm(X).

% Premise 5: All squirrels spotted near campus are skittish
skittish(X) :- squirrel(X), spotted_near_campus(X).

% Additional constraint: An animal can't be both rabbit and squirrel
:- rabbit(X), squirrel(X).

% Additional constraint: An animal can't be both rabbit and turtle
:- rabbit(X), turtle(X).

% Additional constraint: An animal can't be both turtle and squirrel
:- turtle(X), squirrel(X).

% Conclusion evaluation:
% "If Rockie is not both a turtle and a squirrel, then Rockie is either cute or skittish"
% Formally: (¬(turtle(rockie) ∧ squirrel(rockie))) → (cute(rockie) ∨ skittish(rockie))

% Define when conclusion is definitely true
% Case 1: Rockie IS both turtle and squirrel (antecedent false, so implication true)
both_turtle_squirrel :- turtle(rockie), squirrel(rockie).

% Case 2: Rockie is cute or skittish (consequent true, so implication true)
consequent_true :- cute(rockie) OR skittish(rockie).

% Conclusion is true if either case holds
conclusion_true :- both_turtle_squirrel.
conclusion_true :- consequent_true.

% Define when conclusion is definitely false
% This would require: Rockie is NOT both turtle and squirrel, AND Rockie is neither cute nor skittish
conclusion_false :-
    not both_turtle_squirrel,  % Rockie is not both turtle and squirrel
    not cute(rockie),          % Rockie is not cute
    not skittish(rockie).      % Rockie is not skittish

% Final answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

% Show the answer
#show answer/1.

% Also show relevant facts for debugging
#show rabbit/1.
#show turtle/1.
#show squirrel/1.
#show cute/1.
#show skittish/1.
#show calm/1.
#show spotted_near_campus/1.