% Knights and Knaves Puzzle with 24 inhabitants
% Define all persons
person(alice). person(bob). person(charlie). person(diana).
person(ethan). person(fiona). person(george). person(hannah).
person(ian). person(julia). person(kevin). person(lily).
person(mason). person(nina). person(oliver). person(paula).
person(quentin). person(rachel). person(sam). person(tina).
person(ursula). person(victor). person(wendy). person(xavier).

% Define groups
groupA(alice). groupA(bob). groupA(charlie). groupA(diana).
groupA(ethan). groupA(fiona). groupA(george). groupA(hannah).

groupB(ian). groupB(julia). groupB(kevin). groupB(lily).
groupB(mason). groupB(nina). groupB(oliver). groupB(paula).

groupC(quentin). groupC(rachel). groupC(sam). groupC(tina).
groupC(ursula). groupC(victor). groupC(wendy). groupC(xavier).

% Each person is exactly one type: knight or knave
1 { type(P, knight) ; type(P, knave) } 1 :- person(P).

% Helper predicate for knights
knight(P) :- type(P, knight).

% Compute counts for groups and total
countA(N) :- N = #count{ P : knight(P), groupA(P) }.
countB(N) :- N = #count{ P : knight(P), groupB(P) }.
countC(N) :- N = #count{ P : knight(P), groupC(P) }.
countTotal(N) :- N = #count{ P : knight(P) }.

% Define subsets for specific statements
bcd(bob). bcd(charlie). bcd(diana).  % For Hannah's statement
ghij(george). ghij(hannah). ghij(ian). ghij(julia).  % For Oliver's statement
abcd(alice). abcd(bob). abcd(charlie). abcd(diana).  % For Victor's statement

% Compute counts for these subsets
countBCD(N) :- N = #count{ P : knight(P), bcd(P) }.
countGHij(N) :- N = #count{ P : knight(P), ghij(P) }.
countKnavesABCD(N) :- N = #count{ P : type(P, knave), abcd(P) }.

% Helper for same type
same_type(X, Y) :- type(X, knight), type(Y, knight).
same_type(X, Y) :- type(X, knave), type(Y, knave).

% Helper for different type
different_type(X, Y) :- type(X, knight), type(Y, knave).
different_type(X, Y) :- type(X, knave), type(Y, knight).

% ===== GROUP A STATEMENTS =====

% 1. Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
% Create helper for Bob knave OR Charlie knight
bob_or_charlie :- type(bob, knave).
bob_or_charlie :- type(charlie, knight).
alice_condition :- type(hannah, knave), bob_or_charlie, countA(4).
:- type(alice, knight), not alice_condition.
:- type(alice, knave), alice_condition.

% 2. Bob: "Diana is the same type as me."
bob_condition :- same_type(diana, bob).
:- type(bob, knight), not bob_condition.
:- type(bob, knave), bob_condition.

% 3. Charlie: "Exactly twelve of us are knights."
charlie_condition :- countTotal(12).
:- type(charlie, knight), not charlie_condition.
:- type(charlie, knave), charlie_condition.

% 4. Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_condition :- different_type(ethan, fiona), type(hannah, knave).
:- type(diana, knight), not diana_condition.
:- type(diana, knave), diana_condition.

% 5. Ethan: "George is a knight if and only if Alice is a knight."
% (George knight AND Alice knight) OR (George knave AND Alice knave)
ethan_cond1 :- type(george, knight), type(alice, knight).
ethan_cond2 :- type(george, knave), type(alice, knave).
ethan_condition :- ethan_cond1.
ethan_condition :- ethan_cond2.
:- type(ethan, knight), not ethan_condition.
:- type(ethan, knave), ethan_condition.

% 6. Fiona: "Bob and Charlie are of different types, and I am a knight."
fiona_condition :- different_type(bob, charlie), type(fiona, knight).
:- type(fiona, knight), not fiona_condition.
:- type(fiona, knave), fiona_condition.

% 7. George: "Alice and Hannah are of the same type."
george_condition :- same_type(alice, hannah).
:- type(george, knight), not george_condition.
:- type(george, knave), george_condition.

% 8. Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_condition :- countBCD(1).
:- type(hannah, knight), not hannah_condition.
:- type(hannah, knave), hannah_condition.

% ===== GROUP B STATEMENTS =====

% 9. Ian: "Alice and Paula are of the same type, and Julia is a knave."
ian_condition :- same_type(alice, paula), type(julia, knave).
:- type(ian, knight), not ian_condition.
:- type(ian, knave), ian_condition.

% 10. Julia: "Kevin is a knight and Nina is a knight."
julia_condition :- type(kevin, knight), type(nina, knight).
:- type(julia, knight), not julia_condition.
:- type(julia, knave), julia_condition.

% 11. Kevin: "Either Oliver is a knight or Lily is a knave."
kevin_cond1 :- type(oliver, knight).
kevin_cond2 :- type(lily, knave).
kevin_condition :- kevin_cond1.
kevin_condition :- kevin_cond2.
:- type(kevin, knight), not kevin_condition.
:- type(kevin, knave), kevin_condition.

% 12. Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_condition :- countB(4), type(oliver, knave).
:- type(lily, knight), not lily_condition.
:- type(lily, knave), lily_condition.

% 13. Mason: "Bob and Ethan are of the same type, and Julia is a knave."
mason_condition :- same_type(bob, ethan), type(julia, knave).
:- type(mason, knight), not mason_condition.
:- type(mason, knave), mason_condition.

% 14. Nina: "Ian and Paula are of different types."
nina_condition :- different_type(ian, paula).
:- type(nina, knight), not nina_condition.
:- type(nina, knave), nina_condition.

% 15. Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_condition :- countGHij(2).
:- type(oliver, knight), not oliver_condition.
:- type(oliver, knave), oliver_condition.

% 16. Paula: "Rachel is a knight if and only if Quentin is a knave."
% (Rachel knight AND Quentin knave) OR (Rachel knave AND Quentin knight)
paula_cond1 :- type(rachel, knight), type(quentin, knave).
paula_cond2 :- type(rachel, knave), type(quentin, knight).
paula_condition :- paula_cond1.
paula_condition :- paula_cond2.
:- type(paula, knight), not paula_condition.
:- type(paula, knave), paula_condition.

% ===== GROUP C STATEMENTS =====

% 17. Quentin: "At least five of us in Group C are knights."
quentin_condition :- countC(N), N >= 5.
:- type(quentin, knight), not quentin_condition.
:- type(quentin, knave), quentin_condition.

% 18. Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_condition :- type(charlie, knight), type(lily, knight), type(victor, knave).
:- type(rachel, knight), not rachel_condition.
:- type(rachel, knave), rachel_condition.

% 19. Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_condition :- type(tina, knave), type(oliver, knave), type(ursula, knave).
:- type(sam, knight), not sam_condition.
:- type(sam, knave), sam_condition.

% 20. Tina: "Rachel is a knave or Mason is a knave."
tina_cond1 :- type(rachel, knave).
tina_cond2 :- type(mason, knave).
tina_condition :- tina_cond1.
tina_condition :- tina_cond2.
:- type(tina, knight), not tina_condition.
:- type(tina, knave), tina_condition.

% 21. Ursula: "Ian and Julia are both knights."
ursula_condition :- type(ian, knight), type(julia, knight).
:- type(ursula, knight), not ursula_condition.
:- type(ursula, knave), ursula_condition.

% 22. Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_condition :- countKnavesABCD(2).
:- type(victor, knight), not victor_condition.
:- type(victor, knave), victor_condition.

% 23. Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_condition :- type(victor, knave), type(ursula, knave), type(xavier, knight).
:- type(wendy, knight), not wendy_condition.
:- type(wendy, knave), wendy_condition.

% 24. Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_condition :- countC(4), type(sam, knight).
:- type(xavier, knight), not xavier_condition.
:- type(xavier, knave), xavier_condition.

% Show the solution
#show type/2.
#show countA/1.
#show countB/1.
#show countC/1.
#show countTotal/1.