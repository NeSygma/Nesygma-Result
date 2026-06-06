% Negative version: negated conclusion as conjecture
% Original conclusion: If roses are given out during Breaking Bad, then it is on Monday at 8 pm.
% Negated: ~(gives_roses(breaking_bad) => airs_at_8pm_monday(breaking_bad))
% Which is equivalent to: gives_roses(breaking_bad) & ~airs_at_8pm_monday(breaking_bad)

% Premise 1: Some show airing at 8 pm on Monday gives out roses on TV.
fof(premise1, axiom, ? [S] : (show(S) & airs_at_8pm_monday(S) & gives_roses(S))).

% Premise 2: If a show gives out roses on TV, then the show is an episode of The Bachelor.
fof(premise2, axiom, ! [S] : (gives_roses(S) => bachelor_episode(S))).

% Premise 3: The Bachelor portrays the lives of real people.
fof(premise3, axiom, ! [S] : (bachelor_episode(S) => portrays_real_people(S))).

% Premise 4: All shows portraying the lives of real people are reality TV shows.
fof(premise4, axiom, ! [S] : (portrays_real_people(S) => reality_show(S))).

% Premise 5: Breaking Bad is a show.
fof(premise5, axiom, show(breaking_bad)).

% Premise 6: Breaking Bad is not a reality TV show.
fof(premise6, axiom, ~reality_show(breaking_bad)).

% Distinctness (only one named constant)
fof(distinct, axiom, ! [S] : $true).

% Negated conclusion: gives_roses(breaking_bad) & ~airs_at_8pm_monday(breaking_bad)
fof(negated_conclusion, conjecture, (gives_roses(breaking_bad) & ~airs_at_8pm_monday(breaking_bad))).