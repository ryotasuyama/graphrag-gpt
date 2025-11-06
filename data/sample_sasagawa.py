import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("スケッチ1","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","デフォルト","384.92570447799812,276.54630352599389","-135.29311966786784,276.54630352599389",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","デフォルト","-135.29311966786781,276.54630352599389","-135.29311966786781,-486.20309829181588",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","デフォルト","-135.29311966786781,-486.20309829181593","384.92570447799812,-486.20309829181593",False)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","デフォルト","384.92570447799812,-486.20309829181593","384.92570447799812,276.54630352599384",False)
solid1 = part.CreateSolid("PL1","","SS400")
part.SetElementColor(solid1,"225","225","225","0")
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.Name="押し出し1"
extrudePram1.AddProfile(skt_pl1)
extrudePram1.DirectionType="N"
extrudePram1.DirectionParameter1="10"
extrudePram1.RefByGeometricMethod=True
extrude1 = part.CreateLinearSweep(solid1,"+",extrudePram1,False)
skt_pl2 = part.CreateSketchPlane("スケッチ2","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl2,True)
skt_ln5 = part.CreateSketchLine(skt_pl2,"","デフォルト","355.50976864133878,194.5295209304914","-99.567300286613147,194.5295209304914",False)
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType=0
ProfilePram1.AddAttachLines(skt_ln5)
ProfilePram1.AddAttachSurfaces(solid1+",F,124.81629240506514,-104.82839738291105,10")
ProfilePram1.BaseOnAttachLines=False
ProfilePram1.NotProjectAttachLines=False
ProfilePram1.ProfileName="Prf1"
ProfilePram1.MaterialName="SS400"
ProfilePram1.ProfileType=1003
ProfilePram1.ProfileParams=["300","90","13.000000000000002","17","19","9.5"]
ProfilePram1.Mold="+"
ProfilePram1.ReverseDir=False
ProfilePram1.ReverseAngle=False
ProfilePram1.CalcSnipOnlyAttachLines=False
ProfilePram1.AttachDirMethod=0
ProfilePram1.CCWDefAngle=False
ProfilePram1.End1Type=1103
ProfilePram1.End1TypeParams=["0"]
ProfilePram1.End2Type=1103
ProfilePram1.End2TypeParams=["0"]
ProfilePram1.End1ScallopType=-1
ProfilePram1.End2ScallopType=-1
profile1 = part.CreateProfile(ProfilePram1,False)
part.SetElementColor(profile1[0],"225","225","225","0")
bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=0
bracketPram1.BracketName="Bkt1"
bracketPram1.MaterialName="SS400"
bracketPram1.BasePlane="PL,X"
bracketPram1.BasePlaneOffset="50"
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="+"
bracketPram1.Thickness="10"
bracketPram1.BracketType=1501
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=0
bracketPram1.Surfaces1=[profile1[0]+",F,127.9712341773628,194.5295209304914,160"]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=["PLS","True","False","0","-0","1",solid1]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1531
bracketPram1.Sf1DimensonParams=["100","15"]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["100","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"225","225","225","0")
stlOpt = doc.CreateSTLOption()
stlOpt.ChordalTolerance=0.1
stlOpt.NormalTolerance=3.0
stlOpt.SigDigits = 12
stlOpt.Elements = [bracket1]
doc.ExporAsSTL("D:/WorkFiles/Bkt1.stl",stlOpt)
views = doc.GetViews()
views[0].SetDirection("1,0,0","0,0,1",True)

