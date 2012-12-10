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

function misclass=old_main(lambda, size_test)

load duplicates
pairs = pairs_less;
load vectors

%choose test 
ind_test = mod((1:size_test)*37,2347)+1;
test_id = pairs(ind_test, 1);
test_expected_id = pairs(ind_test, 2);
    
misclass = iteration(test_id, test_expected_id, lambda);
%hist(misclass,50)
end