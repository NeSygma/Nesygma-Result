% Negative version: conjecture is "Bonnie does NOT perform in school talent shows often"
% Predicates:
%   club_member(X)       - X is in this club
%   performs_often(X)    - X performs in school talent shows often
%   attends_engaged(X)   - X attends and is very engaged with school events
%   inactive_disinterested(X) - X is inactive and disinterested community member
%   chaperones(X)        - X chaperones high school dances
%   student_attends(X)   - X is a student who attends the school
%   young_child_teen(X)  - X is a young child or teenager
%   wishes_academic(X)   - X wishes to further academic careers and educational opportunities

% Premise 1: People in this club who perform in school talent shows often attend and are very engaged with school events.
fof(premise1, axiom, ! [X] : ((club_member(X) & performs_often(X)) => attends_engaged(X))).

% Premise 2: People in this club either perform in school talent shows often or are inactive and disinterested community members.
fof(premise2, axiom, ! [X] : (club_member(X) => (performs_often(X) | inactive_disinterested(X)))).

% Premise 3: People in this club who chaperone high school dances are not students who attend the school.
fof(premise3, axiom, ! [X] : ((club_member(X) & chaperones(X)) => ~student_attends(X))).

% Premise 4: All people in this club who are inactive and disinterested members of their community chaperone high school dances.
fof(premise4, axiom, ! [X] : ((club_member(X) & inactive_disinterested(X)) => chaperones(X))).

% Premise 5: All young children and teenagers in this club who wish to further their academic careers and educational opportunities are students who attend the school.
fof(premise5, axiom, ! [X] : ((club_member(X) & young_child_teen(X) & wishes_academic(X)) => student_attends(X))).

% Premise 6: Bonnie is in this club and she either both attends and is very engaged with school events and is a student who attends the school or is not someone who both attends and is very engaged with school events and is not a student who attends the school.
fof(premise6, axiom, club_member(bonnie) & ((attends_engaged(bonnie) & student_attends(bonnie)) | (~attends_engaged(bonnie) & ~student_attends(bonnie)))).

% Negated conclusion: Bonnie does NOT perform in school talent shows often.
fof(goal_neg, conjecture, ~performs_often(bonnie)).