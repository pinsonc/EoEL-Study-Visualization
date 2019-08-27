% Calculate statistics and plots
clear all;

% General configs
num_channels = 30;

percentile = 50;
avg_span_1 = 1;
avg_span_2 = 10;

% Import data
filename = 'Data/12.17.18/121718_DATA_07.LOG'
header_length = 1;

file = importdata(filename, '\t', header_length);
data_raw = file.data;

col_time = 1;
col_nr   = 2;
col_id   = 3;
col_chan = 4;
col_meas = 5;

%% USE THIS SECTION IF USING ONLY CORRECTLY TIMESTAMPED DATA AND FILTERING ALL ELSE OUT

%  A = find(data_raw(:,col_time) > 1500000000,1,'first');
%  epoch_start = data_raw(A,1);
%  B = find(data_raw(:,col_time) > 1551700000,1,'first');
%  B = B-1;
%  epoch_end = data_raw(B,1);
% 
% dimensions = size(data_raw);
% num_measurements = dimensions(1) / num_channels;
% 
% 
% % Filter out all non-timestamped data
% ranges_chronological = sortrows(data_raw,col_time);
% first_valid_index    = find(ranges_chronological(:,col_time) > epoch_start, 1, 'first');
% %last_valid_index     = find(ranges_chronological(:,col_time) > epoch_end,   1, 'first');
% ranges_chronological = ranges_chronological(first_valid_index:dimensions(1),:);
% 
% dimensions = size(ranges_chronological);
% num_measurements = int32(dimensions(1) / num_channels);

%% USE THIS SECTION IS USING ALL DATA AND IGNORING TIMESTAMPS

% If filtering by time, set the start time of your measurements here
% Epoch time calculation: https://www.epochconverter.com/
duration_measurement = 12 * 3600;
 epoch_start = 1544883908; %this needs to be hard coded from checking the data
 epoch_end   = epoch_start + duration_measurement;

dimensions = size(data_raw);
num_measurements = dimensions(1) / num_channels;

ranges_chronological = data_raw;

% Filter out all non-timestamped data
ranges_chronological = sortrows(data_raw,col_time);

dimensions = size(ranges_chronological);
num_measurements = int32(dimensions(1) / num_channels);


%% NO CHANGES

% Convert uint32 to int32 to get correct negative ranges
ranges_chronological(:,col_meas) = typecast(uint32(ranges_chronological(:,col_meas)),'int32');


% Calculate what the reported range would have been
ranges_sim = zeros(num_measurements, 1);
ranges_avg = zeros(num_measurements, 3);
times_sim  = zeros(num_measurements, 1);

for i = 1:num_measurements
    distance_measurements = ranges_chronological((1 + (i - 1) * num_channels):(i * num_channels), col_meas);
    
    % From the 30 channels, we take the "percentile"th range
    % Example: percentile = 50 -> use the 50th percentile, which is the
    % median value
    ranges_sim(i)   = prctile(distance_measurements, percentile);
    
    % Store the time at which the ranging occurred - useful when having one
    % long measurement series and setting epoch time
    times_sim(i)    = ranges_chronological(1 + (i - 1) * num_channels,col_time);
end

%% CHANGE If time is not accurate (timestamping not used or multiple starts), 
% lets just list all the measurements one after the other

times_sim = 1:num_measurements;

%% Calculate moving averages
for i = 1:num_measurements
    % Calculate median filter with filter width (1 + 2*avg_span_1)
    ranges_avg(i,1) = median(ranges_sim(max(1,i-avg_span_1):min(num_measurements,i+avg_span_1)));
    
    % Calculate median filter with filter width (1 + 2*avg_span_2)
    ranges_avg(i,2) = median(ranges_sim(max(1,i-avg_span_2):min(num_measurements,i+avg_span_2)));
end

% Total data
ranges_tot = ranges_chronological(:,col_meas);

% Load different channels
% channels = zeros(num_measurements, num_channels);
% for i = 1:num_channels
%    channels(:,i) = ranges((1 + (i - 1) * num_measurements):( i * num_measurements));
% end


%% USE THIS SECTION TO CALCULATE CONVERSIONS FOR PLOTTING

%   times_sim_CST = datetime(times_sim, 'convertfrom','posixtime')- hours(6);
%   CST_start = datetime(epoch_start, 'convertfrom','posixtime')- hours(6);
%   CST_end = datetime(epoch_end, 'convertfrom','posixtime')- hours(6);
  ranges_avg_inch = (ranges_avg(:,2))/25.4;
  ranges_avg_feet = ranges_avg_inch/12;

%% PLOTS

% Time plot
font_size = 20;
figure('Name', 'Distribution over time', 'DefaultAxesFontSize', font_size);
hold on
% Uncomment for raw ranges
%time_plot(1) = plot(times_sim, ranges_sim(:));

% Uncomment for median filter with filter width (1 + 2*avg_span_1)
%time_plot(2) = plot(times_sim, ranges_avg(:,1));

% Uncomment for median filter with filter width (1 + 2*avg_span_2)
%time_plot(3) = plot(times_sim, ranges_avg(:,2));
time_plot(3) = plot(times_sim, ranges_avg_feet);
%time_plot(3) = plot(times_sim_CST, ranges_avg(:,2));
%time_plot(3) = plot(times_sim_CST, ranges_avg_feet);

ylim([0, 15]);
xlim([epoch_start, epoch_end]);
%xlabel('Unix Epoch Time [s]');
%CST_start = {'10-Dec-2018 20:30:00'};
% xlim([CST_start, CST_end]);
% xlabel('Time CST');
ylabel('Range estimates [feet]');
hold off

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


%ANIMATED TIME PLOT

curve=animatedline
set (gca,'XLim',[CST_start, CST_end],'YLim',[0, 15]);
grid on;
for i=length(times_sim_CST)
    addpoints(curve,times_sim_CST(i),ranges_avg_feet(i));
    drawnow
end;






font_size = 20;
figure('Name', 'Distribution over time', 'DefaultAxesFontSize', font_size);
hold on

time_plot(3) = plot(times_sim_CST, ranges_avg_feet);

ylim([0, 15]);
%xlim([epoch_start, epoch_end]);
%xlabel('Unix Epoch Time [s]');
%CST_start = {'10-Dec-2018 20:30:00'};
xlim([CST_start, CST_end]);
xlabel('Time CST');
ylabel('Range estimates [feet]');
hold off

