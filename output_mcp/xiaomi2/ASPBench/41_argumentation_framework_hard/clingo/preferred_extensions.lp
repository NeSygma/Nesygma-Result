% Hierarchical Argumentation Framework - Preferred Extensions
% Find all maximal admissible sets (preferred extensions)

% Arguments
arg(a1). arg(a2). arg(a3). arg(a4). arg(a5). arg(a6).
arg(a7). arg(a8). arg(a9). arg(a10). arg(a11). arg(a12).
arg(a13). arg(a14). arg(a15). arg(a16).

% Levels
level(a1, 1). level(a2, 1). level(a3, 1). level(a4, 1). level(a5, 1). level(a6, 1).
level(a7, 2). level(a8, 2). level(a9, 2). level(a10, 2). level(a11, 2). level(a12, 2).
level(a13, 3). level(a14, 3). level(a15, 3). level(a16, 3).

% Strong attacks (always successful)
strong_attack(a2, a1). strong_attack(a9, a8). strong_attack(a14, a13). strong_attack(a15, a16).
strong_attack(a1, a14). strong_attack(a16, a15). strong_attack(a1, a3). strong_attack(a1, a4).
strong_attack(a13, a7). strong_attack(a13, a10). strong_attack(a3, a5). strong_attack(a5, a3).

% Weak attacks (successful only if attacker level > target level)
weak_attack(a8, a2). weak_attack(a13, a9). weak_attack(a8, a5). weak_attack(a8, a6).
weak_attack(a16, a11). weak_attack(a16, a12). weak_attack(a2, a7). weak_attack(a10, a13).

% Derive successful attacks
successful_attack(X, Y) :- strong_attack(X, Y).
successful_attack(X, Y) :- weak_attack(X, Y), level(X, LX), level(Y, LY), LX > LY.

% Choice: each argument is either in or out of the extension
{ in(X) } :- arg(X).
out(X) :- arg(X), not in(X).

% === ADMISSIBILITY ===

% Condition 1: Conflict-free
% No two members of the extension may successfully attack each other
:- in(X), in(Y), successful_attack(X, Y).

% Condition 2: Self-defending (every member is defended)
% A member X is defended if for every external attacker Y, there is a member Z that attacks Y
has_defender(Y) :- in(Z), successful_attack(Z, Y).
undefended(X) :- in(X), successful_attack(Y, X), out(Y), not has_defender(Y).
:- undefended(X).

% === MAXIMALITY (Preferred Extension) ===
% For every argument X not in the extension, S ∪ {X} must NOT be admissible

% X conflicts with a member (attack in either direction)
conflicts_with_member(X) :- out(X), in(Y), successful_attack(X, Y).
conflicts_with_member(X) :- out(X), in(Y), successful_attack(Y, X).

% X would be undefended if added: some external Y attacks X, no one in S defends Y, and X doesn't defend itself against Y
not_defended_if_added(X) :- out(X), successful_attack(Y, X), out(Y), Y != X, not has_defender(Y), not successful_attack(X, Y).

% Every out argument must be unaddable (cannot be added while preserving admissibility)
:- out(X), not conflicts_with_member(X), not not_defended_if_added(X).

#show in/1.