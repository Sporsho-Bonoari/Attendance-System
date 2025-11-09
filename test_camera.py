"""
Quick camera test to diagnose issues
"""
import cv2
import sys

print("=" * 60)
print("🎥 Camera Test Utility")
print("=" * 60)

# Test 1: DirectShow backend
print("\n1️⃣ Testing with DirectShow backend (Windows)...")
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if video.isOpened():
    print("✅ Camera opened successfully with DirectShow!")
    
    # Set properties
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Read a frame
    ret, frame = video.read()
    if ret:
        print(f"✅ Frame captured! Size: {frame.shape}")
        print("\n📹 Showing camera feed...")
        print("Press 'Q' to close the window")
        
        while True:
            ret, frame = video.read()
            if not ret:
                print("❌ Failed to read frame!")
                break
            
            cv2.putText(frame, "Camera Working! Press Q to quit", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("Camera Test - DirectShow", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video.release()
        cv2.destroyAllWindows()
        print("\n✅ Camera test PASSED!")
    else:
        print("❌ Failed to capture frame!")
        video.release()
else:
    print("❌ Failed to open camera with DirectShow")
    
    # Test 2: Default backend
    print("\n2️⃣ Testing with default backend...")
    video = cv2.VideoCapture(0)
    
    if video.isOpened():
        print("✅ Camera opened with default backend!")
        ret, frame = video.read()
        if ret:
            print(f"✅ Frame captured! Size: {frame.shape}")
            print("\n📹 Showing camera feed...")
            print("Press 'Q' to close")
            
            while True:
                ret, frame = video.read()
                if not ret:
                    print("❌ Failed to read frame!")
                    break
                
                cv2.putText(frame, "Camera Working! Press Q to quit", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow("Camera Test - Default", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            video.release()
            cv2.destroyAllWindows()
            print("\n✅ Camera test PASSED!")
        else:
            print("❌ Failed to capture frame!")
            video.release()
    else:
        print("❌ Failed to open camera with default backend")
        print("\n🔍 Possible issues:")
        print("- Camera is being used by another application")
        print("- Camera permission not granted")
        print("- Camera driver issue")
        print("- No camera connected")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)

