% --- Declare all arguments ---
argument(a).
argument(b).
argument(c).
argument(d).
argument(e).
argument(f).

% --- Declare attack relations ---
attacks(a, b).
attacks(b, c).
attacks(c, d).
attacks(d, e).
attacks(e, f).
attacks(f, a).
attacks(b, f).
attacks(d, b).

% --- Helper predicate: attacked_by(X, Y) means Y is attacked by X ---
attacked_by(X, Y) :- attacks(X, Y).

% --- Generate possible extensions ---
{in_extension(X) : argument(X)}.

% --- Conflict-free: No two arguments in the extension attack each other ---
:- in_extension(X), in_extension(Y), attacks(X, Y).

% --- Self-defending: For every X in the extension, all its attackers are attacked by some Z in the extension ---
:- in_extension(X),
   not defended(X).
defended(X) :- in_extension(X), in_extension(Z), attacks(Z, Y), attacks(Y, X).

% --- Maximality: Every argument not in the extension is attacked by some argument in the extension ---
:- argument(X),
   not in_extension(X),
   not attacked_by_extension(X).
attacked_by_extension(X) :- in_extension(Y), attacks(Y, X).

% --- Collect all stable extensions ---
#show in_extension/1.