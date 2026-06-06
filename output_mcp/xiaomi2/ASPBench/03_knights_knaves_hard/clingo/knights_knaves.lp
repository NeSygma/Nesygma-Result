% Define all persons
person(alice). person(bob). person(charlie). person(diana).
person(ethan). person(fiona). person(george). person(hannah).
person(ian). person(julia). person(kevin). person(lily).
person(mason). person(nina). person(oliver). person(paula).
person(quentin). person(rachel). person(sam). person(tina).
person(ursula). person(victor). person(wendy). person(xavier).

% Groups
group_a(alice). group_a(bob). group_a(charlie). group_a(diana).
group_a(ethan). group_a(fiona). group_a(george). group_a(hannah).
group_b(ian). group_b(julia). group_b(kevin). group_b(lily).
group_b(mason). group_b(nina). group_b(oliver). group_b(paula).
group_c(quentin). group_c(rachel). group_c(sam). group_c(tina).
group_c(ursula). group_c(victor). group_c(wendy). group_c(xavier).

% Each person is either knight or knave (choice)
{ knight(X) } :- person(X).
knave(X) :- person(X), not knight(X).

% Helper: count knights in groups
group_a_knights(N) :- N = #count{X : group_a(X), knight(X)}.
group_b_knights(N) :- N = #count{X : group_b(X), knight(X)}.
group_c_knights(N) :- N = #count{X : group_c(X), knight(X)}.
total_knights(N) :- N = #count{X : person(X), knight(X)}.

% Statement truth definitions

% Alice: Hannah is knave, (Bob knave or Charlie knight), exactly 4 knights in group A
% Split disjunction into separate rules
alice_cond1 :- knave(hannah).
alice_cond2 :- knave(bob).
alice_cond2 :- knight(charlie).
alice_cond3 :- group_a_knights(4).
statement_true(alice) :- alice_cond1, alice_cond2, alice_cond3.

% Bob: Diana is same type as me
statement_true(bob) :- knight(bob), knight(diana).
statement_true(bob) :- knave(bob), knave(diana).

% Charlie: Exactly 12 knights total
statement_true(charlie) :- total_knights(12).

% Diana: Ethan and Fiona different types, Hannah knave
statement_true(diana) :- knight(ethan), knave(fiona), knave(hannah).
statement_true(diana) :- knave(ethan), knight(fiona), knave(hannah).

% Ethan: George knight iff Alice knight
statement_true(ethan) :- knight(george), knight(alice).
statement_true(ethan) :- knave(george), knave(alice).

% Fiona: Bob and Charlie different types, and Fiona knight
statement_true(fiona) :- knight(bob), knave(charlie), knight(fiona).
statement_true(fiona) :- knave(bob), knight(charlie), knight(fiona).

% George: Alice and Hannah same type
statement_true(george) :- knight(alice), knight(hannah).
statement_true(george) :- knave(alice), knave(hannah).

% Hannah: Exactly one of Bob, Charlie, Diana is knight
statement_true(hannah) :- knight(bob), knave(charlie), knave(diana).
statement_true(hannah) :- knave(bob), knight(charlie), knave(diana).
statement_true(hannah) :- knave(bob), knave(charlie), knight(diana).

% Ian: Alice and Paula same type, Julia knave
statement_true(ian) :- knight(alice), knight(paula), knave(julia).
statement_true(ian) :- knave(alice), knave(paula), knave(julia).

% Julia: Kevin knight and Nina knight
statement_true(julia) :- knight(kevin), knight(nina).

% Kevin: Oliver knight or Lily knave
statement_true(kevin) :- knight(oliver).
statement_true(kevin) :- knave(lily).

% Lily: Exactly 4 knights in group B, Oliver knave
statement_true(lily) :- group_b_knights(4), knave(oliver).

% Mason: Bob and Ethan same type, Julia knave
statement_true(mason) :- knight(bob), knight(ethan), knave(julia).
statement_true(mason) :- knave(bob), knave(ethan), knave(julia).

% Nina: Ian and Paula different types
statement_true(nina) :- knight(ian), knave(paula).
statement_true(nina) :- knave(ian), knight(paula).

% Oliver: Exactly two of George, Hannah, Ian, Julia are knights
oliver_count(N) :- N = #count{1 : knight(george); 2 : knight(hannah); 3 : knight(ian); 4 : knight(julia)}.
statement_true(oliver) :- oliver_count(2).

% Paula: Rachel knight iff Quentin knave
statement_true(paula) :- knight(rachel), knave(quentin).
statement_true(paula) :- knave(rachel), knight(quentin).

% Quentin: At least 5 knights in group C
statement_true(quentin) :- group_c_knights(N), N >= 5.

% Rachel: Charlie knight, Lily knight, Victor knave
statement_true(rachel) :- knight(charlie), knight(lily), knave(victor).

% Sam: Tina knave, Oliver knave, Ursula knave
statement_true(sam) :- knave(tina), knave(oliver), knave(ursula).

% Tina: Rachel knave or Mason knave
statement_true(tina) :- knave(rachel).
statement_true(tina) :- knave(mason).

% Ursula: Ian and Julia both knights
statement_true(ursula) :- knight(ian), knight(julia).

% Victor: Exactly two of Alice, Bob, Charlie, Diana are knaves
victor_count(N) :- N = #count{1 : knave(alice); 2 : knave(bob); 3 : knave(charlie); 4 : knave(diana)}.
statement_true(victor) :- victor_count(2).

% Wendy: Victor knave, Ursula knave, Xavier knight
statement_true(wendy) :- knave(victor), knave(ursula), knight(xavier).

% Xavier: Exactly 4 knights in group C, Sam knight
statement_true(xavier) :- group_c_knights(4), knight(sam).

% Constraints: knights must have true statements, knaves must have false statements
:- knight(X), not statement_true(X).
:- knave(X), statement_true(X).

% Show assignments
#show knight/1.
#show knave/1.