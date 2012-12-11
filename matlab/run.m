% load trans_desc_desc
% load trans_title_desc
% load titles
step = 10e3;

questions_matrix = M_title_global;


trans_prob = wordnet_sim;
normalized = diag(sparse(1./sum(questions_matrix,2)))*questions_matrix;
translation = sparse([],[],[],size(normalized,1),size(normalized,2),5e6);

for i=1:step:size(normalized,1)
    rows = i:min(i+step,size(normalized,1));
    aux = normalized(rows,:) * trans_prob;
    aux = aux.*(aux>2.8e-1);
    translation(rows,:) = aux;
    disp(i)
    disp(nnz(translation)/(step+i))
end

%dd,dt,wnet
T_title_desc_wnet = translation;

save('Translated2_title_desc','T_title_desc_dd','T_title_desc_dt','T_title_desc_wnet')

save('ranks25_alpha','ranks25_1e6','ranks25_1e5','ranks25_1e4','ranks25_1e3','ranks25_1e2','ranks25_1e1','ranks25_50')