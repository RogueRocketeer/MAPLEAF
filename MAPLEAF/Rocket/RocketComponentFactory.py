from MAPLEAF.IO.SubDictReader import SubDictReader
from MAPLEAF.Rocket.BoatTail import BoatTail, Transition
from MAPLEAF.Rocket.Bodytube import Bodytube
from MAPLEAF.Rocket.Fins import FinSet
from MAPLEAF.Rocket.Motor import Motor
from MAPLEAF.Rocket.Nosecone import Nosecone
from MAPLEAF.Rocket.RecoverySystem import RecoverySystem
from MAPLEAF.Rocket.RocketComponents import (AeroDamping, AeroForce, FixedForce,
                                         FixedMass, FractionalJetDamping,
                                         TabulatedAeroForce, TabulatedInertia)

    
stringNameToClassMap = {
    "AeroDamping":          AeroDamping,
    "AeroForce":            AeroForce,
    "BoatTail":             BoatTail,
    "Bodytube":             Bodytube,
    "FinSet":               FinSet,
    "Force":                FixedForce,
    "FractionalJetDamping": FractionalJetDamping,
    "Mass":                 FixedMass,
    "Motor":                Motor,
    "Nosecone":             Nosecone,
    "RecoverySystem":       RecoverySystem,
    "TabulatedAeroForce":   TabulatedAeroForce,
    "TabulatedInertia":     TabulatedInertia,
    "Transition":           Transition,
}

def rocketComponentFactory(subDictPath, rocket, stage):
    """
        Initializes a rocket component based on the stringNameToClassMap
        Inputs:
            subDictPath:        (string) Path to subDict in simulation definition, like "Rocket.Stage1.Nosecone"
            rocket:             (Rocket) that the component is a part of
            stage:              (Stage) That the component is a part of
        Also uses the stringNameToClassMap dictionary
    """       
    # Create SubDictReader for the rocket component's dictionary
    componentDictReader = SubDictReader(subDictPath, rocket.simDefinition)

    # Figure out which class to initialize
    className = componentDictReader.getString("class")
    referencedClass = stringNameToClassMap[className]
    
    # Initialize it
    return referencedClass(componentDictReader, rocket, stage)