%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, lambda, idf, wordnet_question)
    similarity = zeros(size(questions_matrix,1),1);
    
    if(lambda(1)~=0)
        similarity = similarity + tfidf_score(question, questions_matrix, idf);
    end
    if(lambda(2)~=0)
        similarity = similarity + wordnet_score(question, questions_matrix, wordnet_question);
    end
end

%% cosine
function [score] =  cosine_score(question, questions_matrix)
    score = questions_matrix * question'./ (.1+norm(question)*sqrt(sum(questions_matrix.^2,2)));
end

%% tfidf 
function [score] =  tfidf_score(question, questions_matrix, idf)
    score = cosine_score(question.*idf, questions_matrix);
end

%% wordnet ONLY FOR GLOBAL DICTIONARY
function [score] =  wordnet_score(~, questions_matrix, wordnet_question)
    score = zeros(size(questions_matrix,1),1);
    similar_terms = wordnet_question;
    num_terms = size(similar_terms,1);
    for i = 1:size(similar_terms,1)
        simmat = (questions_matrix>0) * diag(similar_terms(i,:));
        score = score + max(simmat,[],2);
    end
    score = score/num_terms;
end


%% query likelihood model
function [score] =  query_score(question, questions_matrix)
    score = zeros(size(questions_matrix,1),1);
    similar_terms = wordnet_question;
    num_terms = size(similar_terms,1);
    for i = 1:size(similar_terms,1)
        simmat = (questions_matrix>0) * diag(similar_terms(i,:));
        score = score + max(simmat,[],2);
    end
    score = score/num_terms;
end

%% query likelihood model with translation
function [score] =  query_transl_score(question, questions_matrix, transl_mdl)
    query_score(question*transl_mdl, questions_matrix)
end