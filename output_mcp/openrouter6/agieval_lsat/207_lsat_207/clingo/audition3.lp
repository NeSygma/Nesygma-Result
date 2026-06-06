% Audition problem - multiple choice equivalence
singer(kammer). singer(lugo). singer(trillo). singer(waite). singer(yoshida). singer(zinn).
recorded(kammer). recorded(lugo).
position(1..6).

% Generate all permutations
1 { pos(S, P) : position(P) } 1 :- singer(S).
1 { pos(S, P) : singer(S) } 1 :- position(P).

% Common constraints
recorded_at_4 :- pos(S,4), recorded(S).
has_recorded_at_5 :- pos(S,5), recorded(S).
:- recorded_at_4.
:- not has_recorded_at_5.
:- pos(kammer, Pk), pos(trillo, Pt), Pk >= Pt.
:- pos(zinn, Pz), pos(yoshida, Py), Pz >= Py.

% Original condition 3
original_condition3 :- pos(waite, Pw), pos(kammer, Pk), pos(lugo, Pl), Pw < Pk, Pw < Pl.

% Candidate A
earlier_than_waite(S) :- pos(S, Ps), pos(waite, Pw), Ps < Pw.
other_earlier(S) :- earlier_than_waite(S), S != zinn.
has_other_earlier :- other_earlier(S).
candidate_a :- pos(waite, _), not has_other_earlier.

% Common constraints satisfied
common_constraints_satisfied :-
    not recorded_at_4,
    has_recorded_at_5,
    pos(kammer, Pk), pos(trillo, Pt), Pk < Pt,
    pos(zinn, Pz), pos(yoshida, Py), Pz < Py.

% Equivalence constraints for candidate A
:- common_constraints_satisfied, original_condition3, not candidate_a.
:- common_constraints_satisfied, candidate_a, not original_condition3.

% Ensure there is at least one assignment that satisfies common constraints
has_common_solution :- common_constraints_satisfied.
:- not has_common_solution.

% Derive option(a) if there exists an assignment that satisfies common constraints and the equivalence constraints
solution :- common_constraints_satisfied, original_condition3, candidate_a.
option(a) :- solution.

#show option/1.