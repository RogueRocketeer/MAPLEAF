#Created by: Henry Stoldt
#May 2019

#To run tests:
#In this file: [test_rigidBody.py]
#In all files in the current directory: [python -m unittest discover]
#Add [-v] for verbose output (displays names of all test functions)

import math
import unittest
from math import cos, pi, sin

from MAPLEAF.Motion.CythonAngularVelocity import AngularVelocity
from MAPLEAF.IO.SimDefinition import SimDefinition
from MAPLEAF.Motion.ForceMomentSystem import ForceMomentSystem
from MAPLEAF.Motion.Inertia import Inertia
from MAPLEAF.Motion.CythonQuaternion import Quaternion
from MAPLEAF.Motion.RigidBody import RigidBody, RigidBodyState
from test.testUtilities import (
    assertAngVelAlmostEqual, assertIterablesAlmostEqual,
    assertQuaternionsAlmostEqual, assertRigidBodyStatesalmostEqual,
    assertVectorsAlmostEqual)
from MAPLEAF.Motion.CythonVector import Vector


class TestRigidBody(unittest.TestCase):
    def setUp(self):
        self.zeroVec = Vector(0,0,0)
        self.zeroQuat = Quaternion(axisOfRotation=Vector(1,0,0), angle=0)
        self.zeroAngVel = AngularVelocity(axisOfRotation=Vector(1,0,0), angularVel=0)
        self.zeroForce = ForceMomentSystem(self.zeroVec)
        self.oneVec = Vector(1,1,1)
        self.simDefinition = SimDefinition("test/simDefinitions/AdaptTimeStep.mapleaf", silent=True)
        self.simDefinition.setValue("SimControl.TimeStepAdaptation.minTimeStep", "1")
        #TODO: Get some tests for the higher order adaptive methods in here
        self.integrationMethods = [ "Euler", "RK2Heun", "RK2Midpoint", "RK4", "RK12Adaptive" ]
        self.constInertia = Inertia(self.oneVec, self.zeroVec, 1)

    ############################ TESTS RUN FOR EACH INTEGRATION METHOD #######################
    def uniformXMotionTest(self, integrationMethod):
        movingXState = RigidBodyState(self.zeroVec, Vector(1,0,0), self.zeroQuat, self.zeroAngVel)
        constInertia = Inertia(self.oneVec, self.zeroVec, 1)
        def constInertiaFunc(*allArgs):
            return constInertia
        def zeroForceFunc(*allArgs):
            return self.zeroForce
        movingXBody = RigidBody(movingXState, zeroForceFunc, constInertiaFunc, integrationMethod=integrationMethod, simDefinition=self.simDefinition)
        movingXBody.timeStep(1)

        newPos = movingXBody.state.position
        assertVectorsAlmostEqual(self, newPos, Vector(1,0,0))

    def uniformZRotationTest(self, integrationMethod):
        rotatingZState = RigidBodyState(self.zeroVec, self.zeroVec, self.zeroQuat, AngularVelocity(axisOfRotation=Vector(0,0,1), angularVel=pi))
        constInertia = Inertia(self.oneVec, self.zeroVec, 1)
        def constInertiaFunc(*allArgs):
            return constInertia
        def constForceFunc(*allArgs):
            return self.zeroForce
        rotatingZBody = RigidBody(rotatingZState, constForceFunc, constInertiaFunc, integrationMethod=integrationMethod, simDefinition=self.simDefinition)
        rotatingZBody.timeStep(1)

        newOrientation = rotatingZBody.state.orientation
        expectedOrientation = Quaternion(axisOfRotation=Vector(0,0,1), angle=pi)
        assertQuaternionsAlmostEqual(self, newOrientation, expectedOrientation)

    def uniformXAccelerationTest(self, integrationMethod):
        constantXForce = ForceMomentSystem(Vector(1,0,0))
        movingXState = RigidBodyState(self.zeroVec, self.zeroVec, self.zeroQuat, self.zeroAngVel)
        def constInertiaFunc(*allArgs):
            return self.constInertia
        def constXForceFunc(*allArgs):
            return constantXForce
        movingXBody = RigidBody(movingXState, constXForceFunc, constInertiaFunc, integrationMethod=integrationMethod, simDefinition=self.simDefinition)
        movingXBody.timeStep(1)

        newPos = movingXBody.state.position
        newVel = movingXBody.state.velocity
        assertVectorsAlmostEqual(self, newVel, Vector(1,0,0))
        if integrationMethod == "Euler":
            assertVectorsAlmostEqual(self, newPos, Vector(0,0,0))
        else:
            assertVectorsAlmostEqual(self, newPos, Vector(0.5,0,0))

    def uniformlyAcceleratingRotationTest(self, integrationMethod):
        constantZMoment = ForceMomentSystem(self.zeroVec, moment=Vector(0,0,1))
        restingState = RigidBodyState(self.zeroVec, self.zeroVec, self.zeroQuat, self.zeroAngVel)
        def constZMomentFunc(*allArgs):
            return constantZMoment
        def constInertiaFunc(*allArgs):
            return self.constInertia
        acceleratingZRotBody = RigidBody(restingState, constZMomentFunc, constInertiaFunc, integrationMethod=integrationMethod, simDefinition=self.simDefinition)
        acceleratingZRotBody.timeStep(1)

        newOrientation = acceleratingZRotBody.state.orientation
        newAngVel = acceleratingZRotBody.state.angularVelocity

        #print("{}: {}".format(integrationMethod, newOrientation))

        assertAngVelAlmostEqual(self, newAngVel, AngularVelocity(axisOfRotation=Vector(0,0,1), angularVel=1))
        if integrationMethod == "Euler":
            assertQuaternionsAlmostEqual(self, newOrientation, Quaternion(axisOfRotation=Vector(0,0,1), angle=0))
        else:
            assertQuaternionsAlmostEqual(self, newOrientation, Quaternion(axisOfRotation=Vector(0,0,1), angle=0.5))
        
    def complexRotationTest(self, integrationMethod):
        '''
            Test where the rigid body is first accelerated and decelerated about the y-axis, completing a 90 degree rotaion, 
            subsequently does the same about the z-axis 
        '''
        initXAxis = Vector(1,0,0)
        initYAxis = Vector(0,1,0)
        initZAxis = Vector(0,0,1)

        initOrientation = Quaternion(axisOfRotation = Vector(1,0,0), angle = 0)

        initAngularMomentum = AngularVelocity(rotationVector = self.zeroVec)

        complexRotatingState = RigidBodyState(self.zeroVec, self.zeroVec, initOrientation, initAngularMomentum)

        def step1MomentFunc(*allArgs):
            return ForceMomentSystem(self.zeroVec, moment=Vector(0,0.5,0)) #Acceleration and deceleration steps to give 90 degree rotations in each axis
        def step2MomentFunc(*allArgs):
            return ForceMomentSystem(self.zeroVec, moment=Vector(0,-0.5,0)) #using a time step of pi
        def step3MomentFunc(*allArgs):
            return ForceMomentSystem(self.zeroVec, moment=Vector(0,0,0.5)) #There is one acceleration and one deceleration for each rotation to make it static
        def step4MomentFunc(*allArgs):
            return ForceMomentSystem(self.zeroVec, moment=Vector(0,0,-0.5))

        def constInertiaFunc(*allArgs):
            return self.constInertia

        # Create rigid body and apply moments for one time step each
        self.simDefinition.setValue("SimControl.TimeStepAdaptation.minTimeStep", str(math.sqrt(math.pi)))
        complexRotatingBody = RigidBody(complexRotatingState, step1MomentFunc, constInertiaFunc, integrationMethod = integrationMethod, simDefinition=self.simDefinition)
        complexRotatingBody.timeStep(math.sqrt(math.pi)) #Apply each moment and do the timestep
        complexRotatingBody.forceFunc = step2MomentFunc
        complexRotatingBody.timeStep(math.sqrt(math.pi))
        complexRotatingBody.forceFunc = step3MomentFunc
        complexRotatingBody.timeStep(math.sqrt(math.pi))
        complexRotatingBody.forceFunc = step4MomentFunc
        complexRotatingBody.timeStep(math.sqrt(math.pi))

        newXVector = complexRotatingBody.state.orientation.rotate(initXAxis) #Calculate the new vectors from the integration in the rigid body
        newYVector = complexRotatingBody.state.orientation.rotate(initYAxis)
        newZVector = complexRotatingBody.state.orientation.rotate(initZAxis)

        correctRotation1 = Quaternion(axisOfRotation = initYAxis, angle = math.pi/2) #Calculate the new vectors by hand (90 degree rotations)
        newCorrectXAxis1 = correctRotation1.rotate(initXAxis) # (0, 0, -1)
        newCorrectYAxis1 = correctRotation1.rotate(initYAxis) # (0, 1, 0)
        newCorrectZAxis1 = correctRotation1.rotate(initZAxis) # (1, 0, 0)
        
        correctRotation2Axis = newCorrectZAxis1 #(1, 0, 0)
        correctRotation2 = Quaternion(axisOfRotation = correctRotation2Axis, angle = math.pi/2)
        newCorrectXAxis2 = correctRotation2.rotate(newCorrectXAxis1) # (0, 1, 0)
        newCorrectYAxis2 = correctRotation2.rotate(newCorrectYAxis1) # (0, 0, 1)
        newCorrectZAxis2 = correctRotation2.rotate(newCorrectZAxis1) # (1, 0, 0)

        assertVectorsAlmostEqual(self, newXVector, newCorrectXAxis2)
        assertVectorsAlmostEqual(self, newYVector, newCorrectYAxis2)
        assertVectorsAlmostEqual(self, newZVector, newCorrectZAxis2)
     
    ############## TEST FUNCTIONS CALLED BY UNITTEST, LOOP THROUGH ALL THE INTEGRATION METHODS ######
    def test_UniformXMotion(self):
        for intMethod in self.integrationMethods:
            self.uniformXMotionTest(intMethod)

    def test_UniformZRotation(self):
        for intMethod in self.integrationMethods:
            self.uniformZRotationTest(intMethod)

    def test_UniformXAccel(self):
        for intMethod in self.integrationMethods:
            self.uniformXAccelerationTest(intMethod)

    def test_UniformZRotationAccel(self):
        for intMethod in self.integrationMethods:
            self.uniformlyAcceleratingRotationTest(intMethod)

    def test_ComplexRotations(self):
        for intMethod in self.integrationMethods:
            self.complexRotationTest(intMethod)

    ############## OTHER TESTS ######
    def test_nonPrincipalAxisRotation(self):
        initAngVel = AngularVelocity(rotationVector=Vector(1, 0, 1))
        rotatingZState = RigidBodyState(self.zeroVec, self.zeroVec, self.zeroQuat, initAngVel)
        
        constForce = ForceMomentSystem(self.zeroVec)
        def constForceFunc(*allArgs):
            return constForce
        
        constInertia = Inertia(Vector(2, 2, 8), self.zeroVec, 1)
        def constInertiaFunc(*allArgs):
            return constInertia

        rotatingZBody = RigidBody(rotatingZState, constForceFunc, constInertiaFunc, integrationMethod="RK4", simDefinition=self.simDefinition)

        dt = 0.01
        nTimeSteps = 10
        totalTime = dt*nTimeSteps

        for i in range(nTimeSteps):
            rotatingZBody.timeStep(dt)

        finalAngVel = rotatingZBody.state.angularVelocity

        omega = (constInertia.MOI.Z - constInertia.MOI.X) / constInertia.MOI.X
        expectedAngVel = AngularVelocity(rotationVector=Vector(cos(omega*totalTime), sin(omega*totalTime) ,1))

        assertAngVelAlmostEqual(self, finalAngVel, expectedAngVel)

#If the file is run by itself, run the tests above
if __name__ == '__main__':
    unittest.main()