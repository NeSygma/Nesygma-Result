% Arguments and their levels
argument(a1). argument(a2). argument(a3). argument(a4). argument(a5). argument(a6).
argument(a7). argument(a8). argument(a9). argument(a10). argument(a11). argument(a12).
argument(a13). argument(a14). argument(a15). argument(a16).

level(1, a1). level(1, a2). level(1, a3). level(1, a4). level(1, a5). level(1, a6).
level(2, a7). level(2, a8). level(2, a9). level(2, a10). level(2, a11). level(2, a12).
level(3, a13). level(3, a14). level(3, a15). level(3, a16).

% Strong attacks (always successful)
strong_attack(a2, a1). strong_attack(a9, a8). strong_attack(a14, a13). strong_attack(a15, a16).
strong_attack(a1, a14). strong_attack(a16, a15). strong_attack(a1, a3). strong_attack(a1, a4).
strong_attack(a13, a7). strong_attack(a13, a10). strong_attack(a3, a5). strong_attack(a5, a3).

% Weak attacks (successful only if attacker level > target level)
weak_attack(a8, a2). weak_attack(a13, a9). weak_attack(a8, a5). weak_attack(a8, a6).
weak_attack(a16, a11). weak_attack(a16, a12). weak_attack(a2, a7). weak_attack(a10, a13).

% Attack relation (all attacks)
attack(X, Y) :- strong_attack(X, Y).
attack(X, Y) :- weak_attack(X, Y).

% Get level of an argument
level_of(X, L) :- level(L, X).

% Successful attack: strong attacks always succeed, weak attacks succeed only if attacker level > target level
successful_attack(X, Y) :- strong_attack(X, Y).
successful_attack(X, Y) :- weak_attack(X, Y), level_of(X, LX), level_of(Y, LY), LX > LY.

% Extension membership (choice rule - each argument can be in or out)
{ in_extension(X) } :- argument(X).

% Conflict-free: No argument in extension successfully attacks another in extension
:- in_extension(X), in_extension(Y), successful_attack(X, Y).

% Self-defending: For every argument A in extension and every external B that successfully attacks A,
% there must be some C in extension that successfully attacks B
% We need to check: for each A in extension, for each B that successfully attacks A and B not in extension,
% there exists C in extension that successfully attacks B
:- in_extension(A), successful_attack(B, A), not in_extension(B), not (in_extension(C), successful_attack(C, B)).

% For maximality, we need to ensure that no argument outside the extension can be added
% while maintaining conflict-free and self-defending properties.
% We'll check for each argument X not in extension:
%   1. Adding X would violate conflict-free if X attacks some member or is attacked by some member
%   2. Adding X would violate self-defending if:
%      - X attacks some member A, and no member attacks X
%      - OR some member A attacks X, and X doesn't attack A back (and no other member attacks A)

% Helper: Check if adding X would violate conflict-free
violates_conflict_free(X) :- argument(X), not in_extension(X),
   (in_extension(Y), successful_attack(X, Y); in_extension(Y), successful_attack(Y, X)).

% Helper: Check if adding X would violate self-defending
% Case 1: X attacks some member A, and no member attacks X
violates_self_defending_case1(X) :- argument(X), not in_extension(X),
   in_extension(A), successful_attack(X, A),
   not (in_extension(C), successful_attack(C, X)).

% Case 2: Some member A attacks X, and X doesn't attack A back, and no other member attacks A
violates_self_defending_case2(X) :- argument(X), not in_extension(X),
   in_extension(A), successful_attack(A, X),
   not successful_attack(X, A),
   not (in_extension(C), C != A, successful_attack(C, A)).

% If either case holds, adding X violates self-defending
violates_self_defending(X) :- violates_self_defending_case1(X).
violates_self_defending(X) :- violates_self_defending_case2(X).

% Maximal: For every X not in extension, adding X must violate either conflict-free or self-defending
:- argument(X), not in_extension(X), not violates_conflict_free(X), not violates_self_defending(X).

% Show the extension
#show in_extension/1.