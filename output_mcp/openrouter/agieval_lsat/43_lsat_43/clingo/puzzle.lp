% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Assign numeric ids for ordering
student_id(jiang,1). student_id(kramer,2). student_id(lopez,3). student_id(megregian,4). student_id(oneill,5).
less(X,Y) :- student_id(X,IX), student_id(Y,IY), IX < IY.

% Choice of reviews (any subset, possibly empty but we enforce at least one)
{review(S,P)} :- student(S), play(P).
% each student reviews at least one play
:- student(S), not reviewed_any(S).
reviewed_any(S) :- review(S,_).

% Count number of plays per student (safe)
count(S,N) :- student(S), N = #count{P : review(S,P)}.
% Kramer and Lopez review fewer plays than Megregian
:- count(kramer,N1), count(megregian,N2), N1 >= N2.
:- count(lopez,N1), count(megregian,N2), N1 >= N2.

% Lopez and Megregian share no play with Jiang
:- review(lopez,P), review(jiang,P).
:- review(megregian,P), review(jiang,P).

% Kramer and O'Neill both review Tamerlane (forced)
review(kramer,tamerlane).
review(oneill,tamerlane).

% Define difference between review sets
diff(S1,S2) :- student(S1), student(S2), S1 != S2, review(S1,P), not review(S2,P).
% Equality if no difference in either direction
eq(S1,S2) :- student(S1), student(S2), S1 != S2, not diff(S1,S2), not diff(S2,S1).
% Exactly one unordered pair of students have identical review sets
:- #count{S1,S2 : eq(S1,S2), less(S1,S2)} != 1.

% only_sunset predicate: reviews Sunset and nothing else
only_sunset(S) :- review(S,sunset), not review(S,tamerlane), not review(S,undulation).

% Options conditions
option(a) :- only_sunset(lopez), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(megregian), not only_sunset(oneill).
option(b) :- only_sunset(oneill), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(lopez), not only_sunset(megregian).
option(c) :- only_sunset(jiang), only_sunset(lopez), not only_sunset(kramer), not only_sunset(megregian), not only_sunset(oneill).
option(d) :- only_sunset(kramer), only_sunset(oneill), not only_sunset(jiang), not only_sunset(lopez), not only_sunset(megregian).
option(e) :- only_sunset(lopez), only_sunset(megregian), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(oneill).

#show option/1.