%% returns a single value
function [score] = similarity_to_score(expected_id, similarity_vector, TOP_K)
    rank = size(find(similarity_vector > similarity_vector(expected_id)),1);
    if (rank < TOP_K)
        score = 0;
    else
        score = 1;
    end
    score = min(rank,1000);
end