% Define the inhabitants
inhabitant(alice; bob; charlie; diana; ethan; fiona; george; hannah).
inhabitant(ian; julia; kevin; lily; mason; nina; oliver; paula).
inhabitant(quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

% Define groups
group_a(alice; bob; charlie; diana; ethan; fiona; george; hannah).
group_b(ian; julia; kevin; lily; mason; nina; oliver; paula).
group_c(quentin; rachel; sam; tina; ursula; victor; wendy; xavier).

% Each person is either a knight or knave
1 { type(P, knight) ; type(P, knave) } 1 :- inhabitant(P).

% Helper to check if someone is a knight or knave
is_knight(P) :- type(P, knight).
is_knave(P) :- type(P, knave).

% Total number of knights in the entire population
num_knights(N) :- N = #count { P : is_knight(P) }.

% Total number of knights in Group A
num_knights_a(N) :- N = #count { P : is_knight(P), group_a(P) }.

% Total number of knights in Group B
num_knights_b(N) :- N = #count { P : is_knight(P), group_b(P) }.

% Total number of knights in Group C
num_knights_c(N) :- N = #count { P : is_knight(P), group_c(P) }.


% ========== Group A Statements ==========

% Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
% If Alice is a knight, her statement must be true
:- is_knight(alice), not is_knave(hannah).
:- is_knight(alice), not (is_knave(bob) ; is_knight(charlie)).
:- is_knight(alice), num_knights_a != 4.

% If Alice is a knave, her statement must be false
:- is_knave(alice), is_knave(hannah), (is_knight(bob) ; not is_knight(charlie)), num_knights_a = 4.


% Bob: "Diana is the same type as me."
% If Bob is a knight, his statement must be true
:- is_knight(bob), type(bob, T), type(diana, T1), T != T1.

% If Bob is a knave, his statement must be false
:- is_knave(bob), type(bob, T), type(diana, T1), T = T1.


% Charlie: "Exactly twelve of us are knights."
% If Charlie is a knight, his statement must be true
:- is_knight(charlie), num_knights != 12.

% If Charlie is a knave, his statement must be false
:- is_knave(charlie), num_knights = 12.


% Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
% If Diana is a knight, her statement must be true
:- is_knight(diana), not ((is_knight(ethan), is_knave(fiona)) ; (is_knave(ethan), is_knight(fiona))).
:- is_knight(diana), not is_knave(hannah).

% If Diana is a knave, her statement must be false
:- is_knave(diana), ((is_knight(ethan), is_knight(fiona)) ; (is_knave(ethan), is_knave(fiona))).
:- is_knave(diana), not is_knave(hannah).


% Ethan: "George is a knight if and only if Alice is a knight."
% If Ethan is a knight, his statement must be true
:- is_knight(ethan), not ((is_knight(george), is_knight(alice)) ; (is_knave(george), is_knave(alice))).

% If Ethan is a knave, his statement must be false
:- is_knave(ethan), ((is_knight(george), is_knight(alice)) ; (is_knave(george), is_knave(alice))).


% Fiona: "Bob and Charlie are of different types, and I am a knight."
% If Fiona is a knight, her statement must be true
:- is_knight(fiona), not (type(bob, T), type(charlie, T1), T != T1).
:- is_knight(fiona), not is_knight(fiona).

% If Fiona is a knave, her statement must be false
:- is_knave(fiona), type(bob, T), type(charlie, T1), T != T1.
:- is_knave(fiona), is_knight(fiona).


% George: "Alice and Hannah are of the same type."
% If George is a knight, his statement must be true
:- is_knight(george), type(alice, T), type(hannah, T1), T != T1.

% If George is a knave, his statement must be false
:- is_knave(george), type(alice, T), type(hannah, T1), T = T1.


% Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
% If Hannah is a knight, her statement must be true
hannah_knight_count(N) :- N = #count { P : is_knight(P), P = bob }.
hannah_knight_count(N) :- N = #count { P : is_knight(P), P = charlie }.
hannah_knight_count(N) :- N = #count { P : is_knight(P), P = diana }.

:- is_knight(hannah), hannah_knight_count(N), N != 1.

% If Hannah is a knave, her statement must be false
:- is_knave(hannah), hannah_knight_count(N), N = 1.


% ========== Group B Statements ==========

% Ian: "Alice and Paula are of the same type, and Julia is a knave."
% If Ian is a knight, his statement must be true
:- is_knight(ian), type(alice, T), type(paula, T1), T != T1.
:- is_knight(ian), not is_knave(julia).

% If Ian is a knave, his statement must be false
:- is_knave(ian), type(alice, T), type(paula, T1), T = T1.
:- is_knave(ian), is_knight(julia).


% Julia: "Kevin is a knight and Nina is a knight."
% If Julia is a knight, her statement must be true
:- is_knight(julia), not is_knight(kevin).
:- is_knight(julia), not is_knight(nina).

% If Julia is a knave, her statement must be false
:- is_knave(julia), is_knight(kevin), is_knight(nina).


% Kevin: "Either Oliver is a knight or Lily is a knave."
% If Kevin is a knight, his statement must be true
:- is_knight(kevin), not is_knight(oliver), not is_knave(lily).

% If Kevin is a knave, his statement must be false
:- is_knave(kevin), is_knight(oliver), is_knave(lily).


% Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
% If Lily is a knight, her statement must be true
:- is_knight(lily), num_knights_b != 4.
:- is_knight(lily), not is_knave(oliver).

% If Lily is a knave, her statement must be false
:- is_knave(lily), num_knights_b = 4.
:- is_knave(lily), is_knave(oliver).


% Mason: "Bob and Ethan are of the same type, and Julia is a knave."
% If Mason is a knight, his statement must be true
:- is_knight(mason), type(bob, T), type(ethan, T1), T != T1.
:- is_knight(mason), not is_knave(julia).

% If Mason is a knave, his statement must be false
:- is_knave(mason), type(bob, T), type(ethan, T1), T = T1.
:- is_knave(mason), is_knight(julia).


% Nina: "Ian and Paula are of different types."
% If Nina is a knight, her statement must be true
:- is_knight(nina), type(ian, T), type(paula, T1), T = T1.

% If Nina is a knave, her statement must be false
:- is_knave(nina), type(ian, T), type(paula, T1), T != T1.


% Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_knight_count(N) :- N = #count { P : is_knight(P), P = george }.
oliver_knight_count(N) :- N = #count { P : is_knight(P), P = hannah }.
oliver_knight_count(N) :- N = #count { P : is_knight(P), P = ian }.
oliver_knight_count(N) :- N = #count { P : is_knight(P), P = julia }.

% If Oliver is a knight, his statement must be true
:- is_knight(oliver), oliver_knight_count(N), N != 2.

% If Oliver is a knave, his statement must be false
:- is_knave(oliver), oliver_knight_count(N), N = 2.


% Paula: "Rachel is a knight if and only if Quentin is a knave."
% If Paula is a knight, her statement must be true
:- is_knight(paula), not ((is_knight(rachel), is_knave(quentin)) ; (is_knave(rachel), is_knight(quentin))).

% If Paula is a knave, her statement must be false
:- is_knave(paula), ((is_knight(rachel), is_knave(quentin)) ; (is_knave(rachel), is_knight(quentin))).


% ========== Group C Statements ==========

% Quentin: "At least five of us in Group C are knights."
% If Quentin is a knight, his statement must be true
:- is_knight(quentin), num_knights_c < 5.

% If Quentin is a knave, his statement must be false
:- is_knave(quentin), num_knights_c >= 5.


% Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
% If Rachel is a knight, her statement must be true
:- is_knight(rachel), not is_knight(charlie).
:- is_knight(rachel), not is_knight(lily).
:- is_knight(rachel), not is_knave(victor).

% If Rachel is a knave, her statement must be false
:- is_knave(rachel), is_knight(charlie), is_knight(lily), is_knave(victor).


% Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
% If Sam is a knight, his statement must be true
:- is_knight(sam), not is_knave(tina).
:- is_knight(sam), not is_knave(oliver).
:- is_knight(sam), not is_knave(ursula).

% If Sam is a knave, his statement must be false
:- is_knave(sam), is_knave(tina), is_knave(oliver), is_knave(ursula).


% Tina: "Rachel is a knave or Mason is a knave."
% If Tina is a knight, her statement must be true
:- is_knight(tina), not is_knave(rachel), not is_knave(mason).

% If Tina is a knave, her statement must be false
:- is_knave(tina), is_knave(rachel), is_knave(mason).


% Ursula: "Ian and Julia are both knights."
% If Ursula is a knight, her statement must be true
:- is_knight(ursula), not is_knight(ian).
:- is_knight(ursula), not is_knight(julia).

% If Ursula is a knave, her statement must be false
:- is_knave(ursula), is_knight(ian), is_knight(julia).


% Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
victor_knave_count(N) :- N = #count { P : is_knave(P), group_a(P), P = alice }.
victor_knave_count(N) :- N = #count { P : is_knave(P), group_a(P), P = bob }.
victor_knave_count(N) :- N = #count { P : is_knave(P), group_a(P), P = charlie }.
victor_knave_count(N) :- N = #count { P : is_knave(P), group_a(P), P = diana }.

% If Victor is a knight, his statement must be true
:- is_knight(victor), victor_knave_count(N), N != 2.

% If Victor is a knave, his statement must be false
:- is_knave(victor), victor_knave_count(N), N = 2.


% Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
% If Wendy is a knight, her statement must be true
:- is_knight(wendy), not is_knave(victor).
:- is_knight(wendy), not is_knave(ursula).
:- is_knight(wendy), not is_knight(xavier).

% If Wendy is a knave, her statement must be false
:- is_knave(wendy), is_knave(victor), is_knave(ursula), is_knight(xavier).


% Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
% If Xavier is a knight, his statement must be true
:- is_knight(xavier), num_knights_c != 4.
:- is_knight(xavier), not is_knight(sam).

% If Xavier is a knave, his statement must be false
:- is_knave(xavier), num_knights_c = 4.
:- is_knave(xavier), is_knight(sam).


% Show the solution
#show type/2.