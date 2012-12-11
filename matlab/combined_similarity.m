% INDEX:
% 1. cosine title vs title
% 2. cosinetags title vs title
% 3. semantic title vs title
% 4. cosine title vs description
% 5. cosinetags title vs description
% 6. semantic title vs description
% 7. cosine title vs answer
% 8. cosinetags title vs answer
% 9. semantic title vs answer
% 10. cosine description vs title
% 11. cosinetags description vs title
% 12. semantic description vs title
% 13. cosine description vs description
% 14. cosinetags description vs description
% 15. semantic description vs description
% 16. cosine description vs answer
% 17. cosinetags description vs answer
% 18. semantic description vs answer
% 19. cosine tags vs tags
% 20. query likelihook title vs desc
% 21. query likelihook desc vs desc
% 22. translation description vs title
% 23. translation description vs description
% 24. query likelihook title vs title
% 25. query likelihook desc vs title

function sim = combined_similarity(ques_vectors, corpus_matrices, translated_matrices, lambda, expected_id)
    corpus_title_global = corpus_matrices{1};
    corpus_desc_global = corpus_matrices{2};
    corpus_ans_global = corpus_matrices{3};
    corpus_title_alltags = corpus_matrices{4};
    corpus_desc_alltags = corpus_matrices{5};
    corpus_tag_alltags = corpus_matrices{6};
    corpus_ans_alltags = corpus_matrices{7};
    
    T_title_desc = translated_matrices{1};
    T_title_ans = translated_matrices{2};
    T_desc_desc = translated_matrices{3};
    T_desc_ans = translated_matrices{4};
    
    sim = zeros(size(corpus_matrices,1),1); 
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_title_global,lambda([1,3,10,12,24,25]),'global', expected_id);
    sim = sim + combined_single_corpus(ques_vectors,corpus_desc_global,lambda([4,6,13,15,20,21]),'global', expected_id);
    sim = sim + combined_single_corpus(ques_vectors,corpus_ans_global,lambda([7,9,16,18]),'global', expected_id);
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_title_alltags,lambda([2,11]),'alltags', expected_id);
    sim = sim + combined_single_corpus(ques_vectors,corpus_desc_alltags,lambda([5,14]),'alltags', expected_id);
    sim = sim + combined_single_corpus(ques_vectors,corpus_ans_alltags,lambda([8,17]),'alltags', expected_id);
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_tag_alltags,lambda(19),'onlytags', expected_id);
    
    %translations 
    sim = sim + combined_single_corpus(ques_vectors,T_title_desc,lambda(22),'trans_desc', expected_id);
    sim = sim + combined_single_corpus(ques_vectors,T_desc_desc,lambda(23),'trans_desc', expected_id);
end

function sim = combined_single_corpus(ques_vectors, corpus_matrix, red_lambda, dictionary, expected_id, varargin)
    ques_title_global = ques_vectors{1};
    ques_desc_global = ques_vectors{2};
    ques_title_alltags = ques_vectors{3};
    ques_desc_alltags = ques_vectors{4};
    ques_tag_alltags = ques_vectors{5};
    
    
    sim = zeros(size(corpus_matrix,1),1);
    
    if strcmp(dictionary,'global')
        if (red_lambda(1)~=0)
            sim = sim + red_lambda(1)*calculate_similarity(ques_title_global, corpus_matrix, 'cosine', expected_id,varargin);
        end
        if (red_lambda(2)~=0)
            load wordnet_sim
            sim = sim + red_lambda(2)*calculate_similarity(ques_title_global, corpus_matrix, 'wordnet', expected_id, wordnet_sim);
        end
        if (red_lambda(3)~=0)
            sim = sim + red_lambda(3)*calculate_similarity(ques_desc_global, corpus_matrix, 'cosine', expected_id);
        end
        if (red_lambda(4)~=0)
            load wordnet_sim
            sim = sim + red_lambda(4)*calculate_similarity(ques_desc_global, corpus_matrix, 'wordnet', expected_id, wordnet_sim);
        end
        if (length(red_lambda)==6)
            if (red_lambda(5)~=0)
            	sim = sim + red_lambda(5)*calculate_similarity(ques_title_global, corpus_matrix, 'trans', expected_id);
            end
            if (red_lambda(6)~=0)
            	sim = sim + red_lambda(6)*calculate_similarity(ques_desc_global, corpus_matrix, 'trans', expected_id);
            end
        end
    
    elseif strcmp(dictionary,'alltags')
        if (red_lambda(1)~=0)
            sim = sim + red_lambda(1)*calculate_similarity(ques_title_alltags, corpus_matrix, 'cosine', expected_id);
        end
        if (red_lambda(2)~=0)
            sim = sim + red_lambda(2)*calculate_similarity(ques_desc_alltags, corpus_matrix, 'cosine', expected_id);
        end
        
    elseif strcmp(dictionary,'onlytags')
        if (red_lambda~=0)
            sim = sim + red_lambda*calculate_similarity(ques_tag_alltags, corpus_matrix, 'cosine', expected_id);
        end
        
    elseif strcmp(dictionary,'trans_desc')
        if (red_lambda~=0)
            sim = sim + red_lambda(1)*calculate_similarity(ques_desc_global, corpus_matrix, 'cosine', expected_id);
        end
    end
end
