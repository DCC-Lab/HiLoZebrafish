try:
    from raytracing import *
except ImportError:
    raise ImportError('Raytracing module not found: "pip install raytracing"')

from raytracing import *

class Sparq:
    @staticmethod
    def illuminationFromObjective():
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")
        obj = olympus.XLUMPlanFLN20X()
        obj.flipOrientation()

        illumination = ImagingPath()
        illumination.label = "Sparq illumination"
        illumination.objectHeight = 0.7  # mm maximum, include diffuse spot size
        illumination.fanAngle = 0.5  # NA = 0.5
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = False

        illumination.append(obj)
        illumination.append(Space(d=120))
        illumination.append(L1)
        illumination.append(Space(d=40))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=30))
        illumination.append(L2)
        illumination.append(Space(d=57))
        illumination.append(L3)
        illumination.append(Space(d=40))
        illumination.append(L4)
        illumination.append(Space(d=20))
        illumination.append(LExc)
        illumination.append(Space(d=45))

        return illumination

    def illuminationFromSource():
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")
        obj = olympus.XLUMPlanFLN20X()

        illumination = ImagingPath()
        illumination.label = "Sparq illumination with Excelitas"
        illumination.objectHeight = 3.15
        illumination.fanAngle = 0.5  # NAdiffuser=1 alors mettre 0.5 ou 1?
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = False

        illumination.append(Space(d=45))
        illumination.append(LExc)
        illumination.append(Space(d=20))
        illumination.append(L4)
        illumination.append(Space(d=40))
        illumination.append(L3)
        illumination.append(Space(d=57))
        illumination.append(L2)
        illumination.append(Space(d=30))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=40))
        illumination.append(L1)
        illumination.append(Space(d=120))
        illumination.append(obj)

        return illumination

    def illuminationFromObjectiveWithOptotune():
    # Add tunable lens EL-16-40 and EL-10-30
        optotuneFocal = 100
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")
        Optotune = Lens(f=optotuneFocal, diameter=10, label='Optotune')
        obj = olympus.XLUMPlanFLN20X()
        obj.flipOrientation()

        illumination = ImagingPath()
        illumination.label = "Sparq illumination with Optotune"
        illumination.objectHeight = 0.7  # mm maximum, include diffuse spot size
        illumination.fanAngle = 0.5  # NA = 0.5
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = False

        illumination.append(obj)
        illumination.append(Space(d=40))
        illumination.append(Optotune)
        illumination.append(Space(d=45+47.5))
        illumination.append(L1)
        illumination.append(Space(d=40))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=30))
        illumination.append(L2)
        illumination.append(Space(d=57))
        illumination.append(L3)
        illumination.append(Space(d=40))
        illumination.append(L4)
        illumination.append(Space(d=20))
        illumination.append(LExc)
        illumination.append(Space(d=45))

        return illumination

    def illuminationFromSourceWithOptotune():
    # Add tunable lens EL-16-40 and EL-10-30
        optotuneFocal = 100
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")
        Optotune = Lens(f=optotuneFocal, diameter=10, label='Optotune')
        obj = olympus.XLUMPlanFLN20X()

        illumination = ImagingPath()
        illumination.label = "Sparq illumination with Optotune"
        illumination.objectHeight = 3.15
        illumination.fanAngle = 0.5  # NAdiffuser=1 alors mettre 0.5 ou 1?
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = False

        illumination.append(Space(d=45))
        illumination.append(LExc)
        illumination.append(Space(d=20))
        illumination.append(L4)
        illumination.append(Space(d=40))
        illumination.append(L3)
        illumination.append(Space(d=57))
        illumination.append(L2)
        illumination.append(Space(d=30))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=40))
        illumination.append(L1)
        illumination.append(Space(d=75))
        illumination.append(Optotune)
        illumination.append(Space(d=45))
        illumination.append(obj)

        return illumination

    def illuminationFromSourceWithOptotuneAndDivergentLens():
    # Add tunable lens EL-16-40 and EL-10-30
        optotuneFocal = 58.5
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")
        Optotune = Lens(f=optotuneFocal, diameter=16, label='Optotune')
        L5 = Lens(f=-75, diameter=35, label='Divergent lens')
        obj = olympus.XLUMPlanFLN20X()

        illumination = ImagingPath()
        illumination.label = "Sparq illumination with Optotune and divergent lens"
        illumination.objectHeight = 3.15
        illumination.fanAngle = 0.5  # NAdiffuser=1 alors mettre 0.5 ou 1?
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = False

        illumination.append(Space(d=45))
        illumination.append(LExc)
        illumination.append(Space(d=20))
        illumination.append(L4)
        illumination.append(Space(d=40))
        illumination.append(L3)
        illumination.append(Space(d=57))
        illumination.append(L2)
        illumination.append(Space(d=30))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=40))
        illumination.append(L1)
        illumination.append(Space(d=65))
        illumination.append(L5)
        illumination.append(Space(d=10))
        illumination.append(Optotune)
        illumination.append(Space(d=45))
        illumination.append(obj)

        return illumination

    def illuminationFromObjectiveToCamera():
        """ ADD OPTOTUNE"""
        obj = olympus.XLUMPlanFLN20X()
        tubeLens = Lens(f=100, diameter=75, label="Tube Lens")
        obj.flipOrientation()

        illumination = ImagingPath()
        illumination.label = "Microscope system"
        illumination.objectHeight = 0.7  # mm maximum, include diffuse spot size
        illumination.fanAngle = 0.5  # NA = 0.5
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = True

        illumination.append(obj)
        illumination.append(Space(d=100))
        illumination.append(tubeLens)
        illumination.append(Space(d=100))

        return illumination



    def tracingForIlluminatorMagnification():
        L1 = Lens(f=40, diameter=30, label="$L_1$")
        L2 = Lens(f=30, diameter=20, label="$L_2$")
        L3 = Lens(f=-35, diameter=22, label="$L_3$")
        L4 = Lens(f=75, diameter=32, label="$L_4$")
        LExc = Lens(f=45, diameter=35, label="Exc")

        illumination = ImagingPath()
        illumination.label = "Illumination only illuminator"
        illumination.objectHeight = 3.15
        illumination.fanAngle = 0.5
        illumination.fanNumber = 11
        illumination.rayNumber = 3
        illumination.showImages = True

        illumination.append(Space(d=45))
        illumination.append(LExc)
        illumination.append(Space(d=20))
        illumination.append(L4)
        illumination.append(Space(d=40))
        illumination.append(L3)
        illumination.append(Space(d=57))
        illumination.append(L2)
        illumination.append(Space(d=30))
        illumination.append(Aperture(diameter=30, label="CF"))
        illumination.append(Space(d=20))
        illumination.append(Aperture(diameter=30, label="AF"))
        illumination.append(Space(d=40))
        illumination.append(L1)
        illumination.append(Space(d=120))

        return illumination


if __name__ == "__main__":

    Sparq.illuminationFromObjective().display()
    Sparq.illuminationFromSource().display()
    Sparq.illuminationFromObjectiveWithOptotune().display()
    Sparq.illuminationFromSourceWithOptotune().display()
    Sparq.illuminationFromSourceWithOptotuneAndDivergentLens().display()
    Sparq.illuminationFromObjectiveToCamera().display()
    Sparq.tracingForIlluminatorMagnification().display()