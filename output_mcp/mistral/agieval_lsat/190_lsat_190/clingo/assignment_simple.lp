% Domains
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).
year(1921). year(1922). year(1923). year(1924).

% Base assignment relation
1 { assigned(S, Y) : student(S) } 1 :- year(Y).
1 { assigned(S, Y) : year(Y) } 1 :- student(S).

% Map the options to conditions
% Option A: Louis, Onyx, Ryan, Yoshio (1921: Louis, 1922: Onyx, 1923: Ryan, 1924: Yoshio)
option(a) :- assigned(louis, 1921), assigned(onyx, 1922), assigned(ryan, 1923), assigned(yoshio, 1924).

% Option B: Mollie, Yoshio, Tiffany, Onyx (1921: Mollie, 1922: Yoshio, 1923: Tiffany, 1924: Onyx)
option(b) :- assigned(mollie, 1921), assigned(yoshio, 1922), assigned(tiffany, 1923), assigned(onyx, 1924).

% Option C: Onyx, Ryan, Louis, Tiffany (1921: Onyx, 1922: Ryan, 1923: Louis, 1924: Tiffany)
option(c) :- assigned(onyx, 1921), assigned(ryan, 1922), assigned(louis, 1923), assigned(tiffany, 1924).

% Option D: Tiffany, Onyx, Louis, Ryan (1921: Tiffany, 1922: Onyx, 1923: Louis, 1924: Ryan)
option(d) :- assigned(tiffany, 1921), assigned(onyx, 1922), assigned(louis, 1923), assigned(ryan, 1924).

% Option E: Yoshio, Onyx, Louis, Mollie (1921: Yoshio, 1922: Onyx, 1923: Louis, 1924: Mollie)
option(e) :- assigned(yoshio, 1921), assigned(onyx, 1922), assigned(louis, 1923), assigned(mollie, 1924).

#show option/1.