% TPTP problem for Tom moving into Olive Garden with Fluffy
% Using FOF (first-order logic) without arithmetic

% Entities
fof(tom_is_person, axiom, person(tom)).
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(olive_garden_is_building, axiom, building(olive_garden)).

% Definitions
fof(cat_is_pet, axiom, ! [X] : (cat(X) => pet(X))).
fof(managed_building_def, axiom, ! [X] : (managed_building(X) => building(X))).

% Premises
fof(premise_1, axiom, ? [B] : (managed_building(B) & allows_pets(B))).
fof(premise_2, axiom, ! [B] : (managed_building(B) => deposit_required(B))).
fof(premise_3, axiom, ! [B, R] : (rent(B, R) => deposit_at_least_rent(B, R))).
fof(premise_4, axiom, pet(fluffy)).
fof(premise_5, axiom, managed_building(olive_garden)).
fof(premise_6, axiom, rent(olive_garden, 2000)).
fof(premise_7, axiom, greater(2000, 1500)).
fof(premise_8, axiom, 
    ! [P, B, D] : 
        ((allows_move_in(P, fluffy, B) & deposit_amount(B, D) & D <= 1500) => 
         allows_move_in(P, fluffy, B))).
fof(premise_9, axiom, 
    ! [B] : 
        (allows_pets(B) => ! [P, Pet] : allows_move_in(P, Pet, B))).

% Additional constraints for deposit amounts
fof(premise_10, axiom, 
    ! [B, R] : 
        (rent(B, R) => deposit_amount(B, R) | deposit_amount(B, R+1) | deposit_amount(B, R+2))).

% Goal
fof(goal, conjecture, allows_move_in(tom, fluffy, olive_garden)).