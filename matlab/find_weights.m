K=10;
N=200;
C=19;
a_test=1000*ones(K,N);
L=zeros(1,C);
Score=zeros(3,10);
W=ones(N,1)/N;
for k=1:K
Penalty=a(1:C,1:N)*W;
S=find(Penalty==min(Penalty),1);
L(S)=L(S)+1;
a_test(k,:)=old_main(L,N);
W=W+a_test(k,:)';
Score(1,k)=size(find(a_test(k,:)==0));
Score(2,k)=size(find(a_test(k,:)<=5));
Score(3,k)=size(find(a_test(k,:)<=10));
end