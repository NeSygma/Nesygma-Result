fof(tom, axiom, person(tom)).
fof(fluffy, axiom, cat(fluffy)).
fof(olive_garden, axiom, managed_building(olive_garden)).

% Cats are pets.
fof(cats_are_pets, axiom, ! [X] : (cat(X) => pet(X))).

% Some managed buildings allow pets.
fof(some_allows_pets, axiom, allows_pets(olive_garden)).

% If managed building allows pets, people can move in with a pet.
fof(premise_10, axiom,
    ! [P, A, B] :
      ((managed_building(B) & allows_pets(B) & pet(A))
       => allowed_to_move_in_with(P, A, B))).

% Security deposit >= monthly rent at managed buildings.
% Olive Garden rent is 2000, which is more than 1500.
% So deposit >= 2000 > 1500, meaning deposit > 1500.
% We encode this directly: deposit exceeds 1500 at olive_garden.
fof(deposit_exceeds_1500, axiom,
    deposit_exceeds_1500(olive_garden)).

% Tom will rent if allowed to move in with Fluffy AND deposit <= 1500.
% We encode: deposit_exceeds_1500(B) means deposit > 1500, so condition fails.
fof(premise_9, axiom,
    ! [B] :
      ((managed_building(B) & allowed_to_move_in_with(tom, fluffy, B) & ~deposit_exceeds_1500(B))
       => will_rent(tom, B))).

% Negated Conclusion: Tom will NOT rent at Olive Garden.
fof(goal, conjecture, ~will_rent(tom, olive_garden)).