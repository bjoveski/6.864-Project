%load ranking

ranking_corr = ranking_pair -(ranking_pair>ranking_same);

%maximum vs sim10
hist([min(min(ranking_corr,21),[],2) min(ranking_corr(:,10),21)],10)
title('Ranking histogram')
legend('Best similarity','tf-idf similarity')
grid on
xlabel('Ranking')
ylabel('Frequency')
axis([0 21 0 1800])
set(gca, 'XTickLabel',{'0' '2'     '4'     '6'     '8'    '10'    '12'    '14'    '16'    '18'    'higher'})

print -painters -dpdf -r200 hist_best_vs_10.pdf

%cosine bag of words
ind = [1:3:18];
rank = ranking_corr(:,ind);
topk=[5,10,20];
perf_corr=zeros(3,length(ind))';
for i = 1:3
    perf_corr(:,i) = sum( rank <topk(i))/2000 *100;
end
bar(perf_corr)
legend('Top 5','Top 10', 'Top 20')
axis([0 7 0 100])
grid on
title('Standard tf-idf similarity')
ylabel('Performance (%)')
set(gca, 'XTickLabel',{'Title-Title' 'Title-Desc' 'Title-Ans' 'Desc-Title' 'Desc-Desc' 'Desc-Ans'})

print -painters -dpdf -r200 perf_cosine_global.pdf

%cosine tags
ind = [19 2:3:18];
rank = ranking_corr(:,ind);
topk=[5,10,20];
perf_corr=zeros(3,length(ind))';
for i = 1:3
    perf_corr(:,i) = sum( rank <topk(i))/2000 *100;
end
bar(perf_corr)
legend('Top 5','Top 10', 'Top 20')
axis([0 8 0 100])
grid on
title('Tag based tf-idf similarity')
ylabel('Performance (%)')
set(gca, 'XTickLabel',{'User tags' 'Title-Title' 'Title-Desc' 'Title-Ans' 'Desc-Title' 'Desc-Desc' 'Desc-Ans' })

print -painters -dpdf -r200 perf_cosine_tags.pdf

%wordnet
ind = [3:3:18];
rank = ranking_corr(:,ind);
topk=[5,10,20];
perf_corr=zeros(3,length(ind))';
for i = 1:3
    perf_corr(:,i) = sum( rank <topk(i))/2000 *100;
end
bar(perf_corr)
legend('Top 5','Top 10', 'Top 20')
axis([0 7 0 100])
grid on
title('Wordnet based similarity')
ylabel('Performance (%)')
set(gca, 'XTickLabel',{'Title-Title' 'Title-Desc' 'Title-Ans' 'Desc-Title' 'Desc-Desc' 'Desc-Ans'})

print -painters -dpdf -r200 perf_wordnet.pdf

%Query likl.mdl no trans
ind = [20:23];
rank = ranking_corr(:,ind);
topk=[5,10,20];
perf_corr=zeros(3,length(ind))';
for i = 1:3
    perf_corr(:,i) = sum( rank <topk(i))/2000 *100;
end
bar(perf_corr)
legend('Top 5','Top 10', 'Top 20')
axis([0 5 0 100])
grid on
title('Query likelihood model')
ylabel('Performance (%)')
set(gca, 'XTickLabel',{'Basic Title' 'Basic Desc' 'Transl. Title' 'Transl. Desc'})

print -painters -dpdf -r200 perf_query_mdl.pdf

