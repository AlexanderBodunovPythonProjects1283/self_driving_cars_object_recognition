import cv2
import os
import time
import math
import imutils
import numpy as np

from shape_detection import detect_shapes

frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

IM_WIDTH=1280
IM_HEIGHT=720

#dir_write="/media/pi/USB DISK1/position_detection_proceed/"
#dir_write="/media/pi/USB DISK1/14_01_18_proceed/"
rect_radius_new=5


number_of_led=2
const_width_window=30


def devide_leds(number_of_led,func_,different):
    sum_=0
    for i in func_:
        sum_+=i[1]
    avg=sum_/len(func_)
    
    func_devided=[]
    index__=1
    for i in func_:
        if i[1]>avg:
            #func_devided.append([i[0],i[1],1])
            cv2.putText(img,"y="+str(i[0])+"x+ "+str(i[1]),(different[index__][0]-400,different[index__][1]),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
        else:
            cv2.putText(img,"y="+str(i[0])+"x+ "+str(i[1]),(different[index__][0]-400,different[index__][1]),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),4)
        index__+=1
 
def find_points_x0_y0(a1,a2,b1,b2):
    x=int((b2-b1)/(a1-a2))
    y=int(a1*x+b1)
    return [x,y]
def visualize(img,i,j):
    #cv2.line(img,(i[0],i[1]),(j[0],j[1]),(255,0,255),4)
    try:
        a= (i[1]-j[1])/(i[0]-j[0])
    except:
        a= (i[1]-j[1])/0.0001
        
    b=i[1]-a*i[0]
    
    try:
        a_inv=-1/a
    except:
        a_inv=1e6
    b1_inv=i[1]-a_inv*i[0]
    b2_inv=j[1]-a_inv*j[0]
    
    #cv2.line(img,(int(-b1_inv/a_inv),0),(0,int(b1_inv)),(255,0,255),4)
    #cv2.line(img,(int(-b2_inv/a_inv),0),(0,int(b2_inv)),(255,0,255),4)
    print(str(int(-b1_inv/a_inv))," 0"," 0",str(int(b1_inv)))
    
    p1=find_points_x0_y0(a,a_inv,b+const_width_window,b1_inv)
    p2=find_points_x0_y0(a,a_inv,b-const_width_window,b1_inv)
    p4=find_points_x0_y0(a,a_inv,b+const_width_window,b2_inv)
    p3=find_points_x0_y0(a,a_inv,b-const_width_window,b2_inv)
    print(p1,p2,p3,p4)
    cv2.line(img,(p1[0],p1[1]),(p2[0],p2[1]),(255,0,255),4)
    cv2.line(img,(p2[0],p2[1]),(p3[0],p3[1]),(255,0,255),4)
    cv2.line(img,(p3[0],p3[1]),(p4[0],p4[1]),(255,0,255),4)
    cv2.line(img,(p4[0],p4[1]),(p1[0],p1[1]),(255,0,255),4)
    
    
    cv2.putText(img,"a="+str(a),(p2[0],p2[1]+100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),4)
    return img
    

def calc_distance(x,y):
    return int(math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2))
 

def points_fited(i,j,different):
    try:
        a= (i[1]-j[1])/(i[0]-j[0])
    except:
        a= (i[1]-j[1])/0.0001
        
    b=i[1]-a*i[0]
    
    try:
        a_inv=-1/a
    except:
        a_inv=1e6
    b1_inv=i[1]-a_inv*i[0]
    b2_inv=j[1]-a_inv*j[0]
    result_fit=[]
    result_not_fit=[]
    for i in range(len(different)):
        s=different[i][1]-a*different[i][0]-b
        s1=different[i][1]-a_inv*different[i][0]
        
        if s<const_width_window and s>-const_width_window and (s1-b1_inv)*(s1-b2_inv)<=0:
            result_fit.append(i)
        else:
            result_not_fit.append(i)
    return [result_fit,result_not_fit]
 
def calc_fit_points(i,j,different):
    try:
        a= (i[1]-j[1])/(i[0]-j[0])
    except:
        a= (i[1]-j[1])/0.0001
        
    b=i[1]-a*i[0]
    
    try:
        a_inv=1/a
    except:
        a_inv=1e6
    b1_inv=i[1]+a_inv*i[0]
    b2_inv=j[1]+a_inv*j[0]
    count=0
    for i in different:
        s=i[1]-a*i[0]-b
        s1=i[1]+a_inv*i[0]
        
        if s<const_width_window and s>-const_width_window and (s1-b1_inv)*(s1-b2_inv)<=0:
            count+=1
    abs_alph=abs(a)
    #if abs_alph >0.7 and abs_alph<1.3:
        #return count
    #else:
        #return 0
    return count
    
def calc_dist(different):
    result=[]
    for i in different:
        row=[]
        for j in different:
                row.append(calc_distance(i,j))
        result.append(row)
    return result
            
        
def devide_by_2_group(different):
    result=[]
    arr_x=[]
    for i in different:
        arr_x.append(i[0])
    arr_indexes=np.argsort(arr_x)
    arr_x=sorted(arr_x)
   
    arr_delt=[]
    for i in range (1,len(arr_x)):
       arr_delt.append(arr_x[i]-arr_x[i-1])
    avg_delt=np.mean(arr_delt)*0.8
    for i in range(len(arr_delt)):
       if arr_delt[i]>avg_delt:
           curr=arr_x[arr_indexes[i]]
           prev=arr_x[arr_indexes[i-1]]
           result.append(int((curr+prev)/2))
    return result
       
       
        
 
def devide_leds_1(number_of_led,func_,different):
    #different=sorted(different)
    
    result=[]
    for i in range(len(different)):
        #print([different[i-1][0]-different[i][0],different[i-1][1]-different[i][1]])
        row=[]
        for j in range(len(different)):
           if j>i:
               row.append(calc_fit_points(different[i],different[j],different))
           else:
               row.append(0)
        result.append(row)
    for i in range(len(result)):
        print(result[i], max(result[i]),different[i], i)
    print("\n\n")
    return result
            
    
    

def find_different(arr):
    prev=[]
    for i in arr:
        checked=True
        for j in prev:
            #print("lll     "+str((i[0]-j[0])**2+(i[1]-j[1])**2))
            if ((i[0]-j[0])**2+(i[1]-j[1])**2 <160):
                checked=False
        if checked:
           prev.append(i)
    return prev

def find_a(x_0,x_1,y_0,y_1):
    try:
        return (x_1-y_1)/(x_0-y_0)
    except:
        return (x_1-y_1)/0.0001

def find_b(x_0,x_1,a):
    return x_1-a*x_0
   
def find_max(arr):
    max=0
    index_i=0
    index_j=0
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j]>max:
                max=arr[i][j]
                index_i=i
                index_j=j
    return [index_i,index_j]
    

def find_points_in_radius(arr_dist,radius):
    index=0
    for i in arr_dist:
        arr_in_radius=[]
        for j in range(len(i)):
            if i[j]<=radius:
                arr_in_radius.append(j)
        if len(arr_in_radius)>=5:
            #return arr_in_radius
            radius1=radius+100
            arr_in_radius=[]
            for j in range(len(i)):
                if i[j]<=radius1:
                    arr_in_radius.append(j)
            return [arr_in_radius,index]
        index+=1
            
    return [[],0]
        
                
def devide_by_2(arr):
    result_1=[]
    result_2=[]
    arr_x=[]
    for i in arr:
        arr_x.append(i[0])
        
    avg_=int(np.mean(arr_x))
    for i in arr:
        if i[0]>avg_:
            result_2.append(i)
        else:
            result_1.append(i)
    return [result_1,result_2]
        
def aproximate_(arr):
    
    arr_result=[]
    if len(arr)>=3:
        for i in range(0,len(arr)-2):
            x=arr[i]
            y=arr[i+1]
            z=arr[i+2]
            
            a1=find_a(x[0],x[1],y[0],y[1])
            b1=find_b(x[0],x[1],a1)
            
            a2=find_a(x[0],x[1],z[0],z[1])
            b2=find_b(x[0],x[1],a2)
            
            a3=find_a(y[0],y[1],z[0],z[1])
            b3=find_b(y[0],y[1],a3)
            
            a=((a1+a2+a3)/3)
            if a==0:
                a=0.0001
            b=int((b1+b2+b3)/3)
            
            #arr_result.append([[0,b],[int(-b/a),0]])
            arr_result.append([a,b])
        return(arr_result)
            
    else:
        return []
        

def find_center(arr):
    index=0
    min_=100000
    for i in range(len(arr)):
        sum_=0
        for j in arr:
            sum_+=arr[i][0]-j[0]
        if sum_<min_:
            min=sum
            index=i
    return arr[index]
            
            
        

index=0

if camera_type == 'picamera':
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        print("aa")
        
        
        t1 = cv2.getTickCount()
        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        img = frame1.array
    
        #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        masc=cv2.inRange(img,(200,200,200),(255,255,255))
        #masc=cv2.resize(masc,500)
        
        #im2,contours,hierarchy=cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #image_canny=cv2.Canny(img,30,300)
        
        #lines=cv2.HoughLinesP(image_canny,1,math.pi/2,30,1)
        #for line in lines[0]:
            #pt1=(line[0],line[1])
            #pt2=(line[2],line[3])
        #print(len(lines[0]))
        #cv2.line(image_canny,pt1,pt2,(0,0,255),3)
        
        
        #print(len(contours))
        #for contour in contours:
        #cv2.drawContours(img,contours,-1,(0,255,0),3)
        #cv2.imshow("1",masc)
        
        #cv2.resizeWindow("1",500,500)
        
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        #index+=1
        #if cv2.waitKey(1) == ord('q'):
        #            break
        #time.sleep(1)
        
        #detection=detect_shapes.find_countours(masc,masc)
        #frame = detection[0]
        
        im2,contours,hierarchy=cv2.findContours(masc,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(masc,contours,-1,(0,255,0),3)
        
        resized = imutils.resize(masc, width=300)
        ratio = masc.shape[0] / float(resized.shape[0])
        
        #print(len(contours))
        count_=0
        
        arr_contours=[]
        for i in contours:
            if cv2.contourArea(i)>10:
                M = cv2.moments(i)
                try:
                    cX = int((M["m10"] / M["m00"]) * 1)
                    cY = int((M["m01"] / M["m00"]) * 1)
                except:
                    cX = int((M["m10"] / 0.0001) * 1)
                    cY = int((M["m01"] / 0.0001) * 1)
                arr_contours.append([cX,cY])
        
        
        print(len(arr_contours),"    ",len(find_different(arr_contours)))
        
        different=find_different(arr_contours)
        for i in different:
                count_+=1
                
                
                
                cv2.putText(img,str(i[0])+"  "+str(i[1]),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),4)
                
                
                #print(cX,cY)
        index__=1
        
        with open("/home/pi/tensorflow1/models/research/object_detection/points_2/"+str(num)+".txt","w") as file:
            for i in different:
                file.write(str(i[0])+","+str(i[1])+"\n")
        
        #x_s=devide_by_2_group(different)
        #for k in x_s:
            #cv2.line(img,(k,0),(k,1000),(0,255,0),4)
        
        #cv2.putText(img,str(len(x_s)),(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),4)
        
        arr_groups=[]
        arr_dist=calc_dist(different)
        
        indexes_was=[]
        
        for r in range(1,30):
            #print(arr_dist)
            #print(arr_groups)
            points=find_points_in_radius(arr_dist,r*10)
            arr_coords_detected=[]
            for i in points[0]:
                arr_coords_detected.append(different[i])
                cv2.putText(img,"++++++++++",(different[i][0],different[i][1]),cv2.FONT_HERSHEY_SIMPLEX,2,(255-r*5,r*5,r*5),4)
                indexes_was.append(i)
            arr_coords_detected=[arr_coords_detected,different[points[1]]]
            print("**********************************")
            print(different)
            print(points[1])
            print("\n")
            arr_groups.append(arr_coords_detected)
            
            for i in range (len(points)):
                for j in range(len(arr_dist)):
                    arr_dist[i][j]=10000
                    arr_dist[j][i]=10000
        arr_other=[]    
        for i in  range(len(different)):
            if i not in indexes_was:
                arr_other.append(different[i])
                
        if len(arr_other)>=10:
            arrs_other=devide_by_2(arr_other)
            arr_groups.append(arrs_other[0])
            arr_groups.append(arrs_other[1])
        else:
            center=find_center(arr_other)
            arr_other=[arr_other,center]
            arr_groups.append(arr_other)
        
        for i in arr_groups:
            print(i)
        
        for different1 in arr_groups:
            center=different1[1]
            different1=different1[0]
            if len(different1)>0:
                print(different1)
                if not isinstance(different1[0],int) and different1[0]:
                    for i in range(len(different1)):
                        #print(center[0],center[1])
                        different1[i][0]-=center[0]
                        different1[i][1]-=center[1]
                    print(center)
                print(different1)
                print("\n")
                    
            
        #for i in aproximate_(different):
            #cv2.line(img,(i[0][0],i[0][1]),(i[1][0],i[1][1]),(0,255,0),4)
            #cv2.putText(img,str(i[0])+"  "+str(i[1]),(different[index__][0]-300,different[index__][1]),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),4)
            #index__+=1
        #print(count_)
            #try:
                #print(i[0],i[1])
            #except:
                #pass
        
        #for cntr in contours:
         #   print(cntr[0],cntr[1])
            
        #for cntr in [1]:
                #cv2.rectangle(masc,(cntr[0]-rect_radius_new,cntr[1]-rect_radius_new),(cntr[0]+rect_radius_new,cntr[1]+rect_radius_new),(0,0,255),3)
        
                
        cv2.imwrite(dir_write+num,img)
    
        
    
    
    



