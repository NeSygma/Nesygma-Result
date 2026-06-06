% Historians
hist(farley). hist(garcia). hist(holden). hist(jiang).
% Topics
topic(lithographs). topic(oil). topic(sculptures). topic(watercolors).
% Positions
pos(1..4).
% Assign each historian a unique position
{ at(H,P) : pos(P) } = 1 :- hist(H).
% Ensure each position occupied by exactly one historian
:- at(H1,P), at(H2,P), H1 != H2.
% Assign each historian a unique topic
{ talks(H,T) : topic(T) } = 1 :- hist(H).
% Ensure each topic assigned to exactly one historian
:- talks(H1,T), talks(H2,T), H1 != H2.
% Helper: position of a topic
pos_of_topic(T,P) :- at(H,P), talks(H,T).
% Constraints
% oil and water earlier than lithographs
:- pos_of_topic(oil,Po), pos_of_topic(lithographs,Pl), Po >= Pl.
:- pos_of_topic(watercolors,Pw), pos_of_topic(lithographs,Pl), Pw >= Pl.
% Farley earlier than oil
:- at(farley,Pf), pos_of_topic(oil,Po), Pf >= Po.
% Holden earlier than Garcia and Jiang
:- at(holden,Ph), at(garcia,Pg), Ph >= Pg.
:- at(holden,Ph), at(jiang,Pj), Ph >= Pj.
% Option conditions
holds_a :- at(farley,Pf), pos_of_topic(sculptures,Ps), Pf < Ps.
holds_b :- at(holden,Ph), pos_of_topic(lithographs,Pl), Ph < Pl.
holds_c :- pos_of_topic(sculptures,Ps), at(garcia,Pg), Ps < Pg.
holds_d :- pos_of_topic(sculptures,Ps), at(jiang,Pj), Ps < Pj.
holds_e :- pos_of_topic(watercolors,Pw), at(garcia,Pg), Pw < Pg.
#show holds_a/0.
#show holds_b/0.
#show holds_c/0.
#show holds_d/0.
#show holds_e/0.