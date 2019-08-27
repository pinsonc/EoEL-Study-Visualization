% Calculate statistics and plots
clear all;

% General configs
num_channels = 30;

percentile = 50;
avg_span_1 = 1;
avg_span_2 = 10;

duration_measurement = 10 * 3600;
%epoch_start = 1543357200;
epoch_start = 18;
epoch_end   = epoch_start + duration_measurement;

% Import data
%filename = 'Data/20181127_v1_node9_Master_sanitized.LOG'
filename = 'Data/DATA0A_clean.LOG'
header_length = 0;

file = importdata(filename, '\t', header_length);
data_raw = file;

col_time = 1;
col_nr   = 2;
col_id   = 3;
col_chan = 4;
col_meas = 5;

dimensions = size(data_raw);
num_measurements = dimensions(1) / num_channels;

% Filter out all non-timestamped data
ranges_chronological = sortrows(data_raw,col_time);
% first_valid_index    = find(ranges_chronological(:,col_time) > epoch_start, 1, 'first');
% ranges_chronological = ranges_chronological(first_valid_index:dimensions(1),:);
% 
% dimensions = size(ranges_chronological);
% num_measurements = int32(dimensions(1) / num_channels);


% Convert uint32 to int32 to get correct negative ranges
ranges_chronological(:,col_meas) = typecast(uint32(ranges_chronological(:,col_meas)),'int32');

% Find number of IDs
ids = unique(ranges_chronological(:,col_id));
ids_dim = size(ids);
num_ids = ids_dim(1);
num_ids = num_ids - 1; % FIX: Special case where a single 0 got detected

% Sort by ID
ranges_chronological = sortrows(ranges_chronological,[col_id col_time col_chan]);
index_start = 31;

% Common plot: Time plot
font_size = 20;
figure('Name', 'Distribution over time', 'DefaultAxesFontSize', font_size);
hold on

for j = 1:num_ids

    if j == num_ids
        index_end = dimensions(1);
    else
        index_end = find(ranges_chronological(:,col_id) > ranges_chronological(index_start,col_id),1, 'first') - 1;
    end
    
    num_measurements = (index_end - index_start + 1) / num_channels;
    
    % Calculate what the reported range would have been
    ranges     = zeros(num_channels * num_measurements, 1);
    ranges_sim = zeros(               num_measurements, 1);
    ranges_avg = zeros(               num_measurements, 3);
    times_sim  = zeros(               num_measurements, 1);
    
    for i = 1:num_measurements
        distance_measurements = ranges_chronological((index_start + (i - 1) * num_channels):(index_start + i * num_channels - 1), col_meas);
        ranges_sim(i)   = prctile(distance_measurements, percentile);
        times_sim(i)    = ranges_chronological(index_start + (i - 1) * num_channels,col_time);
    end

    % Calculate moving averages
    for i = 1:num_measurements
        ranges_avg(i,1) = median(ranges_sim(max(1,i-avg_span_1):min(num_measurements,i+avg_span_1)));
        ranges_avg(i,2) = median(ranges_sim(max(1,i-avg_span_2):min(num_measurements,i+avg_span_2)));
    end
    
    % Sort data
    ranges = ranges_chronological(index_start:index_end,col_meas);
    
    % Individual plot
%     figure('Name', 'Cumulative distribution function')
%     bin_width = 5;
%     bins      = x_start:bin_width:x_end;
%     hold on
%     cdf_plot(1) = cdfplot(ranges);
%     cdf_plot(2) = cdfplot(ranges_sim);
%     cdf_plot(3) = cdfplot(ranges_avg(:,1));
%     cdf_plot(4) = cdfplot(ranges_avg(:,2));
%     set(cdf_plot(2), 'LineStyle', '--');
%     set(cdf_plot(:), 'Color', 'b');
%     set(cdf_plot(3), 'LineStyle', '--');
%     set(cdf_plot(3), 'Color', [230/255 85/255 13/255], 'LineWidth', 1);
%     set(cdf_plot(4), 'LineStyle', '--');
%     set(cdf_plot(4), 'Color', [94/255 60/255 108/255], 'LineWidth', 1);
%     set(cdf_plot(5), 'LineStyle', '--');
%     set(cdf_plot(5), 'Color', 'r', 'LineWidth', 1);
%     title('Range estimate distribution');
%     legend({'Raw measurements', '50th percentile', 'Additionally taking median with moving window 3', 'Additionally taking median with moving window 11'}, 'Location', 'southeast');
%     xlim([x_start, x_end]);
%     xlabel('Range estimates [mm]');
%     ylabel('Cumulative distribution function (CDF)');
%     hold off

    % Common plot
    %time_plot(j,1) = plot(times_sim, ranges_sim);
    %time_plot(j,2) = plot(times_sim, ranges_avg(:,1));
    time_plot(j,3) = plot(times_sim, ranges_avg(:,2));
    
    % Iterate
    index_start = index_end + 1;
end

% Adjust colors
%set(time_plot(1,3), 'Color', [230/255 85/255  13/255]);
%set(time_plot(2,3), 'Color', [ 94/255 60/255 108/255]);

% Common plot end
ylim([-100, 15000]);
xlim([epoch_start, epoch_end]);
xlabel('Unix epoch time [s]');
ylabel('Range estimates [mm]');
hold off

% Total data
ranges_tot = ranges_chronological(:,col_meas);

% Load different channels
% channels = zeros(num_measurements, num_channels);
% for i = 1:num_channels
%    channels(:,i) = ranges((1 + (i - 1) * num_measurements):( i * num_measurements));
% end


%% Plots

% Histogram
bin_width = 50;
x_start = 0;
x_end   = 10000;
bins    = x_start:bin_width:x_end;

font_size = 30;
figure('Name', 'Histogram', 'DefaultAxesFontSize', font_size)
histogram(ranges_tot, bins);
xlim([x_start, x_end]);
xlabel('Range estimates [mm]', 'FontSize', font_size);
ylabel('Measuremenets per bin', 'FontSize', font_size);

% CDF
figure('Name', 'Cumulative distribution function for entire measurement series')
bin_width = 5;
bins      = x_start:bin_width:x_end;
hold on
cdf_plot(1) = cdfplot(ranges_tot);
title('Range estimate distribution');
xlim([x_start, x_end]);
xlabel('Range estimates [mm]');
ylabel('Cumulative distribution function (CDF)');
hold off
    