load duplicates
load vectors

size_train = 100;
size_test = 100;

rand_ind = randperm(length(pairs));
ind_train = rand_ind(1:size_train);
ind_test = rand_ind(size_train+1:size_train+size_test);

train_id = pairs(ind_train, 1);
train_expected_id = pairs(ind_train, 2);


test_id = pairs(ind_test, 1);
test_expected_id = pairs(ind_test, 2);
test_matrix = M_desc_global(test_id,:);

questionAttributes = ['title','desc','tag'];
corpusAttributes = ['title','desc','tag','ans'];

train_matrix = M_title_global(train_id,:);

totalscore = iteration(test_matrix, test_expected_id, M_desc_global,[0 1 0]);
disp(['Total score: ' num2str(totalscore)])
