% Knights and Knaves Puzzle - 24 inhabitants

% Define the two types
type(knight; knave).

% Define all inhabitants
person(alice; bob; charlie; diana; ethan; fiona; george; hannah;
       ian; julia; kevin; lily; mason; nina; oliver; paula;
       quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

% Each person is exactly one type
1 { is_type(P, T) : type(T) } 1 :- person(P).

% Helper: person is knight or knave
is_knight(P) :- is_type(P, knight).
is_knave(P) :- is_type(P, knave).

% Group definitions
group_a(alice); group_a(bob); group_a(charlie); group_a(diana);
group_a(ethan); group_a(fiona); group_a(george); group_a(hannah).

group_b(ian); group_b(julia); group_b(kevin); group_b(lily);
group_b(mason); group_b(nina); group_b(oliver); group_b(paula).

group_c(quentin); group_c(rachel); group_c(sam); group_c(tina);
group_c(ursula); group_c(victor); group_c(wendy); group_c(xavier).

% Count knights in each group
knights_in_a(N) :- N = #count{P : group_a(P), is_knight(P)}.
knights_in_b(N) :- N = #count{P : group_b(P), is_knight(P)}.
knights_in_c(N) :- N = #count{P : group_c(P), is_knight(P)}.

% Count knights overall
total_knights(N) :- N = #count{P : person(P), is_knight(P)}.

% ===== GROUP A STATEMENTS =====

% Alice says: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
alice_statement_true :- is_knave(hannah), (is_knave(bob) or is_knight(charlie)), knights_in_a(4).
alice_statement_false :- not alice_statement_true.
is_knight(alice) :- alice_statement_true.
is_knave(alice) :- alice_statement_false.

% Bob says: "Diana is the same type as me."
bob_statement_true :- (is_knight(diana) and is_knight(bob)) or (is_knave(diana) and is_knave(bob)).
bob_statement_false :- not bob_statement_true.
is_knight(bob) :- bob_statement_true.
is_knave(bob) :- bob_statement_false.

% Charlie says: "Exactly twelve of us are knights."
charlie_statement_true :- total_knights(12).
charlie_statement_false :- not charlie_statement_true.
is_knight(charlie) :- charlie_statement_true.
is_knave(charlie) :- charlie_statement_false.

% Diana says: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_statement_true :- (is_knight(ethan) and is_knave(fiona)) or (is_knave(ethan) and is_knight(fiona)), is_knave(hannah).
diana_statement_false :- not diana_statement_true.
is_knight(diana) :- diana_statement_true.
is_knave(diana) :- diana_statement_false.

% Ethan says: "George is a knight if and only if Alice is a knight."
ethan_statement_true :- (is_knight(george) and is_knight(alice)) or (is_knave(george) and is_knave(alice)).
ethan_statement_false :- not ethan_statement_true.
is_knight(ethan) :- ethan_statement_true.
is_knave(ethan) :- ethan_statement_false.

% Fiona says: "Bob and Charlie are of different types, and I am a knight."
fiona_statement_true :- ((is_knight(bob) and is_knave(charlie)) or (is_knave(bob) and is_knight(charlie))), is_knight(fiona).
fiona_statement_false :- not fiona_statement_true.
is_knight(fiona) :- fiona_statement_true.
is_knave(fiona) :- fiona_statement_false.

% George says: "Alice and Hannah are of the same type."
george_statement_true :- (is_knight(alice) and is_knight(hannah)) or (is_knave(alice) and is_knave(hannah)).
george_statement_false :- not george_statement_true.
is_knight(george) :- george_statement_true.
is_knave(george) :- george_statement_false.

% Hannah says: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_statement_true :- N = #count{P : (P=bob; P=charlie; P=diana), is_knight(P)}, N = 1.
hannah_statement_false :- not hannah_statement_true.
is_knight(hannah) :- hannah_statement_true.
is_knave(hannah) :- hannah_statement_false.

% ===== GROUP B STATEMENTS =====

% Ian says: "Alice and Paula are of the same type, and Julia is a knave."
ian_statement_true :- ((is_knight(alice) and is_knight(paula)) or (is_knave(alice) and is_knave(paula))), is_knave(julia).
ian_statement_false :- not ian_statement_true.
is_knight(ian) :- ian_statement_true.
is_knave(ian) :- ian_statement_false.

% Julia says: "Kevin is a knight and Nina is a knight."
julia_statement_true :- is_knight(kevin), is_knight(nina).
julia_statement_false :- not julia_statement_true.
is_knight(julia) :- julia_statement_true.
is_knave(julia) :- julia_statement_false.

% Kevin says: "Either Oliver is a knight or Lily is a knave."
kevin_statement_true :- is_knight(oliver) or is_knave(lily).
kevin_statement_false :- not kevin_statement_true.
is_knight(kevin) :- kevin_statement_true.
is_knave(kevin) :- kevin_statement_false.

% Lily says: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_statement_true :- knights_in_b(4), is_knave(oliver).
lily_statement_false :- not lily_statement_true.
is_knight(lily) :- lily_statement_true.
is_knave(lily) :- lily_statement_false.

% Mason says: "Bob and Ethan are of the same type, and Julia is a knave."
mason_statement_true :- ((is_knight(bob) and is_knight(ethan)) or (is_knave(bob) and is_knave(ethan))), is_knave(julia).
mason_statement_false :- not mason_statement_true.
is_knight(mason) :- mason_statement_true.
is_knave(mason) :- mason_statement_false.

% Nina says: "Ian and Paula are of different types."
nina_statement_true :- (is_knight(ian) and is_knave(paula)) or (is_knave(ian) and is_knight(paula)).
nina_statement_false :- not nina_statement_true.
is_knight(nina) :- nina_statement_true.
is_knave(nina) :- nina_statement_false.

% Oliver says: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_statement_true :- N = #count{P : (P=george; P=hannah; P=ian; P=julia), is_knight(P)}, N = 2.
oliver_statement_false :- not oliver_statement_true.
is_knight(oliver) :- oliver_statement_true.
is_knave(oliver) :- oliver_statement_false.

% Paula says: "Rachel is a knight if and only if Quentin is a knave."
paula_statement_true :- (is_knight(rachel) and is_knave(quentin)) or (is_knave(rachel) and is_knight(quentin)).
paula_statement_false :- not paula_statement_true.
is_knight(paula) :- paula_statement_true.
is_knave(paula) :- paula_statement_false.

% ===== GROUP C STATEMENTS =====

% Quentin says: "At least five of us in Group C are knights."
quentin_statement_true :- knights_in_c(N), N >= 5.
quentin_statement_false :- not quentin_statement_true.
is_knight(quentin) :- quentin_statement_true.
is_knave(quentin) :- quentin_statement_false.

% Rachel says: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_statement_true :- is_knight(charlie), is_knight(lily), is_knave(victor).
rachel_statement_false :- not rachel_statement_true.
is_knight(rachel) :- rachel_statement_true.
is_knave(rachel) :- rachel_statement_false.

% Sam says: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_statement_true :- is_knave(tina), is_knave(oliver), is_knave(ursula).
sam_statement_false :- not sam_statement_true.
is_knight(sam) :- sam_statement_true.
is_knave(sam) :- sam_statement_false.

% Tina says: "Rachel is a knave or Mason is a knave."
tina_statement_true :- is_knave(rachel) or is_knave(mason).
tina_statement_false :- not tina_statement_true.
is_knight(tina) :- tina_statement_true.
is_knave(tina) :- tina_statement_false.

% Ursula says: "Ian and Julia are both knights."
ursula_statement_true :- is_knight(ian), is_knight(julia).
ursula_statement_false :- not ursula_statement_true.
is_knight(ursula) :- ursula_statement_true.
is_knave(ursula) :- ursula_statement_false.

% Victor says: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_statement_true :- N = #count{P : (P=alice; P=bob; P=charlie; P=diana), is_knave(P)}, N = 2.
victor_statement_false :- not victor_statement_true.
is_knight(victor) :- victor_statement_true.
is_knave(victor) :- victor_statement_false.

% Wendy says: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_statement_true :- is_knave(victor), is_knave(ursula), is_knight(xavier).
wendy_statement_false :- not wendy_statement_true.
is_knight(wendy) :- wendy_statement_true.
is_knave(wendy) :- wendy_statement_false.

% Xavier says: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_statement_true :- knights_in_c(4), is_knight(sam).
xavier_statement_false :- not xavier_statement_true.
is_knight(xavier) :- xavier_statement_true.
is_knave(xavier) :- xavier_statement_false.

% ===== OUTPUT =====
#show is_type/2.
#show knights_in_a/1.
#show knights_in_b/1.
#show knights_in_c/1.
#show total_knights/1.