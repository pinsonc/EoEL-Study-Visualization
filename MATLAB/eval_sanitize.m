% Sanitize data and extend timestamps if needed
clear all;


% Load original file
%filename_input = 'Data/20181127_v1_node5_Slave.LOG'
filename_input = 'Data/DATA0A.LOG'
header_length = 1;

file = importdata(filename_input, '\t', header_length);
data_raw = file.data;

dimensions = size(data_raw);

col_time = 1;
col_nr   = 2;

duration_max = 13 * 3600;
epoch_start = 1543357377;
epoch_end   = epoch_start + duration_max;

% Rewrite part
%index_zeros = find(data_raw(:,col_nr) == 0);
index_zeros = find(data_raw(:, col_time) < 100);
index_rewrite_start = 784201;
index_rewrite_end   = dimensions(1);

epoch_time_start = 1543374461;

data_raw(index_rewrite_start:index_rewrite_end,col_time) = epoch_time_start + data_raw(index_rewrite_start:index_rewrite_end,col_time);


% Filter out all non-timestamped data
ranges_chronological = sortrows(data_raw,col_time);
first_valid_index    = find(ranges_chronological(:,col_time) > epoch_start, 1, 'first');
last_valid_index     = find(ranges_chronological(:,col_time) > epoch_end,   1, 'first');
ranges_chronological = ranges_chronological(first_valid_index:(last_valid_index - 1),:);

% Store again
filename_length = size(filename_input);
filename_output = filename_input(1:(filename_length(2)-4)) + "_sanitized.LOG";

%ranges_chronological = int32(ranges_chronological);

save(filename_output, 'ranges_chronological', '-ascii', '-double', '-tabs');