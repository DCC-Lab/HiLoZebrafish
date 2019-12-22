function [wx, wy, normCorr] = speckleFWHMFourier(image)
    image = double(image) - mean(mean(double(image)));
    image = image .* (hann(size(image,1))*hann(size(image,2))')
    powerSpectrum = fft2(image).*conj(fft2(image));
    corr = ifft2(powerSpectrum);
    normCorr = corr./max(max(corr));
    normCorr = fftshift(normCorr,1);
    normCorr = fftshift(normCorr,2);
    
    [wy, wx] = fwhm(normCorr);
end    