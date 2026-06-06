fof(distinct_constants, axiom, the_bachelor != breaking_bad & the_bachelor != real_people & the_bachelor != monday & the_bachelor != eight_pm & breaking_bad != real_people & breaking_bad != monday & breaking_bad != eight_pm & real_people != monday & real_people != eight_pm & monday != eight_pm).
fof(exist_show, axiom, ? [S] : (airs_at(S, monday, eight_pm) & gives_out_roses_on_tv(S))).
fof(rule_gives_roses_implies_episode, axiom, ! [S] : (gives_out_roses_on_tv(S) => episode_of(S, the_bachelor))).
fof(axiom_portrays_real_people, axiom, portrays(the_bachelor, real_people)).
fof(axiom_all_portrayed_are_reality, axiom, ! [S] : (portrays(S, real_people) => reality_tv_show(S))).
fof(axiom_breaking_bad_is_show, axiom, show(breaking_bad)).
fof(axiom_breaking_bad_not_reality, axiom, ~reality_tv_show(breaking_bad)).
fof(conjecture, conjecture, airs_at(breaking_bad, monday, eight_pm)).