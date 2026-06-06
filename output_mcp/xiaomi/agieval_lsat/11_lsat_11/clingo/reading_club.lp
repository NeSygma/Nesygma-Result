% Domain: Works by type
french_novel(1). french_novel(2). french_novel(3).
russian_novel(1). russian_novel(2). russian_novel(3).
french_play(1). french_play(2).
russian_play(1).

% All works
work(W) :- french_novel(W).
work(W) :- russian_novel(W).
work(W) :- french_play(W).
work(W) :- russian_play(W).

% Choice: select each work or not
{select(W)} :- work(W).

% Count selections by type
fn_count(N) :- N = #count{W : french_novel(W), select(W)}.
rn_count(N) :- N = #count{W : russian_novel(W), select(W)}.
fp_count(N) :- N = #count{W : french_play(W), select(W)}.
rp_count(N) :- N = #count{W : russian_play(W), select(W)}.

% Derived counts
total_selected(N) :- N = #count{W : work(W), select(W)}.
french_count(N) :- N = #count{W : french_novel(W), select(W); W : french_play(W), select(W)}.
russian_count(N) :- N = #count{W : russian_novel(W), select(W); W : russian_play(W), select(W)}.
novel_count(N) :- N = #count{W : french_novel(W), select(W); W : russian_novel(W), select(W)}.
play_count(N) :- N = #count{W : french_play(W), select(W); W : russian_play(W), select(W)}.

% Constraints
% 1. Select 5-6 works
:- total_selected(N), N < 5.
:- total_selected(N), N > 6.

% 2. No more than 4 French works
:- french_count(N), N > 4.

% 3. 3-4 novels
:- novel_count(N), N < 3.
:- novel_count(N), N > 4.

% 4. French novels >= Russian novels
:- fn_count(FN), rn_count(RN), FN < RN.

% 5. If both French plays selected, Russian play not selected
:- fp_count(2), rp_count(1).

% Helper predicates for option conditions
% Option A: No Russian novels and exactly one play
no_russian_novels :- rn_count(0).
exactly_one_play :- play_count(1).
option_a :- no_russian_novels, exactly_one_play.

% Option B: Exactly one Russian novel and both French plays
exactly_one_russian_novel :- rn_count(1).
both_french_plays :- fp_count(2).
option_b :- exactly_one_russian_novel, both_french_plays.

% Option C: Exactly two French novels and the Russian play
exactly_two_french_novels :- fn_count(2).
russian_play_selected :- rp_count(1).
option_c :- exactly_two_french_novels, russian_play_selected.

% Option D: Exactly two French novels and exactly two plays
exactly_two_plays :- play_count(2).
option_d :- exactly_two_french_novels, exactly_two_plays.

% Option E: Exactly two Russian novels and exactly one play
exactly_two_russian_novels :- rn_count(2).
option_e :- exactly_two_russian_novels, exactly_one_play.

% Map options
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.