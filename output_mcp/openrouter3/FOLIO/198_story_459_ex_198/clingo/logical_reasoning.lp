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
dog(X) :- animal(X), barks(X).  % If X is a dog, then X barks
% Also: dogs are animals (already covered by domain)

% Premise 3: Jane likes all animals that jump
likes_jane(X) :- jumps(X).

% Premise 4: If an animal has legs, then it jumps
jumps(X) :- has_legs(X).

% Premise 5: If an animal is terricolous, then it has legs
has_legs(X) :- terricolous(X).

% Premise 6: KiKi is an animal (already stated)

% Premise 7: If KiKi neither jumps nor has legs, then KiKi is terricolous or has legs
% This is: (¬jumps(kiki) ∧ ¬has_legs(kiki)) → (terricolous(kiki) ∨ has_legs(kiki))
% In ASP: forbid the case where KiKi neither jumps nor has legs AND is neither terricolous nor has legs
:- not jumps(kiki), not has_legs(kiki), not terricolous(kiki), not has_legs(kiki).

% Conclusion to evaluate: KiKi does not bark and he is not a dog
% We need to determine if this is True, False, or Uncertain
conclusion_true :- not barks(kiki), not dog(kiki).
conclusion_false :- barks(kiki).
conclusion_false :- dog(kiki).

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.
#show barks/1.
#show dog/1.
#show jumps/1.
#show has_legs/1.
#show terricolous/1.
#show likes_jane/1.