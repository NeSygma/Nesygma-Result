% Positive version: original conclusion as conjecture

% Predicates:
% club_member(X) - X is in this club
% performs_often(X) - X performs in school talent shows often
% attends_engaged(X) - X attends and is very engaged with school events
% inactive_disinterested(X) - X is inactive and disinterested community member
% chaperones_dances(X) - X chaperones high school dances
% student_attends(X) - X is a student who attends the school
% young_child_teen(X) - X is a young child or teenager
% wishes_academic(X) - X wishes to further their academic career and educational opportunities

% Constants:
% bonnie

% Distinctness (only one named entity)
fof(distinct, axiom, $true).

% Premise 1: People in this club who perform in school talent shows often attend and are very engaged with school events.
fof(premise1, axiom, ! [X] : ((club_member(X) & performs_often(X)) => attends_engaged(X))).

% Premise 2: People in this club either perform in school talent shows often or are inactive and disinterested community members.
% (exclusive or - either one but not both)
fof(premise2, axiom, ! [X] : (club_member(X) => ((performs_often(X) & ~inactive_disinterested(X)) | (~performs_often(X) & inactive_disinterested(X))))).

% Premise 3: People in this club who chaperone high school dances are not students who attend the school.
fof(premise3, axiom, ! [X] : ((club_member(X) & chaperones_dances(X)) => ~student_attends(X))).

% Premise 4: All people in this club who are inactive and disinterested members of their community chaperone high school dances.
fof(premise4, axiom, ! [X] : ((club_member(X) & inactive_disinterested(X)) => chaperones_dances(X))).

% Premise 5: All young children and teenagers in this club who wish to further their academic careers and educational opportunities are students who attend the school.
fof(premise5, axiom, ! [X] : ((club_member(X) & young_child_teen(X) & wishes_academic(X)) => student_attends(X))).

% Premise 6: Bonnie is in this club and she either both attends and is very engaged with school events and is a student who attends the school or is not someone who both attends and is very engaged with school events and is not a student who attends the school.
% (attends_engaged(bonnie) & student_attends(bonnie)) XOR (~attends_engaged(bonnie) & ~student_attends(bonnie))
fof(premise6, axiom, club_member(bonnie)).
fof(premise6b, axiom, ((attends_engaged(bonnie) & student_attends(bonnie)) & ~(~attends_engaged(bonnie) & ~student_attends(bonnie))) | ((~attends_engaged(bonnie) & ~student_attends(bonnie)) & ~(attends_engaged(bonnie) & student_attends(bonnie)))).

% Conclusion to evaluate:
% If Bonnie either chaperones high school dances or, if she does not, she performs in school talent shows often, then Bonnie is both a young child or teenager who wishes to further her academic career and educational opportunities and an inactive and disinterested member of the community.
% Formalized: (chaperones_dances(bonnie) | (~chaperones_dances(bonnie) => performs_often(bonnie))) => (young_child_teen(bonnie) & wishes_academic(bonnie) & inactive_disinterested(bonnie))

% Let's simplify the antecedent: (chaperones_dances(bonnie) | (~chaperones_dances(bonnie) => performs_often(bonnie)))
% (~chaperones_dances(bonnie) => performs_often(bonnie)) is equivalent to (chaperones_dances(bonnie) | performs_often(bonnie))
% So the antecedent is: chaperones_dances(bonnie) | (chaperones_dances(bonnie) | performs_often(bonnie))
% Which simplifies to: chaperones_dances(bonnie) | performs_often(bonnie)

fof(conclusion, conjecture, (chaperones_dances(bonnie) | performs_often(bonnie)) => (young_child_teen(bonnie) & wishes_academic(bonnie) & inactive_disinterested(bonnie))).