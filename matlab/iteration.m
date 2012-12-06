%%retuns how many questions we classified correctly for a given iteration
% ranges from 0 to size(pair_ids)
function [scores] = iteration (testing_matrix, expected_id_vector, corpus_matrix, lambda)
    load wordnet_sim;
    idf = log(331895./(sum(corpus_matrix>0)+1));
    
    scores = zeros(size(testing_matrix,1),1);
    for i = 1:size(testing_matrix,1)
        expected_id = expected_id_vector(i);
        question = testing_matrix(i,:);
        wordnet_question = wordnet_sim(question~=0,:);
        similarity = calculate_similarity(question, corpus_matrix, lambda, idf, wordnet_question);
        scores(i) = similarity_to_score(expected_id, similarity, 10);  
        if (mod(i,10)==0)
            disp(['finished question' num2str(i)])
        end
    end
end