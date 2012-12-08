mutual=sparse(114268,114268);
count=0;
for i= 5e3:5e3:110e3
    load(['mut_inf_5000_' num2str(i) '.mat'])
    mut = mut_inf.*(mut_inf>0.00007);
    x = nnz(mutual) + nnz(mut);
    mutual = mutual + mut;
    disp(nnz(mutual) - x)
end
