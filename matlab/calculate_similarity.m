%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, lambda, idf, wordnet_question)
    similarity = zeros(size(questions_matrix,1),1);
    
    if(lambda(1)~=0)
        similarity = similarity + cosine_score(question, questions_matrix);
    end
    if(lambda(2)~=0)
        similarity = similarity + tfidf_score(question, questions_matrix, idf);
    end
    if(lambda(3)~=0)
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
    
%     similar_terms = wordnet_sim(question~=0,:);
%     num_terms = size(similar_terms,1);
%     score = sparse(size(questions_matrix,1),num_terms);
%     J = find(~all(similar_terms==0));
%     for j = J
%         score = max(score, (questions_matrix(:,j)>0) * similar_terms(:,j)');
%     end
%     %disp(fullmax)
%     score = sum(score,2)/num_terms;
end
