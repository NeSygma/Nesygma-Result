person(luke).

{ born_multiple_birth(luke) } :- person(luke).
{ lives_with_strangers(luke) } :- person(luke).

:- born_multiple_birth(luke), not lives_with_strangers(luke).
:- lives_with_strangers(luke), not born_multiple_birth(luke).

spends_time_with_siblings(X) :- born_multiple_birth(X), person(X).
born_multiple_birth(X) :- has_siblings_born_together(X), person(X).
has_siblings_born_together(X) :- complains_often(X), person(X).
:- lives_at_home(X), lives_with_strangers(X), person(X).
lives_at_home(X) :- spends_time_with_siblings(X), person(X).

conclusion_true :- complains_often(luke).
conclusion_false :- false.

answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.