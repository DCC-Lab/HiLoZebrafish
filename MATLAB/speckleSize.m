files = {'speckle0.tiff','speckle1pouce_12ms.tiff','speckle2pouces_30ms.tiff','speckle3pouces_50ms.tiff','speckle4pouces_80ms.tiff','speckle5pouces_120ms.tiff','speckle6pouces_150ms.tiff'};
distFiles = [0,1,2,3,4,5,6];

widths = [];
distances = [];
for i = 1:7
    s = imread(files{i});
    theSize = 1000;
    s = cropCenter(s,theSize);
    [x,y,c]=speckleFWHMFourier(s);
    widths = [widths, x];
    distances = [distances, distFiles(i)];
end

widths

figure(1);
plot(distances, widths,'o');

function showSpeckleSize(image, width)
    corr=normxcorr2(image,image);
    surf(corr)
end
