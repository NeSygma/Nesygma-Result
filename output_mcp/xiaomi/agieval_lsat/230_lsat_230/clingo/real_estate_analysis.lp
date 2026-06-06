% Define buildings and their classes
building(garza_tower). building(yates_house). building(zimmer_house).
building(flores_tower). building(lynch_building).
building(king_building). building(meyer_building). building(ortiz_building).

class(garza_tower, 1). class(yates_house, 3). class(zimmer_house, 3).
class(flores_tower, 1). class(lynch_building, 2).
class(king_building, 2). class(meyer_building, 2). class(ortiz_building, 2).

% Define companies
company(realprop). company(southco). company(trustcorp).

% Initial ownership
owns(realprop, garza_tower). owns(realprop, yates_house). owns(realprop, zimmer_house).
owns(southco, flores_tower). owns(southco, lynch_building).
owns(trustcorp, king_building). owns(trustcorp, meyer_building). owns(trustcorp, ortiz_building).

% Count buildings by class for each company
% RealProp: 1 class1, 0 class2, 2 class3
% Southco: 1 class1, 1 class2, 0 class3
% Trustcorp: 0 class1, 3 class2, 0 class3

% Total buildings by class
total_class1(2). total_class2(4). total_class3(2).

% For each option, we need to check if the target distribution is reachable
% Let's analyze the class count changes needed for each option

% Option A: RealProp should have Lynch (2), Meyer (2), Ortiz (2)
% Target RealProp: 0 class1, 3 class2, 0 class3
% Change needed: -1 class1, +3 class2, -2 class3
% This requires: give away 1 class1, receive 3 class2, give away 2 class3

% Option B: Southco should have Garza (1), Meyer (2)
% Target Southco: 1 class1, 1 class2, 0 class3
% Change needed: 0 class1, 0 class2, 0 class3 (same as initial!)
% This is just swapping buildings within same classes

% Option C: Southco should have King (2), Meyer (2), Ortiz (2)
% Target Southco: 0 class1, 3 class2, 0 class3
% Change needed: -1 class1, +2 class2, 0 class3
% This requires: give away 1 class1, receive 2 class2

% Option D: Trustcorp should have Flores (1), Yates (3)
% Target Trustcorp: 1 class1, 0 class2, 1 class3
% Change needed: +1 class1, -3 class2, +1 class3
% This requires: receive 1 class1, give away 3 class2, receive 1 class3

% Option E: Trustcorp should have Garza (1), Lynch (2)
% Target Trustcorp: 1 class1, 1 class2, 0 class3
% Change needed: +1 class1, -2 class2, 0 class3
% This requires: receive 1 class1, give away 2 class2

% Now let's check if these changes are possible with the trade rules
% Trade type 1: same class swap - no change in counts
% Trade type 2: give 1 class1, get 2 class2 -> net: -1 class1, +2 class2
% Trade type 3: give 1 class2, get 2 class3 -> net: -1 class2, +2 class3

% For each option, we need to see if there exist non-negative integers
% t2 (type2 trades) and t3 (type3 trades) such that the net changes match

% Let's define variables for the number of trades involving each company
% For a company C:
% a = number of type2 trades where C gives class1
% b = number of type2 trades where C receives class1
% c = number of type3 trades where C gives class2
% d = number of type3 trades where C receives class2

% Net change in class1 for company C: -a + b
% Net change in class2 for company C: +2a - c + 2d
% Net change in class3 for company C: +2c - d

% Let's check each option:

% Option A: RealProp needs -1 class1, +3 class2, -2 class3
% So: -a + b = -1
%     +2a - c + 2d = 3
%     +2c - d = -2
% We need to find non-negative integers a,b,c,d satisfying these equations

% Option B: Southco needs 0 change in all classes
% So: -a + b = 0
%     +2a - c + 2d = 0
%     +2c - d = 0
% This is possible with a=b=c=d=0 (no trades)

% Option C: Southco needs -1 class1, +2 class2, 0 class3
% So: -a + b = -1
%     +2a - c + 2d = 2
%     +2c - d = 0

% Option D: Trustcorp needs +1 class1, -3 class2, +1 class3
% So: -a + b = 1
%     +2a - c + 2d = -3
%     +2c - d = 1

% Option E: Trustcorp needs +1 class1, -2 class2, 0 class3
% So: -a + b = 1
%     +2a - c + 2d = -2
%     +2c - d = 0

% Let's solve these systems of equations
% We'll use ASP to find if solutions exist

% For Option A:
{ a_A(0..10) }.
{ b_A(0..10) }.
{ c_A(0..10) }.
{ d_A(0..10) }.

% Constraints for Option A
:- a_A(A), b_A(B), A - B != 1.  % -a + b = -1 => a - b = 1
:- a_A(A), c_A(C), d_A(D), 2*A - C + 2*D != 3.
:- c_A(C), d_A(D), 2*C - D != -2.

% For Option C:
{ a_C(0..10) }.
{ b_C(0..10) }.
{ c_C(0..10) }.
{ d_C(0..10) }.

% Constraints for Option C
:- a_C(A), b_C(B), A - B != 1.  % -a + b = -1 => a - b = 1
:- a_C(A), c_C(C), d_C(D), 2*A - C + 2*D != 2.
:- c_C(C), d_C(D), 2*C - D != 0.

% For Option D:
{ a_D(0..10) }.
{ b_D(0..10) }.
{ c_D(0..10) }.
{ d_D(0..10) }.

% Constraints for Option D
:- a_D(A), b_D(B), B - A != 1.  % -a + b = 1 => b - a = 1
:- a_D(A), c_D(C), d_D(D), 2*A - C + 2*D != -3.
:- c_D(C), d_D(D), 2*C - D != 1.

% For Option E:
{ a_E(0..10) }.
{ b_E(0..10) }.
{ c_E(0..10) }.
{ d_E(0..10) }.

% Constraints for Option E
:- a_E(A), b_E(B), B - A != 1.  % -a + b = 1 => b - a = 1
:- a_E(A), c_E(C), d_E(D), 2*A - C + 2*D != -2.
:- c_E(C), d_E(D), 2*C - D != 0.

% Check which options are possible
option_a_possible :- a_A(_), b_A(_), c_A(_), d_A(_).
option_c_possible :- a_C(_), b_C(_), c_C(_), d_C(_).
option_d_possible :- a_D(_), b_D(_), c_D(_), d_D(_).
option_e_possible :- a_E(_), b_E(_), c_E(_), d_E(_).

% Option B is always possible (no trades needed)
option_b_possible.

% Show results
#show option_a_possible.
#show option_b_possible.
#show option_c_possible.
#show option_d_possible.
#show option_e_possible.