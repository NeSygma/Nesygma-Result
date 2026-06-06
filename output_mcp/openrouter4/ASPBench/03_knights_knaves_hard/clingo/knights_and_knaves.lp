% --- Domain Definitions ---
% People
person(alice; bob; charlie; diana; ethan; fiona; george; hannah).
person(ian; julia; kevin; lily; mason; nina; oliver; paula).
person(quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

% Groups
group(alice; bob; charlie; diana; ethan; fiona; george; hannah, a).
group(ian; julia; kevin; lily; mason; nina; oliver; paula, b).
group(quentin; rachel; sam; tina; ursula; victor; wendy; xavier, c).

% Each person is exactly one type: knight or knave
1 { type(P, "knight"); type(P, "knave") } 1 :- person(P).

% --- Counts ---
total_knights(N) :- N = #count { P : type(P, "knight") }.
groupA_knights(N) :- N = #count { P : group(P, a), type(P, "knight") }.
groupB_knights(N) :- N = #count { P : group(P, b), type(P, "knight") }.
groupC_knights(N) :- N = #count { P : group(P, c), type(P, "knight") }.

% --- Type comparison helpers ---
same_type(P1, P2) :- type(P1, T), type(P2, T).
diff_type(P1, P2) :- type(P1, "knight"), type(P2, "knave").
diff_type(P1, P2) :- type(P1, "knave"), type(P2, "knight").

% --- Statement truth conditions ---

% Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
alice_or_cond :- type(bob, "knave").
alice_or_cond :- type(charlie, "knight").
statement_true(alice) :- type(hannah, "knave"), alice_or_cond, groupA_knights(4).

% Bob: "Diana is the same type as me."
statement_true(bob) :- same_type(diana, bob).

% Charlie: "Exactly twelve of us are knights."
statement_true(charlie) :- total_knights(12).

% Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
statement_true(diana) :- diff_type(ethan, fiona), type(hannah, "knave").

% Ethan: "George is a knight if and only if Alice is a knight."
statement_true(ethan) :- type(george, "knight"), type(alice, "knight").
statement_true(ethan) :- type(george, "knave"), type(alice, "knave").

% Fiona: "Bob and Charlie are of different types, and I am a knight."
statement_true(fiona) :- diff_type(bob, charlie), type(fiona, "knight").

% George: "Alice and Hannah are of the same type."
statement_true(george) :- same_type(alice, hannah).

% Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
statement_true(hannah) :- 1 = #count { 1,bob : type(bob, "knight"); 2,charlie : type(charlie, "knight"); 3,diana : type(diana, "knight") }.

% Ian: "Alice and Paula are of the same type, and Julia is a knave."
statement_true(ian) :- same_type(alice, paula), type(julia, "knave").

% Julia: "Kevin is a knight and Nina is a knight."
statement_true(julia) :- type(kevin, "knight"), type(nina, "knight").

% Kevin: "Either Oliver is a knight or Lily is a knave."
statement_true(kevin) :- type(oliver, "knight").
statement_true(kevin) :- type(lily, "knave").

% Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
statement_true(lily) :- groupB_knights(4), type(oliver, "knave").

% Mason: "Bob and Ethan are of the same type, and Julia is a knave."
statement_true(mason) :- same_type(bob, ethan), type(julia, "knave").

% Nina: "Ian and Paula are of different types."
statement_true(nina) :- diff_type(ian, paula).

% Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
statement_true(oliver) :- 2 = #count { 1,george : type(george, "knight"); 2,hannah : type(hannah, "knight"); 3,ian : type(ian, "knight"); 4,julia : type(julia, "knight") }.

% Paula: "Rachel is a knight if and only if Quentin is a knave."
statement_true(paula) :- type(rachel, "knight"), type(quentin, "knave").
statement_true(paula) :- type(rachel, "knave"), type(quentin, "knight").

% Quentin: "At least five of us in Group C are knights."
statement_true(quentin) :- groupC_knights(N), N >= 5.

% Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
statement_true(rachel) :- type(charlie, "knight"), type(lily, "knight"), type(victor, "knave").

% Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
statement_true(sam) :- type(tina, "knave"), type(oliver, "knave"), type(ursula, "knave").

% Tina: "Rachel is a knave or Mason is a knave."
statement_true(tina) :- type(rachel, "knave").
statement_true(tina) :- type(mason, "knave").

% Ursula: "Ian and Julia are both knights."
statement_true(ursula) :- type(ian, "knight"), type(julia, "knight").

% Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
statement_true(victor) :- 2 = #count { 1,alice : type(alice, "knave"); 2,bob : type(bob, "knave"); 3,charlie : type(charlie, "knave"); 4,diana : type(diana, "knave") }.

% Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
statement_true(wendy) :- type(victor, "knave"), type(ursula, "knave"), type(xavier, "knight").

% Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
statement_true(xavier) :- groupC_knights(4), type(sam, "knight").

% --- Constraints: Knights tell truth, Knaves lie ---
:- type(P, "knight"), not statement_true(P).
:- type(P, "knave"), statement_true(P).

% --- Output ---
#show type/2.