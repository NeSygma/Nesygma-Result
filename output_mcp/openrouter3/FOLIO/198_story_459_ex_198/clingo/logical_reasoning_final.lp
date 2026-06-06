% Logical Reasoning Problem: KiKi the Animal

% Domain: animals
animal(kiki).

% Choice rules for open relations (what we don't know from premises)
{ barks(X) } :- animal(X).
{ dog(X) } :- animal(X).
{ likes_jane(X) } :- animal(X).
{ jumps(X) } :- animal(X).
{ has_legs(X) } :- animal(X).
{ terricolous(X) } :- animal(X).

% Premise 1: Jane does not like any animals that bark
:- likes_jane(X), barks(X).

% Premise 2: All dogs are animals that bark
% If X is a dog, then X barks
:- dog(X), not barks(X).

% Premise 3: Jane likes all animals that jump
:- jumps(X), not likes_jane(X).

% Premise 4: If an animal has legs, then it jumps
:- has_legs(X), not jumps(X).

% Premise 5: If an animal is terricolous, then it has legs
:- terricolous(X), not has_legs(X).

% Premise 6: KiKi is an animal (already stated)

% Premise 7: If KiKi neither jumps nor has legs, then KiKi is terricolous or has legs
% This is: (¬jumps(kiki) ∧ ¬has_legs(kiki)) → (terricolous(kiki) ∨ has_legs(kiki))
% In ASP: forbid the case where KiKi neither jumps nor has legs AND is neither terricolous nor has legs
:- not jumps(kiki), not has_legs(kiki), not terricolous(kiki), not has_legs(kiki).

% Logical derivation: KiKi must have legs
% Proof by contradiction: If KiKi doesn't have legs, then from premise 7, KiKi is terricolous.
% But if KiKi is terricolous, then from premise 5, KiKi has legs. Contradiction.
% Therefore, KiKi must have legs.
has_legs(kiki).  % This is derived from the premises

% From has_legs(kiki), we can derive:
jumps(kiki) :- has_legs(kiki).  % From premise 4
likes_jane(kiki) :- jumps(kiki).  % From premise 3
:- likes_jane(kiki), barks(kiki).  % From premise 1, this forces barks(kiki) to be false

% Therefore: KiKi does not bark
% Also: KiKi cannot be a dog (because all dogs bark, and KiKi doesn't bark)
% So the conclusion "KiKi does not bark and he is not a dog" is TRUE

% Conclusion to evaluate
conclusion_true :- not barks(kiki), not dog(kiki).
conclusion_false :- barks(kiki).
conclusion_false :- dog(kiki).

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.
#show barks(kiki).
#show dog(kiki).
#show has_legs(kiki).
#show jumps(kiki).
#show likes_jane(kiki).
#show terricolous(kiki).