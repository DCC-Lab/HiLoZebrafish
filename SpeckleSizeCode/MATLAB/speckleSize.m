files = {'20190924-200ms_20mW_Ave15_Gray_10X0.4_1.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_2.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_3.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_4.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_5.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_6.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_7.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_8.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_9.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_10.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_11.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_12.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_13.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_14.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_15.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_16.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_17.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_18.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_19.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_20.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_21.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_22.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_23.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_24.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_25.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_26.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_27.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_28.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_29.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_30.tif','20190924-200ms_20mW_Ave15_Gray_10X0.4_31.tif'};
distFiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31];

widths1 = [];
distances = [];
for i = 1:31
    s = imread(files{i});
    theSize = 400;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHM(s);
    widths1 = [widths1; x];
    distances = [distances, distFiles(i)];
end

widths1
 
figure(1);
plot(distances, widths1,'o');


  
% function showSpeckleSize(image, width)
%      corr=normxcorr2(image,image);
%      surf(corr)
% end

widths2 = [];
distances = [];
for i = 1:31
    s = imread(files{i});
    theSize = 250;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHM(s);
    widths2 = [widths2; x];
    distances = [distances, distFiles(i)];
end

widths2
% 
%  figure(2);
%  plot(distances, widths2,'o');
% 
%  function showSpeckleSize(image, width)
%      corr=normxcorr2(image,image);
%      surf(corr)
%  end

widths3 = [];
distances = [];
for i = 1:31
    s = imread(files{i});
    theSize = 100;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHM(s);
    widths3 = [widths3; x];
    distances = [distances, distFiles(i)];
end

widths3
% 
%  figure(3);
%  plot(distances, widths3,'o');
% 
%  function showSpeckleSize(image, width)
%     corr=normxcorr2(image,image);
%     surf(corr)
%  end


widths4 = [];
distances = [];
for i = 1:31
    s = imread(files{i});
    theSize = 75;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHM(s);
    widths4 = [widths4; x];
    distances = [distances, distFiles(i)];
end

widths4

widths11 = [];
distances = [];
for i = 1:31
    s = medfilt2(imread(files{i}),[2,2]);
    theSize = 400;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleRealFWHM(s);
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
for i = 1:31
    s = medfilt2(imread(files{i}),[2,2]);
    theSize = 250;
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
for i = 1:31
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