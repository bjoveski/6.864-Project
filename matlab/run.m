load trans_desc_desc
load vectors
questions_matrix = M_desc_global;
trans_prob = trans_desc_desc;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse(size(normalized,1),size(normalized,2));
for i=1:size(normalized,1)
    aux = normalized(i,:) * trans_prob;
    sorted = sort(aux,2,'descend');
    translation(i,:) = aux.*(aux>sorted(20));
    if(mod(i,1000)==0)
        disp(i)
    end
end