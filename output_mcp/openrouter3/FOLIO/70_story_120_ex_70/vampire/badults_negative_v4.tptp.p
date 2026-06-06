% TFF version with proper typing - fixed underscore issue
tff(channel_type, type, channel: $tType).
tff(month_type, type, month: $tType).
tff(year_type, type, year: $tType).
tff(show_type, type, show: $tType).
tff(person_type, type, person: $tType).

% Constants
tff(bbc_two_decl, type, bbc_two: channel).
tff(bbc_three_decl, type, bbc_three: channel).
tff(badults_decl, type, badults: show).
tff(july_decl, type, july: month).
tff(y2013_decl, type, y2013: year).
tff(andrew_collins_decl, type, andrew_collins: person).

% Predicates
tff(pappy_member_decl, type, pappy_member: person > $o).
tff(starred_in_decl, type, starred_in: (person * show) > $o).
tff(piloted_in_decl, type, piloted_in: (show * month * year * channel) > $o).
tff(script_editor_decl, type, script_editor: (person * show) > $o).

% Premises
tff(premise_1, axiom, ? [X: person] : (pappy_member(X) & starred_in(X, badults))).
tff(premise_2, axiom, piloted_in(badults, july, y2013, bbc_three)).
tff(premise_4, axiom, script_editor(andrew_collins, badults)).

% Distinctness
tff(distinct_channels, axiom, (bbc_two != bbc_three)).

% Negated conclusion: There exists a member of Pappy's who starred in a show piloting on BBC Two or BBC Three
tff(goal_negated, conjecture, 
    ? [X: person, Y: show, M: month, Yr: year] : 
        (pappy_member(X) & starred_in(X, Y) & 
            (piloted_in(Y, M, Yr, bbc_two) | piloted_in(Y, M, Yr, bbc_three))))).