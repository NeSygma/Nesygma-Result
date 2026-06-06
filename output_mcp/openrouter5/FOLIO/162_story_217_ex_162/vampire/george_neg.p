% Negative version: negated conclusion as conjecture
% Premises:
% 1. If George likes music, he wants to compose.
% 2. If George has access to a program, he can compose.
% 3. If George can compose and wants to compose, he will compose.
% Negated conclusion: ~(~will_compose(george) => ~can_compose(george))
% Which is equivalent to: ~will_compose(george) & can_compose(george)

fof(premise1, axiom, (likes_music(george) => wants_to_compose(george))).
fof(premise2, axiom, (has_access_to_program(george) => can_compose(george))).
fof(premise3, axiom, ((can_compose(george) & wants_to_compose(george)) => will_compose(george))).

% Negated conclusion: ~will_compose(george) & can_compose(george)
fof(negated_conclusion, conjecture, (~will_compose(george) & can_compose(george))).