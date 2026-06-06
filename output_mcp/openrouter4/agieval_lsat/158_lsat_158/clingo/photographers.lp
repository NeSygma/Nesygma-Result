% Define photographers
photographer(frost; gonzalez; heideck; knutson; lai; mays).

% Define ceremonies
ceremony(silva; thorne).

% Each photographer can be assigned to at most one ceremony, or not assigned at all
{ assigned(P, C) : ceremony(C) } <= 1 :- photographer(P).

% Constraint 1: At least 2 photographers assigned to each ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% Constraint 3 (implicit): No photographer assigned to both - handled by the choice rule (<= 1)

% Constraint 4: Frost must be assigned together with Heideck to one ceremony
% Frost is definitely assigned
1 { assigned(frost, C) : ceremony(C) } 1.
% Heideck must be assigned to the same ceremony as Frost
assigned(heideck, C) :- assigned(frost, C).

% Constraint 5: If Lai and Mays are both assigned, they must be to different ceremonies
both_lai_mays_assigned :- assigned(lai, _), assigned(mays, _).
:- both_lai_mays_assigned, assigned(lai, C), assigned(mays, C).

% Constraint 6: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 7: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Helper: photographer is assigned somewhere
assigned_any(P) :- assigned(P, _).

% --- Now let's check which photographers must always be assigned ---
% We'll try to find a solution where each photographer is NOT assigned.
% If no such solution exists, the photographer must be assigned.

% For each photographer, try to find a scenario where they're unassigned
{ try_unassign(P) } :- photographer(P).

% If we try to unassign P, then P cannot be assigned to any ceremony
:- try_unassign(P), assigned(P, _).

% Now, we need to check which try_unassign choices lead to a solution.
% A photographer is a "must assign" if try_unassign(P) cannot be true in any solution.

% We can check this by seeing which try_unassign atoms appear in solutions.
% If try_unassign(P) is never in any solution, then P must be assigned.

% But this mixes scenarios. Let me use a different approach.

% Let me just enumerate all solutions and compute manually who is always assigned.
% I'll show all assignments.

#show assigned/2.
#show assigned_any/1.