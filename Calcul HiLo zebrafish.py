import numpy as np

""" Calculs des différents paramètres pour le microscope HiLo, distance en mm"""
""" Les valeurs choisies sont actuellement celles du macro HiLo, mais elles seront modifiées au fil de la 
progression du microscope """

# Objective
ObjectiveNA = 0.5
ObjectiveWorkingDistance = 3.5
FocalOfLensHabituallyUsedWithObjective = 180
ObjectiveMagnification = 20
FocalObjective = FocalOfLensHabituallyUsedWithObjective/ObjectiveMagnification
ObjectiveDiameterEntrancePupil = 2*FocalObjective*ObjectiveNA
FocalOfTubeLens = 100
FieldNumber = 26.5
Magnification = FocalOfTubeLens/FocalObjective
ObjectiveMaximumFOV = FieldNumber/Magnification

# Camera
CameraDiagonal = 16
CameraMaximumFOV = CameraDiagonal/Magnification
CameraPixelSize = 4.54

# Suite objective
ObjectiveINV = ObjectiveNA*((CameraMaximumFOV*0.5)**2)*np.pi
ObjectiveNAWithINV = ObjectiveINV/(((ObjectiveDiameterEntrancePupil*0.5)**2)*np.pi)
SourceMinAngleAtObjective = np.degrees(ObjectiveNAWithINV)

# 4f system
Lens1Focal = 100
Lens1Diameter = 75
Lens2Focal = 200
Lens2Diameter = 75
LensMagnification = Lens2Focal/Lens1Focal

# Source (Diffuser)
SourceDiameter = 22
SourceDiameterToFillEntrancePupil = ObjectiveDiameterEntrancePupil/LensMagnification
SourceDiameterAtEntrancePupil = SourceDiameter*LensMagnification
SourceMaxAngleAtObjective = np.degrees(np.sin(((Lens2Diameter-SourceDiameterAtEntrancePupil)/2)/Lens2Focal))
DiffuserNA = 1

# Fiber and Speckles
Wavelength = 488*10**-6
FiberRadius = 0.75
FiberNA = 0.39
AverageGrainSize = Wavelength/(2*FiberNA)
MaxGrainNumber = np.pi*(FiberRadius/AverageGrainSize)**2
# DistanceBetweenFiberDifuser = ?

# Resolution
IndexBetweenObjectiveAndSample = 1
ResolutionLateralTheoretical = 1.22*Wavelength/ObjectiveNA
ResolutionAxialTheoretical = IndexBetweenObjectiveAndSample*(Wavelength/ObjectiveNA**2+ResolutionLateralTheoretical/(ObjectiveMagnification*ObjectiveNA))

print("FocalObjective = {} mm".format(FocalObjective),
      "ObjectiveDiameterEntrancePupil = {} mm".format(ObjectiveDiameterEntrancePupil),
      "Magnification = {}".format(Magnification),
      "ObjectiveMaximumFOV = {} mm".format(ObjectiveMaximumFOV),
      "CameraMaximumFOV = {} mm".format(CameraMaximumFOV),
      "ObjectiveINV = {}".format(ObjectiveINV),
      "ObjectiveNAWithINV = {}".format(ObjectiveNAWithINV),
      "SourceMinAngleAtObjective = {}°".format(SourceMinAngleAtObjective),
      "LensMagnification = {}".format(LensMagnification),
      "SourceOriginalDiameterToFillEntrancePupil = {} mm".format(SourceDiameterToFillEntrancePupil),
      "SourceDiameterAtEntrancePupil = {} mm".format(SourceDiameterAtEntrancePupil),
      "SourceMaxAngleAtObjective = {}°".format(SourceMaxAngleAtObjective),
      "AverageGrainSize = {} nm".format(AverageGrainSize*10**6),
      "MaxGrainNumber = {}".format(MaxGrainNumber),
      "ResolutionLateralTheoretical = {} µm".format(ResolutionLateralTheoretical*10**3),
      "ResolutionAxialTheoretical = {} µm".format(ResolutionAxialTheoretical*10**3),
      sep="\n")

