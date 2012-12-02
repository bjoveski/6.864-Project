%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, lambdas, wordnet_sim)

    s1 = cosine_score(question, questions_matrix); % vector 
    s2 = tfidf_score(question, questions_matrix);
    s3 = wordnet_score(question, questions_matrix, wordnet_sim);
    
    similarity = lambdas(1) * s1 + lambdas(1) * s2 + lambdas(1) * s3;
end

%% cosine
function [score] =  cosine_score(question, questions_matrix)
    score = questions_matrix * question'./ (.1+norm(question)*sqrt(sum(questions_matrix.^2,2)));
end

%% tfidf 
function [score] =  tfidf_score(question, questions_matrix)
    idf = log(331895./(sum(questions_matrix>0)+1));
    score = cosine_score(question.*idf, questions_matrix);
end

%% wordnet ONLY FOR GLOBAL DICTIONARY
function [score] =  wordnet_score(question, questions_matrix, wordnet_sim)
    %load wordnet_sim
    score = zeros(size(questions_matrix,1),1);
    similar_terms = wordnet_sim(find(question),:);
    for i = 1:size(similar_terms,1)
        simmat = (questions_matrix>0) * diag(similar_terms(i,:));
        score = score + max(simmat,[],2);
    end
    
end