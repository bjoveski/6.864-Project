%% vector of scores between q and matrix 
function [similarity] = calculate_similarity(question, questions_matrix, type, expected_id, varargin)
    switch type
        case 'cosine'
            similarity = tfidf_score(question, questions_matrix);
        case 'wordnet'
            %similarity = tfidf_score(question * varargin{1}, questions_matrix);
            similarity = wordnet_score(question, questions_matrix, varargin{1});
        case 'trans'
            %similarity = tfidf_score(question * varargin{1}, questions_matrix);
            similarity = query_transl_score(question, questions_matrix, varargin{1});
    end
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
    wordnet_question = wordnet_sim(question~=0,:);
    wordnet_question = diag(question(question~=0)) * wordnet_question;%with count
    score = zeros(size(questions_matrix,1),1);
    similar_terms = wordnet_question;
    num_terms = size(similar_terms,1);
    for i = 1:num_terms
        simmat = (questions_matrix>0) * diag(similar_terms(i,:));
        score = score + max(simmat,[],2);
    end
    score = score/num_terms;
end


%% query likelihood model with translation
function [score] =  query_transl_score(question, questions_matrix, translation_type)
    switch translation_type
        case 'desc'
            load trans_desc_desc
            normalized = diag(1./sum(questions_matrix,2))*questions_matrix;
            translation = normalized * trans_desc_desc;
            logprob = spfun(@log, translation*1e6);
            score = logprob * question';
        case 'title'
            %similarity = tfidf_score(question * varargin{1}, questions_matrix);
            load trans_title_desc
            normalized = diag(1./sum(questions_matrix,2))*questions_matrix;
            translation = normalized * trans_title_desc;
            logprob = spfun(@log, translation*1e6);
            score = logprob * question';
    end
    
end
