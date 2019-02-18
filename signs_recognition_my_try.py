import imageio
import numpy as np
import cv2
import os
from shape_detection import detect_shapes

num_segments_row=16
num_segments_column=9


IM_WIDTH = 1280
IM_HEIGHT = 720

size_segment=IM_HEIGHT/num_segments_column

frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX


filename='video/SJCM0019.mp4'
distanation_folder='/media/pi/USB DISK/0_170_cuted_1/'
vid=imageio.get_reader(filename,'ffmpeg')

try:
    for i in range(10000):
       os.mkdir(distanation_folder+str(i)+"/")
       for j in range(num_segments_column):
           os.mkdir(distanation_folder+str(i)+"/"+str(j)+"/")
except:
   pass
        


index=0
rect_size=50
rect_radius=int((rect_size)/2)
for num in range(1,10000):
        print(str(num))
        num1=num
        frame1=vid.get_data(num*5)
        t1 = cv2.getTickCount()
        
        frame=np.array(frame1)
        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(frame, (120), (180))  # blue

        frame = cv2.bitwise_and(frame, frame, mask=mask)
        '''
        #number_srt=int((int(IM_HEIGHT/2)-81)/10)
        #number_collumn=int((IM_WIDTH-81)/10)
        #cv2.imwrite(distanation_folder+str(num)+"/0.jpg",frame)
        #for j in range(1,number_srt):
        #    j1=j*10
        #    for k in range (1,number_collumn):
        #        k1=k*10
        #        frame5=np.array(frame[j1:j1+81,k1:k1+81])
        #        print(len(frame),j1,j1+81,k1,k1+81)
                #print(j,k)
                #print(frame5)
                
        #        cv2.imwrite(distanation_folder+str(num)+"/"+str(j*1000+k)+".jpg",frame5)
                
        #        try:
        #            pass
                    #cv2.imshow("",frame5)
                    #t2 = cv2.getTickCount()
                    #time1 = (t2-t1)/freq
                    #frame_rate_calc = 1/time1
        #        except:
        #            pass
                
        #frame5=np.array(frame[500:600,500:600])
        #cv2.imshow(" ",frame5)
        
        #mask=cv2.inRange(frame,(0,170,0),(255,255,255))
        #mask=cv2.inRange(frame,(100,0,0),(255,180,180))
        #mask=cv2.inRange(frame,(0,0,100),(180,180,255))
        #delt_color=
        
        #frame_half=frame[0:int(IM_HEIGHT/2),0:IM_WIDTH]
        
        mask=cv2.inRange(frame,(40,0,0),(255,89,50)) #blue
        #mask=cv2.inRange(frame,(40,0,0),(255,120,120)) #blue1
        
        #mask=cv2.inRange(frame,(0,0,40),(75,75,140)) #red
            
        
        mask=cv2.dilate(mask,None,iterations=2)
        
        #_, contours0,hierarhy=cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #for cnt in contours0:
        #    if len(cnt)>4:
        #        ellipse=cv2.fitTriangle(cnt)
        #        cv2.ellipse(frame,ellipse,(0,0,255),2)
                
        result=cv2.bitwise_and(frame,frame,mask=mask)
        
        detection=detect_shapes.find_countours(result,frame)
        frame = detection[0]
        for cntr in detection[1]:
            rect_radius_new=cntr[2]*4
            if rect_radius_new>rect_radius:
                rect_radius_new=rect_radius
            cv2.rectangle(frame,(cntr[0]-rect_radius_new,cntr[1]-rect_radius_new),(cntr[0]+rect_radius_new,cntr[1]+rect_radius_new),(0,0,255),3)
        #for j in range(IM_HEIGHT): #IM_HEIGHT
            #for k in range(IM_WIDTH):
                #pix=result[j]
                #print(pix)
                #r=pix[0]
                #g=pix[1]
                #b=pix[2]
                #print(r,g,b)
                #print(j,k)
                #avg=int((r+g+b)/3)
                #if abs(r-avg)<20 or abs(g-avg)<20 or abs(b-avg)<20:
                    #result[j][k]=(0,0,0)
        cv2.imshow("",frame)
        #index+=1
        #index_i=0
        #for i in np.hsplit(result,num_segments_row):
            #image=np.vsplit(i,num_segments_column)
            #for j in range(len(image)):
                #cv2.imwrite(distanation_folder+str(index_i)+"/"+str(j)+"/"+str(index)+".jpg",image[j])
                #cv2.imshow(str(index)+" "+str(j),image[j])
                #index+=1
                #print(distanation_folder+str(index_i)+"/"+str(j)+"/")
            #index_i+=1
        
        #for i in range(num_segments_row):
            #cv2.line(frame,(int(i*size_segment),0),(int((i)*size_segment),IM_HEIGHT),(0,255,255),1)
        #for i in range(num_segments_column):
            #cv2.line(frame,(0,int(i*size_segment)),(IM_WIDTH,int((i)*size_segment)),(0,255,255),1)
        
        '''
        cv2.imshow("",frame)
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
        
while(True):
            pass
cv2.destroyAllWindows()
        