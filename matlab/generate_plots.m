load ranking

%maximum vs sim10
hist([min(min(ranking_pair,20),[],2) min(ranking_pair(:,10),20)],20)
title('Ranking histogram')
legend('Best similarity','tf-idf similarity')
grid on


