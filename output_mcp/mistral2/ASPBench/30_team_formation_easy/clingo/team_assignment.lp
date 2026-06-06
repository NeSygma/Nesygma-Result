% Domain declarations
person(alice; bob; carol; dave; eve; frank; grace; henry).

% Skills of each person
skill(alice, programming).
skill(alice, design).
skill(bob, programming).
skill(bob, testing).
skill(carol, design).
skill(carol, management).
skill(dave, testing).
skill(dave, management).
skill(eve, programming).
skill(eve, documentation).
skill(frank, design).
skill(frank, documentation).
skill(grace, testing).
skill(grace, documentation).
skill(henry, management).
skill(henry, documentation).

% Required skills for team formation
required_skill(programming).
required_skill(design).
required_skill(testing).
required_skill(management).

% Teams
team(1..2).

% Choice rule: Assign each person to a team
1 { assigned(Person, Team) : team(Team) } 1 :- person(Person).

% Each team must have exactly 4 people
:- team(T), { assigned(P, T) : person(P) } != 4.

% All 8 people must be assigned to teams (no overlaps, no omissions)
:- person(P), not assigned(P, _).

% Ensure each team has at least one person with each required skill
:- team(T), required_skill(S), not has_required_skill(T, S).
has_required_skill(T, S) :- assigned(P, T), skill(P, S), required_skill(S).

% Helper: Count how many people in a team have a specific skill
skill_count(T, S, N) :- 
    team(T), 
    required_skill(S), 
    N = #count { P : assigned(P, T), skill(P, S) }.

% Overlap for a team: sum over all skills of max(0, skill_count - 1)
overlap(T) :- 
    team(T), 
    #sum { N-1 : skill_count(T, S, N), N > 1 } > 0.

% Total overlap to minimize
total_overlap(O) :- O = #sum { O1 : overlap(1, O1) } + #sum { O2 : overlap(2, O2) }.

% Minimize the total overlap
#minimize { O : total_overlap(O) }.

% Show the assignment
#show assigned/2.
#show total_overlap/1.