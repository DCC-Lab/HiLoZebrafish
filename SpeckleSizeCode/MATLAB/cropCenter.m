function cropped = cropCenter(image, width)
    [h,w] = size(image);
    cx = uint32(h/2);
    cy = uint32(w/2);
    hw = uint32(width/2);
    cropped = image(cx-hw:cx+hw-1,cy-hw:cy+hw-1);
end
