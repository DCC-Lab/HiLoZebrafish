function [ypeak, xpeak] = peakCoordinates(image)
    [ypeak, xpeak] = find(image==max(image(:)));
end