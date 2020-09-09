
#Created by: Declan Quinn
#May 2019

#To run tests:
#In this file: [test_StandardAtmosphere.py]
#In all files in the current directory: [python -m unittest discover]
#Add [-v] for verbose output (displays names of all test functions)

import math
import unittest
from test.testUtilities import (assertForceMomentSystemsAlmostEqual,
                                assertVectorsAlmostEqual)

import MAPLEAF.Rocket.AeroFunctions as AeroFunctions
from MAPLEAF.ENV.Environment import Environment
from MAPLEAF.IO.SimDefinition import SimDefinition
from MAPLEAF.IO.SubDictReader import SubDictReader
from MAPLEAF.Motion.CythonAngularVelocity import AngularVelocity
from MAPLEAF.Motion.CythonQuaternion import Quaternion
from MAPLEAF.Motion.CythonVector import Vector
from MAPLEAF.Motion.ForceMomentSystem import ForceMomentSystem
from MAPLEAF.Motion.Inertia import Inertia
from MAPLEAF.Motion.RigidBody import RigidBodyState
from MAPLEAF.Rocket.Bodytube import Bodytube
from MAPLEAF.Rocket.Rocket import Rocket
from MAPLEAF.SimulationRunners import SingleSimRunner


class TestBodyTube(unittest.TestCase):
    def setUp(self):
        simDef = SimDefinition("test/simDefinitions/test3.mapleaf")
        rocketDictReader = SubDictReader("Rocket", simDef)
        self.rocket = Rocket(rocketDictReader)

        self.environment = Environment(silent=True)
        self.currentConditions = self.environment.getAirProperties(Vector(0,0,200)) # m

        self.rocketState1 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 200), Quaternion(Vector(0, 0, 1), 0), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState2 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 200), Quaternion(Vector(1, 0, 0), math.radians(2)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState3 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 500), Quaternion(Vector(1, 0, 0), math.radians(2)), AngularVelocity(rotationVector=Vector(0, 0, 0)))

    # def test_bodytubeOpenRocketAeroCoefficients(self):
    #     time = 1

    #     bodyTube = self.rocket.stages[0].getComponentsOfType(Bodytube)[0]

    #     aeroForce = bodyTube.getAeroForce(self.rocketState1, time, self.currentConditions, self.rocket.getCG(0, self.rocketState1))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState1, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 0
    #     axialForceHandCalc = 86.86005
    #     CpWRTNoseconeTip = Vector(0, 0,  -0.762 - 1) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce

    #     assertVectorsAlmostEqual(self, bodyTube.CPLocation, Vector(0,0,-1.762))
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce, 4)
    
    #     aeroForce = bodyTube.getAeroForce(self.rocketState2, time, self.currentConditions, self.rocket.getCG(0, self.rocketState2))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState2, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 9.820304
    #     axialForceHandCalc = 87.857221
    #     CpWRTNoseconeTip = Vector(0, 0,  -1.762) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce

    #     assertVectorsAlmostEqual(self, bodyTube.CPLocation, Vector(0,0,-1.762))
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce, 6)

    #     aeroForce = bodyTube.getAeroForce(self.rocketState3, time, self.currentConditions, self.rocket.getCG(0, self.rocketState3))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState3, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 61.3769010
    #     axialForceHandCalc = 483.10726
    #     CpWRTNoseconeTip = Vector(0, 0,  -0.762 - 1) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce

    #     assertVectorsAlmostEqual(self, bodyTube.CPLocation, Vector(0,0,-1.762))
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce, 5)

    def test_bodyTubeDampingMoment(self):
        simRunner = SingleSimRunner("test/simDefinitions/test3.mapleaf", silent=True)
        rocket = simRunner.prepRocketForSingleSimulation()

        bodyTube = rocket.stages[0].getComponentsOfType(Bodytube)[0]

        # Create a rigid body state rotating at 2 rad/s about the x-axis
        pos = Vector(0,0,0)
        vel = Vector(0,0,0)
        orientation = Quaternion(1,0,0,0)
        angVel = AngularVelocity(2,0,0)
        xRotatingState = RigidBodyState(pos, vel , orientation, angVel)
        envConditions = rocket.environment.getAirProperties(Vector(0,0,0))
        
         #### CoR = Middle of the body tube ####
        fakeRocketCG = Vector(0,0,-1.762)

        # Get computed (numerically-integrated) result
        calculatedDampingMoment = bodyTube._computeLongitudinalDampingMoments(xRotatingState, envConditions, fakeRocketCG, nSegments=100)

        # Compute analytical result (Niskanen Eqn 3.58) * 2 for both halves of the body tube (above and below center of rotation)
        expectedXDampingMoment = 2 * 0.275 * envConditions.Density * (bodyTube.outerDiameter/2) * 4
        expectedTotalDampingMoment = Vector(-expectedXDampingMoment, 0, 0)

        # Compare
        assertVectorsAlmostEqual(self, calculatedDampingMoment, expectedTotalDampingMoment, 4)



        #### Case 2: CoR at End of Body Tube ####
        fakeRocketCG = Vector(0,0,-2.762)

        # Get computed (numerically-integrated) result
        calculatedDampingMoment = bodyTube._computeLongitudinalDampingMoments(xRotatingState, envConditions, fakeRocketCG, nSegments=150)

        # Factor of 16 from moving to a tube length of two (2^4 = 16), but dividing by two (one half instead of two)
        expectedTotalDampingMoment *= 8

        # Compare
        assertVectorsAlmostEqual(self, calculatedDampingMoment, expectedTotalDampingMoment, 4)        

#If this file is run by itself, run the tests above
if __name__ == '__main__':
    unittest.main()
