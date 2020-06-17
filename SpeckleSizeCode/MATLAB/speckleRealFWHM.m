% Autocorrelation process

function [wx, wy, normCorr] = speckleFWHM(image)
    image = double(image) - mean(mean(double(image)));
    normCorr=normxcorr2(image,image);
    normCorr=cropCenter(normCorr, size(image,1));
    [wy, wx] = fwhm(normCorr);
end    