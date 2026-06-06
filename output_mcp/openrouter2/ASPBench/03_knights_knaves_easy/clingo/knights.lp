person(alice). person(bob). person(charlie).

{ type(Person, knight); type(Person, knave) } 1 :- person(Person).

statement_true(alice) :- type(bob, knave).
statement_true(bob) :- type(alice, T), type(charlie, T).
statement_true(charlie) :- type(alice, knight).

:- type(Person, knight), not statement_true(Person).
:- type(Person, knave), statement_true(Person).

#show type/2.