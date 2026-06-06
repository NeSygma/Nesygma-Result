% History project assignment problem

% Domains
year(1921). year(1922). year(1923). year(1924).
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).

% Option identifiers
option_id(a). option_id(b). option_id(c). option_id(d). option_id(e).

% Assignments for each option (from earliest year to latest)
assign(a, 1921, louis). assign(a, 1922, onyx). assign(a, 1923, ryan). assign(a, 1924, yoshio).
assign(b, 1921, mollie). assign(b, 1922, yoshio). assign(b, 1923, tiffany). assign(b, 1924, onyx).
assign(c, 1921, onyx). assign(c, 1922, ryan). assign(c, 1923, louis). assign(c, 1924, tiffany).
assign(d, 1921, tiffany). assign(d, 1922, onyx). assign(d, 1923, louis). assign(d, 1924, ryan).
assign(e, 1921, yoshio). assign(e, 1922, onyx). assign(e, 1923, louis). assign(e, 1924, mollie).

% Prior year mapping
prior(1922, 1921). prior(1923, 1922). prior(1924, 1923).

% Constraints (violation conditions)
violated(O) :- assign(O, 1923, Student), Student != louis, Student != tiffany.
violated(O) :- assign(O, Year, mollie), Year != 1921, Year != 1922.
violated(O) :- assign(O, _, tiffany), not assign(O, _, ryan).
violated(O) :- assign(O, Year, ryan), not assign(O, Prior, onyx), prior(Year, Prior).

% Derive option if not violated (and each year has exactly one student, which is already ensured by facts)
option(O) :- option_id(O), not violated(O).

% Show the correct option
#show option/1.