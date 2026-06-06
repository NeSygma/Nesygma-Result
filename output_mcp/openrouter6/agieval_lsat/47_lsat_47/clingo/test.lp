student(jiang).
play(sunset).
reviews(jiang, sunset).

answer_a :- reviews(jiang, sunset).
answer_b :- reviews(jiang, undulation).

#show answer_a.
#show answer_b.
#show reviews/2.