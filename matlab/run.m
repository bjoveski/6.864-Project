load trans_desc_desc
load vectors
step = 10e3;

questions_matrix = M_desc_global;
trans_prob = trans_desc_desc;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse([],[],[],size(normalized,1),size(normalized,2),5e6);

for i=1:step:size(normalized,1)
    rows = i:min(i+step,size(normalized,1));
    aux = normalized(rows,:) * trans_prob;
    aux = aux.*(aux>7e-4);
    translation(rows,:) = aux;
    disp(i)
    disp(nnz(translation)/(step+i))
end

T_desc_desc = translation;

load trans_desc_ans
questions_matrix = M_desc_global;
trans_prob = trans_desc_ans;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse([],[],[],size(normalized,1),size(normalized,2),5e6);

for i=1:step:size(normalized,1)
    rows = i:min(i+step,size(normalized,1));
    aux = normalized(rows,:) * trans_prob;
    aux = aux.*(aux>2e-5);
    translation(rows,:) = aux;
    disp(i)
    disp(nnz(translation)/(step+i))
end

T_desc_ans = translation;

load trans_title_desc
questions_matrix = M_title_global;
trans_prob = trans_title_desc;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse([],[],[],size(normalized,1),size(normalized,2),5e6);

for i=1:step:size(normalized,1)
    rows = i:min(i+step,size(normalized,1));
    aux = normalized(rows,:) * trans_prob;
    aux = aux.*(aux>4e-4);
    translation(rows,:) = aux;
    disp(i)
    disp(nnz(translation)/(step+i))
end

T_title_desc = translation;

load vectors
load trans_title_answer
questions_matrix = M_title_global;
trans_prob = trans_title_answer;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse([],[],[],size(normalized,1),size(normalized,2),5e6);

for i=1:step:size(normalized,1)
    rows = i:min(i+step,size(normalized,1));
    aux = normalized(rows,:) * trans_prob;
    aux = aux.*(aux>3e-5);
    translation(rows,:) = aux;
    disp(i)
    disp(nnz(translation)/(step+i))
end

T_title_ans = translation;

save('Translated','T_title_ans','T_title_desc','T_desc_ans','T_desc_desc')
