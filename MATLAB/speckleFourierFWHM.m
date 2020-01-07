function [wx, wy, normCorr] = speckleFourierFWHM(image)
    w1 = size(image,1);
    w2 = size(image,2);
    image = double(image) - mean(mean(double(image)));
    spectrum = fft2(image,5*w1,5*w2);

    spectrum = fftshift(spectrum,1);
    spectrum = fftshift(spectrum,2);
    
    [wy, wx] = fwhm(spectrum);
    %% Convert wy and wy
end    