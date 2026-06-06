% Inhabitants
groupA(alice; bob; charlie; diana; ethan; fiona; george; hannah).
groupB(ian; julia; kevin; lily; mason; nina; oliver; paula).
groupC(quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

person(P) :- groupA(P).
person(P) :- groupB(P).
person(P) :- groupC(P).

% Each person is either a knight or a knave
{is_knight(P)} :- person(P).
is_knave(P) :- person(P), not is_knight(P).

% Helper for equality
same_type(P1, P2) :- is_knight(P1), is_knight(P2).
same_type(P1, P2) :- is_knave(P1), is_knave(P2).

% Statements
% Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
countA(N) :- N = #count{P : groupA(P), is_knight(P)}.
alice_stmt :- is_knave(hannah), (is_knave(bob) ; is_knight(charlie)), countA(4).
is_knight(alice) :- alice_stmt.
is_knave(alice) :- not alice_stmt.

% Bob: "Diana is the same type as me."
bob_stmt :- same_type(diana, bob).
is_knight(bob) :- bob_stmt.
is_knave(bob) :- not bob_stmt.

% Charlie: "Exactly twelve of us are knights."
countAll(N) :- N = #count{P : is_knight(P)}.
charlie_stmt :- countAll(12).
is_knight(charlie) :- charlie_stmt.
is_knave(charlie) :- not charlie_stmt.

% Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_stmt :- not same_type(ethan, fiona), is_knave(hannah).
is_knight(diana) :- diana_stmt.
is_knave(diana) :- not diana_stmt.

% Ethan: "George is a knight if and only if Alice is a knight."
ethan_stmt :- is_knight(george) == is_knight(alice).
is_knight(ethan) :- ethan_stmt.
is_knave(ethan) :- not ethan_stmt.

% Fiona: "Bob and Charlie are of different types, and I am a knight."
fiona_stmt :- not same_type(bob, charlie), is_knight(fiona).
is_knight(fiona) :- fiona_stmt.
is_knave(fiona) :- not fiona_stmt.

% George: "Alice and Hannah are of the same type."
george_stmt :- same_type(alice, hannah).
is_knight(george) :- george_stmt.
is_knave(george) :- not george_stmt.

% Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_stmt :- #count{P : P=bob, is_knight(P); P=charlie, is_knight(P); P=diana, is_knight(P)} = 1.
is_knight(hannah) :- hannah_stmt.
is_knave(hannah) :- not hannah_stmt.

% Ian: "Alice and Paula are of the same type, and Julia is a knave."
ian_stmt :- same_type(alice, paula), is_knave(julia).
is_knight(ian) :- ian_stmt.
is_knave(ian) :- not ian_stmt.

% Julia: "Kevin is a knight and Nina is a knight."
julia_stmt :- is_knight(kevin), is_knight(nina).
is_knight(julia) :- julia_stmt.
is_knave(julia) :- not julia_stmt.

% Kevin: "Either Oliver is a knight or Lily is a knave."
kevin_stmt :- is_knight(oliver) ; is_knave(lily).
is_knight(kevin) :- kevin_stmt.
is_knave(kevin) :- not kevin_stmt.

% Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
countB(N) :- N = #count{P : groupB(P), is_knight(P)}.
lily_stmt :- countB(4), is_knave(oliver).
is_knight(lily) :- lily_stmt.
is_knave(lily) :- not lily_stmt.

% Mason: "Bob and Ethan are of the same type, and Julia is a knave."
mason_stmt :- same_type(bob, ethan), is_knave(julia).
is_knight(mason) :- mason_stmt.
is_knave(mason) :- not mason_stmt.

% Nina: "Ian and Paula are of different types."
nina_stmt :- not same_type(ian, paula).
is_knight(nina) :- nina_stmt.
is_knave(nina) :- not nina_stmt.

% Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_stmt :- #count{P : P=george, is_knight(P); P=hannah, is_knight(P); P=ian, is_knight(P); P=julia, is_knight(P)} = 2.
is_knight(oliver) :- oliver_stmt.
is_knave(oliver) :- not oliver_stmt.

% Paula: "Rachel is a knight if and only if Quentin is a knave."
paula_stmt :- is_knight(rachel) == is_knave(quentin).
is_knight(paula) :- paula_stmt.
is_knave(paula) :- not paula_stmt.

% Quentin: "At least five of us in Group C are knights."
countC(N) :- N = #count{P : groupC(P), is_knight(P)}.
quentin_stmt :- countC(N), N >= 5.
is_knight(quentin) :- quentin_stmt.
is_knave(quentin) :- not quentin_stmt.

% Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_stmt :- is_knight(charlie), is_knight(lily), is_knave(victor).
is_knight(rachel) :- rachel_stmt.
is_knave(rachel) :- not rachel_stmt.

% Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_stmt :- is_knave(tina), is_knave(oliver), is_knave(ursula).
is_knight(sam) :- sam_stmt.
is_knave(sam) :- not sam_stmt.

% Tina: "Rachel is a knave or Mason is a knave."
tina_stmt :- is_knave(rachel) ; is_knave(mason).
is_knight(tina) :- tina_stmt.
is_knave(tina) :- not tina_stmt.

% Ursula: "Ian and Julia are both knights."
ursula_stmt :- is_knight(ian), is_knight(julia).
is_knight(ursula) :- ursula_stmt.
is_knave(ursula) :- not ursula_stmt.

% Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_stmt :- #count{P : P=alice, is_knave(P); P=bob, is_knave(P); P=charlie, is_knave(P); P=diana, is_knave(P)} = 2.
is_knight(victor) :- victor_stmt.
is_knave(victor) :- not victor_stmt.

% Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_stmt :- is_knave(victor), is_knave(ursula), is_knight(xavier).
is_knight(wendy) :- wendy_stmt.
is_knave(wendy) :- not wendy_stmt.

% Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_stmt :- countC(4), is_knight(sam).
is_knight(xavier) :- xavier_stmt.
is_knave(xavier) :- not xavier_stmt.

#show is_knight/1.
#show is_knave/1.