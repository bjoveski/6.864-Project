%%retuns how many questions we classified correctly for a given iteration
% ranges from 0 to size(pair_ids)
function [scores] = iteration (test_ids, expected_ids, lambda)
    load vectors;
    load Translated;
    
    corpus_matrices = {M_title_global,M_desc_global,M_ans_global,M_title_alltags,M_desc_alltags,M_tag_alltags,M_ans_alltags};
    translated_matrices = {T_title_desc,T_title_ans,T_desc_desc,T_desc_ans};
        
    scores = zeros(length(test_ids),2);
    for i = 1:length(test_ids)
        id = test_ids(i);
        expected_id = expected_ids(i);
        ques_vectors = {M_title_global(id,:),M_desc_global(id,:),M_title_alltags(id,:),M_desc_alltags(id,:),M_tag_alltags(id,:)};
        similarity = combined_similarity(ques_vectors, corpus_matrices, translated_matrices, lambda, expected_id);
        scores(i,1) = similarity_to_score(expected_id, similarity);  
        scores(i,2) = similarity_to_score(id, similarity);  
        if(mod(i,10)==0)
            disp(['finished question' num2str(i)])
        end
    end
end
