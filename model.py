import cv2
import numpy as np

class Model:
    def __init__(self):
        pass

    def background_subtraction(self, vidPath):
        cap = cv2.VideoCapture(vidPath)
        ret, frame = cap.read()
        if not ret:
            return
        
        # Create background subtractor
        history = 500
        dist2Threshold = 400
        subtractor = cv2.createBackgroundSubtractorKNN(history, dist2Threshold, detectShadows=True)
        
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Blur frame
            blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            
            # Get background mask
            mask = subtractor.apply(blurred_frame)

            # Generate Frame (R) with only moving object by cv2.bitwise_and
            result = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Show the frame with the background mask
            cv2.imshow('frame', frame)
            cv2.imshow('mask', mask)
            cv2.imshow('result', result)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        

    def preprocessing(self, vidPath):
        cap = cv2.VideoCapture(vidPath)
        ret, frame = cap.read()
        if not ret:
            return
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Adjust parameters for goodFeaturesToTrack
        maxCorners = 1
        qualityLevel = 0.3
        minDistance = 7
        blockSize = 7
        
        # Detect corners using goodFeaturesToTrack
        corners = cv2.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance, blockSize)
        
        if corners is not None:
            # Get the coordinates of the corner
            x, y = corners[0][0]
            
            # Draw a red cross mark at the corner point, set the length of the line to 20 pixels, and the line thickness to 4 pixels
            cv2.line(frame, (int(x)-10, int(y)), (int(x)+10, int(y)), (0, 0, 255), 4)
            cv2.line(frame, (int(x), int(y)-10), (int(x), int(y)+10), (0, 0, 255), 4)
        
        # Show the frame with the cross mark
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 960, 540)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        
        cap.release()
        cv2.destroyAllWindows()
    
    def video_tracking(self, vidPath):
        cap = cv2.VideoCapture(vidPath)
        ret, prev_frame = cap.read()
        if not ret:
            return
        
        # Convert previous frame to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        # Adjust parameters for goodFeaturesToTrack
        maxCorners = 1
        qualityLevel = 0.3
        minDistance = 7
        blockSize = 7
        
        # Detect corners using goodFeaturesToTrack
        prev_corners = cv2.goodFeaturesToTrack(prev_gray, maxCorners, qualityLevel, minDistance, blockSize)
        
        # Create an empty mask image
        mask = np.zeros_like(prev_frame)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert current frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow using cv2.calcOpticalFlowPyrLK
            next_corners, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, None)
            
            # Select good points
            good_new = next_corners[status == 1]
            good_old = prev_corners[status == 1]
            
            # Draw trajectory lines
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 100, 255), 2)
                frame = cv2.line(frame, (int(a)-10, int(b)), (int(a)+10, int(b)), (0, 0, 255), 4)
                frame = cv2.line(frame, (int(a), int(b)-10), (int(a), int(b)+10), (0, 0, 255), 4)
                # frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 100, 255), -1)
            
            # Overlay trajectory lines on the frame
            output = cv2.add(frame, mask)
            
            # Show the frame with the trajectory lines
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 960, 540)
            cv2.imshow('frame', output)
            
            if cv2.waitKey(15) & 0xFF == ord('q'):
                break
            
            # Update previous frame and corners
            prev_gray = gray.copy()
            prev_corners = good_new.reshape(-1, 1, 2)
        
        cap.release()
        cv2.destroyAllWindows()

    
        
        
        