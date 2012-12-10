function [rank_pair rank_same] = compute_all_sim(test_ind)

    N=23;
    I = eye(N);

    rank_pair = zeros(length(test_ind),N);
    rank_same = zeros(length(test_ind),N);

    for i=1:N
        disp(['Similarity' num2str(i)]);
        scores = main(I(i,:),test_ind);
        rank_pair(:,i) = scores(:,1);
        rank_same(:,i) = scores(:,2);
        fprintf('Finished\n\n')
    end

end