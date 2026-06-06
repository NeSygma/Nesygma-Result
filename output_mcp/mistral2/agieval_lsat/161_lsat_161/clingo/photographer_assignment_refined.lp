% Base facts: photographers and ceremonies
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Assignments: assigned(P, C) means photographer P is assigned to ceremony C
% Each photographer can be assigned to at most one ceremony
1 { assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% Each ceremony must have at least two photographers
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% No photographer can be assigned to both ceremonies
:- assigned(P, C1), assigned(P, C2), C1 != C2.

% Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% If Lai and Mays are both assigned, they must be assigned to different ceremonies
:- assigned(lai, C), assigned(mays, C), ceremony(C).

% If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Original constraint: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
% This is encoded as: If Knutson is not assigned to Thorne, then Heideck and Mays must be assigned to Thorne
original_constraint_holds :-
    not assigned(knutson, thorne),
    assigned(heideck, thorne),
    assigned(mays, thorne).

% (C) Unless Knutson is assigned to the Thorne University ceremony, both Frost and Mays must be assigned to that ceremony.
substitution_c_holds :-
    not assigned(knutson, thorne),
    assigned(frost, thorne),
    assigned(mays, thorne).

% (D) Unless Knutson is assigned to the Thorne University ceremony, Heideck cannot be assigned to the same ceremony as Lai.
substitution_d_holds :-
    not assigned(knutson, thorne),
    not (assigned(heideck, C), assigned(lai, C), ceremony(C)).

% (E) Unless either Heideck or Mays is assigned to the Thorne University ceremony, Knutson must be assigned to that ceremony.
substitution_e_holds :-
    not (assigned(heideck, thorne) ; assigned(mays, thorne)),
    not assigned(knutson, thorne).

% The correct substitution is the one that enforces the same effect as the original constraint
% We will check if the substitution leads to the same assignments as the original constraint

% If original_constraint_holds is true, substitution_c_holds, substitution_d_holds, or substitution_e_holds must be true
:- original_constraint_holds, not substitution_c_holds, not substitution_d_holds, not substitution_e_holds.

% If substitution_c_holds, substitution_d_holds, or substitution_e_holds is true, original_constraint_holds must be true
:- substitution_c_holds, not original_constraint_holds.
:- substitution_d_holds, not original_constraint_holds.
:- substitution_e_holds, not original_constraint_holds.

% The correct substitution is the one that satisfies the equivalence
correct_substitution(c) :- substitution_c_holds.
correct_substitution(d) :- substitution_d_holds.
correct_substitution(e) :- substitution_e_holds.

% Map the correct answer to option/1
option(c) :- correct_substitution(c).
option(d) :- correct_substitution(d).
option(e) :- correct_substitution(e).

#show option/1.