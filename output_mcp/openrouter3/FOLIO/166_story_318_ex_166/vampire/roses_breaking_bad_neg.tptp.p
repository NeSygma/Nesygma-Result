% Premises
fof(show_breaking_bad, axiom, show(breaking_bad)).
fof(show_the_bachelor, axiom, show(the_bachelor)).
fof(distinct_shows, axiom, (breaking_bad != the_bachelor)).

% Premise 1: Some show airing at 8 pm on Monday gives out roses on TV
% We'll represent time slots as constants: time_8pm, day_monday
fof(premise_1, axiom, ? [S] : (show(S) & airs_at(S, day_monday, time_8pm) & gives_out_roses(S))).

% Premise 2: If a show gives out roses on TV, then the show is an episode of The Bachelor
fof(premise_2, axiom, ! [S] : (gives_out_roses(S) => is_episode_of(S, the_bachelor))).

% Premise 3: The Bachelor portrays the lives of real people
fof(premise_3, axiom, portrays_real_people(the_bachelor)).

% Premise 4: All shows portraying the lives of real people are reality TV shows
fof(premise_4, axiom, ! [S] : (portrays_real_people(S) => is_reality_tv(S))).

% Premise 5: Breaking Bad is a show (already stated)
% Premise 6: Breaking Bad is not a reality TV show
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).

% Negated conclusion: Roses are given out during Breaking Bad AND it is NOT on Monday at 8 pm
fof(negated_conclusion, conjecture, gives_out_roses(breaking_bad) & ~airs_at(breaking_bad, day_monday, time_8pm)).