%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, lambdas)

    s1 = cosine_score(question, questions_matrix); % vector 
 %   s2 = tfidf(question, questions_matrix);
    
 %   similarity = lambdas(1) * (s1) + lambdas(2) * (s2);
    similarity = lambdas(1) * (s1);
end


function [cos_score] =  cosine_score(question, questions_matrix)
    cos_score = question * questions_matrix;
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