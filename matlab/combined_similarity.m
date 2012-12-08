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

function sim = combined_similarity(ques_vectors, corpus_matrices, lambda, wordnet_sim)
    corpus_title_global = corpus_matrices{1};
    corpus_desc_global = corpus_matrices{2};
    corpus_ans_global = corpus_matrices{3};
    corpus_title_alltags = corpus_matrices{4};
    corpus_desc_alltags = corpus_matrices{5};
    corpus_tag_alltags = corpus_matrices{6};
    corpus_ans_alltags = corpus_matrices{7};

    sim = zeros(size(corpus_matrices,1),1);
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_title_global,lambda([1,3,10,12]),'global', wordnet_sim);
    sim = sim + combined_single_corpus(ques_vectors,corpus_desc_global,lambda([4,6,13,15]),'global', wordnet_sim);
    sim = sim + combined_single_corpus(ques_vectors,corpus_ans_global,lambda([7,9,16,18]),'global', wordnet_sim);
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_title_alltags,lambda([2,11]),'alltags', wordnet_sim);
    sim = sim + combined_single_corpus(ques_vectors,corpus_desc_alltags,lambda([5,14]),'alltags', wordnet_sim);
    sim = sim + combined_single_corpus(ques_vectors,corpus_ans_alltags,lambda([8,17]),'alltags', wordnet_sim);
    
    sim = sim + combined_single_corpus(ques_vectors,corpus_tag_alltags,lambda(19),'onlytags', wordnet_sim);

end

function sim = combined_single_corpus(ques_vectors, corpus_matrix, red_lambda, dictionary, wordnet_sim)
    ques_title_global = ques_vectors{1};
    ques_desc_global = ques_vectors{2};
    ques_title_alltags = ques_vectors{3};
    ques_desc_alltags = ques_vectors{4};
    ques_tag_alltags = ques_vectors{5};
    
    sim = zeros(size(corpus_matrix,1),1);
    
    if strcmp(dictionary,'global')
        if (red_lambda(1)~=0)
            sim = sim + red_lambda(1)*calculate_similarity(ques_title_global, corpus_matrix, 'cosine');
        end
        if (red_lambda(2)~=0)
            sim = sim + red_lambda(2)*calculate_similarity(ques_title_global, corpus_matrix, 'wordnet', wordnet_sim);
        end
        if (red_lambda(3)~=0)
            sim = sim + red_lambda(3)*calculate_similarity(ques_desc_global, corpus_matrix, 'cosine');
        end
        if (red_lambda(4)~=0)
            sim = sim + red_lambda(4)*calculate_similarity(ques_desc_global, corpus_matrix, 'wordnet', wordnet_sim);
        end
    
    elseif strcmp(dictionary,'alltags')
        if (red_lambda(1)~=0)
            sim = sim + red_lambda(1)*calculate_similarity(ques_title_alltags, corpus_matrix, 'cosine');
        end
        if (red_lambda(2)~=0)
            sim = sim + red_lambda(2)*calculate_similarity(ques_desc_alltags, corpus_matrix, 'cosine');
        end
        
    elseif strcmp(dictionary,'onlytags')
        if (red_lambda~=0)
            sim = sim + red_lambda*calculate_similarity(ques_tag_alltags, corpus_matrix, 'cosine');
        end
    end
end
