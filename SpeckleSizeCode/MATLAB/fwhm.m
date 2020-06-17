function [ wx, wy] = fwhm(normCorr)

[yPeak, xPeak] = peakCoordinates(normCorr);
maxValue = normCorr(yPeak, xPeak);
delta= 0.01;

a = normCorr(yPeak,:)';
range = [1:delta:size(a)];
morePoints = interp1([1:size(a)],a,range);
% wy = size(find(morePoints>=0.5*maxValue),2)*delta;

[p,loc,wy] = findpeaks(morePoints,range,'SortStr','descend','MinPeakWidth',2,'NPeaks',1);

a = normCorr(:,xPeak);
range = [1:delta:size(a)];
morePoints = interp1([1:size(a)],a,range);
% wx = size(find(morePoints>=0.5*maxValue),2)*delta;
[p,loc,wx] = findpeaks(morePoints,range,'SortStr','descend','MinPeakWidth',2,'NPeaks',1);

