function [mut_inf] = mutual_information(title_matrix, answers_matrix, THRESHOLD, START, END)
    N = 92789; % number of documents
    num_words = 114268;
    BATCH_SIZE = 5000;
    mut_inf = sparse(num_words, num_words); %sparse(num_words, num_words);
%    save(save_file, 'res')
    
    individual_prob_answer = individual_count(answers_matrix) / N;
    individual_prob_title = individual_count(title_matrix) / N;
    
    i = 1;
    % range = 1:50;
    range = START:END;
    % range = randi([1,num_words], 50);
    % range = range(1,:);
    tic;
    for w_index=range
        % calculate mutual_info prob
        term_col_title = title_matrix(:, w_index);
        mutual_info_prob = mutual_count_col(term_col_title, answers_matrix) / N;
  
        % get p(X_w)
        indiviual_title_w_prob = individual_prob_title(w_index);
        
        [~, rows] = size(mutual_info_prob);
        if rows > 1
            mut_inf(w_index,:) = mutual_information_row(indiviual_title_w_prob, individual_prob_answer, mutual_info_prob, THRESHOLD);
        end
        
        % progress bar
        if (mod(w_index, 128) == 0)
           str = sprintf('processing %5d    frac=%2f', w_index, w_index / (END - START));
           disp(str);
           toc;
           tic;
        end
        
        % flush
        if (i >= BATCH_SIZE)
           str = sprintf('#### outputing %5d #####', w_index);
           disp(str);
           save_file = sprintf('mut_inf_title_ans_%d_%d.mat', BATCH_SIZE, w_index);
           save(save_file, 'mut_inf')
           % reset vars
           i = 0;
           mut_inf = sparse(num_words, num_words);
        end
        
        i = i + 1;
    end
end



%% mutual info
function [wth_row] = mutual_information_row(indiviual_title_w_prob, individual_count_prob, mutual_info_prob, THRESHOLD)
    %% X_w = 1 X_u = 1
    
    p_w = indiviual_title_w_prob;
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
    p_w = indiviual_title_w_prob;
    p_u_row = 1 - individual_count_prob;
    p_wu_row = indiviual_title_w_prob - mutual_info_prob;

    
    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);
    
    %% X_w = 0 X_u = 1
    p_w = 1 - indiviual_title_w_prob;
    p_u_row = individual_count_prob;
    p_wu_row = individual_count_prob - mutual_info_prob;

    wth_row = wth_row + calculate_summand(p_w, p_u_row, p_wu_row);
    
    %% X_w = 0 X_u = 0
    p_w = 1 - indiviual_title_w_prob;
    p_u_row = 1 - individual_count_prob;
    p_wu_row = (1 + mutual_info_prob) - (indiviual_title_w_prob + individual_count_prob);

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
function [mutual_count_row] = mutual_count(w_index, answer_matrix)
    term = answer_matrix(:, w_index);
    term_matrix = (answer_matrix(term>0,:)>0);
    mutual_count_row = sum(term_matrix);
end

function [mutual_count_row] = mutual_count_col(term_col_title, answer_matrix)
    term_matrix = (answer_matrix(term_col_title>0,:)>0);
    mutual_count_row = sum(term_matrix);
end


function [individual_count_row] = individual_count(document_matrix)
    individual_count_row = sum(document_matrix > 0, 1);
end

