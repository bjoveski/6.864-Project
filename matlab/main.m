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

function main(index, size_test)

load duplicates
pairs = pairs_less;
load vectors

%choose test 
ind_test = mod((1:size_test)*37,2347)+1;
test_id = pairs(ind_test, 1);
test_expected_id = pairs(ind_test, 2);


i=index;
        aspect = get_question_aspect(i);
        dictionary = get_dictionary(i);
        str_test = ['test_matrix = M_' aspect '_' dictionary '(test_id,:);'];
        aspect = get_corpus_aspect(i);
        str_corpus = ['corpus_matrix = M_' aspect '_' dictionary ';'];
        eval(str_test);
        eval(str_corpus);
        lambda = get_lambda(i);
    
        misclass = iteration(test_matrix, test_expected_id, corpus_matrix,lambda);
        hist(misclass,50)

end

%% parsing functions

function aspect = get_question_aspect(i)
    if(i<=9)
        aspect = 'title';
    elseif(i<=18)
        aspect = 'desc';
    else
        aspect = 'tag';
    end
end


function dict = get_dictionary(i)
    if (i==18 || mod(i,3)==2)
        dict = 'alltags';
    else
        dict = 'global';
    end
end

function aspect = get_corpus_aspect(i)
    if(i==19)
        aspect = 'tag';
    else
        j = mod(i,9);
        if(j<=3)
            aspect = 'title';
        elseif(j<=6)
            aspect = 'desc';
        else
            aspect = 'ans';
        end
    end
end


function lambda =get_lambda(i)
    if(mod(i,3)==3)
        lambda = [0 1];
    else
        lambda = [1 0];
    end
end