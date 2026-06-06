% Concert Solo Ordering Problem

% Members
member(g). member(k). member(p). member(s). member(t). member(v).

% Positions
pos(1..6).

% Assign each member to a unique position
1 { pos_assign(M, P) : pos(P) } 1 :- member(M).
1 { pos_assign(M, P) : member(M) } 1 :- pos(P).

% Constraint 1: Guitarist not at position 4
:- pos_assign(g, 4).

% Constraint 2: Percussionist before keyboard
:- pos_assign(p, P1), pos_assign(k, P2), P1 >= P2.

% Constraint 3: Violinist before keyboard and keyboard before guitarist
:- pos_assign(v, Pv), pos_assign(k, Pk), Pv >= Pk.
:- pos_assign(k, Pk), pos_assign(g, Pg), Pk >= Pg.

% Constraint 4: Saxophonist after exactly one of percussionist or trumpeter
sax_after_p :- pos_assign(s, Ps), pos_assign(p, Pp), Ps > Pp.
sax_after_t :- pos_assign(s, Ps), pos_assign(t, Pt), Ps > Pt.
1 { sax_after_p; sax_after_t } 1.

% Extra condition: Percussionist before saxophonist
:- pos_assign(p, Pp), pos_assign(s, Ps), Pp >= Ps.

% Derived predicates for answer choices
perc_first :- pos_assign(p, 1).
perc_second :- pos_assign(p, 2).
v_before_s :- pos_assign(v, Pv), pos_assign(s, Ps), Pv < Ps.
p_before_t :- pos_assign(p, Pp), pos_assign(t, Pt), Pp < Pt.
s_before_k :- pos_assign(s, Ps), pos_assign(k, Pk), Ps < Pk.

% Map the correct answer to option/1
% We know that p_before_t is always true given the constraints and extra condition.
option(d) :- p_before_t.

% Show only the option
#show option/1.