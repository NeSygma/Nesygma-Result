% --- Domain Facts ---
user("u1"). cost("u1",250). category("u1","influencer"). threshold("u1",10).
user("u2"). cost("u2",80). category("u2","regular"). threshold("u2",60).
user("u3"). cost("u3",70). category("u3","regular"). threshold("u3",90).
user("u4"). cost("u4",150). category("u4","expert"). threshold("u4",100).
user("u5"). cost("u5",90). category("u5","regular"). threshold("u5",70).
user("u6"). cost("u6",200). category("u6","influencer"). threshold("u6",120).
user("u7"). cost("u7",300). category("u7","influencer"). threshold("u7",10).
user("u8"). cost("u8",110). category("u8","regular"). threshold("u8",40).
user("u9"). cost("u9",60). category("u9","regular"). threshold("u9",80).
user("u10"). cost("u10",220). category("u10","expert"). threshold("u10",150).
user("u11"). cost("u11",50). category("u11","regular"). threshold("u11",50).
user("u12"). cost("u12",130). category("u12","regular"). threshold("u12",90).
user("u13"). cost("u13",280). category("u13","influencer"). threshold("u13",10).
user("u14"). cost("u14",85). category("u14","regular"). threshold("u14",60).
user("u15"). cost("u15",180). category("u15","expert"). threshold("u15",10).
user("u16"). cost("u16",95). category("u16","regular"). threshold("u16",50).
user("u17"). cost("u17",40). category("u17","regular"). threshold("u17",100).
user("u18"). cost("u18",190). category("u18","expert"). threshold("u18",110).
user("u19"). cost("u19",210). category("u19","influencer"). threshold("u19",130).
user("u20"). cost("u20",75). category("u20","regular"). threshold("u20",70).
user("u21"). cost("u21",100). category("u21","expert"). threshold("u21",80).
user("u22"). cost("u22",120). category("u22","regular"). threshold("u22",10).
user("u23"). cost("u23",140). category("u23","regular"). threshold("u23",120).
user("u24"). cost("u24",160). category("u24","expert"). threshold("u24",90).
user("u25"). cost("u25",240). category("u25","influencer"). threshold("u25",10).

% Connections
connection("u1","u2",70).
connection("u1","u5",50).
connection("u7","u8",50).
connection("u7","u9",30).
connection("u15","u16",60).
connection("u22","u5",30).
connection("u2","u3",40).
connection("u8","u3",50).
connection("u8","u9",60).

% Time horizon
time(0..25).

% --- Seed Selection ---
{ seed(U) } :- user(U).

% Constraints
:- #sum { C, U : seed(U), cost(U, C) } > 1000.
:- #count { U : seed(U) } > 5.
:- #count { U : seed(U), category(U, "expert") } < 1.
:- #sum { C, U : seed(U), category(U, "influencer"), cost(U, C) } > 600.

% --- Cascade Dynamics ---

% Step 0: Seeds are activated
activated(U, 0) :- seed(U).

% Persistence: if activated at T-1, still activated at T
activated(U, T) :- activated(U, T-1), time(T).

% New activation at step T if threshold is met by already-activated neighbors
activated(U, T) :- user(U), time(T), T > 0,
                   not activated(U, T-1),
                   threshold(U, Th),
                   #sum { Str, V : connection(V, U, Str), activated(V, T-1) } >= Th.

% Ultimately activated
final_activated(U) :- activated(U, T).

% Key user
key_activated :- final_activated("u4").

% --- Objective ---
activated_count(N) :- N = #count { U : final_activated(U) }.

score(S) :- activated_count(N), key_activated, S = N * 10 + 50.
score(S) :- activated_count(N), not key_activated, S = N * 10.

#maximize { S : score(S) }.

% --- Output ---
#show seed/1.
#show final_activated/1.
#show activated_count/1.
#show key_activated/0.
#show score/1.