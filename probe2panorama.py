import cv2
import numpy as np
from math import pi, sin, cos

def main():
    fn_src = "image/park_probe.jpg"

    fn_dst = "image/park_panorama.jpg"

    height_panorama = 180 * 4
    width_panorama = height_panorama*2
    
    sampling_type = 1 #0:nearest neighbor, 1:bilinear interpolation
   
    img_probe = cv2.imread(fn_src, 1)
    height_probe, width_probe = img_probe.shape[:2]
    print("probe size:", width_probe, height_probe)
    assert height_probe==width_probe, "Enter an image with aspect ratio 1:1"

    img_panorama = np.zeros((height_panorama, width_panorama, 3), dtype=np.uint8)

    for col in range(height_panorama):
        for row in range(width_panorama):
            u = row/(width_panorama-1)*2 #0~2
            v = col/(height_panorama-1) #0~1
            theta = pi * (u-1) 
            phi = pi * v
            Dx = sin(phi) * sin(theta)
            Dy = cos(phi)
            Dz = -sin(phi) * cos(theta)
            D = np.array([Dx, Dy, Dz]) #Light source vector
            V = np.array([0, 0, -1]) #Line of sight vector
            n = (D+V) / np.linalg.norm(D+V) #Normal vector

            s = n[0] #-1~1
            t = -n[1] #-1~1
            x = (s+1)*0.5*(width_probe-1)
            y = (t+1)*0.5*(height_probe-1)
            
            if sampling_type==0:
                img_panorama[col][row] = img_probe[int(y)][int(x)]
            else:
                img_panorama[col][row] = cv2.getRectSubPix(img_probe, (1, 1), (x, y))

    cv2.imwrite(fn_dst, img_panorama)
    print("panorama size:", width_panorama, height_panorama)

if __name__=='__main__':
    main()
