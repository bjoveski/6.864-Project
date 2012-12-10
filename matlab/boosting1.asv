N=300;
M=17;
PP=a/300;
W=ones(1,N)/N;
L=zeros(M,1);
for i=1:17
    G=W*PP';
    k=find(G==min(G),1);
    L(k)=1-(G(k)/sum(W));
    W=W+N*PP(k,:);
    PP(k,:)=N*ones(1,N);
end