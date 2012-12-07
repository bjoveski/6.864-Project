function [res] = mutual_information(document_matrix)
    N = 92789; % number of documents
    num_words = 114268;
    res = zeros(10, num_words); %sparse(num_words, num_words);
    
    individual_prob = individual_count(document_matrix) / N;
    
    for w_index=1:10
        mutual_info_prob = mutual_count(w_index, document_matrix) / N;
        res(w_index,:) = mutual_information_row(w_index, individual_prob, mutual_info_prob);
    end
end

%% mutual info
function [wth_row] = mutual_information_row(w_index, individual_count_prob, mutual_info_prob)
    %% X_w = 1 X_u = 1
    p_w = individual_count_prob(w_index);
    p_u_row = individual_count_prob;
    p_wu_row = mutual_info_prob;
    
    wth_row = calculate_summand(p_w, p_u_row, p_wu_row);
    
    %% X_w = 1 X_u = 0
    p_w = individual_count_prob(w_index);
    p_u_row = 1 - individual_count_prob;
    p_wu_row = individual_count_prob(w_index) - mutual_info_prob;
    
    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);
    
    %% X_w = 0 X_u = 1
    p_w = 1 - individual_count_prob(w_index);
    p_u_row = individual_count_prob;
    p_wu_row = individual_count_prob - mutual_info_prob;
    
    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);
    
    %% X_w = 0 X_u = 0
    p_w = 1 - individual_count_prob(w_index);
    p_u_row = 1 - individual_count_prob;
    p_wu_row = (1 - individual_count_prob(w_index)) - (individual_count_prob - mutual_info_prob);
    
    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);
    
end



function [mut_inf_row] = calculate_summand(p_w, p_u_row, p_wu_row)
    log_prob = log(p_wu_row./(p_u_row * p_w));
    mut_inf_row = times(p_wu_row, log_prob); % maybe adding > 0.0001 or sth to dramatically reduce dimensionality
end


%% function compute mutual count
% mutual_count_row(1,i) = number of docs s.t. count(w_index=1, i=1)
function [mutual_count_row] = mutual_count(w_index, document_matrix)
    term = document_matrix(:, w_index);
    term_matrix = (document_matrix(term>0,:)>0);
    mutual_count_row = sum(term_matrix);
end

function [individual_count_row] = individual_count(document_matrix)
    individual_count_row = sum(document_matrix > 0, 1);
end

