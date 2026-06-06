% Domains
accomplice(peters; quinn; rovero; stanton; tao; villas; white).
opt(a; b; c; d; e).

% Order facts for each option
% Option A
order(a, quinn, 1).
order(a, tao, 2).
order(a, stanton, 3).
order(a, peters, 4).
order(a, villas, 5).
order(a, white, 6).
order(a, rovero, 7).

% Option B
order(b, quinn, 1).
order(b, white, 2).
order(b, rovero, 3).
order(b, peters, 4).
order(b, stanton, 5).
order(b, villas, 6).
order(b, tao, 7).

% Option C
order(c, villas, 1).
order(c, white, 2).
order(c, quinn, 3).
order(c, stanton, 4).
order(c, peters, 5).
order(c, tao, 6).
order(c, rovero, 7).

% Option D
order(d, villas, 1).
order(d, white, 2).
order(d, stanton, 3).
order(d, peters, 4).
order(d, quinn, 5).
order(d, tao, 6).
order(d, rovero, 7).

% Option E
order(e, villas, 1).
order(e, white, 2).
order(e, stanton, 3).
order(e, peters, 4).
order(e, rovero, 5).
order(e, tao, 6).
order(e, quinn, 7).

% Constraint 1: Stanton not immediately before or after Tao
adjacent(O) :- order(O, stanton, P1), order(O, tao, P2), P1 = P2 + 1.
adjacent(O) :- order(O, stanton, P1), order(O, tao, P2), P2 = P1 + 1.
invalid(O) :- adjacent(O).

% Constraint 2: Quinn earlier than Rovero
invalid(O) :- order(O, quinn, P1), order(O, rovero, P2), P1 >= P2.

% Constraint 3: Villas immediately before White
immediate_before(O) :- order(O, villas, P1), order(O, white, P2), P2 = P1 + 1.
invalid(O) :- opt(O), not immediate_before(O).

% Constraint 4: Peters fourth
invalid(O) :- order(O, peters, P), P != 4.

% Valid option if not invalid
valid(O) :- opt(O), not invalid(O).

% Map valid options to option/1
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

#show option/1.