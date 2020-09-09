
#Created by: Declan Quinn
#May 2019

#To run tests:
#In this file: [test_StandardAtmosphere.py]
#In all files in the current directory: [python -m unittest discover]
#Add [-v] for verbose output (displays names of all test functions)

import math
import unittest
from test.testUtilities import assertForceMomentSystemsAlmostEqual, assertIterablesAlmostEqual

from Main import SingleSimRunner
from MAPLEAF.ENV.Environment import Environment
from MAPLEAF.IO.SimDefinition import SimDefinition
from MAPLEAF.IO.SubDictReader import SubDictReader
from MAPLEAF.Motion.ForceMomentSystem import ForceMomentSystem
from MAPLEAF.Motion.Inertia import Inertia
from MAPLEAF.Motion.CythonVector import Vector
from MAPLEAF.Motion.CythonQuaternion import Quaternion
from MAPLEAF.Motion.RigidBodyStates import RigidBodyState
from MAPLEAF.Rocket.Bodytube import Bodytube
from MAPLEAF.Rocket.Nosecone import Nosecone
from MAPLEAF.Rocket.Rocket import Rocket
from MAPLEAF.Rocket.RocketComponents import FixedMass, FixedForce, TabulatedAeroForce


class TestRocketComponents(unittest.TestCase):
    def setUp(self):
        simDef = SimDefinition("test/simDefinitions/test3.mapleaf", silent=True)
        rocketDictReader = SubDictReader("Rocket", simDef)
        self.rocket = Rocket(rocketDictReader, silent=True)

        self.nosecone = self.rocket.stages[0].getComponentsOfType(Nosecone)[0]
        self.bodytube = self.rocket.stages[0].getComponentsOfType(Bodytube)[0]
        
        # Find the Fixed Mass component that's actually just a Fixed Mass, not a child class (Nosecone, Bodytube)
        fixedMassComponents = self.rocket.stages[0].getComponentsOfType(FixedMass)
        for comp in fixedMassComponents:
            if type(comp) == FixedMass:
                self.fixedMass = comp

        self.environment = Environment(silent=True)
        self.currentConditions = self.environment.getAirProperties(Vector(0,0,200)) # m

    #### FixedMass ####
    def test_getMass(self):
        self.assertEqual(self.nosecone.getMass(0), 5)
        self.assertEqual(self.bodytube.getMass(0), 50)
        self.assertEqual(self.fixedMass.getMass(0), 100)

    def test_getCG(self):
        self.almostEqualVectors(self.nosecone.getCG(0), Vector(0, 0, -0.2))
        self.almostEqualVectors(self.bodytube.getCG(0), Vector(0, 0, -1))
        self.almostEqualVectors(self.fixedMass.getCG(0), Vector(0, 0, 0))

    def test_getInertia(self):
        noseconeInertia = Inertia(Vector(0.001,0.001,0.001), Vector(0,0,-0.2), mass=5)
        bodytubeInertia = Inertia(Vector(0.001,0.001,0.001), Vector(0,0,-1), mass=50)
        generalInertia = Inertia(Vector(0.001,0.001,0.001), Vector(0,0,0.0), mass=100)
        
        state = self.rocket.rigidBody.state
        
        self.almostEqualVectors(self.nosecone.getInertia(0, state).CG, noseconeInertia.CG)        
        self.assertEqual(self.nosecone.getInertia(0, state).mass, noseconeInertia.mass)
        self.almostEqualVectors(self.bodytube.getInertia(0, state).CG, bodytubeInertia.CG)
        self.assertEqual(self.bodytube.getInertia(0, state).mass, bodytubeInertia.mass)
        self.almostEqualVectors(self.fixedMass.getInertia(0, state).CG, generalInertia.CG)
        self.assertEqual(self.fixedMass.getInertia(0, state).mass, generalInertia.mass)
    
    ### FixedForce ###
    def test_fixedForceInit(self):
        simDef = SimDefinition("test/simDefinitions/FixedForce.mapleaf", silent=True)
        rocketDictReader = SubDictReader("Rocket", simDef)
        rocket = Rocket(rocketDictReader, silent=True)

        fixedForce = rocket.stages[0].getComponentsOfType(FixedForce)[0]

        expectedFMS = ForceMomentSystem(Vector(0,0,0), Vector(0,0,0), Vector(0,1,0))
        assertForceMomentSystemsAlmostEqual(self, fixedForce.force, expectedFMS)

    def test_getFixedForceInertia(self):
        simDef = SimDefinition("test/simDefinitions/FixedForce.mapleaf", silent=True)
        rocketDictReader = SubDictReader("Rocket", simDef)
        rocket = Rocket(rocketDictReader, silent=True)
        
        fixedForce = rocket.stages[0].getComponentsOfType(FixedForce)[0]
        
        inertia = fixedForce.getInertia(0, "fakeState")
        expectedInertia = Inertia(Vector(0,0,0), Vector(0,0,0), 0)
        self.assertEqual(inertia, expectedInertia)

    def test_getFixedForce(self):
        simDef = SimDefinition("test/simDefinitions/FixedForce.mapleaf", silent=True)
        rocketDictReader = SubDictReader("Rocket", simDef)
        rocket = Rocket(rocketDictReader, silent=True)

        fixedForce = rocket.stages[0].getComponentsOfType(FixedForce)[0]

        force = fixedForce.getAeroForce("fakeState", 0, "fakeEnv", Vector(0,0,0))
        expectedForce = ForceMomentSystem(Vector(0,0,0), moment=Vector(0,1,0))
        self.assertEqual(force.force, expectedForce.force)
        self.assertEqual(force.moment, expectedForce.moment)

    ### TabulatedAeroForce ###
    def test_TabulatedAeroForce(self):
        # Init rocket that uses tabulated aero data
        simDef = SimDefinition("test/simDefinitions/NASATwoStageOrbitalRocket.mapleaf", silent=True)
        rocketDictReader = SubDictReader("Rocket", simDef)
        rocket = Rocket(rocketDictReader, silent=True)

        comp1, comp2, comp3 = rocket.stages[0].getComponentsOfType(TabulatedAeroForce)

        if comp1.Lref == 3.0:
            tabMoment = comp1
            tabFOrce = comp2
        else:
            tabMoment = comp2
            tabForce = comp1

        zeroAOAState = RigidBodyState(Vector(0,0,0), Vector(0,0,100), Quaternion(1,0,0,0), Vector(0,0,0))
        
        # CD, CL, CMx, CMy, CMz
        expectedAero = [ 0.21, 0, 0, 0, 0 ]
        calculatedAero = tabForce._getAeroCoefficients(zeroAOAState, self.currentConditions)
        assertIterablesAlmostEqual(self, expectedAero, calculatedAero)

        expectedAero = [ 0, 0, 0, 0, 0 ]
        calculatedAero = tabMoment._getAeroCoefficients(zeroAOAState, self.currentConditions)
        assertIterablesAlmostEqual(self, expectedAero, calculatedAero)

    #### Test Number of headers match number of entries for Force Logging ####
    def test_Logging(self):
        simRunner = SingleSimRunner("test/simDefinitions/test9.mapleaf", silent=True)
        rocket = simRunner.prepRocketForSingleSimulation()

        state = rocket.rigidBody.state
        time = 1

        # Check that each component logs an equal number of columns to what it has in its header
        for stage in rocket.stages:
            for component in stage.components:
                rocket.forceEvaluationLog = ["",]

                try:
                    headerItemsCount = len(component.getLogHeader().split())
                    component.getAeroForce(state, time, self.currentConditions, Vector(0,0,0))
                    loggedItemsCount = len(simRunner.forceEvaluationLog[0].split())
                    self.assertEqual(headerItemsCount, loggedItemsCount)
                except AttributeError:
                    pass

    #### Utilities ####
    def almostEqualVectors(self, Vector1, Vector2, n=7):
        self.assertAlmostEqual(Vector1.X, Vector2.X, n)
        self.assertAlmostEqual(Vector1.Y, Vector2.Y, n)
        self.assertAlmostEqual(Vector1.Z, Vector2.Z, n)

#If this file is run by itself, run the tests above
if __name__ == '__main__':
    unittest.main()
