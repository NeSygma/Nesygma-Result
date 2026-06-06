% Domain facts
person(michael).
person(peter).
person(windy).

% Man predicate
man(michael).
man(peter).
man(windy).

% Class membership
class_member(michael).
class_member(windy).
% Note: Peter is not in class.

% Premises
% Michael taller than everyone else in his class
% For all Y, if class_member(Y) and Y != michael, then taller(michael, Y).
taller(michael, Y) :- class_member(Y), Y != michael.

% Peter taller than Michael
% Fact
% Note: This contradicts the previous premise if Peter were in class.
taller(peter, michael).

% Transitivity
% If taller(X, Y) and taller(Y, Z) then taller(X, Z).
taller(X, Z) :- taller(X, Y), taller(Y, Z).

% Conclusion
% There exists a man in Michael's class taller than Peter.
conclusion_true :- man(M), class_member(M), taller(M, peter).
% We do not derive conclusion_false because we cannot prove it.

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.