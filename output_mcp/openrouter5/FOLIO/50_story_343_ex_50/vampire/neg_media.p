% Negative version: negated claim as conjecture
% Premises:
% 1. No digital media are analog.
fof(premise1, axiom, ! [X] : (digital_media(X) => ~analog(X))).

% 2. Every printed text is analog media.
fof(premise2, axiom, ! [X] : (printed_text(X) => analog(X))).

% 3. All streaming services are digital media.
fof(premise3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).

% 4. If an object is a hardcover book, then it is printed text.
fof(premise4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).

% 5. If 1984 is a streaming service, then 1984 is a hardcover book.
fof(premise5, axiom, (streaming_service(s1984) => hardcover_book(s1984))).

% Negated conclusion: 1984 is NOT a streaming service.
fof(neg_conclusion, conjecture, ~streaming_service(s1984)).