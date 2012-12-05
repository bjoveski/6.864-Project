%%retuns how many questions we classified correctly for a given iteration
% ranges from 0 to size(pair_ids)
function [total_score] = iteration (testing_matrix, expected_id_vector, corpus_matrix, lambda)
    load wordnet_sim;
    idf = log(331895./(sum(corpus_matrix>0)+1));
    
    total_score = 0;
    for i = 1:size(testing_matrix,1)
        expected_id = expected_id_vector(i);
        question = testing_matrix(i,:);
        wordnet_question = wordnet_sim(question~=0,:);
        lambdas = (1);
        similarity = calculate_similarity(question, corpus_matrix, lambda, idf, wordnet_question);
        total_score = total_score + similarity_to_score(expected_id, similarity, 10);  
        disp(['finished question' num2str(i)])
    end
end