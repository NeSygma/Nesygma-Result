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

% Count knaves in subset
knave_count_in_subset(N, S) :- N = #count{P : S(P), is_knave(P)}.

% ===== GROUP A STATEMENTS =====

% Alice says: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
% Statement is true iff Alice is knight
alice_statement :- is_knave(hannah), (is_knave(bob) ; is_knight(charlie)), knights_in_a(4).
% Alice's statement is false iff Alice is knave
alice_statement_false :- not (is_knave(hannah) and (is_knave(bob) or is_knight(charlie)) and knights_in_a(4)).
% Constraint: Alice is knight iff her statement is true, knave iff false
is_knight(alice) :- alice_statement.
is_knave(alice) :- alice_statement_false.

% Bob says: "Diana is the same type as me."
bob_statement :- (is_knight(diana) and is_knight(bob)) or (is_knave(diana) and is_knave(bob)).
bob_statement_false :- not ((is_knight(diana) and is_knight(bob)) or (is_knave(diana) and is_knave(bob))).
is_knight(bob) :- bob_statement.
is_knave(bob) :- bob_statement_false.

% Charlie says: "Exactly twelve of us are knights."
charlie_statement :- total_knights(12).
charlie_statement_false :- not total_knights(12).
is_knight(charlie) :- charlie_statement.
is_knave(charlie) :- charlie_statement_false.

% Diana says: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_statement :- (is_knight(ethan) and is_knave(fiona)) or (is_knave(ethan) and is_knight(fiona)), is_knave(hannah).
diana_statement_false :- not ((is_knight(ethan) and is_knave(fiona)) or (is_knave(ethan) and is_knight(fiona)) and is_knave(hannah)).
is_knight(diana) :- diana_statement.
is_knave(diana) :- diana_statement_false.

% Ethan says: "George is a knight if and only if Alice is a knight."
ethan_statement :- (is_knight(george) and is_knight(alice)) or (is_knave(george) and is_knave(alice)).
ethan_statement_false :- not ((is_knight(george) and is_knight(alice)) or (is_knave(george) and is_knave(alice))).
is_knight(ethan) :- ethan_statement.
is_knave(ethan) :- ethan_statement_false.

% Fiona says: "Bob and Charlie are of different types, and I am a knight."
fiona_statement :- ((is_knight(bob) and is_knave(charlie)) or (is_knave(bob) and is_knight(charlie))), is_knight(fiona).
fiona_statement_false :- not (((is_knight(bob) and is_knave(charlie)) or (is_knave(bob) and is_knight(charlie))) and is_knight(fiona)).
is_knight(fiona) :- fiona_statement.
is_knave(fiona) :- fiona_statement_false.

% George says: "Alice and Hannah are of the same type."
george_statement :- (is_knight(alice) and is_knight(hannah)) or (is_knave(alice) and is_knave(hannah)).
george_statement_false :- not ((is_knight(alice) and is_knight(hannah)) or (is_knave(alice) and is_knave(hannah))).
is_knight(george) :- george_statement.
is_knave(george) :- george_statement_false.

% Hannah says: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_statement :- N = #count{P : (P=bob; P=charlie; P=diana), is_knight(P)}, N = 1.
hannah_statement_false :- N = #count{P : (P=bob; P=charlie; P=diana), is_knight(P)}, N != 1.
is_knight(hannah) :- hannah_statement.
is_knave(hannah) :- hannah_statement_false.

% ===== GROUP B STATEMENTS =====

% Ian says: "Alice and Paula are of the same type, and Julia is a knave."
ian_statement :- ((is_knight(alice) and is_knight(paula)) or (is_knave(alice) and is_knave(paula))), is_knave(julia).
ian_statement_false :- not (((is_knight(alice) and is_knight(paula)) or (is_knave(alice) and is_knave(paula))) and is_knave(julia)).
is_knight(ian) :- ian_statement.
is_knave(ian) :- ian_statement_false.

% Julia says: "Kevin is a knight and Nina is a knight."
julia_statement :- is_knight(kevin), is_knight(nina).
julia_statement_false :- not (is_knight(kevin) and is_knight(nina)).
is_knight(julia) :- julia_statement.
is_knave(julia) :- julia_statement_false.

% Kevin says: "Either Oliver is a knight or Lily is a knave."
kevin_statement :- is_knight(oliver) or is_knave(lily).
kevin_statement_false :- not (is_knight(oliver) or is_knave(lily)).
is_knight(kevin) :- kevin_statement.
is_knave(kevin) :- kevin_statement_false.

% Lily says: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_statement :- knights_in_b(4), is_knave(oliver).
lily_statement_false :- not (knights_in_b(4) and is_knave(oliver)).
is_knight(lily) :- lily_statement.
is_knave(lily) :- lily_statement_false.

% Mason says: "Bob and Ethan are of the same type, and Julia is a knave."
mason_statement :- ((is_knight(bob) and is_knight(ethan)) or (is_knave(bob) and is_knave(ethan))), is_knave(julia).
mason_statement_false :- not (((is_knight(bob) and is_knight(ethan)) or (is_knave(bob) and is_knave(ethan))) and is_knave(julia)).
is_knight(mason) :- mason_statement.
is_knave(mason) :- mason_statement_false.

% Nina says: "Ian and Paula are of different types."
nina_statement :- (is_knight(ian) and is_knave(paula)) or (is_knave(ian) and is_knight(paula)).
nina_statement_false :- not ((is_knight(ian) and is_knave(paula)) or (is_knave(ian) and is_knight(paula))).
is_knight(nina) :- nina_statement.
is_knave(nina) :- nina_statement_false.

% Oliver says: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_statement :- N = #count{P : (P=george; P=hannah; P=ian; P=julia), is_knight(P)}, N = 2.
oliver_statement_false :- N = #count{P : (P=george; P=hannah; P=ian; P=julia), is_knight(P)}, N != 2.
is_knight(oliver) :- oliver_statement.
is_knave(oliver) :- oliver_statement_false.

% Paula says: "Rachel is a knight if and only if Quentin is a knave."
paula_statement :- (is_knight(rachel) and is_knave(quentin)) or (is_knave(rachel) and is_knight(quentin)).
paula_statement_false :- not ((is_knight(rachel) and is_knave(quentin)) or (is_knave(rachel) and is_knight(quentin))).
is_knight(paula) :- paula_statement.
is_knave(paula) :- paula_statement_false.

% ===== GROUP C STATEMENTS =====

% Quentin says: "At least five of us in Group C are knights."
quentin_statement :- knights_in_c(N), N >= 5.
quentin_statement_false :- knights_in_c(N), N < 5.
is_knight(quentin) :- quentin_statement.
is_knave(quentin) :- quentin_statement_false.

% Rachel says: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_statement :- is_knight(charlie), is_knight(lily), is_knave(victor).
rachel_statement_false :- not (is_knight(charlie) and is_knight(lily) and is_knave(victor)).
is_knight(rachel) :- rachel_statement.
is_knave(rachel) :- rachel_statement_false.

% Sam says: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_statement :- is_knave(tina), is_knave(oliver), is_knave(ursula).
sam_statement_false :- not (is_knave(tina) and is_knave(oliver) and is_knave(ursula)).
is_knight(sam) :- sam_statement.
is_knave(sam) :- sam_statement_false.

% Tina says: "Rachel is a knave or Mason is a knave."
tina_statement :- is_knave(rachel) or is_knave(mason).
tina_statement_false :- not (is_knave(rachel) or is_knave(mason)).
is_knight(tina) :- tina_statement.
is_knave(tina) :- tina_statement_false.

% Ursula says: "Ian and Julia are both knights."
ursula_statement :- is_knight(ian), is_knight(julia).
ursula_statement_false :- not (is_knight(ian) and is_knight(julia)).
is_knight(ursula) :- ursula_statement.
is_knave(ursula) :- ursula_statement_false.

% Victor says: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_statement :- N = #count{P : (P=alice; P=bob; P=charlie; P=diana), is_knave(P)}, N = 2.
victor_statement_false :- N = #count{P : (P=alice; P=bob; P=charlie; P=diana), is_knave(P)}, N != 2.
is_knight(victor) :- victor_statement.
is_knave(victor) :- victor_statement_false.

% Wendy says: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_statement :- is_knave(victor), is_knave(ursula), is_knight(xavier).
wendy_statement_false :- not (is_knave(victor) and is_knave(ursula) and is_knight(xavier)).
is_knight(wendy) :- wendy_statement.
is_knave(wendy) :- wendy_statement_false.

% Xavier says: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_statement :- knights_in_c(4), is_knight(sam).
xavier_statement_false :- not (knights_in_c(4) and is_knight(sam)).
is_knight(xavier) :- xavier_statement.
is_knave(xavier) :- xavier_statement_false.

% ===== OUTPUT =====
#show is_type/2.
#show knights_in_a/1.
#show knights_in_b/1.
#show knights_in_c/1.
#show total_knights/1.