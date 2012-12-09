% INDEX:
% 1. cosine title vs title
% 2. cosinetags title vs title
% 3. semantic title vs title
% 4. cosine title vs description
% 5. cosinetags title vs description
% 6. semantic title vs description
% 7. cosine title vs answer
% 8. cosinetags title vs answer
% 9. semantic title vs answer
% 10. cosine description vs title
% 11. cosinetags description vs title
% 12. semantic description vs title
% 13. cosine description vs description
% 14. cosinetags description vs description
% 15. semantic description vs description
% 16. cosine description vs answer
% 17. cosinetags description vs answer
% 18. semantic description vs answer
% 19. cosine tags vs tags
% 20. translation title vs description
% 21. translation title vs answer
% 22. translation description vs description



function ranking = main(simil_index, indices_test)

load duplicates
pairs = pairs_less;
load vectors

lambda = zeros(1,22);
lambda(simil_index)=1;

%choose test 
ind_test = indices_test;
test_id = pairs(ind_test, 1);
test_expected_id = pairs(ind_test, 2);
    
misclass = iteration(test_id, test_expected_id, lambda);
%hist(misclass,50)
end
