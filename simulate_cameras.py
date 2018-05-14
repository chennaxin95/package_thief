'''
Generate n camera with different ID
Use multiprocessing to make these cameras send frames to edge server
'''

from multiprocessing import Pool


lenght = 10000

def generate_cameras(cam_num):
    cam_list = []
    for i in range(cam_num):
        cam = Camera(i)
        cam_list.append(cam)
        
    return cam_list



def f(x):
    return x.send_random_video_frame(length, 30)

if __name__ == '__main__':
    cam_list = generate+cameras(5)
    p = Pool(5)
    print(p.map(f, cam_list))