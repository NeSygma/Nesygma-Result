% Positive version: original claim as conjecture
% Premises:
% 1. Events are either happy or sad.
% 2. At least one event is happy.
% Conclusion: All events are sad.

fof(either_happy_or_sad, axiom, ! [E] : (happy(E) | sad(E))).
fof(at_least_one_happy, axiom, ? [E] : happy(E)).

fof(goal, conjecture, ! [E] : sad(E)).