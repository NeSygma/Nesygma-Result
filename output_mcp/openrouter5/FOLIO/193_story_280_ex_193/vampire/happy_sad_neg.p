% Negative version: negated claim as conjecture
% Premises:
% 1. Events are either happy or sad.
% 2. At least one event is happy.
% Negated conclusion: Not all events are sad (i.e., there exists an event that is not sad)

fof(either_happy_or_sad, axiom, ! [E] : (happy(E) | sad(E))).
fof(at_least_one_happy, axiom, ? [E] : happy(E)).

fof(goal_negated, conjecture, ~! [E] : sad(E)).