%% returns a single value
function [score] = similarity_to_score(expected_id, similarity_vector)
    rank = sum(similarity_vector >= similarity_vector(expected_id));
    score = min(rank-1,1000);
end