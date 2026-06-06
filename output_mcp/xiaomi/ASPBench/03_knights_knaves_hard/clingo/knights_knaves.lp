% ===== DOMAIN =====
person(alice). person(bob). person(charlie). person(diana).
person(ethan). person(fiona). person(george). person(hannah).
person(ian). person(julia). person(kevin). person(lily).
person(mason). person(nina). person(oliver). person(paula).
person(quentin). person(rachel). person(sam). person(tina).
person(ursula). person(victor). person(wendy). person(xavier).

% Group membership
group_a(alice). group_a(bob). group_a(charlie). group_a(diana).
group_a(ethan). group_a(fiona). group_a(george). group_a(hannah).
group_b(ian). group_b(julia). group_b(kevin). group_b(lily).
group_b(mason). group_b(nina). group_b(oliver). group_b(paula).
group_c(quentin). group_c(rachel). group_c(sam). group_c(tina).
group_c(ursula). group_c(victor). group_c(wendy). group_c(xavier).

% ===== CHOICE: Each person is knight or knave =====
{ knight(X) } :- person(X).

% ===== HELPER: knave definition =====
knave(X) :- person(X), not knight(X).

% ===== GROUP A KNIGHT COUNTS =====
group_a_knights(N) :- N = #count{X : group_a(X), knight(X)}.
group_b_knights(N) :- N = #count{X : group_b(X), knight(X)}.
group_c_knights(N) :- N = #count{X : group_c(X), knight(X)}.
total_knights(N) :- N = #count{X : person(X), knight(X)}.

% ===== STATEMENT TRUTH CONDITIONS =====

% Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
alice_stmt_true :- knave(hannah), knave(bob), group_a_knights(4).
alice_stmt_true :- knave(hannah), knight(charlie), group_a_knights(4).

% Bob: "Diana is the same type as me."
bob_stmt_true :- knight(bob), knight(diana).
bob_stmt_true :- knave(bob), knave(diana).

% Charlie: "Exactly twelve of us are knights."
charlie_stmt_true :- total_knights(12).

% Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_stmt_true :- knight(ethan), knave(fiona), knave(hannah).
diana_stmt_true :- knave(ethan), knight(fiona), knave(hannah).

% Ethan: "George is a knight if and only if Alice is a knight."
ethan_stmt_true :- knight(george), knight(alice).
ethan_stmt_true :- knave(george), knave(alice).

% Fiona: "Bob and Charlie are of different types, and I am a knight."
fiona_stmt_true :- knight(fiona), knight(bob), knave(charlie).
fiona_stmt_true :- knight(fiona), knave(bob), knight(charlie).

% George: "Alice and Hannah are of the same type."
george_stmt_true :- knight(alice), knight(hannah).
george_stmt_true :- knave(alice), knave(hannah).

% Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_stmt_true :- N = #count{1 : knight(bob); 2 : knight(charlie); 3 : knight(diana)}, N = 1.

% Ian: "Alice and Paula are of the same type, and Julia is a knave."
ian_stmt_true :- knight(alice), knight(paula), knave(julia).
ian_stmt_true :- knave(alice), knave(paula), knave(julia).

% Julia: "Kevin is a knight and Nina is a knight."
julia_stmt_true :- knight(kevin), knight(nina).

% Kevin: "Either Oliver is a knight or Lily is a knave."
kevin_stmt_true :- knight(oliver).
kevin_stmt_true :- knave(lily).

% Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_stmt_true :- group_b_knights(4), knave(oliver).

% Mason: "Bob and Ethan are of the same type, and Julia is a knave."
mason_stmt_true :- knight(bob), knight(ethan), knave(julia).
mason_stmt_true :- knave(bob), knave(ethan), knave(julia).

% Nina: "Ian and Paula are of different types."
nina_stmt_true :- knight(ian), knave(paula).
nina_stmt_true :- knave(ian), knight(paula).

% Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_stmt_true :- N = #count{1 : knight(george); 2 : knight(hannah); 3 : knight(ian); 4 : knight(julia)}, N = 2.

% Paula: "Rachel is a knight if and only if Quentin is a knave."
paula_stmt_true :- knight(rachel), knave(quentin).
paula_stmt_true :- knave(rachel), knight(quentin).

% Quentin: "At least five of us in Group C are knights."
quentin_stmt_true :- group_c_knights(N), N >= 5.

% Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_stmt_true :- knight(charlie), knight(lily), knave(victor).

% Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_stmt_true :- knave(tina), knave(oliver), knave(ursula).

% Tina: "Rachel is a knave or Mason is a knave."
tina_stmt_true :- knave(rachel).
tina_stmt_true :- knave(mason).

% Ursula: "Ian and Julia are both knights."
ursula_stmt_true :- knight(ian), knight(julia).

% Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_stmt_true :- N = #count{1 : knave(alice); 2 : knave(bob); 3 : knave(charlie); 4 : knave(diana)}, N = 2.

% Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_stmt_true :- knave(victor), knave(ursula), knight(xavier).

% Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_stmt_true :- group_c_knights(4), knight(sam).

% ===== CONSISTENCY CONSTRAINTS =====
% Knight iff statement is true
:- knight(alice), not alice_stmt_true.
:- knave(alice), alice_stmt_true.

:- knight(bob), not bob_stmt_true.
:- knave(bob), bob_stmt_true.

:- knight(charlie), not charlie_stmt_true.
:- knave(charlie), charlie_stmt_true.

:- knight(diana), not diana_stmt_true.
:- knave(diana), diana_stmt_true.

:- knight(ethan), not ethan_stmt_true.
:- knave(ethan), ethan_stmt_true.

:- knight(fiona), not fiona_stmt_true.
:- knave(fiona), fiona_stmt_true.

:- knight(george), not george_stmt_true.
:- knave(george), george_stmt_true.

:- knight(hannah), not hannah_stmt_true.
:- knave(hannah), hannah_stmt_true.

:- knight(ian), not ian_stmt_true.
:- knave(ian), ian_stmt_true.

:- knight(julia), not julia_stmt_true.
:- knave(julia), julia_stmt_true.

:- knight(kevin), not kevin_stmt_true.
:- knave(kevin), kevin_stmt_true.

:- knight(lily), not lily_stmt_true.
:- knave(lily), lily_stmt_true.

:- knight(mason), not mason_stmt_true.
:- knave(mason), mason_stmt_true.

:- knight(nina), not nina_stmt_true.
:- knave(nina), nina_stmt_true.

:- knight(oliver), not oliver_stmt_true.
:- knave(oliver), oliver_stmt_true.

:- knight(paula), not paula_stmt_true.
:- knave(paula), paula_stmt_true.

:- knight(quentin), not quentin_stmt_true.
:- knave(quentin), quentin_stmt_true.

:- knight(rachel), not rachel_stmt_true.
:- knave(rachel), rachel_stmt_true.

:- knight(sam), not sam_stmt_true.
:- knave(sam), sam_stmt_true.

:- knight(tina), not tina_stmt_true.
:- knave(tina), tina_stmt_true.

:- knight(ursula), not ursula_stmt_true.
:- knave(ursula), ursula_stmt_true.

:- knight(victor), not victor_stmt_true.
:- knave(victor), victor_stmt_true.

:- knight(wendy), not wendy_stmt_true.
:- knave(wendy), wendy_stmt_true.

:- knight(xavier), not xavier_stmt_true.
:- knave(xavier), xavier_stmt_true.

% ===== OUTPUT =====
#show knight/1.
#show knave/1.