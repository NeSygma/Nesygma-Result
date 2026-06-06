% Clients and targets
client(image). client(solide). client(truvest).
target(1). target(2). target(3).

% Each client has exactly one website target and one voicemail target
1 { website(C, T) : target(T) } 1 :- client(C).
1 { voicemail(C, T) : target(T) } 1 :- client(C).

% Condition 1: website target <= voicemail target for each client
:- website(C, W), voicemail(C, V), W > V.

% Condition 2: Image's voicemail target shorter than others
:- voicemail(image, V_img), voicemail(solide, V_sol), V_img >= V_sol.
:- voicemail(image, V_img), voicemail(truvest, V_tru), V_img >= V_tru.

% Condition 3: Solide's website target shorter than Truvest's website target
:- website(solide, W_sol), website(truvest, W_tru), W_sol >= W_tru.

% Given: Image's website target is 2
website(image, 2).

% Derive that voicemail(image) must be 2
% From website(image,2) and website <= voicemail, we have voicemail(image) >=2.
% From voicemail(image) < voicemail(solide) and voicemail(image) < voicemail(truvest),
% and voicemail(solide), voicemail(truvest) <=3, we have voicemail(image) cannot be 3.
% So voicemail(image) must be 2.
% We can add constraints to enforce this.
:- voicemail(image, 1). % because voicemail(image) >=2
:- voicemail(image, 3). % because then others would have to be >3, impossible.

% Now, we need to check which option must be 2.
% We'll derive the correct answer based on the constraints.

% Option A: Image's voicemail target is 2
% We have already derived that voicemail(image) must be 2.
% So option A is forced.

% Option B: Solide's website target is 2
% Is it forced? Let's see if we can have a valid model where website(solide) != 2.
% We can have website(solide)=1 and website(truvest)=2 or 3.
% So not forced.

% Option C: Solide's voicemail target is 2
% From voicemail(image)=2 and voicemail(image) < voicemail(solide), we have voicemail(solide) >2.
% So voicemail(solide) must be 3. So not 2.

% Option D: Truvest's website target is 2
% Is it forced? We can have website(truvest)=3 and website(solide)=1 or 2.
% So not forced.

% Option E: Truvest's voicemail target is 2
% From voicemail(image)=2 and voicemail(image) < voicemail(truvest), we have voicemail(truvest) >2.
% So voicemail(truvest) must be 3. So not 2.

% Therefore, the only forced option is A.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- voicemail(image, 2).  % condition for A
option(b) :- website(solide, 2).   % condition for B
option(c) :- voicemail(solide, 2). % condition for C
option(d) :- website(truvest, 2).  % condition for D
option(e) :- voicemail(truvest, 2).% condition for E

#show option/1.