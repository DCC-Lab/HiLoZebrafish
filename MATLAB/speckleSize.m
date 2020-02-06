files = {'20190924-200ms_20mW_Ave15_Gray_20X0.75_1.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_2.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_3.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_4.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_5.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_6.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_7.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_8.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_9.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_10.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_11.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_12.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_13.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_14.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_15.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_16.tif','20190924-200ms_20mW_Ave15_Gray_20X0.75_17.tif'};
distFiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17];

widths1 = [];
distances = [];
for i = 1:17
    s = imread(files{i});
    theSize = 1000;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths1 = [widths1; x];
    distances = [distances, distFiles(i)];
end

widths1

% figure(1);
% plot(distances, widths1,'o');
% 
% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end

widths2 = [];
distances = [];
for i = 1:17
    s = imread(files{i});
    theSize = 500;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths2 = [widths2; x];
    distances = [distances, distFiles(i)];
end

widths2

% figure(2);
% plot(distances, widths2,'o');

% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end

widths3 = [];
distances = [];
for i = 1:17
    s = imread(files{i});
    theSize = 100;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths3 = [widths3; x];
    distances = [distances, distFiles(i)];
end

widths3

% figure(3);
% plot(distances, widths3,'o');

% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end

widths11 = [];
distances = [];
for i = 1:17
    s = medfilt2(imread(files{i}),[2,2]);
    theSize = 1000;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths11 = [widths11; x];
    distances = [distances, distFiles(i)];
end

widths11

% figure(4);
% plot(distances, widths,'o');

% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end

widths22 = [];
distances = [];
for i = 1:17
    s = medfilt2(imread(files{i}),[2,2]);
    theSize = 500;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths22 = [widths22; x];
    distances = [distances, distFiles(i)];
end

widths22

% figure(5);
% plot(distances, widths,'o');

% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end


widths33 = [];
distances = [];
for i = 1:17
    s = medfilt2(imread(files{i}),[2,2]);
    theSize = 100;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHMFourier(s);
    widths33 = [widths33; x];
    distances = [distances, distFiles(i)];
end

widths33

% figure(5);
% plot(distances, widths,'o');

% function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
% end