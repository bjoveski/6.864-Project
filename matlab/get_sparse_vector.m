%% Main function to read a file (maybe huge)
% returns all vectors as rows of V
% warning: I am using sed to split the file

function [V , id_full] = get_sparse_vector(filename)

    %correct file name
    filename = strrep(filename,' ','\ ');
    
    %split huge file into smaller files
    N = 92789;
    step = 10e3;
    enum_full =[];
    index_full =[];
    count_full =[];
    id_full=[];
    for i = 1:step:N
        f = min(i+step-1,N);
        !rm deleteme.txt
        system(sprintf('sed -n %d,%dp %s >> deleteme.txt',i,f,filename));
        [enum,index,count,id] = read_small_file('deleteme.txt');
        enum_full = [enum_full;enum+i-1];
        index_full = [index_full;index];
        count_full = [count_full;count];
        id_full = [id_full;id];
        fprintf('finished lines %d to %d\n',i,f)
    end
    V = sparse(enum_full,index_full,count_full);

end

%% Read small file

function [enum,index,count,id] = read_small_file(filename)
    M = csvread(filename);
    id = M(:,1);
    M = M(:,2:end);
    numvec = size(M,1);
    col = size(M,2);
    if(mod(col,2))
        M=[M zeros(numvec,1)];
        col=col+1;
    end
    
    enum = repmat(transpose(1:numvec),[col/2 1]);
    even = 2:2:col;
    odd = even-1;
    index = reshape(M(:,odd),[numel(M)/2 1]);
    count = reshape(M(:,even),[numel(M)/2 1]);
    
    nonz = find(index ~= 0);
    enum = enum(nonz);
    index = index(nonz);
    count = count(nonz);
end
