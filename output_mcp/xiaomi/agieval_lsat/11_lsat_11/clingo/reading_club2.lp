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

% Test each option individually
% Option A: No Russian novels and exactly one play
test_a :- rn_count(0), play_count(1).

% Option B: Exactly one Russian novel and both French plays
test_b :- rn_count(1), fp_count(2).

% Option C: Exactly two French novels and the Russian play
test_c :- fn_count(2), rp_count(1).

% Option D: Exactly two French novels and exactly two plays
test_d :- fn_count(2), play_count(2).

% Option E: Exactly two Russian novels and exactly one play
test_e :- rn_count(2), play_count(1).

% Show which tests are possible
#show test_a/0.
#show test_b/0.
#show test_c/0.
#show test_d/0.
#show test_e/0.