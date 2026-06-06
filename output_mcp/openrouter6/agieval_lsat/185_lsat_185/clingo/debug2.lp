% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Option A: leader Ruiz, members Taylor, Wells
leader_a(ruiz).
member_a(ruiz). % leader is also a member
member_a(taylor).
member_a(wells).

% Option B: leader Verma, members Quinn, Taylor
leader_b(verma).
member_b(verma).
member_b(quinn).
member_b(taylor).

% Option C: leader Verma, members Smith, Taylor
leader_c(verma).
member_c(verma).
member_c(smith).
member_c(taylor).

% Option D: leader Verma, members Smith, Xue
leader_d(verma).
member_d(verma).
member_d(smith).
member_d(xue).

% Option E: leader Xue, members Verma, Wells
leader_e(xue).
member_e(xue).
member_e(verma).
member_e(wells).

% Helper: count members for each option
count_a(N) :- N = #count{W : member_a(W)}.
count_b(N) :- N = #count{W : member_b(W)}.
count_c(N) :- N = #count{W : member_c(W)}.
count_d(N) :- N = #count{W : member_d(W)}.
count_e(N) :- N = #count{W : member_e(W)}.

% Check exactly three members
exact_three_a :- count_a(3).
exact_three_b :- count_b(3).
exact_three_c :- count_c(3).
exact_three_d :- count_d(3).
exact_three_e :- count_e(3).

% Check exactly one leader (should be true by construction)
% Check leader is a member
leader_is_member_a :- leader_a(L), member_a(L).
leader_is_member_b :- leader_b(L), member_b(L).
leader_is_member_c :- leader_c(L), member_c(L).
leader_is_member_d :- leader_d(L), member_d(L).
leader_is_member_e :- leader_e(L), member_e(L).

% Constraint: Quinn or Ruiz can be a project member only if leading the project.
% i.e., if member(quinn) then leader(quinn); if member(ruiz) then leader(ruiz)
constraint_quinn_ruiz_a :- (member_a(quinn) -> leader_a(quinn)) & (member_a(ruiz) -> leader_a(ruiz)).
% Actually, we need to check each option separately.
% For each option, if quinn is a member, then leader must be quinn.
% Similarly for ruiz.
constraint_quinn_a :- not (member_a(quinn) and not leader_a(quinn)).
constraint_ruiz_a :- not (member_a(ruiz) and not leader_a(ruiz)).
% Combine
constraint_quinn_ruiz_a :- constraint_quinn_a, constraint_ruiz_a.

% Similarly for other options
constraint_quinn_b :- not (member_b(quinn) and not leader_b(quinn)).
constraint_ruiz_b :- not (member_b(ruiz) and not leader_b(ruiz)).
constraint_quinn_ruiz_b :- constraint_quinn_b, constraint_ruiz_b.

constraint_quinn_c :- not (member_c(quinn) and not leader_c(quinn)).
constraint_ruiz_c :- not (member_c(ruiz) and not leader_c(ruiz)).
constraint_quinn_ruiz_c :- constraint_quinn_c, constraint_ruiz_c.

constraint_quinn_d :- not (member_d(quinn) and not leader_d(quinn)).
constraint_ruiz_d :- not (member_d(ruiz) and not leader_d(ruiz)).
constraint_quinn_ruiz_d :- constraint_quinn_d, constraint_ruiz_d.

constraint_quinn_e :- not (member_e(quinn) and not leader_e(quinn)).
constraint_ruiz_e :- not (member_e(ruiz) and not leader_e(ruiz)).
constraint_quinn_ruiz_e :- constraint_quinn_e, constraint_ruiz_e.

% Constraint: If Smith is a project member, Taylor must also be.
constraint_smith_taylor_a :- not (member_a(smith) and not member_a(taylor)).
constraint_smith_taylor_b :- not (member_b(smith) and not member_b(taylor)).
constraint_smith_taylor_c :- not (member_c(smith) and not member_c(taylor)).
constraint_smith_taylor_d :- not (member_d(smith) and not member_d(taylor)).
constraint_smith_taylor_e :- not (member_e(smith) and not member_e(taylor)).

% Constraint: If Wells is a project member, neither Ruiz nor Verma can be.
constraint_wells_a :- not (member_a(wells) and (member_a(ruiz) or member_a(verma))).
constraint_wells_b :- not (member_b(wells) and (member_b(ruiz) or member_b(verma))).
constraint_wells_c :- not (member_c(wells) and (member_c(ruiz) or member_c(verma))).
constraint_wells_d :- not (member_d(wells) and (member_d(ruiz) or member_d(verma))).
constraint_wells_e :- not (member_e(wells) and (member_e(ruiz) or member_e(verma))).

% Derive option if all constraints satisfied
option(a) :- exact_three_a, leader_is_member_a, constraint_quinn_ruiz_a, constraint_smith_taylor_a, constraint_wells_a.
option(b) :- exact_three_b, leader_is_member_b, constraint_quinn_ruiz_b, constraint_smith_taylor_b, constraint_wells_b.
option(c) :- exact_three_c, leader_is_member_c, constraint_quinn_ruiz_c, constraint_smith_taylor_c, constraint_wells_c.
option(d) :- exact_three_d, leader_is_member_d, constraint_quinn_ruiz_d, constraint_smith_taylor_d, constraint_wells_d.
option(e) :- exact_three_e, leader_is_member_e, constraint_quinn_ruiz_e, constraint_smith_taylor_e, constraint_wells_e.

#show option/1.