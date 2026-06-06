% Positive version: original claim as conjecture
% Predicates:
% multiple_birth(X) - X is born in a multiple birth with siblings
% has_siblings_together(X) - X has siblings who were born together
% spends_time(X) - X spends a lot of time hanging out with and playing with siblings
% complains(X) - X complains often about annoying siblings
% lives_at_home(X) - X lives at home
% lives_with_strangers(X) - X lives with strangers
% baby_multiple_birth(X) - X is a baby born in a multiple birth

fof(premise1, axiom, ! [X] : (multiple_birth(X) => spends_time(X))).
fof(premise2, axiom, ! [X] : (has_siblings_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains(X) => has_siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time(X) => lives_at_home(X))).

% Luke either is a baby born in a multiple birth and lives with strangers, 
% or is not a baby born in a multiple birth and does not live with strangers
% (baby_multiple_birth(luke) & lives_with_strangers(luke)) | (~baby_multiple_birth(luke) & ~lives_with_strangers(luke))
fof(premise6, axiom, 
    ((baby_multiple_birth(luke) & lives_with_strangers(luke)) | (~baby_multiple_birth(luke) & ~lives_with_strangers(luke)))).

% Note: "baby born in a multiple birth" is a specific term. We need to relate baby_multiple_birth to multiple_birth.
% A baby born in a multiple birth IS born in a multiple birth.
fof(baby_link, axiom, ! [X] : (baby_multiple_birth(X) => multiple_birth(X))).

fof(goal, conjecture, spends_time(luke)).