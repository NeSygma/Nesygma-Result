% Negative version: negated conclusion as conjecture

% Predicates:
% perform(X)   - X performs in school talent shows often
% attend_engaged(X) - X attends and is very engaged with school events
% inactive_disinterested(X) - X is an inactive and disinterested community member
% chaperone(X) - X chaperones high school dances
% student(X)   - X is a student who attends the school
% young_teen(X) - X is a young child or teenager
% further(X)   - X wishes to further their academic career and educational opportunities

% Distinct entities
fof(distinct, axiom, bonnie != other).

% Premise 1: People in this club who perform in school talent shows often attend and are very engaged with school events.
fof(premise1, axiom, ! [X] : (perform(X) => attend_engaged(X))).

% Premise 2: People in this club either perform in school talent shows often or are inactive and disinterested community members.
fof(premise2, axiom, ! [X] : (perform(X) | inactive_disinterested(X))).

% Premise 3: People in this club who chaperone high school dances are not students who attend the school.
fof(premise3, axiom, ! [X] : (chaperone(X) => ~student(X))).

% Premise 4: All people in this club who are inactive and disinterested members of their community chaperone high school dances.
fof(premise4, axiom, ! [X] : (inactive_disinterested(X) => chaperone(X))).

% Premise 5: All young children and teenagers in this club who wish to further their academic careers and educational opportunities are students who attend the school.
fof(premise5, axiom, ! [X] : ((young_teen(X) & further(X)) => student(X))).

% Premise 6: Bonnie is in this club and she either both attends and is very engaged with school events and is a student who attends the school or is not someone who both attends and is very engaged with school events and is not a student who attends the school.
fof(premise6, axiom, (attend_engaged(bonnie) & student(bonnie)) | (~attend_engaged(bonnie) & ~student(bonnie))).

% Negated conclusion:
% ~( ((young_teen(bonnie) & further(bonnie) & chaperone(bonnie)) | (~young_teen(bonnie) & ~further(bonnie))) 
%    => (student(bonnie) | inactive_disinterested(bonnie)) )
% Which is equivalent to:
% ((young_teen(bonnie) & further(bonnie) & chaperone(bonnie)) | (~young_teen(bonnie) & ~further(bonnie))) 
% & ~(student(bonnie) | inactive_disinterested(bonnie))
% = ((young_teen(bonnie) & further(bonnie) & chaperone(bonnie)) | (~young_teen(bonnie) & ~further(bonnie))) 
% & ~student(bonnie) & ~inactive_disinterested(bonnie)

fof(neg_conclusion, conjecture, 
    ( ((young_teen(bonnie) & further(bonnie) & chaperone(bonnie)) | (~young_teen(bonnie) & ~further(bonnie))) 
    & ~student(bonnie) & ~inactive_disinterested(bonnie) )).