SimControl{

    timeDiscretization RK12Adaptive # Dont know what this does
    timeStep           0.1 # Condense total simulation time by a factor of 10
    EndCondition Time # Condition could be apogee too
    EndConditionValue 300 # Simulation end time

    StageDropPaths{
        endCondition Time
        endConditionValue 300
    }

    TimeStepAdaptation{
        targetError 0.0005 # Allowable error?
    }

    plot TimeStep FlightAnimation Velocity FlightPaths


}

Environment{
    EarthModel Round # Round earth model
}

Rocket{
    position        (0 0 12.8943138534095) # m - CG at sea level
    rotationAxis    (0 1 0)
    rotationAngle   0
    Velocity        (0 0 0.1)
    angularVelocity (0 0 0)

    Aero{
        addZeroLengthBoatTailsToAccountForBaseDrag false
    }

    SecondStage{
        class           Stage
        stageNumber     2

      Mass{
            class           Mass
            mass            50
            position        (0 0 -2.6) # m - relative to stage tip
            cg              (0 0 0) # m - relative to position
            MOI             (66.6 66.6 0.21) # kg*m^2
        }

        Force{
            class           Force

            position        (0 0 0) # m, Force application location
            force           (0 0 0) # N
            moment          (0 1 0) # Nm
        }

        AeroForce{
            class           AeroForce
            
            position        (0 0 0) # m, Force application location
            Aref            0.25 # m^2, Reference area for all coefficients
            Lref            0.25 # m, Reference length for all moment coefficients

            Cd              0 # Applied parallel to wind direction
            Cl              0 # Applied normal to wind direction
            
            # (Local) X-, Y-, and Z-Axis Moment coefficients
            momentCoeffs    (0 0 0)
        }

        AeroDamping{
            class AeroDamping
            # No position - only applies moments

            Aref                0.25 # m^2 - used to redimensionalize coefficients
            Lref                0.25 # m - used to redimensionalize coefficients

            # Each damping coefficient is named:
            # For each axis below (x/y/z), damping coefficients are in order: ( x, y, z )
            #   Example xDampingCoeffs[0] == d{xMomentCoefficient}/d{AngularRate_x * Lref / (2 * Airspeed)}
            #   Example xDampingCoeffs[1] == d{xMomentCoefficient}/d{AngularRate_y * Lref / (2 * Airspeed)}
            #   etc...
            xDampingCoeffs      (0 0 0)
            yDampingCoeffs      (0 0 0)
            zDampingCoeffs      (0 0 0)
        }

        SecondStageMotor{
            class Motor
            path  MAPLEAF/Falcon1/Falcon1Stage2Motor.txt
        }
    }

    FirstStage{
        class Stage
        stageNumber 1
        position (0 0 -6.22707645415291)

        separationTriggerType motorBurnout
        separationDelay 100


        firstStageEngineJetDamping{
            class FractionalJetDamping
            fraction -0.5
        }

        FirstStageMotor{
            class Motor
            path MAPLEAF/Falcon1/Falcon1Stage1Motor.txt
        }
    }

    

}

