% --- Data ---
user("u1", 250, "influencer", 10).
user("u2", 80, "regular", 60).
user("u3", 70, "regular", 90).
user("u4", 150, "expert", 100).
user("u5", 90, "regular", 70).
user("u6", 200, "influencer", 120).
user("u7", 300, "influencer", 10).
user("u8", 110, "regular", 40).
user("u9", 60, "regular", 80).
user("u10", 220, "expert", 150).
user("u11", 50, "regular", 50).
user("u12", 130, "regular", 90).
user("u13", 280, "influencer", 10).
user("u14", 85, "regular", 60).
user("u15", 180, "expert", 10).
user("u16", 95, "regular", 50).
user("u17", 40, "regular", 100).
user("u18", 190, "expert", 110).
user("u19", 210, "influencer", 130).
user("u20", 75, "regular", 70).
user("u21", 100, "expert", 80).
user("u22", 120, "regular", 10).
user("u23", 140, "regular", 120).
user("u24", 160, "expert", 90).
user("u25", 240, "influencer", 10).

connection("u1", "u2", 70).
connection("u1", "u5", 50).
connection("u7", "u8", 50).
connection("u7", "u9", 30).
connection("u15", "u16", 60).
connection("u22", "u5", 30).
connection("u2", "u3", 40).
connection("u8", "u3", 50).
connection("u8", "u9", 60).

budget(1000, 600).
max_seeds(5).
key_user("u4").

% --- Logic ---
time(0..25).

{ seed(U) } :- user(U, _, _, _).

% Constraints
:- #count { U : seed(U) } > 5.
:- #sum { C, U : seed(U), user(U, C, _, _) } > 1000.
:- #sum { C, U : seed(U), user(U, C, "influencer", _) } > 600.
:- not #count { U : seed(U), user(U, _, "expert", _) } >= 1.

% Cascade
activated(U, 0) :- seed(U).
activated(U, T+1) :- activated(U, T), time(T+1).
activated(V, T+1) :- not activated(V, T), user(V, _, _, Threshold), 
                     Sum = #sum { S, U : connection(U, V, S), activated(U, T) }, 
                     Sum >= Threshold, time(T+1).

activated_final(U) :- activated(U, 25).

% Scoring
score_activated(N) :- N = #count { U : activated_final(U) }.
score_key(50) :- activated_final("u4").
score_key(0) :- not activated_final("u4").

final_score(S) :- score_activated(N), score_key(K), S = 10 * N + K.

#maximize { S : final_score(S) }.

#show seed/1.
#show activated_final/1.
#show final_score/1.