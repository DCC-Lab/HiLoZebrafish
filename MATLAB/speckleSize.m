files = {'speckle1pouce_12ms.jpg','speckle2pouces_30ms.jpg'};
distFiles = [1,2];

widths = [];
distances = [];
for i = size(files,1)+1
    s = imread(files{i});
    theSize = 200;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleFWHM(s);
    widths = [widths, x]
    distances = [distances, distFiles(i)];
end

figure(1);
plot(distances, widths,'o');

function showSpeckleSize(image, width)
    corr=normxcorr2(image,image);
    surf(corr)
end
