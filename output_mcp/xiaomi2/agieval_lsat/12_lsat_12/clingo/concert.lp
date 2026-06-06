% Compositions
comp(f). comp(h). comp(l). comp(o). comp(p). comp(r). comp(s). comp(t).

% Positions
pos(1..8).

% Define each option as facts: at(Option, Composition, Position)
% Option A: L, P, S, R, O, T, F, H
at(a,l,1). at(a,p,2). at(a,s,3). at(a,r,4). at(a,o,5). at(a,t,6). at(a,f,7). at(a,h,8).

% Option B: O, T, P, F, S, H, R, L
at(b,o,1). at(b,t,2). at(b,p,3). at(b,f,4). at(b,s,5). at(b,h,6). at(b,r,7). at(b,l,8).

% Option C: P, T, F, S, L, R, O, H
at(c,p,1). at(c,t,2). at(c,f,3). at(c,s,4). at(c,l,5). at(c,r,6). at(c,o,7). at(c,h,8).

% Option D: P, T, F, S, O, R, L, H
at(d,p,1). at(d,t,2). at(d,f,3). at(d,s,4). at(d,o,5). at(d,r,6). at(d,l,7). at(d,h,8).

% Option E: T, F, P, R, O, L, S, H
at(e,t,1). at(e,f,2). at(e,p,3). at(e,r,4). at(e,o,5). at(e,l,6). at(e,s,7). at(e,h,8).

% Each option has exactly 8 compositions in positions 1-8 (verified by facts above)

% Helper: position of a composition in an option
pos_of(Opt, Comp, P) :- at(Opt, Comp, P).

% Constraint 1: T is performed either immediately before F or immediately after R
% "immediately before F" means T's position = F's position - 1
% "immediately after R" means T's position = R's position + 1
c1(Opt) :- pos_of(Opt, t, PT), pos_of(Opt, f, PF), PT = PF - 1.
c1(Opt) :- pos_of(Opt, t, PT), pos_of(Opt, r, PR), PT = PR + 1.

% Constraint 2: At least two compositions are performed either after F and before R,
% or after R and before F.
% Count compositions between F and R (exclusive)
between(Opt, C) :- pos_of(Opt, f, PF), pos_of(Opt, r, PR), pos_of(Opt, C, PC),
                   comp(C), C != f, C != r,
                   PF < PR, PC > PF, PC < PR.
between(Opt, C) :- pos_of(Opt, f, PF), pos_of(Opt, r, PR), pos_of(Opt, C, PC),
                   comp(C), C != f, C != r,
                   PR < PF, PC > PR, PC < PF.
count_between(Opt, N) :- N = #count{C : between(Opt, C)}, option(Opt).
c2(Opt) :- count_between(Opt, N), N >= 2.

% Constraint 3: O is performed either first or fifth
c3(Opt) :- pos_of(Opt, o, 1).
c3(Opt) :- pos_of(Opt, o, 5).

% Constraint 4: The eighth composition is either L or H
c4(Opt) :- pos_of(Opt, l, 8).
c4(Opt) :- pos_of(Opt, h, 8).

% Constraint 5: P is performed at some time before S
c5(Opt) :- pos_of(Opt, p, PP), pos_of(Opt, s, PS), PP < PS.

% Constraint 6: At least one composition is performed either after O and before S,
% or after S and before O.
between_os(Opt, C) :- pos_of(Opt, o, PO), pos_of(Opt, s, PS), pos_of(Opt, C, PC),
                      comp(C), C != o, C != s,
                      PO < PS, PC > PO, PC < PS.
between_os(Opt, C) :- pos_of(Opt, o, PO), pos_of(Opt, s, PS), pos_of(Opt, C, PC),
                      comp(C), C != o, C != s,
                      PS < PO, PC > PS, PC < PO.
c6(Opt) :- between_os(Opt, _).

% An option is valid if all constraints hold
valid(Opt) :- c1(Opt), c2(Opt), c3(Opt), c4(Opt), c5(Opt), c6(Opt).

% Map to options
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

#show option/1.