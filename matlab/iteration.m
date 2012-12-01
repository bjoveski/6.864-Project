%%retuns how many questions we classified correctly for a given iteration
% ranges from 0 to size(pair_ids)
function [total_score] = iteration (pair_ids, questions_matrix)
    total_score = 0;
    for i = 1:size(pair_ids,1)
        test_id = pair_ids(i, 1);
        expected_id = pair_ids(i, 2);
        question = questions_matrix(test_id, :);
        lambdas = (1);
        similarity = calculate_similarity(question, questions_matrix, lambdas);
        total_score = total_score + similarity_to_score(expected_id, similarity, 10);  
    end
end