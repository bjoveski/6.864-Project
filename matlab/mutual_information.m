function [mut_inf] = mutual_information(document_matrix, THRESHOLD, NUM_ROWS)
    N = 92789; % number of documents
    num_words = 114268;
    BATCH_SIZE = 5000;
    mut_inf = sparse(NUM_ROWS, num_words); %sparse(num_words, num_words);
%    save(save_file, 'res')
    
    individual_prob = individual_count(document_matrix) / N;
    
    i = 1;
    % range = 1:50;
    range = 1:NUM_ROWS;
    % range = randi([1,num_words], 50);
    % range = range(1,:);
    tic;
    for w_index=range
        mutual_info_prob = mutual_count(w_index, document_matrix) / N;
        [~, rows] = size(mutual_info_prob);
        if rows > 1
            mut_inf(w_index,:) = mutual_information_row(w_index, individual_prob, mutual_info_prob, THRESHOLD);
        end
        
        % progress bar
        if (mod(w_index, 128) == 0)
           str = sprintf('processing %5d    frac=%2f', w_index, w_index / NUM_ROWS);
           disp(str);
           toc;
           tic;
        end
        
        % flush
        if (i >= BATCH_SIZE)
           str = sprintf('#### outputing %5d #####', w_index);
           disp(str);
           save_file = sprintf('mut_inf_%d_%d.mat', BATCH_SIZE, w_index);
           save(save_file, 'mut_inf')
           % reset vars
           i = 0;
           mut_inf = sparse(NUM_ROWS, num_words);
        end
        
        i = i + 1;
    end
end



%% mutual info
function [wth_row] = mutual_information_row(w_index, individual_count_prob, mutual_info_prob, THRESHOLD)
    %% X_w = 1 X_u = 1
    
    p_w = individual_count_prob(w_index);
    p_u_row = individual_count_prob;
    p_wu_row = mutual_info_prob;

    %{
    disp('####');
    size(p_w)
    size(p_u_row)
    size(p_wu_row)
    %}
    
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
    p_wu_row = (1 + mutual_info_prob) - (individual_count_prob(w_index) + individual_count_prob);

    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);

    % clean up
    wth_row(isnan(wth_row)) = 0;
    wth_row = wth_row.*(wth_row > THRESHOLD);
end



function [mut_inf_row] = calculate_summand(p_w, p_u_row, p_wu_row)
    prob = p_wu_row./(p_w * p_u_row);
    
    log_prob = log(prob);
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

