% Domains
inhabitant(alice; bob; charlie; diana; ethan; fiona; george; hannah;
           ian; julia; kevin; lily; mason; nina; oliver; paula;
           quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

% Groups
group(alice, a). group(bob, a). group(charlie, a). group(diana, a).
group(ethan, a). group(fiona, a). group(george, a). group(hannah, a).
group(ian, b). group(julia, b). group(kevin, b). group(lily, b).
group(mason, b). group(nina, b). group(oliver, b). group(paula, b).
group(quentin, c). group(rachel, c). group(sam, c). group(tina, c).
group(ursula, c). group(victor, c). group(wendy, c). group(xavier, c).

% Choice rule: Assign each person as a knight or knave
{ knight(P) ; knave(P) } = 1 :- inhabitant(P).

% Ensure each person is exactly one type
:- knight(P), knave(P).
:- not knight(P), not knave(P).

% Helper: Count knights in a group
group_knights(G, N) :- N = #count{ P : knight(P), group(P, G) }.

% Helper for counting knights in a subset of Group A
knight_in_subset_a(P) :- knight(P), group(P, a).
subset_knights_a(N) :- N = #count{ P : knight_in_subset_a(P) }.

% Helper for counting knights in Group B
subset_knights_b(N) :- N = #count{ P : knight(P), group(P, b) }.

% Helper for counting knights in Group C
subset_knights_c(N) :- N = #count{ P : knight(P), group(P, c) }.

% Statements
% Group A
says(alice, alice_statement).
says(bob, bob_statement).
says(charlie, charlie_statement).
says(diana, diana_statement).
says(ethan, ethan_statement).
says(fiona, fiona_statement).
says(george, george_statement).
says(hannah, hannah_statement).

% Group B
says(ian, ian_statement).
says(julia, julia_statement).
says(kevin, kevin_statement).
says(lily, lily_statement).
says(mason, mason_statement).
says(nina, nina_statement).
says(oliver, oliver_statement).
says(paula, paula_statement).

% Group C
says(quentin, quentin_statement).
says(rachel, rachel_statement).
says(sam, sam_statement).
says(tina, tina_statement).
says(ursula, ursula_statement).
says(victor, victor_statement).
says(wendy, wendy_statement).
says(xavier, xavier_statement).

% Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
:- knight(alice), not knave(hannah).
:- knight(alice), not (knave(bob) ; knight(charlie)).
:- knight(alice), subset_knights_a != 4.
:- knave(alice), knave(hannah).
:- knave(alice), knight(bob), knave(charlie).
:- knave(alice), subset_knights_a == 4.

% Bob: "Diana is the same type as me."
same_type(D, B) :- knight(D), knight(B).
same_type(D, B) :- knave(D), knave(B).
:- knight(bob), not same_type(diana, bob).
:- knave(bob), same_type(diana, bob).

% Charlie: "Exactly twelve of us are knights."
:- knight(charlie), group_knights(a, K), group_knights(b, L), group_knights(c, M), K+L+M != 12.
:- knave(charlie), group_knights(a, K), group_knights(b, L), group_knights(c, M), K+L+M == 12.

% Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
different_type(E, F) :- knight(E), knave(F).
different_type(E, F) :- knave(E), knight(F).
:- knight(diana), not different_type(ethan, fiona).
:- knight(diana), knight(hannah).
:- knave(diana), different_type(ethan, fiona).
:- knave(diana), not knave(hannah).

% Ethan: "George is a knight if and only if Alice is a knight."
:- knight(ethan), knight(george), knave(alice).
:- knight(ethan), knave(george), knight(alice).
:- knave(ethan), knight(george), knight(alice).
:- knave(ethan), knave(george), knave(alice).

% Fiona: "Bob and Charlie are of different types, and I am a knight."
:- knight(fiona), not different_type(bob, charlie).
:- knight(fiona), knave(fiona).
:- knave(fiona), different_type(bob, charlie).
:- knave(fiona), knight(fiona).

% George: "Alice and Hannah are of the same type."
same_type(A, H) :- knight(A), knight(H).
same_type(A, H) :- knave(A), knave(H).
:- knight(george), not same_type(alice, hannah).
:- knave(george), same_type(alice, hannah).

% Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
:- knight(hannah), #count{ P : knight(P), P=bob ; P=charlie ; P=diana } != 1.
:- knave(hannah), #count{ P : knight(P), P=bob ; P=charlie ; P=diana } == 1.

% Group B statements
% Ian: "Alice and Paula are of the same type, and Julia is a knave."
same_type(A, P) :- knight(A), knight(P).
same_type(A, P) :- knave(A), knave(P).
:- knight(ian), not same_type(alice, paula).
:- knight(ian), knight(julia).
:- knave(ian), same_type(alice, paula), not knave(julia).

% Julia: "Kevin is a knight and Nina is a knight."
:- knight(julia), knave(kevin).
:- knight(julia), knave(nina).
:- knave(julia), knight(kevin), knight(nina).

% Kevin: "Either Oliver is a knight or Lily is a knave."
:- knight(kevin), knave(oliver), knight(lily).
:- knave(kevin), knight(oliver), knave(lily).

% Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
:- knight(lily), subset_knights_b != 4.
:- knight(lily), knight(oliver).
:- knave(lily), subset_knights_b == 4.
:- knave(lily), not knave(oliver).

% Mason: "Bob and Ethan are of the same type, and Julia is a knave."
same_type(B, E) :- knight(B), knight(E).
same_type(B, E) :- knave(B), knave(E).
:- knight(mason), not same_type(bob, ethan).
:- knight(mason), knight(julia).
:- knave(mason), same_type(bob, ethan), not knave(julia).

% Nina: "Ian and Paula are of different types."
different_type(I, P) :- knight(I), knave(P).
different_type(I, P) :- knave(I), knight(P).
:- knight(nina), not different_type(ian, paula).
:- knave(nina), different_type(ian, paula).

% Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
:- knight(oliver), #count{ P : knight(P), P=george ; P=hannah ; P=ian ; P=julia } != 2.
:- knave(oliver), #count{ P : knight(P), P=george ; P=hannah ; P=ian ; P=julia } == 2.

% Paula: "Rachel is a knight if and only if Quentin is a knave."
:- knight(paula), knight(rachel), knight(quentin).
:- knight(paula), knave(rachel), knave(quentin).
:- knave(paula), knight(rachel), knave(quentin).
:- knave(paula), knave(rachel), knight(quentin).

% Group C statements
% Quentin: "At least five of us in Group C are knights."
:- knight(quentin), subset_knights_c < 5.
:- knave(quentin), subset_knights_c >= 5.

% Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
:- knight(rachel), knave(charlie).
:- knight(rachel), knave(lily).
:- knight(rachel), knight(victor).
:- knave(rachel), knight(charlie), knight(lily), knave(victor).

% Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
:- knight(sam), knight(tina).
:- knight(sam), knight(oliver).
:- knight(sam), knight(ursula).
:- knave(sam), knave(tina), knave(oliver), knave(ursula).

% Tina: "Rachel is a knave or Mason is a knave."
:- knight(tina), knight(rachel), knight(mason).
:- knave(tina), not (knave(rachel) ; knave(mason)).

% Ursula: "Ian and Julia are both knights."
:- knight(ursula), knave(ian).
:- knight(ursula), knave(julia).
:- knave(ursula), knight(ian), knight(julia).

% Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
:- knight(victor), #count{ P : knave(P), P=alice ; P=bob ; P=charlie ; P=diana } != 2.
:- knave(victor), #count{ P : knave(P), P=alice ; P=bob ; P=charlie ; P=diana } == 2.

% Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
:- knight(wendy), knight(victor).
:- knight(wendy), knight(ursula).
:- knight(wendy), knave(xavier).
:- knave(wendy), knave(victor), knave(ursula), knight(xavier).

% Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
:- knight(xavier), subset_knights_c != 4.
:- knight(xavier), knave(sam).
:- knave(xavier), subset_knights_c == 4.
:- knave(xavier), knight(sam).

% Show the assignment
#show knight/1.
#show knave/1.