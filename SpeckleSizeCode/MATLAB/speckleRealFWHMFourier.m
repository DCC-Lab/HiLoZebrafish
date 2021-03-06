%Take your image, 
%FT, 
%make the product of the FT with its complex conjugate, 
%inverse FT. 

function [wx, wy, normCorr] = speckleRealFWHMFourier(image)
    w1 = size(image,1);
    w2 = size(image,2);
    image = double(image) - mean(mean(double(image)));
    %image = image .* (hann(size(image,1))*hann(size(image,2))');
    powerSpectrum = fft2(image,5*w1,5*w2).*conj(fft2(image,5*w1,5*w2));
    corr = ifft2(powerSpectrum);
    normCorr = corr./max(max(corr));
    normCorr = fftshift(normCorr,1);
    normCorr = fftshift(normCorr,2);
    
    [wy, wx] = fwhm(normCorr);
end    