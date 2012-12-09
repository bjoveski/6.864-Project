%%translational model
function [score] = translational_model(w_index, document_matrix) %question, questions_matrix)
    %question has to be a vector of description, title with global
    %dictionary

    score = calculate_mutual_info(document_matrix);
    

end





%{
function [mutual_count_matrix] = generate_mutual_count(document_matrix)
    
    mutual_count_matrix = sparse(num_words, num_words);
    tic;
    for w_index=1:num_words
       if (mod(w_index,100) == 0)
           w_index
           nnz(mutual_count_matrix)/w_index
           toc;
           tic;
       end
       mutual_count_matrix(w_index,:) = mutual_count_term(w_index, document_matrix);
    end
    toc;
end



%% calculates I(w;u)
function [] = mutual_information(w_index, u_index, document_matrix)
    

N = size(document_matrix, 1); % not correct, should be non-zero rows
    
    
    
end

function [prob] = single(X_w, w_index, document_matrix, N)
    cnt = nnz(document_matrix(:,w_index));
    if (X_w == 1)
       prob =  cnt / N;
    else
        prob = 1 - (cnt / N);
    end
end


function [prob]  = join_prob(X_w, X_u, w_index, u_index, document_matrix, N)
    mutual = 0; %%idk how :)
    w_cnt = nnz(document_matrix(:,w_index));
    u_cnt = nnz(document_matrix(:,u_index));
    if (X_w==1 && X_u==1)
        prob = mutual / N;
    else if (X_w==1 && X_u==0)
            prob = (w_cnt - mutual) / N;
        else if (X_w==0 && X_u==1)
                prob = (u_cnt - mutual) / N;
            else if (X_w==0 && X_u==0)
                    prob = 1 - ((w_cnt + u_cnt - mutual) / N);
                end
            end
        end
    end
end



%% p_t(w | d) = sum_{u \in d} p_t(w|u) * p(u|d)
function [prob] = translational_model(word, document)
    
end


%%
function [log_prob] = document_model_log(word, document)
    log_prob = log(document_model(word, document));
end

%% returns max-likelihood probability 
%  p_ml(word | document) = c(w, d) / {sum_{w'} c(w',d)}
function [prob] = document_model(word, document)
    prob = count(word, document) / count_total(document);
end

function [cnt] = count(word, document)
    cnt = document(1, word);
end

function [tot_cnt] = count_total(document)
    tot_cnt = sum(document, 2);
end

%}