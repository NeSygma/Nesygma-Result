% Facts
plate_in_istanbul(j).
begins_with_35(t).

% Equivalence between plate_in_istanbul and begins_with_34
begins_with_34(P) :- plate_in_istanbul(P).
plate_in_istanbul(P) :- begins_with_34(P).

% Constraint: plates that begin with 35 cannot begin with 34
:- begins_with_35(P), begins_with_34(P).

% Conclusion evaluation
conclusion_true :- begins_with_34(j).
conclusion_false :- not begins_with_34(j).

% Answer mapping
answer(true)      :- conclusion_true.
answer(false)     :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.