% ===== DOMAIN =====
arg(a1). arg(a2). arg(a3). arg(a4). arg(a5). arg(a6).
arg(a7). arg(a8). arg(a9). arg(a10). arg(a11). arg(a12).
arg(a13). arg(a14). arg(a15). arg(a16).

% ===== LEVELS =====
level(a1,1). level(a2,1). level(a3,1). level(a4,1). level(a5,1). level(a6,1).
level(a7,2). level(a8,2). level(a9,2). level(a10,2). level(a11,2). level(a12,2).
level(a13,3). level(a14,3). level(a15,3). level(a16,3).

% ===== STRONG ATTACKS (always successful) =====
strong_attack(a2,a1). strong_attack(a9,a8). strong_attack(a14,a13). strong_attack(a15,a16).
strong_attack(a1,a14). strong_attack(a16,a15). strong_attack(a1,a3). strong_attack(a1,a4).
strong_attack(a13,a7). strong_attack(a13,a10). strong_attack(a3,a5). strong_attack(a5,a3).

% ===== WEAK ATTACKS (successful only if attacker level > target level) =====
weak_attack(a8,a2). weak_attack(a13,a9). weak_attack(a8,a5). weak_attack(a8,a6).
weak_attack(a16,a11). weak_attack(a16,a12). weak_attack(a2,a7). weak_attack(a10,a13).

% ===== DERIVED: SUCCESSFUL ATTACKS =====
% Strong attacks are always successful
successful_attack(A,B) :- strong_attack(A,B).

% Weak attacks are successful only if attacker level > target level
successful_attack(A,B) :- weak_attack(A,B), level(A,LA), level(B,LB), LA > LB.

% ===== CHOICE: SELECT EXTENSION =====
{in_ext(A)} :- arg(A).

% ===== CONDITION 1: CONFLICT-FREE =====
% No two members of the extension can successfully attack each other
:- in_ext(A), in_ext(B), successful_attack(A,B).

% ===== CONDITION 2: SELF-DEFENDING =====
% For every argument A in the extension and every external argument B that 
% successfully attacks A, there must be an argument C in the extension that 
% successfully attacks B
defended(A,B) :- in_ext(A), arg(B), successful_attack(B,A), in_ext(C), successful_attack(C,B).
:- in_ext(A), arg(B), successful_attack(B,A), not in_ext(B), not defended(A,B).

% ===== CONDITION 3: MAXIMAL (PREFERRED EXTENSION) =====
% The extension cannot be extended with any additional argument while 
% maintaining conflict-free and self-defending properties
% An argument X not in the extension cannot be added if:
% (a) adding X would create a conflict with some member, OR
% (b) adding X would require defense that doesn't exist

% X cannot be added if it successfully attacks some member or is attacked by some member
conflicts_with_ext(X) :- arg(X), not in_ext(X), in_ext(A), successful_attack(X,A).
conflicts_with_ext(X) :- arg(X), not in_ext(X), in_ext(A), successful_attack(A,X).

% X cannot be added if it is attacked by some external argument that is not 
% counter-attacked by any current member (and X itself doesn't counter-attack it)
needs_defense_from(X,B) :- arg(X), not in_ext(X), arg(B), not in_ext(B), successful_attack(B,X).
lacks_defense(X) :- needs_defense_from(X,B), not in_ext(C), successful_attack(C,B), not successful_attack(X,B).

% X cannot be added if it would break conflict-free or self-defending
cannot_add(X) :- conflicts_with_ext(X).
cannot_add(X) :- lacks_defense(X).

% Maximal: every argument not in the extension cannot be added
:- arg(X), not in_ext(X), not cannot_add(X).

% ===== OUTPUT =====
#show in_ext/1.