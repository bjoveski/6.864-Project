%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, lambdas)

    s1 = cosine_score(question, questions_matrix); % vector 
    s2 = tfidf_score(question, questions_matrix);
    
    similarity = lambdas(1) * s1 + lambdas(1) * s2;
end


function [score] =  cosine_score(question, questions_matrix)
    score = questions_matrix * question'./ (.1+norm(question)*sqrt(sum(questions_matrix.^2,2)));
end

function [score] =  tfidf_score(question, questions_matrix)
    idf = log(331895./(sum(questions_matrix>0)+1));
    score = cosine_score(question.*idf, questions_matrix);
end

%% returns a single value
function [score] = similarity_to_score(expected, similarity_vector, TOP_K)
    rank = size(find(similarity_vector > similarity_vector(expected)),1);
    if (rank < TOP_K)
        score = 1;
    else
        score = 0;
    end
end