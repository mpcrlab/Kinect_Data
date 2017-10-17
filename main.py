from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
from pygame.locals import *
#from face_detection import face_detection
from deep_face_detection import detect

import ctypes
import _ctypes
import pygame
import sys
import os
import time
import numpy as np

from math import tanh, atan, pi, isnan

import Buttons
import inputbox
from buttons_pygame import Option

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

COLORS = ["red", 
                  "blue", 
                  "green", 
                  "orange", 
                  "purple", 
                  "yellow", 
                  "violet"]
 
class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        self.name = ""
        self.profile_selected = False
        
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)
        print(self._kinect.depth_frame_desc.Width, self._kinect.depth_frame_desc.Height)
        print(self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState
        joint1State = joints[joint1].TrackingState

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        # self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        # self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        #self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:

            if False and not self.profile_selected:
                profiles = os.listdir("profiles")
                if len(profiles) == 0:
                    self.name = inputbox.ask(self._screen, "Enter your name")
                    f = open("profiles/" + self.name, "w")
                    f.close()
                else:
                    menu_font = pygame.font.Font(None, 40)
                    x = 100
                    options = []
                    for prof in profiles:
                        options.append(Option(prof, (140, x), menu_font, self._screen))
                        x += 50
                        if x > 900:
                            break
                    options.append(Option("new profile", (140, x), menu_font, self._screen))
                    while True:
                        pygame.event.pump()

                        ev = pygame.event.get()

                        for event in ev:
                            if event.type == pygame.MOUSEBUTTONUP:
                                for option in options:
                                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                                        if option.text == "new profile":
                                            self.name = inputbox.ask(self._screen, "Enter your name")
                                            f = open("profiles/" + self.name, "w")
                                            f.close()
                                            self.profile_selected = True
                                        else:
                                            self.name = option.text
                                            self.profile_selected = True

                        self._screen.fill((0, 0, 0))
                        for option in options:
                            option.draw(self._screen, menu_font)
                        pygame.display.update()

                        if self.profile_selected:
                            break
                    pass
                    #display profile buttons
                self.profile_selected = True

            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop
                    
                
                            
                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                bb, pts=detect(frame)
                
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

                if len(bb) > 0:
                    pygame.draw.rect(self._frame_surface, (0, 255, 0), tuple(bb), 2)

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            listoflistofnumbers = []
            if self._bodies is not None:
                bodies_drawn = 0 
                for i in range(0, self._kinect.max_body_count):
                    '''if i > 0:
                        break'''
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    center_points = []
                    center_points.append(joint_points[PyKinectV2.JointType_Head])
                    center_points.append(joint_points[PyKinectV2.JointType_Neck])
                    center_points.append(joint_points[PyKinectV2.JointType_SpineShoulder])
                    center_points.append(joint_points[PyKinectV2.JointType_SpineMid])
                    center_points.append(joint_points[PyKinectV2.JointType_SpineBase])
                                       
                    listofnumbers = [point.x for point in center_points]
                    y_range = max([point.y for point in center_points]) - min([point.y for point in center_points])
                    
                    points_avg= (sum(listofnumbers)/len(listofnumbers))
                    diff = sum([min(1000, max(.0001, abs(points_avg - x))) for x in listofnumbers])
                    if isnan(diff):
                        diff = .0001
                    normdiff = atan(diff / float(y_range)) / (pi / 2.0)
                    #normdiff = tanh(diff / 100)
                    print(normdiff)
                    self._screen.fill((0, 0, 0))
                    grade= "?"
                    if(normdiff < 0.05):
                        grade = "A+"
                    elif(normdiff < 0.1):
                        grade = "A"
                    elif(normdiff < 0.2):
                        grade = "B"
                    elif(normdiff < 0.3):
                        grade = "C"
                    elif(normdiff < 0.35):
                        grade = "D"
                    else:
                        grade = "F :("

                    myfont = pygame.font.SysFont("monospace", 50)
                    normdiff = min(1, normdiff * 2.5)
                    difflabel1 = myfont.render(str(int(diff)), 1, (255 * normdiff, 255 * (1 - normdiff), 0))
                    lettergrade = myfont.render(grade, 1, (255 * normdiff, 255 * (1 - normdiff), 0))
                    profile_text = myfont.render(COLORS[i], 1, SKELETON_COLORS[i])
                    if bodies_drawn == 0:
                        pygame.draw.rect(self._frame_surface, (0, 0, 0), (0, 0, 1920, 108))
                    self._frame_surface.blit(difflabel1, (175 + (305 * bodies_drawn), 3))
                    self._frame_surface.blit(lettergrade, (25 + (305 * bodies_drawn), 3))
                    self._frame_surface.blit(profile_text, (25 + (305 * bodies_drawn), 54))
                    bodies_drawn += 1
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                
                                
            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height))
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(30)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()

__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();