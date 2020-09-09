
#Created by: Declan Quinn
#May 2019

#To run tests:
#In this file: [test_StandardAtmosphere.py]
#In all files in the current directory: [python -m unittest discover]
#Add [-v] for verbose output (displays names of all test functions)

import math
import unittest
from test.testUtilities import assertForceMomentSystemsAlmostEqual

import MAPLEAF.Rocket.AeroFunctions as AeroFunctions
from MAPLEAF.ENV.Environment import Environment
from MAPLEAF.IO.SimDefinition import SimDefinition
from MAPLEAF.IO.SubDictReader import SubDictReader
from MAPLEAF.Motion.CythonAngularVelocity import AngularVelocity
from MAPLEAF.Motion.ForceMomentSystem import ForceMomentSystem
from MAPLEAF.Motion.Inertia import Inertia
from MAPLEAF.Motion.CythonQuaternion import Quaternion
from MAPLEAF.Motion.RigidBody import RigidBodyState
from MAPLEAF.Motion.CythonVector import Vector
from MAPLEAF.Rocket.Nosecone import Nosecone
from MAPLEAF.Rocket.Rocket import Rocket


class TestNosecone(unittest.TestCase):
    def setUp(self):
        simDef = SimDefinition("test/simDefinitions/test3.mapleaf")
        rocketDictReader = SubDictReader("Rocket", simDef)
        self.rocket = Rocket(rocketDictReader)

        self.environment = Environment(silent=True)
        self.currentConditions = self.environment.getAirProperties(Vector(0,0,200)) # m

        self.rocketState1 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 200), Quaternion(Vector(0, 0, 1), 0), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState2 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 200), Quaternion(Vector(1, 0, 0), math.radians(2)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState3 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, 500), Quaternion(Vector(1, 0, 0), math.radians(2)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState4 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, -200), Quaternion(Vector(1, 0, 0), math.radians(180)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState5 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, -200), Quaternion(Vector(1, 0, 0), math.radians(178)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState6 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, -200), Quaternion(Vector(1, 0, 0), math.radians(182)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState7 = RigidBodyState(Vector(0, 0, 200), Vector(0, 0, -200), Quaternion(Vector(1, 0, 0), math.radians(90)), AngularVelocity(rotationVector=Vector(0, 0, 0)))
        self.rocketState8 = RigidBodyState(Vector(0, 0, 200), Vector(20.04, -0.12, -52.78), Quaternion(Vector(0, 1, 0), math.radians(90)), AngularVelocity(rotationVector=Vector(0, 0, 0)))

    def test_noseconeGetPlanformArea(self):
        nosecone = self.rocket.stages[0].getComponentsOfType(Nosecone)[0]
        self.assertAlmostEqual(nosecone._getPlanformArea(),0.077573818,3) #From solidworks
    
    # def test_noseconeOpenRocketAeroCoefficients(self):
    #     nosecone = self.rocket.stages[0].getComponentsOfType(Nosecone)[0]

    #     aeroForce = nosecone.getAeroForce(self.rocketState1, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState1))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState1, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 0
    #     axialForceHandCalc = 26.832023606232575
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState2, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState2))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState2, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 30.618783938108784
    #     axialForceHandCalc = 27.140046221672183
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState3, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState3))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState3, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 191.3673996131799
    #     axialForceHandCalc = 334.44731852792586
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState4, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState4))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState4, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 0
    #     axialForceHandCalc = 26.832023606232575
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState5, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState5))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState5, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 30.618783938108784
    #     axialForceHandCalc = 27.140046221672183
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState6, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState6))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState6, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 30.618783938108784
    #     axialForceHandCalc = 27.140046221672183
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce)

    #     aeroForce = nosecone.getAeroForce(self.rocketState7, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState7))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState7, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 877.27104
    #     axialForceHandCalc = 0
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce, 0)

    #     aeroForce = nosecone.getAeroForce(self.rocketState8, 0, self.currentConditions, self.rocket.getCG(0, self.rocketState8))
    #     normalForceDirection = AeroFunctions.getNormalAeroForceDirection(self.rocketState8, self.currentConditions)
    #     axialForceDirection = Vector(0, 0, -1) #By definition of axial force
    #     normalForceHandCalc = 65.6
    #     axialForceHandCalc = 0
    #     CpWRTNoseconeTip = Vector(0, 0, -0.47615415152) #Planform centroid
    #     normalForce = normalForceDirection.__mul__(normalForceHandCalc)
    #     axialForce = axialForceDirection.__mul__(axialForceHandCalc)
    #     appliedNormalForce = ForceMomentSystem(normalForce, CpWRTNoseconeTip)
    #     appliedAxialForce = ForceMomentSystem(axialForce, CpWRTNoseconeTip)
    #     correctAeroForce = appliedNormalForce + appliedAxialForce
        
    #     assertForceMomentSystemsAlmostEqual(self, aeroForce, correctAeroForce, -1)

#If this file is run by itself, run the tests above
if __name__ == '__main__':
    unittest.main()