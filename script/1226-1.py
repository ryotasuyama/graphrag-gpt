import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("HK.Ax.Deck","","PL,X","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","作図","15500,31800","15500,-2999.9999999999964",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","作図","-15499.999999999996,31800","-15500,-2999.9999999999964",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","作図","0,-3000","0,31799.999999999996",False)
skt_layer1 = part.CreateSketchLayer("General.Deck.UpperDeck",skt_pl1)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","General.Deck.UpperDeck","2000,15300","18500,14933.333333333334",False)
skt_ln5 = part.CreateSketchLine(skt_pl1,"","General.Deck.UpperDeck","2000,15300","-2000,15300",False)
skt_ln6 = part.CreateSketchLine(skt_pl1,"","General.Deck.UpperDeck","-2000,15300","-18500,14933.333333333336",False)
skt_layer2 = part.CreateSketchLayer("Casing.Deck.A",skt_pl1)
skt_ln7 = part.CreateSketchLine(skt_pl1,"","Casing.Deck.A","18500,18300","-18500,18300",False)
skt_layer3 = part.CreateSketchLayer("Casing.Deck.B",skt_pl1)
skt_ln8 = part.CreateSketchLine(skt_pl1,"","Casing.Deck.B","18500,21300","-18500,21300",False)
skt_layer4 = part.CreateSketchLayer("Casing.Deck.C",skt_pl1)
skt_ln9 = part.CreateSketchLine(skt_pl1,"","Casing.Deck.C","18500,24300","-18500,24300",False)
skt_layer5 = part.CreateSketchLayer("Casing.Deck.D",skt_pl1)
skt_ln10 = part.CreateSketchLine(skt_pl1,"","Casing.Deck.D","18500,27300","-18500,27300",False)
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.AddProfile(skt_pl1+",Casing.Deck.B")
extrudePram1.DirectionType="2"
extrudePram1.DirectionParameter1="50000"
extrudePram1.DirectionParameter2="10000"
extrudePram1.SweepDirection="+X"
extrudePram1.Name="HK.Casing.Deck.B"
extrudePram1.MaterialName="SS400"
extrudePram1.IntervalSweep=False
extrude_sheet1 = part.CreateLinearSweepSheet(extrudePram1,False)
part.SheetAlignNormal(extrude_sheet1,-0,0,1)
part.BlankElement(extrude_sheet1,True)
part.SetElementColor(extrude_sheet1,"225","225","225","1")
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.AddProfile(skt_pl1+",Casing.Deck.A")
extrudePram2.DirectionType="2"
extrudePram2.DirectionParameter1="50000"
extrudePram2.DirectionParameter2="10000"
extrudePram2.SweepDirection="+X"
extrudePram2.Name="HK.Casing.Deck.A"
extrudePram2.MaterialName="SS400"
extrudePram2.IntervalSweep=False
extrude_sheet2 = part.CreateLinearSweepSheet(extrudePram2,False)
part.SheetAlignNormal(extrude_sheet2,-0,0,1)
part.BlankElement(extrude_sheet2,True)
part.SetElementColor(extrude_sheet2,"225","225","225","1")
skt_pl2 = part.CreateSketchPlane("HK.Az.Wall","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl2,True)
skt_ln11 = part.CreateSketchLine(skt_pl2,"","作図","0,-18500","0,18500",False)
skt_ln12 = part.CreateSketchLine(skt_pl2,"","作図","-50000,15500","250000,15500",False)
skt_ln13 = part.CreateSketchLine(skt_pl2,"","作図","-50000,-15500","250000,-15500",False)
skt_layer6 = part.CreateSketchLayer("Casing.Fore",skt_pl2)
skt_ln14 = part.CreateSketchLine(skt_pl2,"","Casing.Fore","11370.000000000002,-10394.984078409721","11370.000000000002,9605.0159215902786",False)
skt_layer7 = part.CreateSketchLayer("Casing.Aft",skt_pl2)
skt_ln15 = part.CreateSketchLine(skt_pl2,"","Casing.Aft","4019.9999999999995,-10394.984078409721","4019.9999999999995,9605.0159215902786",False)
skt_layer8 = part.CreateSketchLayer("Casing.Side.P",skt_pl2)
skt_ln16 = part.CreateSketchLine(skt_pl2,"","Casing.Side.P","-1500,4800","18500,4800",False)
skt_layer9 = part.CreateSketchLayer("Casing.Side.S",skt_pl2)
skt_ln17 = part.CreateSketchLine(skt_pl2,"","Casing.Side.S","-1500,-4800","18500,-4800",False)
skt_layer10 = part.CreateSketchLayer("Dim.CenterLine",skt_pl2)
skt_ln18 = part.CreateSketchLine(skt_pl2,"","Dim.CenterLine","-50000,0","250000,0",False)
extrudePram3 = part.CreateLinearSweepParam()
extrudePram3.AddProfile(skt_pl2+",Casing.Aft")
extrudePram3.DirectionType="2"
extrudePram3.DirectionParameter1="50000"
extrudePram3.DirectionParameter2="10000"
extrudePram3.SweepDirection="+Z"
extrudePram3.Name="HK.Casing.Wall.Aft"
extrudePram3.MaterialName="SS400"
extrudePram3.IntervalSweep=False
extrude_sheet3 = part.CreateLinearSweepSheet(extrudePram3,False)
part.SheetAlignNormal(extrude_sheet3,1,0,0)
part.BlankElement(extrude_sheet3,True)
part.SetElementColor(extrude_sheet3,"225","225","225","1")
var_elm1 = part.CreateVariable("Casing.DL04","3200","mm","")
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType=1
ProfilePram1.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram1.AddAttachSurfaces(extrude_sheet3)
ProfilePram1.ProfileName="HK.Casing.Wall.Aft.DL04.ABP"
ProfilePram1.MaterialName="SS400"
ProfilePram1.ProfileType=1003
ProfilePram1.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram1.Mold="+"
ProfilePram1.ReverseDir=False
ProfilePram1.ReverseAngle=True
ProfilePram1.CalcSnipOnlyAttachLines=False
ProfilePram1.AttachDirMethod=0
ProfilePram1.CCWDefAngle=False
ProfilePram1.AddEnd1Elements(extrude_sheet1)
ProfilePram1.End1Type=1102
ProfilePram1.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram1.AddEnd2Elements(extrude_sheet2)
ProfilePram1.End2Type=1102
ProfilePram1.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram1.End1ScallopType=1120
ProfilePram1.End1ScallopTypeParams=["50"]
ProfilePram1.End2ScallopType=1120
ProfilePram1.End2ScallopTypeParams=["50"]
profile1 = part.CreateProfile(ProfilePram1,False)
part.SetElementColor(profile1[0],"148","0","211","0.39999997615814209")
var_elm2 = part.CreateVariable("Casing.DL02","1600","mm","")
extrudePram4 = part.CreateLinearSweepParam()
extrudePram4.AddProfile(skt_pl1+",Casing.Deck.C")
extrudePram4.DirectionType="2"
extrudePram4.DirectionParameter1="50000"
extrudePram4.DirectionParameter2="10000"
extrudePram4.SweepDirection="+X"
extrudePram4.Name="HK.Casing.Deck.C"
extrudePram4.MaterialName="SS400"
extrudePram4.IntervalSweep=False
extrude_sheet4 = part.CreateLinearSweepSheet(extrudePram4,False)
part.SheetAlignNormal(extrude_sheet4,-0,0,1)
part.BlankElement(extrude_sheet4,True)
part.SetElementColor(extrude_sheet4,"225","225","225","1")
ProfilePram2 = part.CreateProfileParam()
ProfilePram2.DefinitionType=1
ProfilePram2.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram2.AddAttachSurfaces(extrude_sheet3)
ProfilePram2.ProfileName="HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram2.MaterialName="SS400"
ProfilePram2.FlangeName="HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram2.FlangeMaterialName="SS400"
ProfilePram2.ProfileType=1201
ProfilePram2.ProfileParams=["150","12","388","10"]
ProfilePram2.Mold="-"
ProfilePram2.ReverseDir=False
ProfilePram2.ReverseAngle=False
ProfilePram2.CalcSnipOnlyAttachLines=False
ProfilePram2.AttachDirMethod=0
ProfilePram2.CCWDefAngle=False
ProfilePram2.AddEnd1Elements(extrude_sheet4)
ProfilePram2.End1Type=1103
ProfilePram2.End1TypeParams=["0"]
ProfilePram2.AddEnd2Elements(extrude_sheet1)
ProfilePram2.End2Type=1103
ProfilePram2.End2TypeParams=["0"]
ProfilePram2.End1ScallopType=1120
ProfilePram2.End1ScallopTypeParams=["50"]
ProfilePram2.End2ScallopType=1120
ProfilePram2.End2ScallopTypeParams=["50"]
profile2 = part.CreateProfile(ProfilePram2,False)
part.SetElementColor(profile2[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile2[1],"148","0","211","0.39999997615814209")
mirror_copied1 = part.MirrorCopy([profile2[0]],"PL,Y","")
part.SetElementColor(mirror_copied1[0],"148","0","211","0.39999997615814209")
var_elm3 = part.CreateVariable("FR15","10570","mm","")
extrudePram5 = part.CreateLinearSweepParam()
extrudePram5.AddProfile(skt_pl1+",Casing.Deck.D")
extrudePram5.DirectionType="2"
extrudePram5.DirectionParameter1="50000"
extrudePram5.DirectionParameter2="10000"
extrudePram5.SweepDirection="+X"
extrudePram5.Name="HK.Casing.Deck.D"
extrudePram5.MaterialName="SS400"
extrudePram5.IntervalSweep=False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudePram5,False)
part.SheetAlignNormal(extrude_sheet5,-0,0,1)
part.BlankElement(extrude_sheet5,True)
part.SetElementColor(extrude_sheet5,"225","225","225","1")
extrudePram6 = part.CreateLinearSweepParam()
extrudePram6.AddProfile(skt_pl2+",Casing.Side.P")
extrudePram6.DirectionType="2"
extrudePram6.DirectionParameter1="50000"
extrudePram6.DirectionParameter2="10000"
extrudePram6.SweepDirection="+Z"
extrudePram6.Name="HK.Casing.Wall.SideP"
extrudePram6.MaterialName="SS400"
extrudePram6.IntervalSweep=False
extrude_sheet6 = part.CreateLinearSweepSheet(extrudePram6,False)
part.SheetAlignNormal(extrude_sheet6,0,-1,0)
part.BlankElement(extrude_sheet6,True)
part.SetElementColor(extrude_sheet6,"225","225","225","1")
ProfilePram3 = part.CreateProfileParam()
ProfilePram3.DefinitionType=1
ProfilePram3.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram3.AddAttachSurfaces(extrude_sheet6)
ProfilePram3.ProfileName="HK.Casing.Wall.Side.FR15.CDP"
ProfilePram3.MaterialName="SS400"
ProfilePram3.ProfileType=1002
ProfilePram3.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram3.Mold="+"
ProfilePram3.ReverseDir=False
ProfilePram3.ReverseAngle=True
ProfilePram3.CalcSnipOnlyAttachLines=False
ProfilePram3.AttachDirMethod=0
ProfilePram3.CCWDefAngle=False
ProfilePram3.AddEnd1Elements(extrude_sheet5)
ProfilePram3.End1Type=1102
ProfilePram3.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.AddEnd2Elements(extrude_sheet4)
ProfilePram3.End2Type=1102
ProfilePram3.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.End1ScallopType=1121
ProfilePram3.End1ScallopTypeParams=["35","40"]
ProfilePram3.End2ScallopType=1121
ProfilePram3.End2ScallopTypeParams=["35","40"]
profile3 = part.CreateProfile(ProfilePram3,False)
part.SetElementColor(profile3[0],"255","0","0","0.19999998807907104")
mirror_copied2 = part.MirrorCopy([profile3[0]],"PL,Y","")
part.SetElementColor(mirror_copied2[0],"255","0","0","0.19999998807907104")
extrudePram7 = part.CreateLinearSweepParam()
extrudePram7.AddProfile(skt_pl1+",General.Deck.UpperDeck")
extrudePram7.DirectionType="2"
extrudePram7.DirectionParameter1="190000"
extrudePram7.DirectionParameter2="10000"
extrudePram7.SweepDirection="+X"
extrudePram7.Name="HK.General.Deck.UpperDeck"
extrudePram7.MaterialName="SS400"
extrudePram7.IntervalSweep=False
extrude_sheet7 = part.CreateLinearSweepSheet(extrudePram7,False)
part.SheetAlignNormal(extrude_sheet7,0,0,-1)
part.BlankElement(extrude_sheet7,True)
part.SetElementColor(extrude_sheet7,"225","225","225","1")
var_elm4 = part.CreateVariable("Casing.DL05","4000","mm","")
ProfilePram4 = part.CreateProfileParam()
ProfilePram4.DefinitionType=1
ProfilePram4.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram4.AddAttachSurfaces(extrude_sheet3)
ProfilePram4.ProfileName="HK.Casing.Wall.Aft.DL05.OAP"
ProfilePram4.MaterialName="SS400"
ProfilePram4.ProfileType=1002
ProfilePram4.ProfileParams=["125","75","7","10","5"]
ProfilePram4.Mold="+"
ProfilePram4.ReverseDir=False
ProfilePram4.ReverseAngle=True
ProfilePram4.CalcSnipOnlyAttachLines=False
ProfilePram4.AttachDirMethod=0
ProfilePram4.CCWDefAngle=False
ProfilePram4.AddEnd1Elements(extrude_sheet2)
ProfilePram4.End1Type=1102
ProfilePram4.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.AddEnd2Elements(extrude_sheet7)
ProfilePram4.End2Type=1102
ProfilePram4.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.End1ScallopType=1121
ProfilePram4.End1ScallopTypeParams=["25","40"]
ProfilePram4.End2ScallopType=1121
ProfilePram4.End2ScallopTypeParams=["25","40"]
profile4 = part.CreateProfile(ProfilePram4,False)
part.SetElementColor(profile4[0],"255","0","0","0.19999998807907104")
var_elm5 = part.CreateVariable("FR8","5360","mm","")
ProfilePram5 = part.CreateProfileParam()
ProfilePram5.DefinitionType=1
ProfilePram5.BasePlane="PL,O,"+var_elm5+","+"X"
ProfilePram5.AddAttachSurfaces(extrude_sheet6)
ProfilePram5.ProfileName="HK.Casing.Wall.Side.FR08.BCP"
ProfilePram5.MaterialName="SS400"
ProfilePram5.ProfileType=1002
ProfilePram5.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram5.Mold="+"
ProfilePram5.ReverseDir=False
ProfilePram5.ReverseAngle=True
ProfilePram5.CalcSnipOnlyAttachLines=False
ProfilePram5.AttachDirMethod=0
ProfilePram5.CCWDefAngle=False
ProfilePram5.AddEnd1Elements(extrude_sheet4)
ProfilePram5.End1Type=1102
ProfilePram5.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram5.AddEnd2Elements(extrude_sheet1)
ProfilePram5.End2Type=1102
ProfilePram5.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram5.End1ScallopType=1121
ProfilePram5.End1ScallopTypeParams=["35","40"]
ProfilePram5.End2ScallopType=1121
ProfilePram5.End2ScallopTypeParams=["35","40"]
profile5 = part.CreateProfile(ProfilePram5,False)
part.SetElementColor(profile5[0],"255","0","0","0.19999998807907104")
extrudePram8 = part.CreateLinearSweepParam()
extrudePram8.AddProfile(skt_pl2+",Casing.Fore")
extrudePram8.DirectionType="2"
extrudePram8.DirectionParameter1="50000"
extrudePram8.DirectionParameter2="10000"
extrudePram8.SweepDirection="+Z"
extrudePram8.Name="HK.Casing.Wall.Fore"
extrudePram8.MaterialName="SS400"
extrudePram8.IntervalSweep=False
extrude_sheet8 = part.CreateLinearSweepSheet(extrudePram8,False)
part.SheetAlignNormal(extrude_sheet8,1,0,0)
part.BlankElement(extrude_sheet8,True)
part.SetElementColor(extrude_sheet8,"225","225","225","1")
ProfilePram6 = part.CreateProfileParam()
ProfilePram6.DefinitionType=1
ProfilePram6.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram6.AddAttachSurfaces(extrude_sheet8)
ProfilePram6.ProfileName="HK.Casing.Wall.Fore.DL05.BCP"
ProfilePram6.MaterialName="SS400"
ProfilePram6.ProfileType=1002
ProfilePram6.ProfileParams=["125","75","7","10","5"]
ProfilePram6.Mold="+"
ProfilePram6.ReverseDir=True
ProfilePram6.ReverseAngle=True
ProfilePram6.CalcSnipOnlyAttachLines=False
ProfilePram6.AttachDirMethod=0
ProfilePram6.CCWDefAngle=False
ProfilePram6.AddEnd1Elements(extrude_sheet4)
ProfilePram6.End1Type=1102
ProfilePram6.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram6.AddEnd2Elements(extrude_sheet1)
ProfilePram6.End2Type=1102
ProfilePram6.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram6.End1ScallopType=1121
ProfilePram6.End1ScallopTypeParams=["25","40"]
ProfilePram6.End2ScallopType=1121
ProfilePram6.End2ScallopTypeParams=["25","40"]
profile6 = part.CreateProfile(ProfilePram6,False)
part.SetElementColor(profile6[0],"255","0","0","0.19999998807907104")
ProfilePram7 = part.CreateProfileParam()
ProfilePram7.DefinitionType=1
ProfilePram7.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram7.AddAttachSurfaces(extrude_sheet3)
ProfilePram7.ProfileName="HK.Casing.Wall.Aft.DL05.BCP"
ProfilePram7.MaterialName="SS400"
ProfilePram7.ProfileType=1002
ProfilePram7.ProfileParams=["125","75","7","10","5"]
ProfilePram7.Mold="+"
ProfilePram7.ReverseDir=False
ProfilePram7.ReverseAngle=True
ProfilePram7.CalcSnipOnlyAttachLines=False
ProfilePram7.AttachDirMethod=0
ProfilePram7.CCWDefAngle=False
ProfilePram7.AddEnd1Elements(extrude_sheet4)
ProfilePram7.End1Type=1102
ProfilePram7.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.AddEnd2Elements(extrude_sheet1)
ProfilePram7.End2Type=1102
ProfilePram7.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.End1ScallopType=1121
ProfilePram7.End1ScallopTypeParams=["25","40"]
ProfilePram7.End2ScallopType=1121
ProfilePram7.End2ScallopTypeParams=["25","40"]
profile7 = part.CreateProfile(ProfilePram7,False)
part.SetElementColor(profile7[0],"255","0","0","0.19999998807907104")
ProfilePram8 = part.CreateProfileParam()
ProfilePram8.DefinitionType=1
ProfilePram8.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram8.AddAttachSurfaces(extrude_sheet4)
ProfilePram8.ProfileName="HK.Casing.Deck.C.DL05P"
ProfilePram8.MaterialName="SS400"
ProfilePram8.ProfileType=1002
ProfilePram8.ProfileParams=["125","75","7","10","5"]
ProfilePram8.Mold="+"
ProfilePram8.ReverseDir=True
ProfilePram8.ReverseAngle=True
ProfilePram8.CalcSnipOnlyAttachLines=False
ProfilePram8.AttachDirMethod=0
ProfilePram8.CCWDefAngle=False
ProfilePram8.AddEnd1Elements(profile7[0])
ProfilePram8.End1Type=1102
ProfilePram8.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram8.AddEnd2Elements(profile6[0])
ProfilePram8.End2Type=1102
ProfilePram8.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram8.End1ScallopType=1120
ProfilePram8.End1ScallopTypeParams=["50"]
ProfilePram8.End2ScallopType=1120
ProfilePram8.End2ScallopTypeParams=["50"]
profile8 = part.CreateProfile(ProfilePram8,False)
part.SetElementColor(profile8[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck C DL05 と Fore/Aft DL05 間
bracketPramA1 = part.CreateBracketParam()
bracketPramA1.DefinitionType=1
bracketPramA1.BracketName="HK.Casing.Deck.C.DL05.BKT.AFT"
bracketPramA1.MaterialName="SS400"
bracketPramA1.BaseElement=profile8[0]
bracketPramA1.UseSideSheetForPlane=False
bracketPramA1.Mold="+"
bracketPramA1.Thickness="8"
bracketPramA1.BracketType=1501
bracketPramA1.Scallop1Type=1801
bracketPramA1.Scallop1Params=["0"]
bracketPramA1.Scallop2Type=0
bracketPramA1.Surfaces1=[profile8[0]+",FL"]
bracketPramA1.RevSf1=False
bracketPramA1.Surfaces2=[profile7[0]+",FL"]
bracketPramA1.RevSf2=False
bracketPramA1.RevSf3=False
bracketPramA1.Sf1DimensionType=1531
bracketPramA1.Sf1DimensonParams=["200","15"]
bracketPramA1.Sf2DimensionType=1531
bracketPramA1.Sf2DimensonParams=["200","15"]
bracketA1 = part.CreateBracket(bracketPramA1,False)
part.SetElementColor(bracketA1,"0","255","255","0.19999998807907104")
solid1 = part.CreateSolid("HK.Casing.Deck.C","","SS400")
part.SetElementColor(solid1,"139","69","19","0.78999996185302734")
thicken1 = part.CreateThicken("厚み付け4",solid1,"+",[extrude_sheet4],"+","10","0","0",False,False)
skt_pl3 = part.CreateSketchPlane("HK.Az.Deck.C","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl3,True)
skt_layer11 = part.CreateSketchLayer("Edge00",skt_pl3)
skt_ln19 = part.CreateSketchLine(skt_pl3,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln20 = part.CreateSketchLine(skt_pl3,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln21 = part.CreateSketchLine(skt_pl3,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln22 = part.CreateSketchLine(skt_pl3,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer12 = part.CreateSketchLayer("Edge01",skt_pl3)
skt_ln23 = part.CreateSketchLine(skt_pl3,"","Edge01","9770,3125","4835.0000000000009,3125",False)
skt_ln24 = part.CreateSketchLine(skt_pl3,"","Edge01","10170,-2725","10170,2725",False)
skt_ln25 = part.CreateSketchLine(skt_pl3,"","Edge01","4835.0000000000009,-3125","9770,-3125",False)
skt_ln26 = part.CreateSketchLine(skt_pl3,"","Edge01","4435.0000000000009,2725","4435.0000000000009,-2724.9999999999991",False)
skt_arc1 = part.CreateSketchArc(skt_pl3,"","Edge01","4835.0000000000009,2724.9999999999995","4835.0000000000009,3124.9999999999995","4435.0000000000009,2725",True,False)
skt_arc2 = part.CreateSketchArc(skt_pl3,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3124.9999999999995",True,False)
skt_arc3 = part.CreateSketchArc(skt_pl3,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc4 = part.CreateSketchArc(skt_pl3,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125",True,False)
extrudePram9 = part.CreateLinearSweepParam()
extrudePram9.Name="積-押し出し4"
extrudePram9.AddProfile(skt_pl3+",Edge00")
extrudePram9.DirectionType="N"
extrudePram9.DirectionParameter1="50000"
extrudePram9.SweepDirection="+Z"
extrudePram9.RefByGeometricMethod=True
extrude1 = part.CreateLinearSweep(solid1,"*",extrudePram9,False)
extrudePram10 = part.CreateLinearSweepParam()
extrudePram10.Name="削除-押し出し2"
extrudePram10.AddProfile(skt_pl3+",Edge01")
extrudePram10.DirectionType="T"
extrudePram10.RefByGeometricMethod=True
extrude2 = part.CreateLinearSweep(solid1,"-",extrudePram10,False)
var_elm6 = part.CreateVariable("Casing.DL03","2400","mm","")
ProfilePram9 = part.CreateProfileParam()
ProfilePram9.DefinitionType=1
ProfilePram9.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram9.AddAttachSurfaces(extrude_sheet3)
ProfilePram9.ProfileName="HK.Casing.Wall.Aft.DL03.ABP"
ProfilePram9.MaterialName="SS400"
ProfilePram9.ProfileType=1002
ProfilePram9.ProfileParams=["125","75","7","10","5"]
ProfilePram9.Mold="+"
ProfilePram9.ReverseDir=False
ProfilePram9.ReverseAngle=True
ProfilePram9.CalcSnipOnlyAttachLines=False
ProfilePram9.AttachDirMethod=0
ProfilePram9.CCWDefAngle=False
ProfilePram9.AddEnd1Elements(extrude_sheet1)
ProfilePram9.End1Type=1102
ProfilePram9.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.AddEnd2Elements(extrude_sheet2)
ProfilePram9.End2Type=1102
ProfilePram9.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.End1ScallopType=1121
ProfilePram9.End1ScallopTypeParams=["25","40"]
ProfilePram9.End2ScallopType=1121
ProfilePram9.End2ScallopTypeParams=["25","40"]
profile9 = part.CreateProfile(ProfilePram9,False)
part.SetElementColor(profile9[0],"255","0","0","0.19999998807907104")
var_elm7 = part.CreateVariable("FR11","7370","mm","")
ProfilePram10 = part.CreateProfileParam()
ProfilePram10.DefinitionType=1
ProfilePram10.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram10.AddAttachSurfaces(extrude_sheet6)
ProfilePram10.ProfileName="HK.Casing.Wall.Side.FR11.BCP"
ProfilePram10.MaterialName="SS400"
ProfilePram10.ProfileType=1002
ProfilePram10.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram10.Mold="+"
ProfilePram10.ReverseDir=False
ProfilePram10.ReverseAngle=True
ProfilePram10.CalcSnipOnlyAttachLines=False
ProfilePram10.AttachDirMethod=0
ProfilePram10.CCWDefAngle=False
ProfilePram10.AddEnd1Elements(extrude_sheet4)
ProfilePram10.End1Type=1102
ProfilePram10.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram10.AddEnd2Elements(extrude_sheet1)
ProfilePram10.End2Type=1102
ProfilePram10.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram10.End1ScallopType=1121
ProfilePram10.End1ScallopTypeParams=["35","40"]
ProfilePram10.End2ScallopType=1121
ProfilePram10.End2ScallopTypeParams=["35","40"]
profile10 = part.CreateProfile(ProfilePram10,False)
part.SetElementColor(profile10[0],"255","0","0","0.19999998807907104")
ProfilePram11 = part.CreateProfileParam()
ProfilePram11.DefinitionType=1
ProfilePram11.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram11.AddAttachSurfaces(extrude_sheet3)
ProfilePram11.ProfileName="HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram11.MaterialName="SS400"
ProfilePram11.FlangeName="HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram11.FlangeMaterialName="SS400"
ProfilePram11.ProfileType=1201
ProfilePram11.ProfileParams=["150","12","388","10"]
ProfilePram11.Mold="-"
ProfilePram11.ReverseDir=False
ProfilePram11.ReverseAngle=False
ProfilePram11.CalcSnipOnlyAttachLines=False
ProfilePram11.AttachDirMethod=0
ProfilePram11.CCWDefAngle=False
ProfilePram11.AddEnd1Elements(extrude_sheet2)
ProfilePram11.End1Type=1103
ProfilePram11.End1TypeParams=["0"]
ProfilePram11.AddEnd2Elements(extrude_sheet7)
ProfilePram11.End2Type=1103
ProfilePram11.End2TypeParams=["0"]
ProfilePram11.End1ScallopType=1120
ProfilePram11.End1ScallopTypeParams=["50"]
ProfilePram11.End2ScallopType=1120
ProfilePram11.End2ScallopTypeParams=["50"]
profile11 = part.CreateProfile(ProfilePram11,False)
part.SetElementColor(profile11[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile11[1],"148","0","211","0.39999997615814209")
mirror_copied4 = part.MirrorCopy([profile11[0]],"PL,Y","")
part.SetElementColor(mirror_copied4[0],"148","0","211","0.39999997615814209")
ProfilePram12 = part.CreateProfileParam()
ProfilePram12.DefinitionType=1
ProfilePram12.BasePlane="PL,O,"+var_elm5+","+"X"
ProfilePram12.AddAttachSurfaces(extrude_sheet6)
ProfilePram12.ProfileName="HK.Casing.Wall.Side.FR08.CDP"
ProfilePram12.MaterialName="SS400"
ProfilePram12.ProfileType=1002
ProfilePram12.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram12.Mold="+"
ProfilePram12.ReverseDir=False
ProfilePram12.ReverseAngle=True
ProfilePram12.CalcSnipOnlyAttachLines=False
ProfilePram12.AttachDirMethod=0
ProfilePram12.CCWDefAngle=False
ProfilePram12.AddEnd1Elements(extrude_sheet5)
ProfilePram12.End1Type=1102
ProfilePram12.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.AddEnd2Elements(extrude_sheet4)
ProfilePram12.End2Type=1102
ProfilePram12.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.End1ScallopType=1121
ProfilePram12.End1ScallopTypeParams=["35","40"]
ProfilePram12.End2ScallopType=1121
ProfilePram12.End2ScallopTypeParams=["35","40"]
profile12 = part.CreateProfile(ProfilePram12,False)
part.SetElementColor(profile12[0],"255","0","0","0.19999998807907104")
ProfilePram13 = part.CreateProfileParam()
ProfilePram13.DefinitionType=1
ProfilePram13.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram13.AddAttachSurfaces(extrude_sheet8)
ProfilePram13.ProfileName="HK.Casing.Wall.Fore.DL04.BCP"
ProfilePram13.MaterialName="SS400"
ProfilePram13.ProfileType=1003
ProfilePram13.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram13.Mold="+"
ProfilePram13.ReverseDir=True
ProfilePram13.ReverseAngle=True
ProfilePram13.CalcSnipOnlyAttachLines=False
ProfilePram13.AttachDirMethod=0
ProfilePram13.CCWDefAngle=False
ProfilePram13.AddEnd1Elements(extrude_sheet4)
ProfilePram13.End1Type=1102
ProfilePram13.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram13.AddEnd2Elements(extrude_sheet1)
ProfilePram13.End2Type=1102
ProfilePram13.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram13.End1ScallopType=1120
ProfilePram13.End1ScallopTypeParams=["50"]
ProfilePram13.End2ScallopType=1120
ProfilePram13.End2ScallopTypeParams=["50"]
profile13 = part.CreateProfile(ProfilePram13,False)
part.SetElementColor(profile13[0],"148","0","211","0.39999997615814209")
ProfilePram14 = part.CreateProfileParam()
ProfilePram14.DefinitionType=1
ProfilePram14.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram14.AddAttachSurfaces(extrude_sheet3)
ProfilePram14.ProfileName="HK.Casing.Wall.Aft.DL04.BCP"
ProfilePram14.MaterialName="SS400"
ProfilePram14.ProfileType=1003
ProfilePram14.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram14.Mold="+"
ProfilePram14.ReverseDir=False
ProfilePram14.ReverseAngle=True
ProfilePram14.CalcSnipOnlyAttachLines=False
ProfilePram14.AttachDirMethod=0
ProfilePram14.CCWDefAngle=False
ProfilePram14.AddEnd1Elements(extrude_sheet4)
ProfilePram14.End1Type=1102
ProfilePram14.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.AddEnd2Elements(extrude_sheet1)
ProfilePram14.End2Type=1102
ProfilePram14.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.End1ScallopType=1120
ProfilePram14.End1ScallopTypeParams=["50"]
ProfilePram14.End2ScallopType=1120
ProfilePram14.End2ScallopTypeParams=["50"]
profile14 = part.CreateProfile(ProfilePram14,False)
part.SetElementColor(profile14[0],"148","0","211","0.39999997615814209")
ProfilePram15 = part.CreateProfileParam()
ProfilePram15.DefinitionType=1
ProfilePram15.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram15.AddAttachSurfaces(extrude_sheet4)
ProfilePram15.ProfileName="HK.Casing.Deck.C.DL04P"
ProfilePram15.MaterialName="SS400"
ProfilePram15.ProfileType=1003
ProfilePram15.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram15.Mold="-"
ProfilePram15.ReverseDir=True
ProfilePram15.ReverseAngle=False
ProfilePram15.CalcSnipOnlyAttachLines=False
ProfilePram15.AttachDirMethod=0
ProfilePram15.CCWDefAngle=False
ProfilePram15.AddEnd1Elements(profile14[0])
ProfilePram15.End1Type=1102
ProfilePram15.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram15.AddEnd2Elements(profile13[0])
ProfilePram15.End2Type=1102
ProfilePram15.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram15.End1ScallopType=0
ProfilePram15.End2ScallopType=0
profile15 = part.CreateProfile(ProfilePram15,False)
part.SetElementColor(profile15[0],"148","0","211","0.39999997615814209")
skt_pl4 = part.CreateSketchPlane("HK.Az.Deck.D","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl4,True)
skt_layer13 = part.CreateSketchLayer("Edge00",skt_pl4)
skt_ln27 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln28 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln29 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln30 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer14 = part.CreateSketchLayer("Edge01",skt_pl4)
skt_arc5 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,1195.0000000000002","6345,1495.0000000000002","6045.0000000000009,1195",True,False)
skt_ln31 = part.CreateSketchLine(skt_pl4,"","Edge01","8580,1495","6345,1495",False)
skt_arc6 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,1195","8880,1195.0000000000002","8580,1495",True,False)
skt_ln32 = part.CreateSketchLine(skt_pl4,"","Edge01","8880,-1195","8880,1195.0000000000005",False)
skt_arc7 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,-1195.0000000000002","8580,-1495.0000000000002","8880,-1195",True,False)
skt_ln33 = part.CreateSketchLine(skt_pl4,"","Edge01","6345,-1495","8580,-1495",False)
skt_arc8 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,-1195","6045.0000000000009,-1195.0000000000002","6345,-1495",True,False)
skt_ln34 = part.CreateSketchLine(skt_pl4,"","Edge01","6045,1195","6045,-1195.0000000000005",False)
solid2 = part.CreateSolid("HK.Casing.Deck.D","","SS400")
part.SetElementColor(solid2,"139","69","19","0.78999996185302734")
thicken2 = part.CreateThicken("厚み付け3",solid2,"+",[extrude_sheet5],"+","10","0","0",False,False)
extrudePram11 = part.CreateLinearSweepParam()
extrudePram11.Name="積-押し出し3"
extrudePram11.AddProfile(skt_pl4+",Edge00")
extrudePram11.DirectionType="N"
extrudePram11.DirectionParameter1="50000"
extrudePram11.SweepDirection="+Z"
extrudePram11.RefByGeometricMethod=True
extrude3 = part.CreateLinearSweep(solid2,"*",extrudePram11,False)
extrudePram12 = part.CreateLinearSweepParam()
extrudePram12.Name="削除-押し出し1"
extrudePram12.AddProfile(skt_pl4+",Edge01")
extrudePram12.DirectionType="T"
extrudePram12.RefByGeometricMethod=True
extrude4 = part.CreateLinearSweep(solid2,"-",extrudePram12,False)
var_elm8 = part.CreateVariable("FR7","4690","mm","")
ProfilePram16 = part.CreateProfileParam()
ProfilePram16.DefinitionType=1
ProfilePram16.BasePlane="PL,O,"+var_elm8+","+"X"
ProfilePram16.AddAttachSurfaces(extrude_sheet6)
ProfilePram16.ProfileName="HK.Casing.Wall.Side.FR07.CDP"
ProfilePram16.MaterialName="SS400"
ProfilePram16.ProfileType=1002
ProfilePram16.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram16.Mold="+"
ProfilePram16.ReverseDir=False
ProfilePram16.ReverseAngle=True
ProfilePram16.CalcSnipOnlyAttachLines=False
ProfilePram16.AttachDirMethod=0
ProfilePram16.CCWDefAngle=False
ProfilePram16.AddEnd1Elements(extrude_sheet5)
ProfilePram16.End1Type=1102
ProfilePram16.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.AddEnd2Elements(extrude_sheet4)
ProfilePram16.End2Type=1102
ProfilePram16.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.End1ScallopType=1121
ProfilePram16.End1ScallopTypeParams=["35","40"]
ProfilePram16.End2ScallopType=1121
ProfilePram16.End2ScallopTypeParams=["35","40"]
profile16 = part.CreateProfile(ProfilePram16,False)
part.SetElementColor(profile16[0],"255","0","0","0.19999998807907104")
ProfilePram17 = part.CreateProfileParam()
ProfilePram17.DefinitionType=1
ProfilePram17.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram17.AddAttachSurfaces(extrude_sheet5)
ProfilePram17.ProfileName="HK.Casing.Deck.D.DL05P"
ProfilePram17.MaterialName="SS400"
ProfilePram17.ProfileType=1002
ProfilePram17.ProfileParams=["125","75","7","10","5"]
ProfilePram17.Mold="+"
ProfilePram17.ReverseDir=True
ProfilePram17.ReverseAngle=True
ProfilePram17.CalcSnipOnlyAttachLines=False
ProfilePram17.AttachDirMethod=0
ProfilePram17.CCWDefAngle=False
ProfilePram17.AddEnd1Elements(extrude_sheet3)
ProfilePram17.End1Type=1102
ProfilePram17.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.AddEnd2Elements(extrude_sheet8)
ProfilePram17.End2Type=1102
ProfilePram17.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.End1ScallopType=1120
ProfilePram17.End1ScallopTypeParams=["50"]
ProfilePram17.End2ScallopType=1120
ProfilePram17.End2ScallopTypeParams=["50"]
profile17 = part.CreateProfile(ProfilePram17,False)
part.SetElementColor(profile17[0],"255","0","0","0.19999998807907104")
ProfilePram18 = part.CreateProfileParam()
ProfilePram18.DefinitionType=1
ProfilePram18.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram18.AddAttachSurfaces(extrude_sheet5)
ProfilePram18.ProfileName="HK.Casing.Deck.D.DL02P"
ProfilePram18.MaterialName="SS400"
ProfilePram18.FlangeName="HK.Casing.Deck.D.DL02P"
ProfilePram18.FlangeMaterialName="SS400"
ProfilePram18.ProfileType=1201
ProfilePram18.ProfileParams=["200","14","900","10"]
ProfilePram18.Mold="-"
ProfilePram18.ReverseDir=True
ProfilePram18.ReverseAngle=False
ProfilePram18.CalcSnipOnlyAttachLines=False
ProfilePram18.AttachDirMethod=0
ProfilePram18.CCWDefAngle=False
ProfilePram18.AddEnd1Elements(extrude_sheet3)
ProfilePram18.End1Type=1102
ProfilePram18.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram18.AddEnd2Elements(extrude_sheet8)
ProfilePram18.End2Type=1102
ProfilePram18.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram18.End1ScallopType=1120
ProfilePram18.End1ScallopTypeParams=["50"]
ProfilePram18.End2ScallopType=1120
ProfilePram18.End2ScallopTypeParams=["50"]
profile18 = part.CreateProfile(ProfilePram18,False)
part.SetElementColor(profile18[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile18[1],"148","0","211","0.39999997615814209")
ProfilePram19 = part.CreateProfileParam()
ProfilePram19.DefinitionType=1
ProfilePram19.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram19.AddAttachSurfaces(extrude_sheet3)
ProfilePram19.ProfileName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram19.MaterialName="SS400"
ProfilePram19.FlangeName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram19.FlangeMaterialName="SS400"
ProfilePram19.ProfileType=1201
ProfilePram19.ProfileParams=["150","12","388","10"]
ProfilePram19.Mold="-"
ProfilePram19.ReverseDir=False
ProfilePram19.ReverseAngle=False
ProfilePram19.CalcSnipOnlyAttachLines=False
ProfilePram19.AttachDirMethod=0
ProfilePram19.CCWDefAngle=False
ProfilePram19.AddEnd1Elements(profile18[1])
ProfilePram19.End1Type=1102
ProfilePram19.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram19.AddEnd2Elements(extrude_sheet4)
ProfilePram19.End2Type=1103
ProfilePram19.End2TypeParams=["0"]
ProfilePram19.End1ScallopType=1120
ProfilePram19.End1ScallopTypeParams=["50"]
ProfilePram19.End2ScallopType=1120
ProfilePram19.End2ScallopTypeParams=["50"]
profile19 = part.CreateProfile(ProfilePram19,False)
part.SetElementColor(profile19[0],"148","0","211","0.38999998569488525")
part.SetElementColor(profile19[1],"148","0","211","0.38999998569488525")
# 追加ブラケット: DL02の壁とデッキ間
bracketPramB1 = part.CreateBracketParam()
bracketPramB1.DefinitionType=1
bracketPramB1.BracketName="HK.Casing.DL02.BKT"
bracketPramB1.MaterialName="SS400"
bracketPramB1.BaseElement=profile19[0]
bracketPramB1.UseSideSheetForPlane=False
bracketPramB1.Mold="+"
bracketPramB1.Thickness="10"
bracketPramB1.BracketType=1501
bracketPramB1.Scallop1Type=1801
bracketPramB1.Scallop1Params=["0"]
bracketPramB1.Scallop2Type=0
bracketPramB1.Surfaces1=[profile19[0]+",FL"]
bracketPramB1.RevSf1=False
bracketPramB1.Surfaces2=[profile18[0]+",FL"]
bracketPramB1.RevSf2=False
bracketPramB1.RevSf3=False
bracketPramB1.Sf1DimensionType=1531
bracketPramB1.Sf1DimensonParams=["200","15"]
bracketPramB1.Sf2DimensionType=1531
bracketPramB1.Sf2DimensonParams=["200","15"]
bracketB1 = part.CreateBracket(bracketPramB1,False)
part.SetElementColor(bracketB1,"0","255","255","0.19999998807907104")
ProfilePram20 = part.CreateProfileParam()
ProfilePram20.DefinitionType=1
ProfilePram20.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram20.AddAttachSurfaces(extrude_sheet6)
ProfilePram20.ProfileName="HK.Casing.Wall.Side.FR15.ABP"
ProfilePram20.MaterialName="SS400"
ProfilePram20.ProfileType=1002
ProfilePram20.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram20.Mold="+"
ProfilePram20.ReverseDir=False
ProfilePram20.ReverseAngle=True
ProfilePram20.CalcSnipOnlyAttachLines=False
ProfilePram20.AttachDirMethod=0
ProfilePram20.CCWDefAngle=False
ProfilePram20.AddEnd1Elements(extrude_sheet1)
ProfilePram20.End1Type=1102
ProfilePram20.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.AddEnd2Elements(extrude_sheet2)
ProfilePram20.End2Type=1102
ProfilePram20.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.End1ScallopType=1121
ProfilePram20.End1ScallopTypeParams=["35","40"]
ProfilePram20.End2ScallopType=1121
ProfilePram20.End2ScallopTypeParams=["35","40"]
profile20 = part.CreateProfile(ProfilePram20,False)
part.SetElementColor(profile20[0],"255","0","0","0.19999998807907104")
var_elm9 = part.CreateVariable("FR14","9770","mm","")
ProfilePram21 = part.CreateProfileParam()
ProfilePram21.DefinitionType=1
ProfilePram21.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram21.AddAttachSurfaces(extrude_sheet6)
ProfilePram21.ProfileName="HK.Casing.Wall.Side.FR14.BCP"
ProfilePram21.MaterialName="SS400"
ProfilePram21.ProfileType=1002
ProfilePram21.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram21.Mold="+"
ProfilePram21.ReverseDir=False
ProfilePram21.ReverseAngle=True
ProfilePram21.CalcSnipOnlyAttachLines=False
ProfilePram21.AttachDirMethod=0
ProfilePram21.CCWDefAngle=False
ProfilePram21.AddEnd1Elements(extrude_sheet4)
ProfilePram21.End1Type=1102
ProfilePram21.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram21.AddEnd2Elements(extrude_sheet1)
ProfilePram21.End2Type=1102
ProfilePram21.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram21.End1ScallopType=1121
ProfilePram21.End1ScallopTypeParams=["35","40"]
ProfilePram21.End2ScallopType=1121
ProfilePram21.End2ScallopTypeParams=["35","40"]
profile21 = part.CreateProfile(ProfilePram21,False)
part.SetElementColor(profile21[0],"255","0","0","0.19999998807907104")
mirror_copied5 = part.MirrorCopy([profile18[0]],"PL,Y","")
part.SetElementColor(mirror_copied5[0],"148","0","211","0.39999997615814209")
var_elm10 = part.CreateVariable("FR9","6030","mm","")
ProfilePram22 = part.CreateProfileParam()
ProfilePram22.DefinitionType=1
ProfilePram22.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram22.AddAttachSurfaces(extrude_sheet5)
ProfilePram22.ProfileName="HK.Casing.Deck.D.FR09C"
ProfilePram22.MaterialName="SS400"
ProfilePram22.ProfileType=1003
ProfilePram22.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram22.Mold="+"
ProfilePram22.ReverseDir=True
ProfilePram22.ReverseAngle=False
ProfilePram22.CalcSnipOnlyAttachLines=False
ProfilePram22.AttachDirMethod=0
ProfilePram22.CCWDefAngle=False
ProfilePram22.AddEnd1Elements(mirror_copied5[0])
ProfilePram22.End1Type=1102
ProfilePram22.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram22.AddEnd2Elements(profile18[0])
ProfilePram22.End2Type=1102
ProfilePram22.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram22.End1ScallopType=1120
ProfilePram22.End1ScallopTypeParams=["50"]
ProfilePram22.End2ScallopType=1120
ProfilePram22.End2ScallopTypeParams=["50"]
profile22 = part.CreateProfile(ProfilePram22,False)
part.SetElementColor(profile22[0],"148","0","211","0.39999997615814209")
var_elm11 = part.CreateVariable("Casing.DL01","800","mm","")
ProfilePram23 = part.CreateProfileParam()
ProfilePram23.DefinitionType=1
ProfilePram23.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram23.AddAttachSurfaces(extrude_sheet5)
ProfilePram23.ProfileName="HK.Casing.Deck.D.DL01.AP"
ProfilePram23.MaterialName="SS400"
ProfilePram23.ProfileType=1002
ProfilePram23.ProfileParams=["125","75","7","10","5"]
ProfilePram23.Mold="+"
ProfilePram23.ReverseDir=True
ProfilePram23.ReverseAngle=True
ProfilePram23.CalcSnipOnlyAttachLines=False
ProfilePram23.AttachDirMethod=0
ProfilePram23.CCWDefAngle=False
ProfilePram23.AddEnd1Elements(extrude_sheet3)
ProfilePram23.End1Type=1102
ProfilePram23.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram23.AddEnd2Elements(profile22[0])
ProfilePram23.End2Type=1102
ProfilePram23.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram23.End1ScallopType=1120
ProfilePram23.End1ScallopTypeParams=["50"]
ProfilePram23.End2ScallopType=1120
ProfilePram23.End2ScallopTypeParams=["50"]
profile23 = part.CreateProfile(ProfilePram23,False)
part.SetElementColor(profile23[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck D DL01 と FR09C
bracketPramC1 = part.CreateBracketParam()
bracketPramC1.DefinitionType=1
bracketPramC1.BracketName="HK.Casing.Deck.D.DL01.BKT"
bracketPramC1.MaterialName="SS400"
bracketPramC1.BaseElement=profile23[0]
bracketPramC1.UseSideSheetForPlane=False
bracketPramC1.Mold="+"
bracketPramC1.Thickness="8"
bracketPramC1.BracketType=1501
bracketPramC1.Scallop1Type=1801
bracketPramC1.Scallop1Params=["0"]
bracketPramC1.Scallop2Type=0
bracketPramC1.Surfaces1=[profile23[0]+",FL"]
bracketPramC1.RevSf1=False
bracketPramC1.Surfaces2=[profile22[0]+",FL"]
bracketPramC1.RevSf2=False
bracketPramC1.RevSf3=False
bracketPramC1.Sf1DimensionType=1531
bracketPramC1.Sf1DimensonParams=["200","15"]
bracketPramC1.Sf2DimensionType=1531
bracketPramC1.Sf2DimensonParams=["200","15"]
bracketC1 = part.CreateBracket(bracketPramC1,False)
part.SetElementColor(bracketC1,"0","255","255","0.19999998807907104")
var_elm12 = part.CreateVariable("FR12","8170","mm","")
ProfilePram24 = part.CreateProfileParam()
ProfilePram24.DefinitionType=1
ProfilePram24.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram24.AddAttachSurfaces(extrude_sheet6)
ProfilePram24.ProfileName="HK.Casing.Wall.Side.FR12.OAP"
ProfilePram24.MaterialName="SS400"
ProfilePram24.ProfileType=1002
ProfilePram24.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram24.Mold="+"
ProfilePram24.ReverseDir=False
ProfilePram24.ReverseAngle=True
ProfilePram24.CalcSnipOnlyAttachLines=False
ProfilePram24.AttachDirMethod=0
ProfilePram24.CCWDefAngle=False
ProfilePram24.AddEnd1Elements(extrude_sheet2)
ProfilePram24.End1Type=1102
ProfilePram24.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.AddEnd2Elements(extrude_sheet7)
ProfilePram24.End2Type=1102
ProfilePram24.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.End1ScallopType=1121
ProfilePram24.End1ScallopTypeParams=["35","40"]
ProfilePram24.End2ScallopType=1121
ProfilePram24.End2ScallopTypeParams=["35","40"]
profile24 = part.CreateProfile(ProfilePram24,False)
part.SetElementColor(profile24[0],"255","0","0","0.19999998807907104")
ProfilePram25 = part.CreateProfileParam()
ProfilePram25.DefinitionType=1
ProfilePram25.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram25.AddAttachSurfaces(extrude_sheet8)
ProfilePram25.ProfileName="HK.Casing.Wall.Fore.DL03.ABP"
ProfilePram25.MaterialName="SS400"
ProfilePram25.ProfileType=1002
ProfilePram25.ProfileParams=["125","75","7","10","5"]
ProfilePram25.Mold="+"
ProfilePram25.ReverseDir=True
ProfilePram25.ReverseAngle=True
ProfilePram25.CalcSnipOnlyAttachLines=False
ProfilePram25.AttachDirMethod=0
ProfilePram25.CCWDefAngle=False
ProfilePram25.AddEnd1Elements(extrude_sheet1)
ProfilePram25.End1Type=1102
ProfilePram25.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.AddEnd2Elements(extrude_sheet2)
ProfilePram25.End2Type=1102
ProfilePram25.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.End1ScallopType=1121
ProfilePram25.End1ScallopTypeParams=["25","40"]
ProfilePram25.End2ScallopType=1121
ProfilePram25.End2ScallopTypeParams=["25","40"]
profile25 = part.CreateProfile(ProfilePram25,False)
part.SetElementColor(profile25[0],"255","0","0","0.19999998807907104")
ProfilePram26 = part.CreateProfileParam()
ProfilePram26.DefinitionType=1
ProfilePram26.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram26.AddAttachSurfaces(extrude_sheet8)
ProfilePram26.ProfileName="HK.Casing.Wall.Fore.DL01.BCP"
ProfilePram26.MaterialName="SS400"
ProfilePram26.ProfileType=1002
ProfilePram26.ProfileParams=["125","75","7","10","5"]
ProfilePram26.Mold="+"
ProfilePram26.ReverseDir=True
ProfilePram26.ReverseAngle=True
ProfilePram26.CalcSnipOnlyAttachLines=False
ProfilePram26.AttachDirMethod=0
ProfilePram26.CCWDefAngle=False
ProfilePram26.AddEnd1Elements(extrude_sheet4)
ProfilePram26.End1Type=1102
ProfilePram26.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram26.AddEnd2Elements(extrude_sheet1)
ProfilePram26.End2Type=1102
ProfilePram26.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram26.End1ScallopType=1121
ProfilePram26.End1ScallopTypeParams=["25","40"]
ProfilePram26.End2ScallopType=1121
ProfilePram26.End2ScallopTypeParams=["25","40"]
profile26 = part.CreateProfile(ProfilePram26,False)
part.SetElementColor(profile26[0],"255","0","0","0.19999998807907104")
mirror_copied6 = part.MirrorCopy([profile15[0]],"PL,Y","")
part.SetElementColor(mirror_copied6[0],"148","0","211","0.39999997615814209")
ProfilePram27 = part.CreateProfileParam()
ProfilePram27.DefinitionType=1
ProfilePram27.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram27.AddAttachSurfaces(extrude_sheet4)
ProfilePram27.ProfileName="HK.Casing.Deck.C.FR14F415"
ProfilePram27.MaterialName="SS400"
ProfilePram27.ProfileType=1003
ProfilePram27.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram27.Mold="+"
ProfilePram27.ReverseDir=True
ProfilePram27.ReverseAngle=True
ProfilePram27.CalcSnipOnlyAttachLines=False
ProfilePram27.AttachDirMethod=0
ProfilePram27.CCWDefAngle=False
ProfilePram27.AddEnd1Elements(mirror_copied6[0])
ProfilePram27.End1Type=1111
ProfilePram27.End1TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram27.AddEnd2Elements(profile15[0])
ProfilePram27.End2Type=1111
ProfilePram27.End2TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram27.End1ScallopType=1120
ProfilePram27.End1ScallopTypeParams=["50"]
ProfilePram27.End2ScallopType=1120
ProfilePram27.End2ScallopTypeParams=["50"]
profile27 = part.CreateProfile(ProfilePram27,False)
part.SetElementColor(profile27[0],"255","0","0","0.19999998807907104")
ProfilePram28 = part.CreateProfileParam()
ProfilePram28.DefinitionType=1
ProfilePram28.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram28.AddAttachSurfaces(extrude_sheet4)
ProfilePram28.ProfileName="HK.Casing.Deck.C.DL01.FP"
ProfilePram28.MaterialName="SS400"
ProfilePram28.ProfileType=1002
ProfilePram28.ProfileParams=["125","75","7","10","5"]
ProfilePram28.Mold="+"
ProfilePram28.ReverseDir=True
ProfilePram28.ReverseAngle=True
ProfilePram28.CalcSnipOnlyAttachLines=False
ProfilePram28.AttachDirMethod=0
ProfilePram28.CCWDefAngle=False
ProfilePram28.AddEnd1Elements(profile27[0])
ProfilePram28.End1Type=1102
ProfilePram28.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram28.AddEnd2Elements(profile26[0])
ProfilePram28.End2Type=1102
ProfilePram28.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram28.End1ScallopType=1121
ProfilePram28.End1ScallopTypeParams=["25","40"]
ProfilePram28.End2ScallopType=1121
ProfilePram28.End2ScallopTypeParams=["25","40"]
profile28 = part.CreateProfile(ProfilePram28,False)
part.SetElementColor(profile28[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck C DL01 FP と FR14F415
bracketPramD1 = part.CreateBracketParam()
bracketPramD1.DefinitionType=1
bracketPramD1.BracketName="HK.Casing.Deck.C.DL01.BKT"
bracketPramD1.MaterialName="SS400"
bracketPramD1.BaseElement=profile28[0]
bracketPramD1.UseSideSheetForPlane=False
bracketPramD1.Mold="+"
bracketPramD1.Thickness="8"
bracketPramD1.BracketType=1501
bracketPramD1.Scallop1Type=1801
bracketPramD1.Scallop1Params=["0"]
bracketPramD1.Scallop2Type=0
bracketPramD1.Surfaces1=[profile28[0]+",FL"]
bracketPramD1.RevSf1=False
bracketPramD1.Surfaces2=[profile27[0]+",FL"]
bracketPramD1.RevSf2=False
bracketPramD1.RevSf3=False
bracketPramD1.Sf1DimensionType=1531
bracketPramD1.Sf1DimensonParams=["200","15"]
bracketPramD1.Sf2DimensionType=1531
bracketPramD1.Sf2DimensonParams=["200","15"]
bracketD1 = part.CreateBracket(bracketPramD1,False)
part.SetElementColor(bracketD1,"0","255","255","0.19999998807907104")
skt_pl5 = part.CreateSketchPlane("HK.Az.Deck.B","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl5,True)
skt_layer15 = part.CreateSketchLayer("Edge00",skt_pl5)
skt_ln35 = part.CreateSketchLine(skt_pl5,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln36 = part.CreateSketchLine(skt_pl5,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln37 = part.CreateSketchLine(skt_pl5,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln38 = part.CreateSketchLine(skt_pl5,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer16 = part.CreateSketchLayer("Edge01",skt_pl5)
skt_ln39 = part.CreateSketchLine(skt_pl5,"","Edge01","9770,3125","4835.0000000000009,3125",False)
skt_ln40 = part.CreateSketchLine(skt_pl5,"","Edge01","10170,-2725","10170,2725",False)
skt_ln41 = part.CreateSketchLine(skt_pl5,"","Edge01","4835.0000000000009,-3125","9770,-3125",False)
skt_ln42 = part.CreateSketchLine(skt_pl5,"","Edge01","4435.0000000000009,2725","4435.0000000000009,-2724.9999999999991",False)
skt_arc9 = part.CreateSketchArc(skt_pl5,"","Edge01","4835.0000000000009,2724.9999999999995","4835.0000000000009,3124.9999999999995","4435.0000000000009,2725",True,False)
skt_arc10 = part.CreateSketchArc(skt_pl5,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3124.9999999999995",True,False)
skt_arc11 = part.CreateSketchArc(skt_pl5,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc12 = part.CreateSketchArc(skt_pl5,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125",True,False)
solid3 = part.CreateSolid("HK.Casing.Deck.B","","SS400")
part.SetElementColor(solid3,"139","69","19","0.78999996185302734")
thicken3 = part.CreateThicken("厚み付け5",solid3,"+",[extrude_sheet1],"+","10","0","0",False,False)
extrudePram13 = part.CreateLinearSweepParam()
extrudePram13.Name="積-押し出し5"
extrudePram13.AddProfile(skt_pl5+",Edge00")
extrudePram13.DirectionType="N"
extrudePram13.DirectionParameter1="50000"
extrudePram13.SweepDirection="+Z"
extrudePram13.RefByGeometricMethod=True
extrude5 = part.CreateLinearSweep(solid3,"*",extrudePram13,False)
extrudePram14 = part.CreateLinearSweepParam()
extrudePram14.Name="削除-押し出し3"
extrudePram14.AddProfile(skt_pl5+",Edge01")
extrudePram14.DirectionType="T"
extrudePram14.RefByGeometricMethod=True
extrude6 = part.CreateLinearSweep(solid3,"-",extrudePram14,False)
var_elm13 = part.CreateVariable("FR6","4019.9999999999995","mm","")
ProfilePram29 = part.CreateProfileParam()
ProfilePram29.DefinitionType=1
ProfilePram29.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram29.AddAttachSurfaces(extrude_sheet8)
ProfilePram29.ProfileName="HK.Casing.Wall.Fore.DL04.ABP"
ProfilePram29.MaterialName="SS400"
ProfilePram29.ProfileType=1003
ProfilePram29.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram29.Mold="+"
ProfilePram29.ReverseDir=True
ProfilePram29.ReverseAngle=True
ProfilePram29.CalcSnipOnlyAttachLines=False
ProfilePram29.AttachDirMethod=0
ProfilePram29.CCWDefAngle=False
ProfilePram29.AddEnd1Elements(extrude_sheet1)
ProfilePram29.End1Type=1102
ProfilePram29.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.AddEnd2Elements(extrude_sheet2)
ProfilePram29.End2Type=1102
ProfilePram29.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.End1ScallopType=1120
ProfilePram29.End1ScallopTypeParams=["50"]
ProfilePram29.End2ScallopType=1120
ProfilePram29.End2ScallopTypeParams=["50"]
profile29 = part.CreateProfile(ProfilePram29,False)
part.SetElementColor(profile29[0],"148","0","211","0.39999997615814209")
ProfilePram30 = part.CreateProfileParam()
ProfilePram30.DefinitionType=1
ProfilePram30.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram30.AddAttachSurfaces(extrude_sheet1)
ProfilePram30.ProfileName="HK.Casing.Deck.B.DL04P"
ProfilePram30.MaterialName="SS400"
ProfilePram30.ProfileType=1003
ProfilePram30.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram30.Mold="-"
ProfilePram30.ReverseDir=True
ProfilePram30.ReverseAngle=False
ProfilePram30.CalcSnipOnlyAttachLines=False
ProfilePram30.AttachDirMethod=0
ProfilePram30.CCWDefAngle=False
ProfilePram30.AddEnd1Elements(profile1[0])
ProfilePram30.End1Type=1102
ProfilePram30.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram30.AddEnd2Elements(profile29[0])
ProfilePram30.End2Type=1102
ProfilePram30.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram30.End1ScallopType=0
ProfilePram30.End2ScallopType=0
profile30 = part.CreateProfile(ProfilePram30,False)
part.SetElementColor(profile30[0],"148","0","211","0.39999997615814209")
mirror_copied7 = part.MirrorCopy([profile30[0]],"PL,Y","")
part.SetElementColor(mirror_copied7[0],"148","0","211","0.39999997615814209")
ProfilePram31 = part.CreateProfileParam()
ProfilePram31.DefinitionType=1
ProfilePram31.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram31.AddAttachSurfaces(extrude_sheet1)
ProfilePram31.ProfileName="HK.Casing.Deck.B.FR06F400"
ProfilePram31.MaterialName="SS400"
ProfilePram31.ProfileType=1007
ProfilePram31.ProfileParams=["150","12"]
ProfilePram31.Mold="+"
ProfilePram31.ReverseDir=True
ProfilePram31.ReverseAngle=False
ProfilePram31.CalcSnipOnlyAttachLines=False
ProfilePram31.AttachDirMethod=0
ProfilePram31.CCWDefAngle=False
ProfilePram31.AddEnd1Elements(mirror_copied7[0])
ProfilePram31.End1Type=1102
ProfilePram31.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram31.AddEnd2Elements(profile30[0])
ProfilePram31.End2Type=1102
ProfilePram31.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram31.End1ScallopType=-1
ProfilePram31.End2ScallopType=-1
profile31 = part.CreateProfile(ProfilePram31,False)
part.SetElementColor(profile31[0],"255","0","0","0.19999998807907104")
ProfilePram32 = part.CreateProfileParam()
ProfilePram32.DefinitionType=1
ProfilePram32.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram32.AddAttachSurfaces(extrude_sheet8)
ProfilePram32.ProfileName="HK.Casing.Wall.Fore.DL05.CDP"
ProfilePram32.MaterialName="SS400"
ProfilePram32.ProfileType=1002
ProfilePram32.ProfileParams=["125","75","7","10","5"]
ProfilePram32.Mold="+"
ProfilePram32.ReverseDir=True
ProfilePram32.ReverseAngle=True
ProfilePram32.CalcSnipOnlyAttachLines=False
ProfilePram32.AttachDirMethod=0
ProfilePram32.CCWDefAngle=False
ProfilePram32.AddEnd1Elements(profile17[0])
ProfilePram32.End1Type=1102
ProfilePram32.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram32.AddEnd2Elements(extrude_sheet4)
ProfilePram32.End2Type=1102
ProfilePram32.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram32.End1ScallopType=1120
ProfilePram32.End1ScallopTypeParams=["50"]
ProfilePram32.End2ScallopType=1120
ProfilePram32.End2ScallopTypeParams=["50"]
profile32 = part.CreateProfile(ProfilePram32,False)
part.SetElementColor(profile32[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Fore DL05 と Deck D DL05
bracketPramE1 = part.CreateBracketParam()
bracketPramE1.DefinitionType=1
bracketPramE1.BracketName="HK.Casing.DL05.ForeDeckD.BKT"
bracketPramE1.MaterialName="SS400"
bracketPramE1.BaseElement=profile32[0]
bracketPramE1.UseSideSheetForPlane=False
bracketPramE1.Mold="+"
bracketPramE1.Thickness="8"
bracketPramE1.BracketType=1501
bracketPramE1.Scallop1Type=1801
bracketPramE1.Scallop1Params=["0"]
bracketPramE1.Scallop2Type=0
bracketPramE1.Surfaces1=[profile32[0]+",FL"]
bracketPramE1.RevSf1=False
bracketPramE1.Surfaces2=[profile17[0]+",FL"]
bracketPramE1.RevSf2=False
bracketPramE1.RevSf3=False
bracketPramE1.Sf1DimensionType=1531
bracketPramE1.Sf1DimensonParams=["200","15"]
bracketPramE1.Sf2DimensionType=1531
bracketPramE1.Sf2DimensonParams=["200","15"]
bracketE1 = part.CreateBracket(bracketPramE1,False)
part.SetElementColor(bracketE1,"0","255","255","0.19999998807907104")
var_elm14 = part.CreateVariable("Casing.DL00","0","mm","")
ProfilePram33 = part.CreateProfileParam()
ProfilePram33.DefinitionType=1
ProfilePram33.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram33.AddAttachSurfaces(extrude_sheet5)
ProfilePram33.ProfileName="HK.Casing.Deck.D.DL00.A"
ProfilePram33.MaterialName="SS400"
ProfilePram33.ProfileType=1002
ProfilePram33.ProfileParams=["125","75","7","10","5"]
ProfilePram33.ReverseDir=True
ProfilePram33.ReverseAngle=True
ProfilePram33.CalcSnipOnlyAttachLines=False
ProfilePram33.AttachDirMethod=0
ProfilePram33.CCWDefAngle=False
ProfilePram33.AddEnd1Elements(extrude_sheet3)
ProfilePram33.End1Type=1102
ProfilePram33.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram33.AddEnd2Elements(profile22[0])
ProfilePram33.End2Type=1102
ProfilePram33.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram33.End1ScallopType=1120
ProfilePram33.End1ScallopTypeParams=["50"]
ProfilePram33.End2ScallopType=1120
ProfilePram33.End2ScallopTypeParams=["50"]
profile33 = part.CreateProfile(ProfilePram33,False)
part.SetElementColor(profile33[0],"255","0","0","0.19999998807907104")
ProfilePram34 = part.CreateProfileParam()
ProfilePram34.DefinitionType=1
ProfilePram34.BasePlane="PL,O,"+var_elm8+","+"X"
ProfilePram34.AddAttachSurfaces(extrude_sheet6)
ProfilePram34.ProfileName="HK.Casing.Wall.Side.FR07.OAP"
ProfilePram34.MaterialName="SS400"
ProfilePram34.ProfileType=1002
ProfilePram34.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram34.Mold="+"
ProfilePram34.ReverseDir=False
ProfilePram34.ReverseAngle=True
ProfilePram34.CalcSnipOnlyAttachLines=False
ProfilePram34.AttachDirMethod=0
ProfilePram34.CCWDefAngle=False
ProfilePram34.AddEnd1Elements(extrude_sheet2)
ProfilePram34.End1Type=1102
ProfilePram34.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram34.AddEnd2Elements(extrude_sheet7)
ProfilePram34.End2Type=1102
ProfilePram34.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram34.End1ScallopType=1121
ProfilePram34.End1ScallopTypeParams=["35","40"]
ProfilePram34.End2ScallopType=1121
ProfilePram34.End2ScallopTypeParams=["35","40"]
profile34 = part.CreateProfile(ProfilePram34,False)
part.SetElementColor(profile34[0],"255","0","0","0.19999998807907104")
mirror_copied8 = part.MirrorCopy([profile34[0]],"PL,Y","")
part.SetElementColor(mirror_copied8[0],"255","0","0","0.19999998807907104")
ProfilePram35 = part.CreateProfileParam()
ProfilePram35.DefinitionType=1
ProfilePram35.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram35.AddAttachSurfaces(extrude_sheet5)
ProfilePram35.ProfileName="HK.Casing.Deck.D.DL03P"
ProfilePram35.MaterialName="SS400"
ProfilePram35.ProfileType=1002
ProfilePram35.ProfileParams=["125","75","7","10","5"]
ProfilePram35.Mold="+"
ProfilePram35.ReverseDir=True
ProfilePram35.ReverseAngle=True
ProfilePram35.CalcSnipOnlyAttachLines=False
ProfilePram35.AttachDirMethod=0
ProfilePram35.CCWDefAngle=False
ProfilePram35.AddEnd1Elements(extrude_sheet3)
ProfilePram35.End1Type=1102
ProfilePram35.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram35.AddEnd2Elements(extrude_sheet8)
ProfilePram35.End2Type=1102
ProfilePram35.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram35.End1ScallopType=1120
ProfilePram35.End1ScallopTypeParams=["50"]
ProfilePram35.End2ScallopType=1120
ProfilePram35.End2ScallopTypeParams=["50"]
profile35 = part.CreateProfile(ProfilePram35,False)
part.SetElementColor(profile35[0],"255","0","0","0.19999998807907104")
ProfilePram36 = part.CreateProfileParam()
ProfilePram36.DefinitionType=1
ProfilePram36.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram36.AddAttachSurfaces(extrude_sheet3)
ProfilePram36.ProfileName="HK.Casing.Wall.Aft.DL03.CDP"
ProfilePram36.MaterialName="SS400"
ProfilePram36.ProfileType=1002
ProfilePram36.ProfileParams=["125","75","7","10","5"]
ProfilePram36.Mold="+"
ProfilePram36.ReverseDir=False
ProfilePram36.ReverseAngle=True
ProfilePram36.CalcSnipOnlyAttachLines=False
ProfilePram36.AttachDirMethod=0
ProfilePram36.CCWDefAngle=False
ProfilePram36.AddEnd1Elements(profile35[0])
ProfilePram36.End1Type=1102
ProfilePram36.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram36.AddEnd2Elements(extrude_sheet4)
ProfilePram36.End2Type=1102
ProfilePram36.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram36.End1ScallopType=1120
ProfilePram36.End1ScallopTypeParams=["50"]
ProfilePram36.End2ScallopType=1120
ProfilePram36.End2ScallopTypeParams=["50"]
profile36 = part.CreateProfile(ProfilePram36,False)
part.SetElementColor(profile36[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: DL03 Aft と Deck D DL03
bracketPramF1 = part.CreateBracketParam()
bracketPramF1.DefinitionType=1
bracketPramF1.BracketName="HK.Casing.DL03.AftDeckD.BKT"
bracketPramF1.MaterialName="SS400"
bracketPramF1.BaseElement=profile36[0]
bracketPramF1.UseSideSheetForPlane=False
bracketPramF1.Mold="+"
bracketPramF1.Thickness="8"
bracketPramF1.BracketType=1501
bracketPramF1.Scallop1Type=1801
bracketPramF1.Scallop1Params=["0"]
bracketPramF1.Scallop2Type=0
bracketPramF1.Surfaces1=[profile36[0]+",FL"]
bracketPramF1.RevSf1=False
bracketPramF1.Surfaces2=[profile35[0]+",FL"]
bracketPramF1.RevSf2=False
bracketPramF1.RevSf3=False
bracketPramF1.Sf1DimensionType=1531
bracketPramF1.Sf1DimensonParams=["200","15"]
bracketPramF1.Sf2DimensionType=1531
bracketPramF1.Sf2DimensonParams=["200","15"]
bracketF1 = part.CreateBracket(bracketPramF1,False)
part.SetElementColor(bracketF1,"0","255","255","0.19999998807907104")
var_elm15 = part.CreateVariable("FR13","8970","mm","")
ProfilePram37 = part.CreateProfileParam()
ProfilePram37.DefinitionType=1
ProfilePram37.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram37.AddAttachSurfaces(extrude_sheet6)
ProfilePram37.ProfileName="HK.Casing.Wall.Side.FR13.OAP"
ProfilePram37.MaterialName="SS400"
ProfilePram37.ProfileType=1003
ProfilePram37.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram37.Mold="+"
ProfilePram37.ReverseDir=False
ProfilePram37.ReverseAngle=True
ProfilePram37.CalcSnipOnlyAttachLines=False
ProfilePram37.AttachDirMethod=0
ProfilePram37.CCWDefAngle=False
ProfilePram37.AddEnd1Elements(extrude_sheet2)
ProfilePram37.End1Type=1103
ProfilePram37.End1TypeParams=["0"]
ProfilePram37.AddEnd2Elements(extrude_sheet7)
ProfilePram37.End2Type=1103
ProfilePram37.End2TypeParams=["0"]
ProfilePram37.End1ScallopType=1120
ProfilePram37.End1ScallopTypeParams=["50"]
ProfilePram37.End2ScallopType=1120
ProfilePram37.End2ScallopTypeParams=["50"]
profile37 = part.CreateProfile(ProfilePram37,False)
part.SetElementColor(profile37[0],"148","0","211","0.39999997615814209")
ProfilePram38 = part.CreateProfileParam()
ProfilePram38.DefinitionType=1
ProfilePram38.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram38.AddAttachSurfaces(extrude_sheet3)
ProfilePram38.ProfileName="HK.Casing.Wall.Aft.DL04.OAP"
ProfilePram38.MaterialName="SS400"
ProfilePram38.ProfileType=1003
ProfilePram38.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram38.Mold="+"
ProfilePram38.ReverseDir=False
ProfilePram38.ReverseAngle=True
ProfilePram38.CalcSnipOnlyAttachLines=False
ProfilePram38.AttachDirMethod=0
ProfilePram38.CCWDefAngle=False
ProfilePram38.AddEnd1Elements(extrude_sheet2)
ProfilePram38.End1Type=1102
ProfilePram38.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram38.AddEnd2Elements(extrude_sheet7)
ProfilePram38.End2Type=1102
ProfilePram38.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram38.End1ScallopType=1120
ProfilePram38.End1ScallopTypeParams=["50"]
ProfilePram38.End2ScallopType=1120
ProfilePram38.End2ScallopTypeParams=["50"]
profile38 = part.CreateProfile(ProfilePram38,False)
part.SetElementColor(profile38[0],"148","0","211","0.39999997615814209")
ProfilePram39 = part.CreateProfileParam()
ProfilePram39.DefinitionType=1
ProfilePram39.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram39.AddAttachSurfaces(extrude_sheet8)
ProfilePram39.ProfileName="HK.Casing.Wall.Fore.DL04.OAP"
ProfilePram39.MaterialName="SS400"
ProfilePram39.ProfileType=1003
ProfilePram39.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram39.Mold="+"
ProfilePram39.ReverseDir=True
ProfilePram39.ReverseAngle=True
ProfilePram39.CalcSnipOnlyAttachLines=False
ProfilePram39.AttachDirMethod=0
ProfilePram39.CCWDefAngle=False
ProfilePram39.AddEnd1Elements(extrude_sheet2)
ProfilePram39.End1Type=1102
ProfilePram39.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram39.AddEnd2Elements(extrude_sheet7)
ProfilePram39.End2Type=1102
ProfilePram39.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram39.End1ScallopType=1120
ProfilePram39.End1ScallopTypeParams=["50"]
ProfilePram39.End2ScallopType=1120
ProfilePram39.End2ScallopTypeParams=["50"]
profile39 = part.CreateProfile(ProfilePram39,False)
part.SetElementColor(profile39[0],"148","0","211","0.39999997615814209")
ProfilePram40 = part.CreateProfileParam()
ProfilePram40.DefinitionType=1
ProfilePram40.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram40.AddAttachSurfaces(extrude_sheet2)
ProfilePram40.ProfileName="HK.Casing.Deck.A.DL04P"
ProfilePram40.MaterialName="SS400"
ProfilePram40.ProfileType=1003
ProfilePram40.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram40.Mold="-"
ProfilePram40.ReverseDir=True
ProfilePram40.ReverseAngle=False
ProfilePram40.CalcSnipOnlyAttachLines=False
ProfilePram40.AttachDirMethod=0
ProfilePram40.CCWDefAngle=False
ProfilePram40.AddEnd1Elements(profile38[0])
ProfilePram40.End1Type=1102
ProfilePram40.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram40.AddEnd2Elements(profile39[0])
ProfilePram40.End2Type=1102
ProfilePram40.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram40.End1ScallopType=0
ProfilePram40.End2ScallopType=0
profile40 = part.CreateProfile(ProfilePram40,False)
part.SetElementColor(profile40[0],"148","0","211","0.39999997615814209")
ProfilePram41 = part.CreateProfileParam()
ProfilePram41.DefinitionType=1
ProfilePram41.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram41.AddAttachSurfaces(extrude_sheet2)
ProfilePram41.ProfileName="HK.Casing.Deck.A.FR13P"
ProfilePram41.MaterialName="SS400"
ProfilePram41.ProfileType=1003
ProfilePram41.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram41.Mold="+"
ProfilePram41.ReverseDir=True
ProfilePram41.ReverseAngle=False
ProfilePram41.CalcSnipOnlyAttachLines=False
ProfilePram41.AttachDirMethod=0
ProfilePram41.CCWDefAngle=False
ProfilePram41.AddEnd1Elements(profile40[0])
ProfilePram41.End1Type=1113
ProfilePram41.End1TypeParams=["0","79"]
ProfilePram41.AddEnd2Elements(profile37[0])
ProfilePram41.End2Type=1102
ProfilePram41.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram41.End1ScallopType=1120
ProfilePram41.End1ScallopTypeParams=["50"]
ProfilePram41.End2ScallopType=1120
ProfilePram41.End2ScallopTypeParams=["50"]
profile41 = part.CreateProfile(ProfilePram41,False)
part.SetElementColor(profile41[0],"148","0","211","0.39999997615814209")
ProfilePram42 = part.CreateProfileParam()
ProfilePram42.DefinitionType=1
ProfilePram42.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram42.AddAttachSurfaces(extrude_sheet5)
ProfilePram42.ProfileName="HK.Casing.Deck.D.FR13P"
ProfilePram42.MaterialName="SS400"
ProfilePram42.ProfileType=1003
ProfilePram42.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram42.Mold="+"
ProfilePram42.ReverseDir=True
ProfilePram42.ReverseAngle=False
ProfilePram42.CalcSnipOnlyAttachLines=False
ProfilePram42.AttachDirMethod=0
ProfilePram42.CCWDefAngle=False
ProfilePram42.AddEnd1Elements(profile18[0])
ProfilePram42.End1Type=1102
ProfilePram42.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram42.AddEnd2Elements(extrude_sheet6)
ProfilePram42.End2Type=1102
ProfilePram42.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram42.End1ScallopType=1120
ProfilePram42.End1ScallopTypeParams=["50"]
ProfilePram42.End2ScallopType=1120
ProfilePram42.End2ScallopTypeParams=["50"]
profile42 = part.CreateProfile(ProfilePram42,False)
part.SetElementColor(profile42[0],"148","0","211","0.39999997615814209")
ProfilePram43 = part.CreateProfileParam()
ProfilePram43.DefinitionType=1
ProfilePram43.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram43.AddAttachSurfaces(extrude_sheet6)
ProfilePram43.ProfileName="HK.Casing.Wall.Side.FR13.CDP"
ProfilePram43.MaterialName="SS400"
ProfilePram43.ProfileType=1003
ProfilePram43.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram43.Mold="+"
ProfilePram43.ReverseDir=False
ProfilePram43.ReverseAngle=True
ProfilePram43.CalcSnipOnlyAttachLines=False
ProfilePram43.AttachDirMethod=0
ProfilePram43.CCWDefAngle=False
ProfilePram43.AddEnd1Elements(profile42[0])
ProfilePram43.End1Type=1102
ProfilePram43.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram43.AddEnd2Elements(extrude_sheet4)
ProfilePram43.End2Type=1103
ProfilePram43.End2TypeParams=["0"]
ProfilePram43.End1ScallopType=1120
ProfilePram43.End1ScallopTypeParams=["50"]
ProfilePram43.End2ScallopType=1120
ProfilePram43.End2ScallopTypeParams=["50"]
profile43 = part.CreateProfile(ProfilePram43,False)
part.SetElementColor(profile43[0],"148","0","211","0.39999997615814209")
var_elm16 = part.CreateVariable("FR10","6700","mm","")
ProfilePram44 = part.CreateProfileParam()
ProfilePram44.DefinitionType=1
ProfilePram44.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram44.AddAttachSurfaces(extrude_sheet6)
ProfilePram44.ProfileName="HK.Casing.Wall.Side.FR10.CDP"
ProfilePram44.MaterialName="SS400"
ProfilePram44.ProfileType=1002
ProfilePram44.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram44.Mold="+"
ProfilePram44.ReverseDir=False
ProfilePram44.ReverseAngle=True
ProfilePram44.CalcSnipOnlyAttachLines=False
ProfilePram44.AttachDirMethod=0
ProfilePram44.CCWDefAngle=False
ProfilePram44.AddEnd1Elements(extrude_sheet5)
ProfilePram44.End1Type=1102
ProfilePram44.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram44.AddEnd2Elements(extrude_sheet4)
ProfilePram44.End2Type=1102
ProfilePram44.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram44.End1ScallopType=1121
ProfilePram44.End1ScallopTypeParams=["35","40"]
ProfilePram44.End2ScallopType=1121
ProfilePram44.End2ScallopTypeParams=["35","40"]
profile44 = part.CreateProfile(ProfilePram44,False)
part.SetElementColor(profile44[0],"255","0","0","0.19999998807907104")
ProfilePram45 = part.CreateProfileParam()
ProfilePram45.DefinitionType=1
ProfilePram45.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram45.AddAttachSurfaces(extrude_sheet6)
ProfilePram45.ProfileName="HK.Casing.Wall.Side.FR14.OAP"
ProfilePram45.MaterialName="SS400"
ProfilePram45.ProfileType=1002
ProfilePram45.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram45.Mold="+"
ProfilePram45.ReverseDir=False
ProfilePram45.ReverseAngle=True
ProfilePram45.CalcSnipOnlyAttachLines=False
ProfilePram45.AttachDirMethod=0
ProfilePram45.CCWDefAngle=False
ProfilePram45.AddEnd1Elements(extrude_sheet2)
ProfilePram45.End1Type=1102
ProfilePram45.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram45.AddEnd2Elements(extrude_sheet7)
ProfilePram45.End2Type=1102
ProfilePram45.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram45.End1ScallopType=1121
ProfilePram45.End1ScallopTypeParams=["35","40"]
ProfilePram45.End2ScallopType=1121
ProfilePram45.End2ScallopTypeParams=["35","40"]
profile45 = part.CreateProfile(ProfilePram45,False)
part.SetElementColor(profile45[0],"255","0","0","0.19999998807907104")
skt_pl6 = part.CreateSketchPlane("HK.Az.Deck.A","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl6,True)
skt_layer17 = part.CreateSketchLayer("Edge00",skt_pl6)
skt_ln43 = part.CreateSketchLine(skt_pl6,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln44 = part.CreateSketchLine(skt_pl6,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln45 = part.CreateSketchLine(skt_pl6,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln46 = part.CreateSketchLine(skt_pl6,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer18 = part.CreateSketchLayer("Edge01",skt_pl6)
skt_ln47 = part.CreateSketchLine(skt_pl6,"","Edge01","9770,3125","4835.0000000000009,3125",False)
skt_ln48 = part.CreateSketchLine(skt_pl6,"","Edge01","10170,-2725","10170,2725",False)
skt_ln49 = part.CreateSketchLine(skt_pl6,"","Edge01","4835.0000000000009,-3125","9770,-3125",False)
skt_ln50 = part.CreateSketchLine(skt_pl6,"","Edge01","4435.0000000000009,2725","4435.0000000000009,-2724.9999999999991",False)
skt_arc13 = part.CreateSketchArc(skt_pl6,"","Edge01","4835.0000000000009,2724.9999999999995","4835.0000000000009,3124.9999999999995","4435.0000000000009,2725",True,False)
skt_arc14 = part.CreateSketchArc(skt_pl6,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3124.9999999999995",True,False)
skt_arc15 = part.CreateSketchArc(skt_pl6,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc16 = part.CreateSketchArc(skt_pl6,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125",True,False)
solid4 = part.CreateSolid("HK.Casing.Deck.A","","SS400")
part.SetElementColor(solid4,"139","69","19","0.78999996185302734")
thicken4 = part.CreateThicken("厚み付け6",solid4,"+",[extrude_sheet2],"+","10","0","0",False,False)
extrudePram15 = part.CreateLinearSweepParam()
extrudePram15.Name="積-押し出し6"
extrudePram15.AddProfile(skt_pl6+",Edge00")
extrudePram15.DirectionType="N"
extrudePram15.DirectionParameter1="50000"
extrudePram15.SweepDirection="+Z"
extrudePram15.RefByGeometricMethod=True
extrude7 = part.CreateLinearSweep(solid4,"*",extrudePram15,False)
extrudePram16 = part.CreateLinearSweepParam()
extrudePram16.Name="削除-押し出し4"
extrudePram16.AddProfile(skt_pl6+",Edge01")
extrudePram16.DirectionType="T"
extrudePram16.RefByGeometricMethod=True
extrude8 = part.CreateLinearSweep(solid4,"-",extrudePram16,False)
ProfilePram46 = part.CreateProfileParam()
ProfilePram46.DefinitionType=1
ProfilePram46.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram46.AddAttachSurfaces(extrude_sheet8)
ProfilePram46.ProfileName="HK.Casing.Wall.Fore.DL05.OAP"
ProfilePram46.MaterialName="SS400"
ProfilePram46.ProfileType=1002
ProfilePram46.ProfileParams=["125","75","7","10","5"]
ProfilePram46.Mold="+"
ProfilePram46.ReverseDir=True
ProfilePram46.ReverseAngle=True
ProfilePram46.CalcSnipOnlyAttachLines=False
ProfilePram46.AttachDirMethod=0
ProfilePram46.CCWDefAngle=False
ProfilePram46.AddEnd1Elements(extrude_sheet2)
ProfilePram46.End1Type=1102
ProfilePram46.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram46.AddEnd2Elements(extrude_sheet7)
ProfilePram46.End2Type=1102
ProfilePram46.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram46.End1ScallopType=1121
ProfilePram46.End1ScallopTypeParams=["25","40"]
ProfilePram46.End2ScallopType=1121
ProfilePram46.End2ScallopTypeParams=["25","40"]
profile46 = part.CreateProfile(ProfilePram46,False)
part.SetElementColor(profile46[0],"255","0","0","0.19999998807907104")
ProfilePram47 = part.CreateProfileParam()
ProfilePram47.DefinitionType=1
ProfilePram47.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram47.AddAttachSurfaces(extrude_sheet2)
ProfilePram47.ProfileName="HK.Casing.Deck.A.DL05P"
ProfilePram47.MaterialName="SS400"
ProfilePram47.ProfileType=1002
ProfilePram47.ProfileParams=["125","75","7","10","5"]
ProfilePram47.Mold="+"
ProfilePram47.ReverseDir=True
ProfilePram47.ReverseAngle=True
ProfilePram47.CalcSnipOnlyAttachLines=False
ProfilePram47.AttachDirMethod=0
ProfilePram47.CCWDefAngle=False
ProfilePram47.AddEnd1Elements(profile4[0])
ProfilePram47.End1Type=1102
ProfilePram47.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram47.AddEnd2Elements(profile46[0])
ProfilePram47.End2Type=1102
ProfilePram47.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram47.End1ScallopType=1120
ProfilePram47.End1ScallopTypeParams=["50"]
ProfilePram47.End2ScallopType=1120
ProfilePram47.End2ScallopTypeParams=["50"]
profile47 = part.CreateProfile(ProfilePram47,False)
part.SetElementColor(profile47[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck A DL05 と Fore DL05
bracketPramG1 = part.CreateBracketParam()
bracketPramG1.DefinitionType=1
bracketPramG1.BracketName="HK.Casing.Deck.A.DL05.BKT"
bracketPramG1.MaterialName="SS400"
bracketPramG1.BaseElement=profile47[0]
bracketPramG1.UseSideSheetForPlane=False
bracketPramG1.Mold="+"
bracketPramG1.Thickness="8"
bracketPramG1.BracketType=1501
bracketPramG1.Scallop1Type=1801
bracketPramG1.Scallop1Params=["0"]
bracketPramG1.Scallop2Type=0
bracketPramG1.Surfaces1=[profile47[0]+",FL"]
bracketPramG1.RevSf1=False
bracketPramG1.Surfaces2=[profile46[0]+",FL"]
bracketPramG1.RevSf2=False
bracketPramG1.RevSf3=False
bracketPramG1.Sf1DimensionType=1531
bracketPramG1.Sf1DimensonParams=["200","15"]
bracketPramG1.Sf2DimensionType=1531
bracketPramG1.Sf2DimensonParams=["200","15"]
bracketG1 = part.CreateBracket(bracketPramG1,False)
part.SetElementColor(bracketG1,"0","255","255","0.19999998807907104")
ProfilePram48 = part.CreateProfileParam()
ProfilePram48.DefinitionType=1
ProfilePram48.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram48.AddAttachSurfaces(extrude_sheet8)
ProfilePram48.ProfileName="HK.Casing.Wall.Fore.DL00.OA"
ProfilePram48.MaterialName="SS400"
ProfilePram48.ProfileType=1002
ProfilePram48.ProfileParams=["125","75","7","10","5"]
ProfilePram48.ReverseDir=True
ProfilePram48.ReverseAngle=True
ProfilePram48.CalcSnipOnlyAttachLines=False
ProfilePram48.AttachDirMethod=0
ProfilePram48.CCWDefAngle=False
ProfilePram48.AddEnd1Elements(extrude_sheet2)
ProfilePram48.End1Type=1102
ProfilePram48.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram48.AddEnd2Elements(extrude_sheet7)
ProfilePram48.End2Type=1102
ProfilePram48.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram48.End1ScallopType=1121
ProfilePram48.End1ScallopTypeParams=["25","40"]
ProfilePram48.End2ScallopType=1121
ProfilePram48.End2ScallopTypeParams=["25","40"]
profile48 = part.CreateProfile(ProfilePram48,False)
part.SetElementColor(profile48[0],"255","0","0","0.19999998807907104")
mirror_copied9 = part.MirrorCopy([profile40[0]],"PL,Y","")
part.SetElementColor(mirror_copied9[0],"148","0","211","0.39999997615814209")
ProfilePram49 = part.CreateProfileParam()
ProfilePram49.DefinitionType=1
ProfilePram49.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram49.AddAttachSurfaces(extrude_sheet2)
ProfilePram49.ProfileName="HK.Casing.Deck.A.FR14F415"
ProfilePram49.MaterialName="SS400"
ProfilePram49.ProfileType=1003
ProfilePram49.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram49.Mold="+"
ProfilePram49.ReverseDir=True
ProfilePram49.ReverseAngle=True
ProfilePram49.CalcSnipOnlyAttachLines=False
ProfilePram49.AttachDirMethod=0
ProfilePram49.CCWDefAngle=False
ProfilePram49.AddEnd1Elements(mirror_copied9[0])
ProfilePram49.End1Type=1111
ProfilePram49.End1TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram49.AddEnd2Elements(profile40[0])
ProfilePram49.End2Type=1111
ProfilePram49.End2TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram49.End1ScallopType=1120
ProfilePram49.End1ScallopTypeParams=["50"]
ProfilePram49.End2ScallopType=1120
ProfilePram49.End2ScallopTypeParams=["50"]
profile49 = part.CreateProfile(ProfilePram49,False)
part.SetElementColor(profile49[0],"255","0","0","0.19999998807907104")
ProfilePram50 = part.CreateProfileParam()
ProfilePram50.DefinitionType=1
ProfilePram50.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram50.AddAttachSurfaces(extrude_sheet2)
ProfilePram50.ProfileName="HK.Casing.Deck.A.DL00.F"
ProfilePram50.MaterialName="SS400"
ProfilePram50.ProfileType=1002
ProfilePram50.ProfileParams=["125","75","7","10","5"]
ProfilePram50.ReverseDir=True
ProfilePram50.ReverseAngle=True
ProfilePram50.CalcSnipOnlyAttachLines=False
ProfilePram50.AttachDirMethod=0
ProfilePram50.CCWDefAngle=False
ProfilePram50.AddEnd1Elements(profile49[0])
ProfilePram50.End1Type=1102
ProfilePram50.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram50.AddEnd2Elements(profile48[0])
ProfilePram50.End2Type=1102
ProfilePram50.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram50.End1ScallopType=1121
ProfilePram50.End1ScallopTypeParams=["25","40"]
ProfilePram50.End2ScallopType=1121
ProfilePram50.End2ScallopTypeParams=["25","40"]
profile50 = part.CreateProfile(ProfilePram50,False)
part.SetElementColor(profile50[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck A DL00 と Fore DL00
bracketPramH1 = part.CreateBracketParam()
bracketPramH1.DefinitionType=1
bracketPramH1.BracketName="HK.Casing.Deck.A.DL00.BKT"
bracketPramH1.MaterialName="SS400"
bracketPramH1.BaseElement=profile50[0]
bracketPramH1.UseSideSheetForPlane=False
bracketPramH1.Mold="+"
bracketPramH1.Thickness="8"
bracketPramH1.BracketType=1501
bracketPramH1.Scallop1Type=1801
bracketPramH1.Scallop1Params=["0"]
bracketPramH1.Scallop2Type=0
bracketPramH1.Surfaces1=[profile50[0]+",FL"]
bracketPramH1.RevSf1=False
bracketPramH1.Surfaces2=[profile48[0]+",FL"]
bracketPramH1.RevSf2=False
bracketPramH1.RevSf3=False
bracketPramH1.Sf1DimensionType=1531
bracketPramH1.Sf1DimensonParams=["200","15"]
bracketPramH1.Sf2DimensionType=1531
bracketPramH1.Sf2DimensonParams=["200","15"]
bracketH1 = part.CreateBracket(bracketPramH1,False)
part.SetElementColor(bracketH1,"0","255","255","0.19999998807907104")
ProfilePram51 = part.CreateProfileParam()
ProfilePram51.DefinitionType=1
ProfilePram51.BasePlane="PL,O,"+var_elm8+","+"X"
ProfilePram51.AddAttachSurfaces(extrude_sheet6)
ProfilePram51.ProfileName="HK.Casing.Wall.Side.FR07.BCP"
ProfilePram51.MaterialName="SS400"
ProfilePram51.ProfileType=1002
ProfilePram51.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram51.Mold="+"
ProfilePram51.ReverseDir=False
ProfilePram51.ReverseAngle=True
ProfilePram51.CalcSnipOnlyAttachLines=False
ProfilePram51.AttachDirMethod=0
ProfilePram51.CCWDefAngle=False
ProfilePram51.AddEnd1Elements(extrude_sheet4)
ProfilePram51.End1Type=1102
ProfilePram51.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram51.AddEnd2Elements(extrude_sheet1)
ProfilePram51.End2Type=1102
ProfilePram51.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram51.End1ScallopType=1121
ProfilePram51.End1ScallopTypeParams=["35","40"]
ProfilePram51.End2ScallopType=1121
ProfilePram51.End2ScallopTypeParams=["35","40"]
profile51 = part.CreateProfile(ProfilePram51,False)
part.SetElementColor(profile51[0],"255","0","0","0.19999998807907104")
ProfilePram52 = part.CreateProfileParam()
ProfilePram52.DefinitionType=1
ProfilePram52.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram52.AddAttachSurfaces(extrude_sheet6)
ProfilePram52.ProfileName="HK.Casing.Wall.Side.FR12.CDP"
ProfilePram52.MaterialName="SS400"
ProfilePram52.ProfileType=1002
ProfilePram52.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram52.Mold="+"
ProfilePram52.ReverseDir=False
ProfilePram52.ReverseAngle=True
ProfilePram52.CalcSnipOnlyAttachLines=False
ProfilePram52.AttachDirMethod=0
ProfilePram52.CCWDefAngle=False
ProfilePram52.AddEnd1Elements(extrude_sheet5)
ProfilePram52.End1Type=1102
ProfilePram52.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram52.AddEnd2Elements(extrude_sheet4)
ProfilePram52.End2Type=1102
ProfilePram52.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram52.End1ScallopType=1121
ProfilePram52.End1ScallopTypeParams=["35","40"]
ProfilePram52.End2ScallopType=1121
ProfilePram52.End2ScallopTypeParams=["35","40"]
profile52 = part.CreateProfile(ProfilePram52,False)
part.SetElementColor(profile52[0],"255","0","0","0.19999998807907104")
ProfilePram53 = part.CreateProfileParam()
ProfilePram53.DefinitionType=1
ProfilePram53.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram53.AddAttachSurfaces(extrude_sheet8)
ProfilePram53.ProfileName="HK.Casing.Wall.Fore.DL03.BCP"
ProfilePram53.MaterialName="SS400"
ProfilePram53.ProfileType=1002
ProfilePram53.ProfileParams=["125","75","7","10","5"]
ProfilePram53.Mold="+"
ProfilePram53.ReverseDir=True
ProfilePram53.ReverseAngle=True
ProfilePram53.CalcSnipOnlyAttachLines=False
ProfilePram53.AttachDirMethod=0
ProfilePram53.CCWDefAngle=False
ProfilePram53.AddEnd1Elements(extrude_sheet4)
ProfilePram53.End1Type=1102
ProfilePram53.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram53.AddEnd2Elements(extrude_sheet1)
ProfilePram53.End2Type=1102
ProfilePram53.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram53.End1ScallopType=1121
ProfilePram53.End1ScallopTypeParams=["25","40"]
ProfilePram53.End2ScallopType=1121
ProfilePram53.End2ScallopTypeParams=["25","40"]
profile53 = part.CreateProfile(ProfilePram53,False)
part.SetElementColor(profile53[0],"255","0","0","0.19999998807907104")
ProfilePram54 = part.CreateProfileParam()
ProfilePram54.DefinitionType=1
ProfilePram54.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram54.AddAttachSurfaces(extrude_sheet4)
ProfilePram54.ProfileName="HK.Casing.Deck.C.DL03.FP"
ProfilePram54.MaterialName="SS400"
ProfilePram54.ProfileType=1002
ProfilePram54.ProfileParams=["125","75","7","10","5"]
ProfilePram54.Mold="+"
ProfilePram54.ReverseDir=True
ProfilePram54.ReverseAngle=True
ProfilePram54.CalcSnipOnlyAttachLines=False
ProfilePram54.AttachDirMethod=0
ProfilePram54.CCWDefAngle=False
ProfilePram54.AddEnd1Elements(profile27[0])
ProfilePram54.End1Type=1102
ProfilePram54.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram54.AddEnd2Elements(profile53[0])
ProfilePram54.End2Type=1102
ProfilePram54.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram54.End1ScallopType=1121
ProfilePram54.End1ScallopTypeParams=["25","40"]
ProfilePram54.End2ScallopType=1121
ProfilePram54.End2ScallopTypeParams=["25","40"]
profile54 = part.CreateProfile(ProfilePram54,False)
part.SetElementColor(profile54[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck C DL03 と Fore DL03
bracketPramI1 = part.CreateBracketParam()
bracketPramI1.DefinitionType=1
bracketPramI1.BracketName="HK.Casing.Deck.C.DL03.BKT"
bracketPramI1.MaterialName="SS400"
bracketPramI1.BaseElement=profile54[0]
bracketPramI1.UseSideSheetForPlane=False
bracketPramI1.Mold="+"
bracketPramI1.Thickness="8"
bracketPramI1.BracketType=1501
bracketPramI1.Scallop1Type=1801
bracketPramI1.Scallop1Params=["0"]
bracketPramI1.Scallop2Type=0
bracketPramI1.Surfaces1=[profile54[0]+",FL"]
bracketPramI1.RevSf1=False
bracketPramI1.Surfaces2=[profile53[0]+",FL"]
bracketPramI1.RevSf2=False
bracketPramI1.RevSf3=False
bracketPramI1.Sf1DimensionType=1531
bracketPramI1.Sf1DimensonParams=["200","15"]
bracketPramI1.Sf2DimensionType=1531
bracketPramI1.Sf2DimensonParams=["200","15"]
bracketI1 = part.CreateBracket(bracketPramI1,False)
part.SetElementColor(bracketI1,"0","255","255","0.19999998807907104")
ProfilePram55 = part.CreateProfileParam()
ProfilePram55.DefinitionType=1
ProfilePram55.BasePlane="PL,O,"+var_elm5+","+"X"
ProfilePram55.AddAttachSurfaces(extrude_sheet6)
ProfilePram55.ProfileName="HK.Casing.Wall.Side.FR08.OAP"
ProfilePram55.MaterialName="SS400"
ProfilePram55.ProfileType=1002
ProfilePram55.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram55.Mold="+"
ProfilePram55.ReverseDir=False
ProfilePram55.ReverseAngle=True
ProfilePram55.CalcSnipOnlyAttachLines=False
ProfilePram55.AttachDirMethod=0
ProfilePram55.CCWDefAngle=False
ProfilePram55.AddEnd1Elements(extrude_sheet2)
ProfilePram55.End1Type=1102
ProfilePram55.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram55.AddEnd2Elements(extrude_sheet7)
ProfilePram55.End2Type=1102
ProfilePram55.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram55.End1ScallopType=1121
ProfilePram55.End1ScallopTypeParams=["35","40"]
ProfilePram55.End2ScallopType=1121
ProfilePram55.End2ScallopTypeParams=["35","40"]
profile55 = part.CreateProfile(ProfilePram55,False)
part.SetElementColor(profile55[0],"255","0","0","0.19999998807907104")
ProfilePram56 = part.CreateProfileParam()
ProfilePram56.DefinitionType=1
ProfilePram56.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram56.AddAttachSurfaces(extrude_sheet2)
ProfilePram56.ProfileName="HK.Casing.Deck.A.FR06F400"
ProfilePram56.MaterialName="SS400"
ProfilePram56.ProfileType=1007
ProfilePram56.ProfileParams=["150","12"]
ProfilePram56.Mold="+"
ProfilePram56.ReverseDir=True
ProfilePram56.ReverseAngle=False
ProfilePram56.CalcSnipOnlyAttachLines=False
ProfilePram56.AttachDirMethod=0
ProfilePram56.CCWDefAngle=False
ProfilePram56.AddEnd1Elements(mirror_copied9[0])
ProfilePram56.End1Type=1102
ProfilePram56.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram56.AddEnd2Elements(profile40[0])
ProfilePram56.End2Type=1102
ProfilePram56.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram56.End1ScallopType=-1
ProfilePram56.End2ScallopType=-1
profile56 = part.CreateProfile(ProfilePram56,False)
part.SetElementColor(profile56[0],"255","0","0","0.19999998807907104")
ProfilePram57 = part.CreateProfileParam()
ProfilePram57.DefinitionType=1
ProfilePram57.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram57.AddAttachSurfaces(extrude_sheet6)
ProfilePram57.ProfileName="HK.Casing.Wall.Side.FR09.OAP"
ProfilePram57.MaterialName="SS400"
ProfilePram57.ProfileType=1003
ProfilePram57.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram57.Mold="+"
ProfilePram57.ReverseDir=False
ProfilePram57.ReverseAngle=True
ProfilePram57.CalcSnipOnlyAttachLines=False
ProfilePram57.AttachDirMethod=0
ProfilePram57.CCWDefAngle=False
ProfilePram57.AddEnd1Elements(extrude_sheet2)
ProfilePram57.End1Type=1103
ProfilePram57.End1TypeParams=["0"]
ProfilePram57.AddEnd2Elements(extrude_sheet7)
ProfilePram57.End2Type=1103
ProfilePram57.End2TypeParams=["0"]
ProfilePram57.End1ScallopType=1120
ProfilePram57.End1ScallopTypeParams=["50"]
ProfilePram57.End2ScallopType=1120
ProfilePram57.End2ScallopTypeParams=["50"]
profile57 = part.CreateProfile(ProfilePram57,False)
part.SetElementColor(profile57[0],"148","0","211","0.39999997615814209")
mirror_copied12 = part.MirrorCopy([profile57[0]],"PL,Y","")
part.SetElementColor(mirror_copied12[0],"148","0","211","0.39999997615814209")
ProfilePram58 = part.CreateProfileParam()
ProfilePram58.DefinitionType=1
ProfilePram58.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram58.AddAttachSurfaces(extrude_sheet6)
ProfilePram58.ProfileName="HK.Casing.Wall.Side.FR10.OAP"
ProfilePram58.MaterialName="SS400"
ProfilePram58.ProfileType=1002
ProfilePram58.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram58.Mold="+"
ProfilePram58.ReverseDir=False
ProfilePram58.ReverseAngle=True
ProfilePram58.CalcSnipOnlyAttachLines=False
ProfilePram58.AttachDirMethod=0
ProfilePram58.CCWDefAngle=False
ProfilePram58.AddEnd1Elements(extrude_sheet2)
ProfilePram58.End1Type=1102
ProfilePram58.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram58.AddEnd2Elements(extrude_sheet7)
ProfilePram58.End2Type=1102
ProfilePram58.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram58.End1ScallopType=1121
ProfilePram58.End1ScallopTypeParams=["35","40"]
ProfilePram58.End2ScallopType=1121
ProfilePram58.End2ScallopTypeParams=["35","40"]
profile58 = part.CreateProfile(ProfilePram58,False)
part.SetElementColor(profile58[0],"255","0","0","0.19999998807907104")
ProfilePram59 = part.CreateProfileParam()
ProfilePram59.DefinitionType=1
ProfilePram59.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram59.AddAttachSurfaces(extrude_sheet8)
ProfilePram59.ProfileName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram59.MaterialName="SS400"
ProfilePram59.FlangeName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram59.FlangeMaterialName="SS400"
ProfilePram59.ProfileType=1201
ProfilePram59.ProfileParams=["150","12","388","10"]
ProfilePram59.Mold="-"
ProfilePram59.ReverseDir=True
ProfilePram59.ReverseAngle=False
ProfilePram59.CalcSnipOnlyAttachLines=False
ProfilePram59.AttachDirMethod=0
ProfilePram59.CCWDefAngle=False
ProfilePram59.AddEnd1Elements(profile18[1])
ProfilePram59.End1Type=1102
ProfilePram59.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram59.AddEnd2Elements(extrude_sheet4)
ProfilePram59.End2Type=1102
ProfilePram59.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram59.End1ScallopType=1120
ProfilePram59.End1ScallopTypeParams=["50"]
ProfilePram59.End2ScallopType=1120
ProfilePram59.End2ScallopTypeParams=["50"]
profile59 = part.CreateProfile(ProfilePram59,False)
part.SetElementColor(profile59[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile59[1],"148","0","211","0.39999997615814209")
ProfilePram60 = part.CreateProfileParam()
ProfilePram60.DefinitionType=1
ProfilePram60.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram60.AddAttachSurfaces(extrude_sheet5)
ProfilePram60.ProfileName="HK.Casing.Deck.D.FR13C"
ProfilePram60.MaterialName="SS400"
ProfilePram60.ProfileType=1003
ProfilePram60.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram60.Mold="+"
ProfilePram60.ReverseDir=True
ProfilePram60.ReverseAngle=False
ProfilePram60.CalcSnipOnlyAttachLines=False
ProfilePram60.AttachDirMethod=0
ProfilePram60.CCWDefAngle=False
ProfilePram60.AddEnd1Elements(mirror_copied5[0])
ProfilePram60.End1Type=1102
ProfilePram60.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram60.AddEnd2Elements(profile18[0])
ProfilePram60.End2Type=1102
ProfilePram60.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram60.End1ScallopType=1120
ProfilePram60.End1ScallopTypeParams=["50"]
ProfilePram60.End2ScallopType=1120
ProfilePram60.End2ScallopTypeParams=["50"]
profile60 = part.CreateProfile(ProfilePram60,False)
part.SetElementColor(profile60[0],"148","0","211","0.39999997615814209")
ProfilePram61 = part.CreateProfileParam()
ProfilePram61.DefinitionType=1
ProfilePram61.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram61.AddAttachSurfaces(extrude_sheet5)
ProfilePram61.ProfileName="HK.Casing.Deck.D.DL01.FP"
ProfilePram61.MaterialName="SS400"
ProfilePram61.ProfileType=1002
ProfilePram61.ProfileParams=["125","75","7","10","5"]
ProfilePram61.Mold="+"
ProfilePram61.ReverseDir=True
ProfilePram61.ReverseAngle=True
ProfilePram61.CalcSnipOnlyAttachLines=False
ProfilePram61.AttachDirMethod=0
ProfilePram61.CCWDefAngle=False
ProfilePram61.AddEnd1Elements(profile60[0])
ProfilePram61.End1Type=1102
ProfilePram61.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram61.AddEnd2Elements(extrude_sheet8)
ProfilePram61.End2Type=1102
ProfilePram61.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram61.End1ScallopType=1121
ProfilePram61.End1ScallopTypeParams=["25","40"]
ProfilePram61.End2ScallopType=1121
ProfilePram61.End2ScallopTypeParams=["25","40"]
profile61 = part.CreateProfile(ProfilePram61,False)
part.SetElementColor(profile61[0],"255","0","0","0.19999998807907104")
ProfilePram62 = part.CreateProfileParam()
ProfilePram62.DefinitionType=1
ProfilePram62.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram62.AddAttachSurfaces(extrude_sheet8)
ProfilePram62.ProfileName="HK.Casing.Wall.Fore.DL01.CDP"
ProfilePram62.MaterialName="SS400"
ProfilePram62.ProfileType=1002
ProfilePram62.ProfileParams=["125","75","7","10","5"]
ProfilePram62.Mold="+"
ProfilePram62.ReverseDir=True
ProfilePram62.ReverseAngle=True
ProfilePram62.CalcSnipOnlyAttachLines=False
ProfilePram62.AttachDirMethod=0
ProfilePram62.CCWDefAngle=False
ProfilePram62.AddEnd1Elements(profile61[0])
ProfilePram62.End1Type=1102
ProfilePram62.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram62.AddEnd2Elements(extrude_sheet4)
ProfilePram62.End2Type=1102
ProfilePram62.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram62.End1ScallopType=1120
ProfilePram62.End1ScallopTypeParams=["50"]
ProfilePram62.End2ScallopType=1120
ProfilePram62.End2ScallopTypeParams=["50"]
profile62 = part.CreateProfile(ProfilePram62,False)
part.SetElementColor(profile62[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: DL01 Fore と Deck D DL01
bracketPramJ1 = part.CreateBracketParam()
bracketPramJ1.DefinitionType=1
bracketPramJ1.BracketName="HK.Casing.DL01.ForeDeckD.BKT"
bracketPramJ1.MaterialName="SS400"
bracketPramJ1.BaseElement=profile62[0]
bracketPramJ1.UseSideSheetForPlane=False
bracketPramJ1.Mold="+"
bracketPramJ1.Thickness="8"
bracketPramJ1.BracketType=1501
bracketPramJ1.Scallop1Type=1801
bracketPramJ1.Scallop1Params=["0"]
bracketPramJ1.Scallop2Type=0
bracketPramJ1.Surfaces1=[profile62[0]+",FL"]
bracketPramJ1.RevSf1=False
bracketPramJ1.Surfaces2=[profile61[0]+",FL"]
bracketPramJ1.RevSf2=False
bracketPramJ1.RevSf3=False
bracketPramJ1.Sf1DimensionType=1531
bracketPramJ1.Sf1DimensonParams=["200","15"]
bracketPramJ1.Sf2DimensionType=1531
bracketPramJ1.Sf2DimensonParams=["200","15"]
bracketJ1 = part.CreateBracket(bracketPramJ1,False)
part.SetElementColor(bracketJ1,"0","255","255","0.19999998807907104")
ProfilePram63 = part.CreateProfileParam()
ProfilePram63.DefinitionType=1
ProfilePram63.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram63.AddAttachSurfaces(extrude_sheet3)
ProfilePram63.ProfileName="HK.Casing.Wall.Aft.DL03.BCP"
ProfilePram63.MaterialName="SS400"
ProfilePram63.ProfileType=1002
ProfilePram63.ProfileParams=["125","75","7","10","5"]
ProfilePram63.Mold="+"
ProfilePram63.ReverseDir=False
ProfilePram63.ReverseAngle=True
ProfilePram63.CalcSnipOnlyAttachLines=False
ProfilePram63.AttachDirMethod=0
ProfilePram63.CCWDefAngle=False
ProfilePram63.AddEnd1Elements(extrude_sheet4)
ProfilePram63.End1Type=1102
ProfilePram63.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram63.AddEnd2Elements(extrude_sheet1)
ProfilePram63.End2Type=1102
ProfilePram63.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram63.End1ScallopType=1121
ProfilePram63.End1ScallopTypeParams=["25","40"]
ProfilePram63.End2ScallopType=1121
ProfilePram63.End2ScallopTypeParams=["25","40"]
profile63 = part.CreateProfile(ProfilePram63,False)
part.SetElementColor(profile63[0],"255","0","0","0.19999998807907104")
ProfilePram64 = part.CreateProfileParam()
ProfilePram64.DefinitionType=1
ProfilePram64.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram64.AddAttachSurfaces(extrude_sheet5)
ProfilePram64.ProfileName="HK.Casing.Deck.D.FR09P"
ProfilePram64.MaterialName="SS400"
ProfilePram64.ProfileType=1003
ProfilePram64.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram64.Mold="+"
ProfilePram64.ReverseDir=True
ProfilePram64.ReverseAngle=False
ProfilePram64.CalcSnipOnlyAttachLines=False
ProfilePram64.AttachDirMethod=0
ProfilePram64.CCWDefAngle=False
ProfilePram64.AddEnd1Elements(profile18[0])
ProfilePram64.End1Type=1102
ProfilePram64.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram64.AddEnd2Elements(extrude_sheet6)
ProfilePram64.End2Type=1102
ProfilePram64.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram64.End1ScallopType=1120
ProfilePram64.End1ScallopTypeParams=["50"]
ProfilePram64.End2ScallopType=1120
ProfilePram64.End2ScallopTypeParams=["50"]
profile64 = part.CreateProfile(ProfilePram64,False)
part.SetElementColor(profile64[0],"148","0","211","0.39999997615814209")
ProfilePram65 = part.CreateProfileParam()
ProfilePram65.DefinitionType=1
ProfilePram65.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram65.AddAttachSurfaces(extrude_sheet6)
ProfilePram65.ProfileName="HK.Casing.Wall.Side.FR09.CDP"
ProfilePram65.MaterialName="SS400"
ProfilePram65.ProfileType=1003
ProfilePram65.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram65.Mold="+"
ProfilePram65.ReverseDir=False
ProfilePram65.ReverseAngle=True
ProfilePram65.CalcSnipOnlyAttachLines=False
ProfilePram65.AttachDirMethod=0
ProfilePram65.CCWDefAngle=False
ProfilePram65.AddEnd1Elements(profile64[0])
ProfilePram65.End1Type=1102
ProfilePram65.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram65.AddEnd2Elements(extrude_sheet4)
ProfilePram65.End2Type=1103
ProfilePram65.End2TypeParams=["0"]
ProfilePram65.End1ScallopType=1120
ProfilePram65.End1ScallopTypeParams=["50"]
ProfilePram65.End2ScallopType=1120
ProfilePram65.End2ScallopTypeParams=["50"]
profile65 = part.CreateProfile(ProfilePram65,False)
part.SetElementColor(profile65[0],"148","0","211","0.39999997615814209")
solid5 = part.CreateSolid("HK.Casing.Wall.Aft.CD","","SS400")
part.SetElementColor(solid5,"139","69","19","0.79999995231628418")
thicken5 = part.CreateThicken("厚み付け11",solid5,"+",[extrude_sheet3],"-","10","0","0",False,False)
extrudePram17 = part.CreateLinearSweepParam()
extrudePram17.Name="積-押し出し19"
extrudePram17.AddProfile(extrude_sheet6)
extrudePram17.DirectionType="R"
extrudePram17.DirectionParameter1="50000"
extrudePram17.SweepDirection="+Y"
extrudePram17.RefByGeometricMethod=True
extrude9 = part.CreateLinearSweep(solid5,"*",extrudePram17,False)
extrudePram18 = part.CreateLinearSweepParam()
extrudePram18.AddProfile(skt_pl2+",Casing.Side.S")
extrudePram18.DirectionType="2"
extrudePram18.DirectionParameter1="50000"
extrudePram18.DirectionParameter2="10000"
extrudePram18.SweepDirection="+Z"
extrudePram18.Name="HK.Casing.Wall.SideS"
extrudePram18.MaterialName="SS400"
extrudePram18.IntervalSweep=False
extrude_sheet9 = part.CreateLinearSweepSheet(extrudePram18,False)
part.SheetAlignNormal(extrude_sheet9,0,-1,0)
part.BlankElement(extrude_sheet9,True)
part.SetElementColor(extrude_sheet9,"225","225","225","1")
ProfilePram66 = part.CreateProfileParam()
ProfilePram66.DefinitionType=1
ProfilePram66.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram66.AddAttachSurfaces(extrude_sheet3)
ProfilePram66.ProfileName="HK.Casing.Wall.Aft.DL05.ABP"
ProfilePram66.MaterialName="SS400"
ProfilePram66.ProfileType=1002
ProfilePram66.ProfileParams=["125","75","7","10","5"]
ProfilePram66.Mold="+"
ProfilePram66.ReverseDir=False
ProfilePram66.ReverseAngle=True
ProfilePram66.CalcSnipOnlyAttachLines=False
ProfilePram66.AttachDirMethod=0
ProfilePram66.CCWDefAngle=False
ProfilePram66.AddEnd1Elements(extrude_sheet1)
ProfilePram66.End1Type=1102
ProfilePram66.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram66.AddEnd2Elements(extrude_sheet2)
ProfilePram66.End2Type=1102
ProfilePram66.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram66.End1ScallopType=1121
ProfilePram66.End1ScallopTypeParams=["25","40"]
ProfilePram66.End2ScallopType=1121
ProfilePram66.End2ScallopTypeParams=["25","40"]
profile66 = part.CreateProfile(ProfilePram66,False)
part.SetElementColor(profile66[0],"255","0","0","0.19999998807907104")
ProfilePram67 = part.CreateProfileParam()
ProfilePram67.DefinitionType=1
ProfilePram67.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram67.AddAttachSurfaces(extrude_sheet8)
ProfilePram67.ProfileName="HK.Casing.Wall.Fore.DL05.ABP"
ProfilePram67.MaterialName="SS400"
ProfilePram67.ProfileType=1002
ProfilePram67.ProfileParams=["125","75","7","10","5"]
ProfilePram67.Mold="+"
ProfilePram67.ReverseDir=True
ProfilePram67.ReverseAngle=True
ProfilePram67.CalcSnipOnlyAttachLines=False
ProfilePram67.AttachDirMethod=0
ProfilePram67.CCWDefAngle=False
ProfilePram67.AddEnd1Elements(extrude_sheet1)
ProfilePram67.End1Type=1102
ProfilePram67.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram67.AddEnd2Elements(extrude_sheet2)
ProfilePram67.End2Type=1102
ProfilePram67.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram67.End1ScallopType=1121
ProfilePram67.End1ScallopTypeParams=["25","40"]
ProfilePram67.End2ScallopType=1121
ProfilePram67.End2ScallopTypeParams=["25","40"]
profile67 = part.CreateProfile(ProfilePram67,False)
part.SetElementColor(profile67[0],"255","0","0","0.19999998807907104")
ProfilePram68 = part.CreateProfileParam()
ProfilePram68.DefinitionType=1
ProfilePram68.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram68.AddAttachSurfaces(extrude_sheet1)
ProfilePram68.ProfileName="HK.Casing.Deck.B.DL05P"
ProfilePram68.MaterialName="SS400"
ProfilePram68.ProfileType=1002
ProfilePram68.ProfileParams=["125","75","7","10","5"]
ProfilePram68.Mold="+"
ProfilePram68.ReverseDir=True
ProfilePram68.ReverseAngle=True
ProfilePram68.CalcSnipOnlyAttachLines=False
ProfilePram68.AttachDirMethod=0
ProfilePram68.CCWDefAngle=False
ProfilePram68.AddEnd1Elements(profile66[0])
ProfilePram68.End1Type=1102
ProfilePram68.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram68.AddEnd2Elements(profile67[0])
ProfilePram68.End2Type=1102
ProfilePram68.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram68.End1ScallopType=1120
ProfilePram68.End1ScallopTypeParams=["50"]
ProfilePram68.End2ScallopType=1120
ProfilePram68.End2ScallopTypeParams=["50"]
profile68 = part.CreateProfile(ProfilePram68,False)
part.SetElementColor(profile68[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck B/A の DL05 対応
bracketPramK1 = part.CreateBracketParam()
bracketPramK1.DefinitionType=1
bracketPramK1.BracketName="HK.Casing.Deck.B.DL05.BKT"
bracketPramK1.MaterialName="SS400"
bracketPramK1.BaseElement=profile68[0]
bracketPramK1.UseSideSheetForPlane=False
bracketPramK1.Mold="+"
bracketPramK1.Thickness="8"
bracketPramK1.BracketType=1501
bracketPramK1.Scallop1Type=1801
bracketPramK1.Scallop1Params=["0"]
bracketPramK1.Scallop2Type=0
bracketPramK1.Surfaces1=[profile68[0]+",FL"]
bracketPramK1.RevSf1=False
bracketPramK1.Surfaces2=[profile67[0]+",FL"]
bracketPramK1.RevSf2=False
bracketPramK1.RevSf3=False
bracketPramK1.Sf1DimensionType=1531
bracketPramK1.Sf1DimensonParams=["200","15"]
bracketPramK1.Sf2DimensionType=1531
bracketPramK1.Sf2DimensonParams=["200","15"]
bracketK1 = part.CreateBracket(bracketPramK1,False)
part.SetElementColor(bracketK1,"0","255","255","0.19999998807907104")
ProfilePram69 = part.CreateProfileParam()
ProfilePram69.DefinitionType=1
ProfilePram69.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram69.AddAttachSurfaces(extrude_sheet8)
ProfilePram69.ProfileName="HK.Casing.Wall.Fore.DL01.ABP"
ProfilePram69.MaterialName="SS400"
ProfilePram69.ProfileType=1002
ProfilePram69.ProfileParams=["125","75","7","10","5"]
ProfilePram69.Mold="+"
ProfilePram69.ReverseDir=True
ProfilePram69.ReverseAngle=True
ProfilePram69.CalcSnipOnlyAttachLines=False
ProfilePram69.AttachDirMethod=0
ProfilePram69.CCWDefAngle=False
ProfilePram69.AddEnd1Elements(extrude_sheet1)
ProfilePram69.End1Type=1102
ProfilePram69.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram69.AddEnd2Elements(extrude_sheet2)
ProfilePram69.End2Type=1102
ProfilePram69.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram69.End1ScallopType=1121
ProfilePram69.End1ScallopTypeParams=["25","40"]
ProfilePram69.End2ScallopType=1121
ProfilePram69.End2ScallopTypeParams=["25","40"]
profile69 = part.CreateProfile(ProfilePram69,False)
part.SetElementColor(profile69[0],"255","0","0","0.19999998807907104")
ProfilePram70 = part.CreateProfileParam()
ProfilePram70.DefinitionType=1
ProfilePram70.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram70.AddAttachSurfaces(extrude_sheet1)
ProfilePram70.ProfileName="HK.Casing.Deck.B.FR14F415"
ProfilePram70.MaterialName="SS400"
ProfilePram70.ProfileType=1003
ProfilePram70.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram70.Mold="+"
ProfilePram70.ReverseDir=True
ProfilePram70.ReverseAngle=True
ProfilePram70.CalcSnipOnlyAttachLines=False
ProfilePram70.AttachDirMethod=0
ProfilePram70.CCWDefAngle=False
ProfilePram70.AddEnd1Elements(mirror_copied7[0])
ProfilePram70.End1Type=1111
ProfilePram70.End1TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram70.AddEnd2Elements(profile30[0])
ProfilePram70.End2Type=1111
ProfilePram70.End2TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram70.End1ScallopType=1120
ProfilePram70.End1ScallopTypeParams=["50"]
ProfilePram70.End2ScallopType=1120
ProfilePram70.End2ScallopTypeParams=["50"]
profile70 = part.CreateProfile(ProfilePram70,False)
part.SetElementColor(profile70[0],"255","0","0","0.19999998807907104")
ProfilePram71 = part.CreateProfileParam()
ProfilePram71.DefinitionType=1
ProfilePram71.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram71.AddAttachSurfaces(extrude_sheet1)
ProfilePram71.ProfileName="HK.Casing.Deck.B.DL01.FP"
ProfilePram71.MaterialName="SS400"
ProfilePram71.ProfileType=1002
ProfilePram71.ProfileParams=["125","75","7","10","5"]
ProfilePram71.Mold="+"
ProfilePram71.ReverseDir=True
ProfilePram71.ReverseAngle=True
ProfilePram71.CalcSnipOnlyAttachLines=False
ProfilePram71.AttachDirMethod=0
ProfilePram71.CCWDefAngle=False
ProfilePram71.AddEnd1Elements(profile70[0])
ProfilePram71.End1Type=1102
ProfilePram71.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram71.AddEnd2Elements(profile69[0])
ProfilePram71.End2Type=1102
ProfilePram71.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram71.End1ScallopType=1121
ProfilePram71.End1ScallopTypeParams=["25","40"]
ProfilePram71.End2ScallopType=1121
ProfilePram71.End2ScallopTypeParams=["25","40"]
profile71 = part.CreateProfile(ProfilePram71,False)
part.SetElementColor(profile71[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck B DL01 と Fore DL01
bracketPramL1 = part.CreateBracketParam()
bracketPramL1.DefinitionType=1
bracketPramL1.BracketName="HK.Casing.Deck.B.DL01.BKT"
bracketPramL1.MaterialName="SS400"
bracketPramL1.BaseElement=profile71[0]
bracketPramL1.UseSideSheetForPlane=False
bracketPramL1.Mold="+"
bracketPramL1.Thickness="8"
bracketPramL1.BracketType=1501
bracketPramL1.Scallop1Type=1801
bracketPramL1.Scallop1Params=["0"]
bracketPramL1.Scallop2Type=0
bracketPramL1.Surfaces1=[profile71[0]+",FL"]
bracketPramL1.RevSf1=False
bracketPramL1.Surfaces2=[profile69[0]+",FL"]
bracketPramL1.RevSf2=False
bracketPramL1.RevSf3=False
bracketPramL1.Sf1DimensionType=1531
bracketPramL1.Sf1DimensonParams=["200","15"]
bracketPramL1.Sf2DimensionType=1531
bracketPramL1.Sf2DimensonParams=["200","15"]
bracketL1 = part.CreateBracket(bracketPramL1,False)
part.SetElementColor(bracketL1,"0","255","255","0.19999998807907104")
mirror_copied13 = part.MirrorCopy([profile63[0]],"PL,Y","")
part.SetElementColor(mirror_copied13[0],"255","0","0","0.19999998807907104")
mirror_copied14 = part.MirrorCopy([profile38[0]],"PL,Y","")
part.SetElementColor(mirror_copied14[0],"148","0","211","0.39999997615814209")
ProfilePram72 = part.CreateProfileParam()
ProfilePram72.DefinitionType=1
ProfilePram72.BasePlane="PL,O,"+var_elm4+","+"Y"
ProfilePram72.AddAttachSurfaces(extrude_sheet3)
ProfilePram72.ProfileName="HK.Casing.Wall.Aft.DL05.CDP"
ProfilePram72.MaterialName="SS400"
ProfilePram72.ProfileType=1002
ProfilePram72.ProfileParams=["125","75","7","10","5"]
ProfilePram72.Mold="+"
ProfilePram72.ReverseDir=False
ProfilePram72.ReverseAngle=True
ProfilePram72.CalcSnipOnlyAttachLines=False
ProfilePram72.AttachDirMethod=0
ProfilePram72.CCWDefAngle=False
ProfilePram72.AddEnd1Elements(profile17[0])
ProfilePram72.End1Type=1102
ProfilePram72.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram72.AddEnd2Elements(extrude_sheet4)
ProfilePram72.End2Type=1102
ProfilePram72.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram72.End1ScallopType=1120
ProfilePram72.End1ScallopTypeParams=["50"]
ProfilePram72.End2ScallopType=1120
ProfilePram72.End2ScallopTypeParams=["50"]
profile72 = part.CreateProfile(ProfilePram72,False)
part.SetElementColor(profile72[0],"255","0","0","0.19999998807907104")
ProfilePram73 = part.CreateProfileParam()
ProfilePram73.DefinitionType=1
ProfilePram73.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram73.AddAttachSurfaces(extrude_sheet8)
ProfilePram73.ProfileName="HK.Casing.Wall.Fore.DL00.BC"
ProfilePram73.MaterialName="SS400"
ProfilePram73.ProfileType=1002
ProfilePram73.ProfileParams=["125","75","7","10","5"]
ProfilePram73.ReverseDir=True
ProfilePram73.ReverseAngle=True
ProfilePram73.CalcSnipOnlyAttachLines=False
ProfilePram73.AttachDirMethod=0
ProfilePram73.CCWDefAngle=False
ProfilePram73.AddEnd1Elements(extrude_sheet4)
ProfilePram73.End1Type=1102
ProfilePram73.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram73.AddEnd2Elements(extrude_sheet1)
ProfilePram73.End2Type=1102
ProfilePram73.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram73.End1ScallopType=1121
ProfilePram73.End1ScallopTypeParams=["25","40"]
ProfilePram73.End2ScallopType=1121
ProfilePram73.End2ScallopTypeParams=["25","40"]
profile73 = part.CreateProfile(ProfilePram73,False)
part.SetElementColor(profile73[0],"255","0","0","0.19999998807907104")
ProfilePram74 = part.CreateProfileParam()
ProfilePram74.DefinitionType=1
ProfilePram74.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram74.AddAttachSurfaces(extrude_sheet4)
ProfilePram74.ProfileName="HK.Casing.Deck.C.DL00.F"
ProfilePram74.MaterialName="SS400"
ProfilePram74.ProfileType=1002
ProfilePram74.ProfileParams=["125","75","7","10","5"]
ProfilePram74.ReverseDir=True
ProfilePram74.ReverseAngle=True
ProfilePram74.CalcSnipOnlyAttachLines=False
ProfilePram74.AttachDirMethod=0
ProfilePram74.CCWDefAngle=False
ProfilePram74.AddEnd1Elements(profile27[0])
ProfilePram74.End1Type=1102
ProfilePram74.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram74.AddEnd2Elements(profile73[0])
ProfilePram74.End2Type=1102
ProfilePram74.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram74.End1ScallopType=1121
ProfilePram74.End1ScallopTypeParams=["25","40"]
ProfilePram74.End2ScallopType=1121
ProfilePram74.End2ScallopTypeParams=["25","40"]
profile74 = part.CreateProfile(ProfilePram74,False)
part.SetElementColor(profile74[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: Deck C DL00 と Fore DL00
bracketPramM1 = part.CreateBracketParam()
bracketPramM1.DefinitionType=1
bracketPramM1.BracketName="HK.Casing.Deck.C.DL00.BKT"
bracketPramM1.MaterialName="SS400"
bracketPramM1.BaseElement=profile74[0]
bracketPramM1.UseSideSheetForPlane=False
bracketPramM1.Mold="+"
bracketPramM1.Thickness="8"
bracketPramM1.BracketType=1501
bracketPramM1.Scallop1Type=1801
bracketPramM1.Scallop1Params=["0"]
bracketPramM1.Scallop2Type=0
bracketPramM1.Surfaces1=[profile74[0]+",FL"]
bracketPramM1.RevSf1=False
bracketPramM1.Surfaces2=[profile73[0]+",FL"]
bracketPramM1.RevSf2=False
bracketPramM1.RevSf3=False
bracketPramM1.Sf1DimensionType=1531
bracketPramM1.Sf1DimensonParams=["200","15"]
bracketPramM1.Sf2DimensionType=1531
bracketPramM1.Sf2DimensonParams=["200","15"]
bracketM1 = part.CreateBracket(bracketPramM1,False)
part.SetElementColor(bracketM1,"0","255","255","0.19999998807907104")
ProfilePram75 = part.CreateProfileParam()
ProfilePram75.DefinitionType=1
ProfilePram75.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram75.AddAttachSurfaces(extrude_sheet3)
ProfilePram75.ProfileName="HK.Casing.Wall.Aft.DL01.CDP"
ProfilePram75.MaterialName="SS400"
ProfilePram75.ProfileType=1002
ProfilePram75.ProfileParams=["125","75","7","10","5"]
ProfilePram75.Mold="+"
ProfilePram75.ReverseDir=False
ProfilePram75.ReverseAngle=True
ProfilePram75.CalcSnipOnlyAttachLines=False
ProfilePram75.AttachDirMethod=0
ProfilePram75.CCWDefAngle=False
ProfilePram75.AddEnd1Elements(profile23[0])
ProfilePram75.End1Type=1102
ProfilePram75.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram75.AddEnd2Elements(extrude_sheet4)
ProfilePram75.End2Type=1102
ProfilePram75.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram75.End1ScallopType=1120
ProfilePram75.End1ScallopTypeParams=["50"]
ProfilePram75.End2ScallopType=1120
ProfilePram75.End2ScallopTypeParams=["50"]
profile75 = part.CreateProfile(ProfilePram75,False)
part.SetElementColor(profile75[0],"255","0","0","0.19999998807907104")
ProfilePram76 = part.CreateProfileParam()
ProfilePram76.DefinitionType=1
ProfilePram76.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram76.AddAttachSurfaces(extrude_sheet6)
ProfilePram76.ProfileName="HK.Casing.Wall.Side.FR14.ABP"
ProfilePram76.MaterialName="SS400"
ProfilePram76.ProfileType=1002
ProfilePram76.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram76.Mold="+"
ProfilePram76.ReverseDir=False
ProfilePram76.ReverseAngle=True
ProfilePram76.CalcSnipOnlyAttachLines=False
ProfilePram76.AttachDirMethod=0
ProfilePram76.CCWDefAngle=False
ProfilePram76.AddEnd1Elements(extrude_sheet1)
ProfilePram76.End1Type=1102
ProfilePram76.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram76.AddEnd2Elements(extrude_sheet2)
ProfilePram76.End2Type=1102
ProfilePram76.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram76.End1ScallopType=1121
ProfilePram76.End1ScallopTypeParams=["35","40"]
ProfilePram76.End2ScallopType=1121
ProfilePram76.End2ScallopTypeParams=["35","40"]
profile76 = part.CreateProfile(ProfilePram76,False)
part.SetElementColor(profile76[0],"255","0","0","0.19999998807907104")
ProfilePram77 = part.CreateProfileParam()
ProfilePram77.DefinitionType=1
ProfilePram77.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram77.AddAttachSurfaces(extrude_sheet6)
ProfilePram77.ProfileName="HK.Casing.Wall.Side.FR13.ABP"
ProfilePram77.MaterialName="SS400"
ProfilePram77.ProfileType=1003
ProfilePram77.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram77.Mold="+"
ProfilePram77.ReverseDir=False
ProfilePram77.ReverseAngle=True
ProfilePram77.CalcSnipOnlyAttachLines=False
ProfilePram77.AttachDirMethod=0
ProfilePram77.CCWDefAngle=False
ProfilePram77.AddEnd1Elements(extrude_sheet1)
ProfilePram77.End1Type=1103
ProfilePram77.End1TypeParams=["0"]
ProfilePram77.AddEnd2Elements(extrude_sheet2)
ProfilePram77.End2Type=1103
ProfilePram77.End2TypeParams=["0"]
ProfilePram77.End1ScallopType=1120
ProfilePram77.End1ScallopTypeParams=["50"]
ProfilePram77.End2ScallopType=1120
ProfilePram77.End2ScallopTypeParams=["50"]
profile77 = part.CreateProfile(ProfilePram77,False)
part.SetElementColor(profile77[0],"148","0","211","0.39999997615814209")
ProfilePram78 = part.CreateProfileParam()
ProfilePram78.DefinitionType=1
ProfilePram78.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram78.AddAttachSurfaces(extrude_sheet1)
ProfilePram78.ProfileName="HK.Casing.Deck.B.FR13P"
ProfilePram78.MaterialName="SS400"
ProfilePram78.ProfileType=1003
ProfilePram78.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram78.Mold="+"
ProfilePram78.ReverseDir=True
ProfilePram78.ReverseAngle=False
ProfilePram78.CalcSnipOnlyAttachLines=False
ProfilePram78.AttachDirMethod=0
ProfilePram78.CCWDefAngle=False
ProfilePram78.AddEnd1Elements(profile30[0])
ProfilePram78.End1Type=1113
ProfilePram78.End1TypeParams=["0","79"]
ProfilePram78.AddEnd2Elements(profile77[0])
ProfilePram78.End2Type=1102
ProfilePram78.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram78.End1ScallopType=1120
ProfilePram78.End1ScallopTypeParams=["50"]
ProfilePram78.End2ScallopType=1120
ProfilePram78.End2ScallopTypeParams=["50"]
profile78 = part.CreateProfile(ProfilePram78,False)
part.SetElementColor(profile78[0],"148","0","211","0.39999997615814209")
ProfilePram79 = part.CreateProfileParam()
ProfilePram79.DefinitionType=1
ProfilePram79.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram79.AddAttachSurfaces(extrude_sheet6)
ProfilePram79.ProfileName="HK.Casing.Wall.Side.FR12.BCP"
ProfilePram79.MaterialName="SS400"
ProfilePram79.ProfileType=1002
ProfilePram79.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram79.Mold="+"
ProfilePram79.ReverseDir=False
ProfilePram79.ReverseAngle=True
ProfilePram79.CalcSnipOnlyAttachLines=False
ProfilePram79.AttachDirMethod=0
ProfilePram79.CCWDefAngle=False
ProfilePram79.AddEnd1Elements(extrude_sheet4)
ProfilePram79.End1Type=1102
ProfilePram79.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram79.AddEnd2Elements(extrude_sheet1)
ProfilePram79.End2Type=1102
ProfilePram79.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram79.End1ScallopType=1121
ProfilePram79.End1ScallopTypeParams=["35","40"]
ProfilePram79.End2ScallopType=1121
ProfilePram79.End2ScallopTypeParams=["35","40"]
profile79 = part.CreateProfile(ProfilePram79,False)
part.SetElementColor(profile79[0],"255","0","0","0.19999998807907104")
ProfilePram80 = part.CreateProfileParam()
ProfilePram80.DefinitionType=1
ProfilePram80.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram80.AddAttachSurfaces(extrude_sheet3)
ProfilePram80.ProfileName="HK.Casing.Wall.Aft.DL00.BC"
ProfilePram80.MaterialName="SS400"
ProfilePram80.ProfileType=1002
ProfilePram80.ProfileParams=["125","75","7","10","5"]
ProfilePram80.ReverseDir=False
ProfilePram80.ReverseAngle=True
ProfilePram80.CalcSnipOnlyAttachLines=False
ProfilePram80.AttachDirMethod=0
ProfilePram80.CCWDefAngle=False
ProfilePram80.AddEnd1Elements(extrude_sheet4)
ProfilePram80.End1Type=1102
ProfilePram80.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram80.AddEnd2Elements(extrude_sheet1)
ProfilePram80.End2Type=1102
ProfilePram80.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram80.End1ScallopType=1121
ProfilePram80.End1ScallopTypeParams=["25","40"]
ProfilePram80.End2ScallopType=1121
ProfilePram80.End2ScallopTypeParams=["25","40"]
profile80 = part.CreateProfile(ProfilePram80,False)
part.SetElementColor(profile80[0],"255","0","0","0.19999998807907104")
ProfilePram81 = part.CreateProfileParam()
ProfilePram81.DefinitionType=1
ProfilePram81.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram81.AddAttachSurfaces(extrude_sheet4)
ProfilePram81.ProfileName="HK.Casing.Deck.C.FR06F400"
ProfilePram81.MaterialName="SS400"
ProfilePram81.ProfileType=1007
ProfilePram81.ProfileParams=["150","12"]
ProfilePram81.Mold="+"
ProfilePram81.ReverseDir=True
ProfilePram81.ReverseAngle=False
ProfilePram81.CalcSnipOnlyAttachLines=False
ProfilePram81.AttachDirMethod=0
ProfilePram81.CCWDefAngle=False
ProfilePram81.AddEnd1Elements(mirror_copied6[0])
ProfilePram81.End1Type=1102
ProfilePram81.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram81.AddEnd2Elements(profile15[0])
ProfilePram81.End2Type=1102
ProfilePram81.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram81.End1ScallopType=-1
ProfilePram81.End2ScallopType=-1
profile81 = part.CreateProfile(ProfilePram81,False)
part.SetElementColor(profile81[0],"255","0","0","0.19999998807907104")
ProfilePram82 = part.CreateProfileParam()
ProfilePram82.DefinitionType=1
ProfilePram82.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram82.AddAttachSurfaces(extrude_sheet6)
ProfilePram82.ProfileName="HK.Casing.Wall.Side.FR10.ABP"
ProfilePram82.MaterialName="SS400"
ProfilePram82.ProfileType=1002
ProfilePram82.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram82.Mold="+"
ProfilePram82.ReverseDir=False
ProfilePram82.ReverseAngle=True
ProfilePram82.CalcSnipOnlyAttachLines=False
ProfilePram82.AttachDirMethod=0
ProfilePram82.CCWDefAngle=False
ProfilePram82.AddEnd1Elements(extrude_sheet1)
ProfilePram82.End1Type=1102
ProfilePram82.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram82.AddEnd2Elements(extrude_sheet2)
ProfilePram82.End2Type=1102
ProfilePram82.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram82.End1ScallopType=1121
ProfilePram82.End1ScallopTypeParams=["35","40"]
ProfilePram82.End2ScallopType=1121
ProfilePram82.End2ScallopTypeParams=["35","40"]
profile82 = part.CreateProfile(ProfilePram82,False)
part.SetElementColor(profile82[0],"255","0","0","0.19999998807907104")
ProfilePram83 = part.CreateProfileParam()
ProfilePram83.DefinitionType=1
ProfilePram83.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram83.AddAttachSurfaces(extrude_sheet3)
ProfilePram83.ProfileName="HK.Casing.Wall.Aft.DL01.OAP"
ProfilePram83.MaterialName="SS400"
ProfilePram83.ProfileType=1002
ProfilePram83.ProfileParams=["125","75","7","10","5"]
ProfilePram83.Mold="+"
ProfilePram83.ReverseDir=False
ProfilePram83.ReverseAngle=True
ProfilePram83.CalcSnipOnlyAttachLines=False
ProfilePram83.AttachDirMethod=0
ProfilePram83.CCWDefAngle=False
ProfilePram83.AddEnd1Elements(extrude_sheet2)
ProfilePram83.End1Type=1102
ProfilePram83.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram83.AddEnd2Elements(extrude_sheet7)
ProfilePram83.End2Type=1102
ProfilePram83.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram83.End1ScallopType=1121
ProfilePram83.End1ScallopTypeParams=["25","40"]
ProfilePram83.End2ScallopType=1121
ProfilePram83.End2ScallopTypeParams=["25","40"]
profile83 = part.CreateProfile(ProfilePram83,False)
part.SetElementColor(profile83[0],"255","0","0","0.19999998807907104")
ProfilePram84 = part.CreateProfileParam()
ProfilePram84.DefinitionType=1
ProfilePram84.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram84.AddAttachSurfaces(extrude_sheet8)
ProfilePram84.ProfileName="HK.Casing.Wall.Fore.DL00.AB"
ProfilePram84.MaterialName="SS400"
ProfilePram84.ProfileType=1002
ProfilePram84.ProfileParams=["125","75","7","10","5"]
ProfilePram84.ReverseDir=True
ProfilePram84.ReverseAngle=True
ProfilePram84.CalcSnipOnlyAttachLines=False
ProfilePram84.AttachDirMethod=0
ProfilePram84.CCWDefAngle=False
ProfilePram84.AddEnd1Elements(extrude_sheet1)
ProfilePram84.End1Type=1102
ProfilePram84.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram84.AddEnd2Elements(extrude_sheet2)
ProfilePram84.End2Type=1102
ProfilePram84.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram84.End1ScallopType=1121
ProfilePram84.End1ScallopTypeParams=["25","40"]
ProfilePram84.End2ScallopType=1121
ProfilePram84.End2ScallopTypeParams=["25","40"]
profile84 = part.CreateProfile(ProfilePram84,False)
part.SetElementColor(profile84[0],"255","0","0","0.19999998807907104")
ProfilePram85 = part.CreateProfileParam()
ProfilePram85.DefinitionType=1
ProfilePram85.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram85.AddAttachSurfaces(extrude_sheet1)
ProfilePram85.ProfileName="HK.Casing.Deck.B.DL00.F"
ProfilePram85.MaterialName="SS400"
ProfilePram85.ProfileType=1002
ProfilePram85.ProfileParams=["125","75","7","10","5"]
ProfilePram85.ReverseDir=True
ProfilePram85.ReverseAngle=True
ProfilePram85.CalcSnipOnlyAttachLines=False
ProfilePram85.AttachDirMethod=0
ProfilePram85.CCWDefAngle=False
ProfilePram85.AddEnd1Elements(profile70[0])
ProfilePram85.End1Type=1102
ProfilePram85.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram85.AddEnd2Elements(profile84[0])
ProfilePram85.End2Type=1102
ProfilePram85.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram85.End1ScallopType=1121
ProfilePram85.End1ScallopTypeParams=["25","40"]
ProfilePram85.End2ScallopType=1121
ProfilePram85.End2ScallopTypeParams=["25","40"]
profile85 = part.CreateProfile(ProfilePram85,False)
part.SetElementColor(profile85[0],"255","0","0","0.19999998807907104")
ProfilePram86 = part.CreateProfileParam()
ProfilePram86.DefinitionType=1
ProfilePram86.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram86.AddAttachSurfaces(extrude_sheet5)
ProfilePram86.ProfileName="HK.Casing.Deck.D.DL04P"
ProfilePram86.MaterialName="SS400"
ProfilePram86.ProfileType=1002
ProfilePram86.ProfileParams=["125","75","7","10","5"]
ProfilePram86.Mold="+"
ProfilePram86.ReverseDir=True
ProfilePram86.ReverseAngle=True
ProfilePram86.CalcSnipOnlyAttachLines=False
ProfilePram86.AttachDirMethod=0
ProfilePram86.CCWDefAngle=False
ProfilePram86.AddEnd1Elements(extrude_sheet3)
ProfilePram86.End1Type=1102
ProfilePram86.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram86.AddEnd2Elements(extrude_sheet8)
ProfilePram86.End2Type=1102
ProfilePram86.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram86.End1ScallopType=1120
ProfilePram86.End1ScallopTypeParams=["50"]
ProfilePram86.End2ScallopType=1120
ProfilePram86.End2ScallopTypeParams=["50"]
profile86 = part.CreateProfile(ProfilePram86,False)
part.SetElementColor(profile86[0],"255","0","0","0.19999998807907104")
ProfilePram87 = part.CreateProfileParam()
ProfilePram87.DefinitionType=1
ProfilePram87.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram87.AddAttachSurfaces(extrude_sheet3)
ProfilePram87.ProfileName="HK.Casing.Wall.Aft.DL04.CDP"
ProfilePram87.MaterialName="SS400"
ProfilePram87.ProfileType=1002
ProfilePram87.ProfileParams=["125","75","7","10","5"]
ProfilePram87.Mold="+"
ProfilePram87.ReverseDir=False
ProfilePram87.ReverseAngle=True
ProfilePram87.CalcSnipOnlyAttachLines=False
ProfilePram87.AttachDirMethod=0
ProfilePram87.CCWDefAngle=False
ProfilePram87.AddEnd1Elements(profile86[0])
ProfilePram87.End1Type=1102
ProfilePram87.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram87.AddEnd2Elements(extrude_sheet4)
ProfilePram87.End2Type=1102
ProfilePram87.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram87.End1ScallopType=1120
ProfilePram87.End1ScallopTypeParams=["50"]
ProfilePram87.End2ScallopType=1120
ProfilePram87.End2ScallopTypeParams=["50"]
profile87 = part.CreateProfile(ProfilePram87,False)
part.SetElementColor(profile87[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: DL04 Aft と Deck D DL04
bracketPramN1 = part.CreateBracketParam()
bracketPramN1.DefinitionType=1
bracketPramN1.BracketName="HK.Casing.DL04.AftDeckD.BKT"
bracketPramN1.MaterialName="SS400"
bracketPramN1.BaseElement=profile87[0]
bracketPramN1.UseSideSheetForPlane=False
bracketPramN1.Mold="+"
bracketPramN1.Thickness="8"
bracketPramN1.BracketType=1501
bracketPramN1.Scallop1Type=1801
bracketPramN1.Scallop1Params=["0"]
bracketPramN1.Scallop2Type=0
bracketPramN1.Surfaces1=[profile87[0]+",FL"]
bracketPramN1.RevSf1=False
bracketPramN1.Surfaces2=[profile86[0]+",FL"]
bracketPramN1.RevSf2=False
bracketPramN1.RevSf3=False
bracketPramN1.Sf1DimensionType=1531
bracketPramN1.Sf1DimensonParams=["200","15"]
bracketPramN1.Sf2DimensionType=1531
bracketPramN1.Sf2DimensonParams=["200","15"]
bracketN1 = part.CreateBracket(bracketPramN1,False)
part.SetElementColor(bracketN1,"0","255","255","0.19999998807907104")
solid6 = part.CreateSolid("HK.Casing.Wall.Fore.AB","","SS400")
part.SetElementColor(solid6,"139","69","19","0.79999995231628418")
thicken6 = part.CreateThicken("厚み付け17",solid6,"+",[extrude_sheet8],"+","10","0","0",False,False)
solid7 = part.CreateSolid("HK.Casing.Wall.Fore.OA","","SS400")
part.SetElementColor(solid7,"139","69","19","0.79999995231628418")
thicken7 = part.CreateThicken("厚み付け18",solid7,"+",[extrude_sheet8],"+","10","0","0",False,False)
extrudePram19 = part.CreateLinearSweepParam()
extrudePram19.Name="積-押し出し47"
extrudePram19.AddProfile(extrude_sheet6)
extrudePram19.DirectionType="R"
extrudePram19.DirectionParameter1="50000"
extrudePram19.SweepDirection="+Y"
extrudePram19.RefByGeometricMethod=True
extrude10 = part.CreateLinearSweep(solid7,"*",extrudePram19,False)
extrudePram20 = part.CreateLinearSweepParam()
extrudePram20.Name="積-押し出し48"
extrudePram20.AddProfile(extrude_sheet9)
extrudePram20.DirectionType="N"
extrudePram20.DirectionParameter1="50000"
extrudePram20.SweepDirection="+Y"
extrudePram20.RefByGeometricMethod=True
extrude11 = part.CreateLinearSweep(solid7,"*",extrudePram20,False)
extrudePram21 = part.CreateLinearSweepParam()
extrudePram21.Name="積-押し出し49"
extrudePram21.AddProfile(extrude_sheet2)
extrudePram21.DirectionType="R"
extrudePram21.DirectionParameter1="50000"
extrudePram21.SweepDirection="+Z"
extrudePram21.RefByGeometricMethod=True
extrude12 = part.CreateLinearSweep(solid7,"*",extrudePram21,False)
extrudePram22 = part.CreateLinearSweepParam()
extrudePram22.Name="積-押し出し50"
extrudePram22.AddProfile(extrude_sheet7)
extrudePram22.DirectionType="N"
extrudePram22.DirectionParameter1="50000"
extrudePram22.SweepDirection="+Z"
extrudePram22.RefByGeometricMethod=True
extrude13 = part.CreateLinearSweep(solid7,"*",extrudePram22,False)
ProfilePram88 = part.CreateProfileParam()
ProfilePram88.DefinitionType=1
ProfilePram88.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram88.AddAttachSurfaces(extrude_sheet8)
ProfilePram88.ProfileName="HK.Casing.Wall.Fore.DL02.ABP"
ProfilePram88.MaterialName="SS400"
ProfilePram88.FlangeName="HK.Casing.Wall.Fore.DL02.ABP"
ProfilePram88.FlangeMaterialName="SS400"
ProfilePram88.ProfileType=1201
ProfilePram88.ProfileParams=["150","12","388","10"]
ProfilePram88.Mold="-"
ProfilePram88.ReverseDir=True
ProfilePram88.ReverseAngle=False
ProfilePram88.CalcSnipOnlyAttachLines=False
ProfilePram88.AttachDirMethod=0
ProfilePram88.CCWDefAngle=False
ProfilePram88.AddEnd1Elements(extrude_sheet1)
ProfilePram88.End1Type=1102
ProfilePram88.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram88.AddEnd2Elements(extrude_sheet2)
ProfilePram88.End2Type=1102
ProfilePram88.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram88.End1ScallopType=1120
ProfilePram88.End1ScallopTypeParams=["50"]
ProfilePram88.End2ScallopType=1120
ProfilePram88.End2ScallopTypeParams=["50"]
profile88 = part.CreateProfile(ProfilePram88,False)
part.SetElementColor(profile88[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile88[1],"148","0","211","0.39999997615814209")
ProfilePram89 = part.CreateProfileParam()
ProfilePram89.DefinitionType=1
ProfilePram89.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram89.AddAttachSurfaces(extrude_sheet6)
ProfilePram89.ProfileName="HK.Casing.Wall.Side.FR15.BCP"
ProfilePram89.MaterialName="SS400"
ProfilePram89.ProfileType=1002
ProfilePram89.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram89.Mold="+"
ProfilePram89.ReverseDir=False
ProfilePram89.ReverseAngle=True
ProfilePram89.CalcSnipOnlyAttachLines=False
ProfilePram89.AttachDirMethod=0
ProfilePram89.CCWDefAngle=False
ProfilePram89.AddEnd1Elements(extrude_sheet4)
ProfilePram89.End1Type=1102
ProfilePram89.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram89.AddEnd2Elements(extrude_sheet1)
ProfilePram89.End2Type=1102
ProfilePram89.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram89.End1ScallopType=1121
ProfilePram89.End1ScallopTypeParams=["35","40"]
ProfilePram89.End2ScallopType=1121
ProfilePram89.End2ScallopTypeParams=["35","40"]
profile89 = part.CreateProfile(ProfilePram89,False)
part.SetElementColor(profile89[0],"255","0","0","0.19999998807907104")
extrudePram23 = part.CreateLinearSweepParam()
extrudePram23.Name="積-押し出し20"
extrudePram23.AddProfile(extrude_sheet9)
extrudePram23.DirectionType="N"
extrudePram23.DirectionParameter1="50000"
extrudePram23.SweepDirection="+Y"
extrudePram23.RefByGeometricMethod=True
extrude14 = part.CreateLinearSweep(solid5,"*",extrudePram23,False)
extrudePram24 = part.CreateLinearSweepParam()
extrudePram24.Name="積-押し出し21"
extrudePram24.AddProfile(extrude_sheet5)
extrudePram24.DirectionType="R"
extrudePram24.DirectionParameter1="50000"
extrudePram24.SweepDirection="+Z"
extrudePram24.RefByGeometricMethod=True
extrude15 = part.CreateLinearSweep(solid5,"*",extrudePram24,False)
mirror_copied17 = part.MirrorCopy([profile12[0]],"PL,Y","")
part.SetElementColor(mirror_copied17[0],"255","0","0","0.19999998807907104")
solid8 = part.CreateSolid("HK.Casing.Wall.Side.OAP","","SS400")
part.SetElementColor(solid8,"139","69","19","0.79999995231628418")
thicken8 = part.CreateThicken("厚み付け10",solid8,"+",[extrude_sheet6],"-","10","0","0",False,False)
extrudePram25 = part.CreateLinearSweepParam()
extrudePram25.Name="積-押し出し16"
extrudePram25.AddProfile(skt_pl4+",Edge00")
extrudePram25.DirectionType="N"
extrudePram25.DirectionParameter1="50000"
extrudePram25.SweepDirection="+Z"
extrudePram25.RefByGeometricMethod=True
extrude16 = part.CreateLinearSweep(solid8,"*",extrudePram25,False)
extrudePram26 = part.CreateLinearSweepParam()
extrudePram26.Name="積-押し出し17"
extrudePram26.AddProfile(extrude_sheet2)
extrudePram26.DirectionType="R"
extrudePram26.DirectionParameter1="50000"
extrudePram26.SweepDirection="+Z"
extrudePram26.RefByGeometricMethod=True
extrude17 = part.CreateLinearSweep(solid8,"*",extrudePram26,False)
extrudePram27 = part.CreateLinearSweepParam()
extrudePram27.Name="積-押し出し18"
extrudePram27.AddProfile(extrude_sheet7)
extrudePram27.DirectionType="N"
extrudePram27.DirectionParameter1="50000"
extrudePram27.SweepDirection="+Z"
extrudePram27.RefByGeometricMethod=True
extrude18 = part.CreateLinearSweep(solid8,"*",extrudePram27,False)
mirror_copied18 = part.MirrorCopy([solid8],"PL,Y","")
part.SetElementColor(mirror_copied18[0],"139","69","19","0.79999995231628418")
ProfilePram90 = part.CreateProfileParam()
ProfilePram90.DefinitionType=1
ProfilePram90.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram90.AddAttachSurfaces(extrude_sheet2)
ProfilePram90.ProfileName="HK.Casing.Deck.A.FR09P"
ProfilePram90.MaterialName="SS400"
ProfilePram90.ProfileType=1003
ProfilePram90.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram90.Mold="+"
ProfilePram90.ReverseDir=True
ProfilePram90.ReverseAngle=False
ProfilePram90.CalcSnipOnlyAttachLines=False
ProfilePram90.AttachDirMethod=0
ProfilePram90.CCWDefAngle=False
ProfilePram90.AddEnd1Elements(profile40[0])
ProfilePram90.End1Type=1113
ProfilePram90.End1TypeParams=["0","79"]
ProfilePram90.AddEnd2Elements(profile57[0])
ProfilePram90.End2Type=1102
ProfilePram90.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram90.End1ScallopType=1120
ProfilePram90.End1ScallopTypeParams=["50"]
ProfilePram90.End2ScallopType=1120
ProfilePram90.End2ScallopTypeParams=["50"]
profile90 = part.CreateProfile(ProfilePram90,False)
part.SetElementColor(profile90[0],"148","0","211","0.39999997615814209")
ProfilePram91 = part.CreateProfileParam()
ProfilePram91.DefinitionType=1
ProfilePram91.BasePlane="PL,O,"+var_elm8+","+"X"
ProfilePram91.AddAttachSurfaces(extrude_sheet6)
ProfilePram91.ProfileName="HK.Casing.Wall.Side.FR07.ABP"
ProfilePram91.MaterialName="SS400"
ProfilePram91.ProfileType=1002
ProfilePram91.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram91.Mold="+"
ProfilePram91.ReverseDir=False
ProfilePram91.ReverseAngle=True
ProfilePram91.CalcSnipOnlyAttachLines=False
ProfilePram91.AttachDirMethod=0
ProfilePram91.CCWDefAngle=False
ProfilePram91.AddEnd1Elements(extrude_sheet1)
ProfilePram91.End1Type=1102
ProfilePram91.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram91.AddEnd2Elements(extrude_sheet2)
ProfilePram91.End2Type=1102
ProfilePram91.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram91.End1ScallopType=1121
ProfilePram91.End1ScallopTypeParams=["35","40"]
ProfilePram91.End2ScallopType=1121
ProfilePram91.End2ScallopTypeParams=["35","40"]
profile91 = part.CreateProfile(ProfilePram91,False)
part.SetElementColor(profile91[0],"255","0","0","0.19999998807907104")
mirror_copied19 = part.MirrorCopy([profile68[0]],"PL,Y","")
part.SetElementColor(mirror_copied19[0],"255","0","0","0.19999998807907104")
ProfilePram92 = part.CreateProfileParam()
ProfilePram92.DefinitionType=1
ProfilePram92.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram92.AddAttachSurfaces(extrude_sheet6)
ProfilePram92.ProfileName="HK.Casing.Wall.Side.FR10.BCP"
ProfilePram92.MaterialName="SS400"
ProfilePram92.ProfileType=1002
ProfilePram92.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram92.Mold="+"
ProfilePram92.ReverseDir=False
ProfilePram92.ReverseAngle=True
ProfilePram92.CalcSnipOnlyAttachLines=False
ProfilePram92.AttachDirMethod=0
ProfilePram92.CCWDefAngle=False
ProfilePram92.AddEnd1Elements(extrude_sheet4)
ProfilePram92.End1Type=1102
ProfilePram92.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram92.AddEnd2Elements(extrude_sheet1)
ProfilePram92.End2Type=1102
ProfilePram92.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram92.End1ScallopType=1121
ProfilePram92.End1ScallopTypeParams=["35","40"]
ProfilePram92.End2ScallopType=1121
ProfilePram92.End2ScallopTypeParams=["35","40"]
profile92 = part.CreateProfile(ProfilePram92,False)
part.SetElementColor(profile92[0],"255","0","0","0.19999998807907104")
ProfilePram93 = part.CreateProfileParam()
ProfilePram93.DefinitionType=1
ProfilePram93.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram93.AddAttachSurfaces(extrude_sheet5)
ProfilePram93.ProfileName="HK.Casing.Deck.D.DL00.F"
ProfilePram93.MaterialName="SS400"
ProfilePram93.ProfileType=1002
ProfilePram93.ProfileParams=["125","75","7","10","5"]
ProfilePram93.ReverseDir=True
ProfilePram93.ReverseAngle=True
ProfilePram93.CalcSnipOnlyAttachLines=False
ProfilePram93.AttachDirMethod=0
ProfilePram93.CCWDefAngle=False
ProfilePram93.AddEnd1Elements(profile60[0])
ProfilePram93.End1Type=1102
ProfilePram93.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram93.AddEnd2Elements(extrude_sheet8)
ProfilePram93.End2Type=1102
ProfilePram93.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram93.End1ScallopType=1121
ProfilePram93.End1ScallopTypeParams=["25","40"]
ProfilePram93.End2ScallopType=1121
ProfilePram93.End2ScallopTypeParams=["25","40"]
profile93 = part.CreateProfile(ProfilePram93,False)
part.SetElementColor(profile93[0],"255","0","0","0.19999998807907104")
ProfilePram94 = part.CreateProfileParam()
ProfilePram94.DefinitionType=1
ProfilePram94.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram94.AddAttachSurfaces(extrude_sheet8)
ProfilePram94.ProfileName="HK.Casing.Wall.Fore.DL00.CD"
ProfilePram94.MaterialName="SS400"
ProfilePram94.ProfileType=1002
ProfilePram94.ProfileParams=["125","75","7","10","5"]
ProfilePram94.ReverseDir=True
ProfilePram94.ReverseAngle=True
ProfilePram94.CalcSnipOnlyAttachLines=False
ProfilePram94.AttachDirMethod=0
ProfilePram94.CCWDefAngle=False
ProfilePram94.AddEnd1Elements(profile93[0])
ProfilePram94.End1Type=1102
ProfilePram94.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram94.AddEnd2Elements(extrude_sheet4)
ProfilePram94.End2Type=1102
ProfilePram94.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram94.End1ScallopType=1120
ProfilePram94.End1ScallopTypeParams=["50"]
ProfilePram94.End2ScallopType=1120
ProfilePram94.End2ScallopTypeParams=["50"]
profile94 = part.CreateProfile(ProfilePram94,False)
part.SetElementColor(profile94[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: DL00 Fore と Deck D DL00
bracketPramO1 = part.CreateBracketParam()
bracketPramO1.DefinitionType=1
bracketPramO1.BracketName="HK.Casing.DL00.ForeDeckD.BKT"
bracketPramO1.MaterialName="SS400"
bracketPramO1.BaseElement=profile94[0]
bracketPramO1.UseSideSheetForPlane=False
bracketPramO1.Mold="+"
bracketPramO1.Thickness="8"
bracketPramO1.BracketType=1501
bracketPramO1.Scallop1Type=1801
bracketPramO1.Scallop1Params=["0"]
bracketPramO1.Scallop2Type=0
bracketPramO1.Surfaces1=[profile94[0]+",FL"]
bracketPramO1.RevSf1=False
bracketPramO1.Surfaces2=[profile93[0]+",FL"]
bracketPramO1.RevSf2=False
bracketPramO1.RevSf3=False
bracketPramO1.Sf1DimensionType=1531
bracketPramO1.Sf1DimensonParams=["200","15"]
bracketPramO1.Sf2DimensionType=1531
bracketPramO1.Sf2DimensonParams=["200","15"]
bracketO1 = part.CreateBracket(bracketPramO1,False)
part.SetElementColor(bracketO1,"0","255","255","0.19999998807907104")
mirror_copied20 = part.MirrorCopy([profile83[0]],"PL,Y","")
part.SetElementColor(mirror_copied20[0],"255","0","0","0.19999998807907104")
mirror_copied21 = part.MirrorCopy([profile87[0]],"PL,Y","")
part.SetElementColor(mirror_copied21[0],"255","0","0","0.19999998807907104")
ProfilePram95 = part.CreateProfileParam()
ProfilePram95.DefinitionType=1
ProfilePram95.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram95.AddAttachSurfaces(extrude_sheet6)
ProfilePram95.ProfileName="HK.Casing.Wall.Side.FR09.BCP"
ProfilePram95.MaterialName="SS400"
ProfilePram95.ProfileType=1003
ProfilePram95.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram95.Mold="+"
ProfilePram95.ReverseDir=False
ProfilePram95.ReverseAngle=True
ProfilePram95.CalcSnipOnlyAttachLines=False
ProfilePram95.AttachDirMethod=0
ProfilePram95.CCWDefAngle=False
ProfilePram95.AddEnd1Elements(extrude_sheet4)
ProfilePram95.End1Type=1103
ProfilePram95.End1TypeParams=["0"]
ProfilePram95.AddEnd2Elements(extrude_sheet1)
ProfilePram95.End2Type=1103
ProfilePram95.End2TypeParams=["0"]
ProfilePram95.End1ScallopType=1120
ProfilePram95.End1ScallopTypeParams=["50"]
ProfilePram95.End2ScallopType=1120
ProfilePram95.End2ScallopTypeParams=["50"]
profile95 = part.CreateProfile(ProfilePram95,False)
part.SetElementColor(profile95[0],"148","0","211","0.39999997615814209")
ProfilePram96 = part.CreateProfileParam()
ProfilePram96.DefinitionType=1
ProfilePram96.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram96.AddAttachSurfaces(extrude_sheet4)
ProfilePram96.ProfileName="HK.Casing.Deck.C.FR09P"
ProfilePram96.MaterialName="SS400"
ProfilePram96.ProfileType=1003
ProfilePram96.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram96.Mold="+"
ProfilePram96.ReverseDir=True
ProfilePram96.ReverseAngle=False
ProfilePram96.CalcSnipOnlyAttachLines=False
ProfilePram96.AttachDirMethod=0
ProfilePram96.CCWDefAngle=False
ProfilePram96.AddEnd1Elements(profile15[0])
ProfilePram96.End1Type=1113
ProfilePram96.End1TypeParams=["0","79"]
ProfilePram96.AddEnd2Elements(profile95[0])
ProfilePram96.End2Type=1102
ProfilePram96.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram96.End1ScallopType=1120
ProfilePram96.End1ScallopTypeParams=["50"]
ProfilePram96.End2ScallopType=1120
ProfilePram96.End2ScallopTypeParams=["50"]
profile96 = part.CreateProfile(ProfilePram96,False)
part.SetElementColor(profile96[0],"148","0","211","0.39999997615814209")
solid9 = part.CreateSolid("HK.Casing.Wall.Aft.OA","","SS400")
part.SetElementColor(solid9,"139","69","19","0.79999995231628418")
thicken9 = part.CreateThicken("厚み付け14",solid9,"+",[extrude_sheet3],"-","10","0","0",False,False)
extrudePram28 = part.CreateLinearSweepParam()
extrudePram28.Name="積-押し出し31"
extrudePram28.AddProfile(extrude_sheet6)
extrudePram28.DirectionType="R"
extrudePram28.DirectionParameter1="50000"
extrudePram28.SweepDirection="+Y"
extrudePram28.RefByGeometricMethod=True
extrude19 = part.CreateLinearSweep(solid9,"*",extrudePram28,False)
extrudePram29 = part.CreateLinearSweepParam()
extrudePram29.Name="積-押し出し32"
extrudePram29.AddProfile(extrude_sheet9)
extrudePram29.DirectionType="N"
extrudePram29.DirectionParameter1="50000"
extrudePram29.SweepDirection="+Y"
extrudePram29.RefByGeometricMethod=True
extrude20 = part.CreateLinearSweep(solid9,"*",extrudePram29,False)
extrudePram30 = part.CreateLinearSweepParam()
extrudePram30.Name="積-押し出し33"
extrudePram30.AddProfile(extrude_sheet2)
extrudePram30.DirectionType="R"
extrudePram30.DirectionParameter1="50000"
extrudePram30.SweepDirection="+Z"
extrudePram30.RefByGeometricMethod=True
extrude21 = part.CreateLinearSweep(solid9,"*",extrudePram30,False)
extrudePram31 = part.CreateLinearSweepParam()
extrudePram31.Name="積-押し出し34"
extrudePram31.AddProfile(extrude_sheet7)
extrudePram31.DirectionType="N"
extrudePram31.DirectionParameter1="50000"
extrudePram31.SweepDirection="+Z"
extrudePram31.RefByGeometricMethod=True
extrude22 = part.CreateLinearSweep(solid9,"*",extrudePram31,False)
mirror_copied22 = part.MirrorCopy([profile95[0]],"PL,Y","")
part.SetElementColor(mirror_copied22[0],"148","0","211","0.39999997615814209")
mirror_copied23 = part.MirrorCopy([profile78[0]],"PL,Y","")
part.SetElementColor(mirror_copied23[0],"148","0","211","0.39999997615814209")
ProfilePram97 = part.CreateProfileParam()
ProfilePram97.DefinitionType=1
ProfilePram97.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram97.AddAttachSurfaces(extrude_sheet8)
ProfilePram97.ProfileName="HK.Casing.Wall.Fore.DL02.BCP"
ProfilePram97.MaterialName="SS400"
ProfilePram97.FlangeName="HK.Casing.Wall.Fore.DL02.BCP"
ProfilePram97.FlangeMaterialName="SS400"
ProfilePram97.ProfileType=1201
ProfilePram97.ProfileParams=["150","12","388","10"]
ProfilePram97.Mold="-"
ProfilePram97.ReverseDir=True
ProfilePram97.ReverseAngle=False
ProfilePram97.CalcSnipOnlyAttachLines=False
ProfilePram97.AttachDirMethod=0
ProfilePram97.CCWDefAngle=False
ProfilePram97.AddEnd1Elements(extrude_sheet4)
ProfilePram97.End1Type=1102
ProfilePram97.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram97.AddEnd2Elements(extrude_sheet1)
ProfilePram97.End2Type=1102
ProfilePram97.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram97.End1ScallopType=1120
ProfilePram97.End1ScallopTypeParams=["50"]
ProfilePram97.End2ScallopType=1120
ProfilePram97.End2ScallopTypeParams=["50"]
profile97 = part.CreateProfile(ProfilePram97,False)
part.SetElementColor(profile97[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile97[1],"148","0","211","0.39999997615814209")
mirror_copied26 = part.MirrorCopy([profile97[0]],"PL,Y","")
part.SetElementColor(mirror_copied26[0],"148","0","211","0.39999997615814209")
mirror_copied27 = part.MirrorCopy([profile24[0]],"PL,Y","")
part.SetElementColor(mirror_copied27[0],"255","0","0","0.19999998807907104")
ProfilePram98 = part.CreateProfileParam()
ProfilePram98.DefinitionType=1
ProfilePram98.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram98.AddAttachSurfaces(extrude_sheet8)
ProfilePram98.ProfileName="HK.Casing.Wall.Fore.DL02.OAP"
ProfilePram98.MaterialName="SS400"
ProfilePram98.FlangeName="HK.Casing.Wall.Fore.DL02.OAP"
ProfilePram98.FlangeMaterialName="SS400"
ProfilePram98.ProfileType=1201
ProfilePram98.ProfileParams=["150","12","388","10"]
ProfilePram98.Mold="-"
ProfilePram98.ReverseDir=True
ProfilePram98.ReverseAngle=False
ProfilePram98.CalcSnipOnlyAttachLines=False
ProfilePram98.AttachDirMethod=0
ProfilePram98.CCWDefAngle=False
ProfilePram98.AddEnd1Elements(extrude_sheet2)
ProfilePram98.End1Type=1102
ProfilePram98.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram98.AddEnd2Elements(extrude_sheet7)
ProfilePram98.End2Type=1102
ProfilePram98.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram98.End1ScallopType=1120
ProfilePram98.End1ScallopTypeParams=["50"]
ProfilePram98.End2ScallopType=1120
ProfilePram98.End2ScallopTypeParams=["50"]
profile98 = part.CreateProfile(ProfilePram98,False)
part.SetElementColor(profile98[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile98[1],"148","0","211","0.39999997615814209")
solid10 = part.CreateSolid("HK.Casing.Wall.Fore.CD","","SS400")
part.SetElementColor(solid10,"139","69","19","0.79999995231628418")
thicken10 = part.CreateThicken("厚み付け15",solid10,"+",[extrude_sheet8],"+","10","0","0",False,False)
extrudePram32 = part.CreateLinearSweepParam()
extrudePram32.Name="積-押し出し35"
extrudePram32.AddProfile(extrude_sheet6)
extrudePram32.DirectionType="R"
extrudePram32.DirectionParameter1="50000"
extrudePram32.SweepDirection="+Y"
extrudePram32.RefByGeometricMethod=True
extrude23 = part.CreateLinearSweep(solid10,"*",extrudePram32,False)
extrudePram33 = part.CreateLinearSweepParam()
extrudePram33.Name="積-押し出し36"
extrudePram33.AddProfile(extrude_sheet9)
extrudePram33.DirectionType="N"
extrudePram33.DirectionParameter1="50000"
extrudePram33.SweepDirection="+Y"
extrudePram33.RefByGeometricMethod=True
extrude24 = part.CreateLinearSweep(solid10,"*",extrudePram33,False)
extrudePram34 = part.CreateLinearSweepParam()
extrudePram34.Name="積-押し出し37"
extrudePram34.AddProfile(extrude_sheet5)
extrudePram34.DirectionType="R"
extrudePram34.DirectionParameter1="50000"
extrudePram34.SweepDirection="+Z"
extrudePram34.RefByGeometricMethod=True
extrude25 = part.CreateLinearSweep(solid10,"*",extrudePram34,False)
extrudePram35 = part.CreateLinearSweepParam()
extrudePram35.Name="積-押し出し38"
extrudePram35.AddProfile(extrude_sheet4)
extrudePram35.DirectionType="N"
extrudePram35.DirectionParameter1="50000"
extrudePram35.SweepDirection="+Z"
extrudePram35.RefByGeometricMethod=True
extrude26 = part.CreateLinearSweep(solid10,"*",extrudePram35,False)
ProfilePram99 = part.CreateProfileParam()
ProfilePram99.DefinitionType=1
ProfilePram99.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram99.AddAttachSurfaces(extrude_sheet3)
ProfilePram99.ProfileName="HK.Casing.Wall.Aft.DL00.AB"
ProfilePram99.MaterialName="SS400"
ProfilePram99.ProfileType=1002
ProfilePram99.ProfileParams=["125","75","7","10","5"]
ProfilePram99.ReverseDir=False
ProfilePram99.ReverseAngle=True
ProfilePram99.CalcSnipOnlyAttachLines=False
ProfilePram99.AttachDirMethod=0
ProfilePram99.CCWDefAngle=False
ProfilePram99.AddEnd1Elements(extrude_sheet1)
ProfilePram99.End1Type=1102
ProfilePram99.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram99.AddEnd2Elements(extrude_sheet2)
ProfilePram99.End2Type=1102
ProfilePram99.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram99.End1ScallopType=1121
ProfilePram99.End1ScallopTypeParams=["25","40"]
ProfilePram99.End2ScallopType=1121
ProfilePram99.End2ScallopTypeParams=["25","40"]
profile99 = part.CreateProfile(ProfilePram99,False)
part.SetElementColor(profile99[0],"255","0","0","0.19999998807907104")
ProfilePram100 = part.CreateProfileParam()
ProfilePram100.DefinitionType=1
ProfilePram100.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram100.AddAttachSurfaces(extrude_sheet8)
ProfilePram100.ProfileName="HK.Casing.Wall.Fore.DL04.CDP"
ProfilePram100.MaterialName="SS400"
ProfilePram100.ProfileType=1002
ProfilePram100.ProfileParams=["125","75","7","10","5"]
ProfilePram100.Mold="+"
ProfilePram100.ReverseDir=True
ProfilePram100.ReverseAngle=True
ProfilePram100.CalcSnipOnlyAttachLines=False
ProfilePram100.AttachDirMethod=0
ProfilePram100.CCWDefAngle=False
ProfilePram100.AddEnd1Elements(profile86[0])
ProfilePram100.End1Type=1102
ProfilePram100.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram100.AddEnd2Elements(extrude_sheet4)
ProfilePram100.End2Type=1102
ProfilePram100.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram100.End1ScallopType=1120
ProfilePram100.End1ScallopTypeParams=["50"]
ProfilePram100.End2ScallopType=1120
ProfilePram100.End2ScallopTypeParams=["50"]
profile100 = part.CreateProfile(ProfilePram100,False)
part.SetElementColor(profile100[0],"255","0","0","0.19999998807907104")
# 追加ブラケット: DL04 Fore と Deck D DL04
bracketPramP1 = part.CreateBracketParam()
bracketPramP1.DefinitionType=1
bracketPramP1.BracketName="HK.Casing.DL04.ForeDeckD.BKT"
bracketPramP1.MaterialName="SS400"
bracketPramP1.BaseElement=profile100[0]
bracketPramP1.UseSideSheetForPlane=False
bracketPramP1.Mold="+"
bracketPramP1.Thickness="8"
bracketPramP1.BracketType=1501
bracketPramP1.Scallop1Type=1801
bracketPramP1.Scallop1Params=["0"]
bracketPramP1.Scallop2Type=0
bracketPramP1.Surfaces1=[profile100[0]+",FL"]
bracketPramP1.RevSf1=False
bracketPramP1.Surfaces2=[profile86[0]+",FL"]
bracketPramP1.RevSf2=False
bracketPramP1.RevSf3=False
bracketPramP1.Sf1DimensionType=1531
bracketPramP1.Sf1DimensonParams=["200","15"]
bracketPramP1.Sf2DimensionType=1531
bracketPramP1.Sf2DimensonParams=["200","15"]
bracketP1 = part.CreateBracket(bracketPramP1,False)
part.SetElementColor(bracketP1,"0","255","255","0.19999998807907104")
solid11 = part.CreateSolid("HK.Casing.Wall.Aft.AB","","SS400")
part.SetElementColor(solid11,"139","69","19","0.79999995231628418")
thicken11 = part.CreateThicken("厚み付け13",solid11,"+",[extrude_sheet3],"-","10","0","0",False,False)
extrudePram36 = part.CreateLinearSweepParam()
extrudePram36.Name="積-押し出し27"
extrudePram36.AddProfile(extrude_sheet6)
extrudePram36.DirectionType="R"
extrudePram36.DirectionParameter1="50000"
extrudePram36.SweepDirection="+Y"
extrudePram36.RefByGeometricMethod=True
extrude27 = part.CreateLinearSweep(solid11,"*",extrudePram36,False)
extrudePram37 = part.CreateLinearSweepParam()
extrudePram37.Name="積-押し出し28"
extrudePram37.AddProfile(extrude_sheet9)
extrudePram37.DirectionType="N"
extrudePram37.DirectionParameter1="50000"
extrudePram37.SweepDirection="+Y"
extrudePram37.RefByGeometricMethod=True
extrude28 = part.CreateLinearSweep(solid11,"*",extrudePram37,False)
extrudePram38 = part.CreateLinearSweepParam()
extrudePram38.Name="積-押し出し29"
extrudePram38.AddProfile(extrude_sheet1)
extrudePram38.DirectionType="R"
extrudePram38.DirectionParameter1="50000"
extrudePram38.SweepDirection="+Z"
extrudePram38.RefByGeometricMethod=True
extrude29 = part.CreateLinearSweep(solid11,"*",extrudePram38,False)
extrudePram39 = part.CreateLinearSweepParam()
extrudePram39.Name="積-押し出し30"
extrudePram39.AddProfile(extrude_sheet2)
extrudePram39.DirectionType="N"
extrudePram39.DirectionParameter1="50000"
extrudePram39.SweepDirection="+Z"
extrudePram39.RefByGeometricMethod=True
extrude30 = part.CreateLinearSweep(solid11,"*",extrudePram39,False)
ProfilePram101 = part.CreateProfileParam()
ProfilePram101.DefinitionType=1
ProfilePram101.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram101.AddAttachSurfaces(extrude_sheet6)
ProfilePram101.ProfileName="HK.Casing.Wall.Side.FR13.BCP"
ProfilePram101.MaterialName="SS400"
ProfilePram101.ProfileType=1003
ProfilePram101.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram101.Mold="+"
ProfilePram101.ReverseDir=False
ProfilePram101.ReverseAngle=True
ProfilePram101.CalcSnipOnlyAttachLines=False
ProfilePram101.AttachDirMethod=0
ProfilePram101.CCWDefAngle=False
ProfilePram101.AddEnd1Elements(extrude_sheet4)
ProfilePram101.End1Type=1103
ProfilePram101.End1TypeParams=["0"]
ProfilePram101.AddEnd2Elements(extrude_sheet1)
ProfilePram101.End2Type=1103
ProfilePram101.End2TypeParams=["0"]
ProfilePram101.End1ScallopType=1120
ProfilePram101.End1ScallopTypeParams=["50"]
ProfilePram101.End2ScallopType=1120
ProfilePram101.End2ScallopTypeParams=["50"]
profile101 = part.CreateProfile(ProfilePram101,False)
part.SetElementColor(profile101[0],"148","0","211","0.39999997615814209")
mirror_copied29 = part.MirrorCopy([profile101[0]],"PL,Y","")
part.SetElementColor(mirror_copied29[0],"148","0","211","0.39999997615814209")
ProfilePram102 = part.CreateProfileParam()
ProfilePram102.DefinitionType=1
ProfilePram102.BasePlane="PL,O,"+var_elm5+","+"X"
ProfilePram102.AddAttachSurfaces(extrude_sheet6)
ProfilePram102.ProfileName="HK.Casing.Wall.Side.FR08.ABP"
ProfilePram102.MaterialName="SS400"
ProfilePram102.ProfileType=1002
ProfilePram102.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram102.Mold="+"
ProfilePram102.ReverseDir=False
ProfilePram102.ReverseAngle=True
ProfilePram102.CalcSnipOnlyAttachLines=False
ProfilePram102.AttachDirMethod=0
ProfilePram102.CCWDefAngle=False
ProfilePram102.AddEnd1Elements(extrude_sheet1)
ProfilePram102.End1Type=1102
ProfilePram102.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram102.AddEnd2Elements(extrude_sheet2)
ProfilePram102.End2Type=1102
ProfilePram102.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram102.End1ScallopType=1121
ProfilePram102.End1ScallopTypeParams=["35","40"]
ProfilePram102.End2ScallopType=1121
ProfilePram102.End2ScallopTypeParams=["35","40"]
profile102 = part.CreateProfile(ProfilePram102,False)
part.SetElementColor(profile102[0],"255","0","0","0.19999998807907104")
mirror_copied30 = part.MirrorCopy([profile102[0]],"PL,Y","")
part.SetElementColor(mirror_copied30[0],"255","0","0","0.19999998807907104")
ProfilePram103 = part.CreateProfileParam()
ProfilePram103.DefinitionType=1
ProfilePram103.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram103.AddAttachSurfaces(extrude_sheet6)
ProfilePram103.ProfileName="HK.Casing.Wall.Side.FR11.ABP"
ProfilePram103.MaterialName="SS400"
ProfilePram103.ProfileType=1002
ProfilePram103.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram103.Mold="+"
ProfilePram103.ReverseDir=False
ProfilePram103.ReverseAngle=True
ProfilePram103.CalcSnipOnlyAttachLines=False
ProfilePram103.AttachDirMethod=0
ProfilePram103.CCWDefAngle=False
ProfilePram103.AddEnd1Elements(extrude_sheet1)
ProfilePram103.End1Type=1102
ProfilePram103.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram103.AddEnd2Elements(extrude_sheet2)
ProfilePram103.End2Type=1102
ProfilePram103.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram103.End1ScallopType=1121
ProfilePram103.End1ScallopTypeParams=["35","40"]
ProfilePram103.End2ScallopType=1121
ProfilePram103.End2ScallopTypeParams=["35","40"]
profile103 = part.CreateProfile(ProfilePram103,False)
part.SetElementColor(profile103[0],"255","0","0","0.19999998807907104")
mirror_copied31 = part.MirrorCopy([profile5[0]],"PL,Y","")
part.SetElementColor(mirror_copied31[0],"255","0","0","0.19999998807907104")
solid12 = part.CreateSolid("HK.Casing.Wall.Side.CDP","","SS400")
part.SetElementColor(solid12,"139","69","19","0.79999995231628418")
thicken12 = part.CreateThicken("厚み付け7",solid12,"+",[extrude_sheet6],"-","10","0","0",False,False)
ProfilePram104 = part.CreateProfileParam()
ProfilePram104.DefinitionType=1
ProfilePram104.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram104.AddAttachSurfaces(extrude_sheet8)
ProfilePram104.ProfileName="HK.Casing.Wall.Fore.DL01.OAP"
ProfilePram104.MaterialName="SS400"
ProfilePram104.ProfileType=1002
ProfilePram104.ProfileParams=["125","75","7","10","5"]
ProfilePram104.Mold="+"
ProfilePram104.ReverseDir=True
ProfilePram104.ReverseAngle=True
ProfilePram104.CalcSnipOnlyAttachLines=False
ProfilePram104.AttachDirMethod=0
ProfilePram104.CCWDefAngle=False
ProfilePram104.AddEnd1Elements(extrude_sheet2)
ProfilePram104.End1Type=1102
ProfilePram104.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram104.AddEnd2Elements(extrude_sheet7)
ProfilePram104.End2Type=1102
ProfilePram104.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram104.End1ScallopType=1121
ProfilePram104.End1ScallopTypeParams=["25","40"]
ProfilePram104.End2ScallopType=1121
ProfilePram104.End2ScallopTypeParams=["25","40"]
profile104 = part.CreateProfile(ProfilePram104,False)
part.SetElementColor(profile104[0],"255","0","0","0.19999998807907104")
mirror_copied32 = part.MirrorCopy([profile21[0]],"PL,Y","")
part.SetElementColor(mirror_copied32[0],"255","0","0","0.19999998807907104")
mirror_copied33 = part.MirrorCopy([profile58[0]],"PL,Y","")
part.SetElementColor(mirror_copied33[0],"255","0","0","0.19999998807907104")
solid13 = part.CreateSolid("HK.Casing.Wall.Aft.BC","","SS400")
part.SetElementColor(solid13,"139","69","19","0.79999995231628418")
thicken13 = part.CreateThicken("厚み付け12",solid13,"+",[extrude_sheet3],"-","10","0","0",False,False)
extrudePram40 = part.CreateLinearSweepParam()
extrudePram40.Name="積-押し出し23"
extrudePram40.AddProfile(extrude_sheet6)
extrudePram40.DirectionType="R"
extrudePram40.DirectionParameter1="50000"
extrudePram40.SweepDirection="+Y"
extrudePram40.RefByGeometricMethod=True
extrude31 = part.CreateLinearSweep(solid13,"*",extrudePram40,False)
extrudePram41 = part.CreateLinearSweepParam()
extrudePram41.Name="積-押し出し24"
extrudePram41.AddProfile(extrude_sheet9)
extrudePram41.DirectionType="N"
extrudePram41.DirectionParameter1="50000"
extrudePram41.SweepDirection="+Y"
extrudePram41.RefByGeometricMethod=True
extrude32 = part.CreateLinearSweep(solid13,"*",extrudePram41,False)
ProfilePram105 = part.CreateProfileParam()
ProfilePram105.DefinitionType=1
ProfilePram105.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram105.AddAttachSurfaces(extrude_sheet3)
ProfilePram105.ProfileName="HK.Casing.Wall.Aft.DL01.BCP"
ProfilePram105.MaterialName="SS400"
ProfilePram105.ProfileType=1002
ProfilePram105.ProfileParams=["125","75","7","10","5"]
ProfilePram105.Mold="+"
ProfilePram105.ReverseDir=False
ProfilePram105.ReverseAngle=True
ProfilePram105.CalcSnipOnlyAttachLines=False
ProfilePram105.AttachDirMethod=0
ProfilePram105.CCWDefAngle=False
ProfilePram105.AddEnd1Elements(extrude_sheet4)
ProfilePram105.End1Type=1102
ProfilePram105.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram105.AddEnd2Elements(extrude_sheet1)
ProfilePram105.End2Type=1102
ProfilePram105.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram105.End1ScallopType=1121
ProfilePram105.End1ScallopTypeParams=["25","40"]
ProfilePram105.End2ScallopType=1121
ProfilePram105.End2ScallopTypeParams=["25","40"]
profile105 = part.CreateProfile(ProfilePram105,False)
part.SetElementColor(profile105[0],"255","0","0","0.19999998807907104")
ProfilePram106 = part.CreateProfileParam()
ProfilePram106.DefinitionType=1
ProfilePram106.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram106.AddAttachSurfaces(extrude_sheet6)
ProfilePram106.ProfileName="HK.Casing.Wall.Side.FR09.ABP"
ProfilePram106.MaterialName="SS400"
ProfilePram106.ProfileType=1003
ProfilePram106.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram106.Mold="+"
ProfilePram106.ReverseDir=False
ProfilePram106.ReverseAngle=True
ProfilePram106.CalcSnipOnlyAttachLines=False
ProfilePram106.AttachDirMethod=0
ProfilePram106.CCWDefAngle=False
ProfilePram106.AddEnd1Elements(extrude_sheet1)
ProfilePram106.End1Type=1103
ProfilePram106.End1TypeParams=["0"]
ProfilePram106.AddEnd2Elements(extrude_sheet2)
ProfilePram106.End2Type=1103
ProfilePram106.End2TypeParams=["0"]
ProfilePram106.End1ScallopType=1120
ProfilePram106.End1ScallopTypeParams=["50"]
ProfilePram106.End2ScallopType=1120
ProfilePram106.End2ScallopTypeParams=["50"]
profile106 = part.CreateProfile(ProfilePram106,False)
part.SetElementColor(profile106[0],"148","0","211","0.39999997615814209")
ProfilePram107 = part.CreateProfileParam()
ProfilePram107.DefinitionType=1
ProfilePram107.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram107.AddAttachSurfaces(extrude_sheet8)
ProfilePram107.ProfileName="HK.Casing.Wall.Fore.DL03.OAP"
ProfilePram107.MaterialName="SS400"
ProfilePram107.ProfileType=1002
ProfilePram107.ProfileParams=["125","75","7","10","5"]
ProfilePram107.Mold="+"
ProfilePram107.ReverseDir=True
ProfilePram107.ReverseAngle=True
ProfilePram107.CalcSnipOnlyAttachLines=False
ProfilePram107.AttachDirMethod=0
ProfilePram107.CCWDefAngle=False
ProfilePram107.AddEnd1Elements(extrude_sheet2)
ProfilePram107.End1Type=1102
ProfilePram107.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram107.AddEnd2Elements(extrude_sheet7)
ProfilePram107.End2Type=1102
ProfilePram107.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram107.End1ScallopType=1121
ProfilePram107.End1ScallopTypeParams=["25","40"]
ProfilePram107.End2ScallopType=1121
ProfilePram107.End2ScallopTypeParams=["25","40"]
profile107 = part.CreateProfile(ProfilePram107,False)
part.SetElementColor(profile107[0],"255","0","0","0.19999998807907104")
ProfilePram108 = part.CreateProfileParam()
ProfilePram108.DefinitionType=1
ProfilePram108.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram108.AddAttachSurfaces(extrude_sheet2)
ProfilePram108.ProfileName="HK.Casing.Deck.A.DL03.FP"
ProfilePram108.MaterialName="SS400"
ProfilePram108.ProfileType=1002
ProfilePram108.ProfileParams=["125","75","7","10","5"]
ProfilePram108.Mold="+"
ProfilePram108.ReverseDir=True
ProfilePram108.ReverseAngle=True
ProfilePram108.CalcSnipOnlyAttachLines=False
ProfilePram108.AttachDirMethod=0
ProfilePram108.CCWDefAngle=False
ProfilePram108.AddEnd1Elements(profile49[0])
ProfilePram108.End1Type=1102
ProfilePram108.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram108.AddEnd2Elements(profile107[0])
ProfilePram108.End2Type=1102
ProfilePram108.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram108.End1ScallopType=1121
ProfilePram108.End1ScallopTypeParams=["25","40"]
ProfilePram108.End2ScallopType=1121
ProfilePram108.End2ScallopTypeParams=["25","40"]
profile108 = part.CreateProfile(ProfilePram108,False)
part.SetElementColor(profile108[0],"255","0","0","0.19999998807907104")
ProfilePram109 = part.CreateProfileParam()
ProfilePram109.DefinitionType=1
ProfilePram109.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram109.AddAttachSurfaces(extrude_sheet2)
ProfilePram109.ProfileName="HK.Casing.Deck.A.DL01.FP"
ProfilePram109.MaterialName="SS400"
ProfilePram109.ProfileType=1002
ProfilePram109.ProfileParams=["125","75","7","10","5"]
ProfilePram109.Mold="+"
ProfilePram109.ReverseDir=True
ProfilePram109.ReverseAngle=True
ProfilePram109.CalcSnipOnlyAttachLines=False
ProfilePram109.AttachDirMethod=0
ProfilePram109.CCWDefAngle=False
ProfilePram109.AddEnd1Elements(profile49[0])
ProfilePram109.End1Type=1102
ProfilePram109.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram109.AddEnd2Elements(profile104[0])
ProfilePram109.End2Type=1102
ProfilePram109.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram109.End1ScallopType=1121
ProfilePram109.End1ScallopTypeParams=["25","40"]
ProfilePram109.End2ScallopType=1121
ProfilePram109.End2ScallopTypeParams=["25","40"]
profile109 = part.CreateProfile(ProfilePram109,False)
part.SetElementColor(profile109[0],"255","0","0","0.19999998807907104")
mirror_copied35 = part.MirrorCopy([profile44[0]],"PL,Y","")
part.SetElementColor(mirror_copied35[0],"255","0","0","0.19999998807907104")
ProfilePram110 = part.CreateProfileParam()
ProfilePram110.DefinitionType=1
ProfilePram110.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram110.AddAttachSurfaces(extrude_sheet4)
ProfilePram110.ProfileName="HK.Casing.Deck.C.FR13P"
ProfilePram110.MaterialName="SS400"
ProfilePram110.ProfileType=1003
ProfilePram110.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram110.Mold="+"
ProfilePram110.ReverseDir=True
ProfilePram110.ReverseAngle=False
ProfilePram110.CalcSnipOnlyAttachLines=False
ProfilePram110.AttachDirMethod=0
ProfilePram110.CCWDefAngle=False
ProfilePram110.AddEnd1Elements(profile15[0])
ProfilePram110.End1Type=1113
ProfilePram110.End1TypeParams=["0","79"]
ProfilePram110.AddEnd2Elements(profile101[0])
ProfilePram110.End2Type=1102
ProfilePram110.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram110.End1ScallopType=1120
ProfilePram110.End1ScallopTypeParams=["50"]
ProfilePram110.End2ScallopType=1120
ProfilePram110.End2ScallopTypeParams=["50"]
profile110 = part.CreateProfile(ProfilePram110,False)
part.SetElementColor(profile110[0],"148","0","211","0.39999997615814209")
solid14 = part.CreateSolid("HK.Casing.Wall.Fore.BC","","SS400")
part.SetElementColor(solid14,"139","69","19","0.79999995231628418")
thicken14 = part.CreateThicken("厚み付け16",solid14,"+",[extrude_sheet8],"+","10","0","0",False,False)
extrudePram42 = part.CreateLinearSweepParam()
extrudePram42.Name="積-押し出し39"
extrudePram42.AddProfile(extrude_sheet6)
extrudePram42.DirectionType="R"
extrudePram42.DirectionParameter1="50000"
extrudePram42.SweepDirection="+Y"
extrudePram42.RefByGeometricMethod=True
extrude33 = part.CreateLinearSweep(solid14,"*",extrudePram42,False)
extrudePram43 = part.CreateLinearSweepParam()
extrudePram43.Name="積-押し出し40"
extrudePram43.AddProfile(extrude_sheet9)
extrudePram43.DirectionType="N"
extrudePram43.DirectionParameter1="50000"
extrudePram43.SweepDirection="+Y"
extrudePram43.RefByGeometricMethod=True
extrude34 = part.CreateLinearSweep(solid14,"*",extrudePram43,False)
mirror_copied39 = part.MirrorCopy([profile75[0]],"PL,Y","")
part.SetElementColor(mirror_copied39[0],"255","0","0","0.19999998807907104")
ProfilePram111 = part.CreateProfileParam()
ProfilePram111.DefinitionType=1
ProfilePram111.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram111.AddAttachSurfaces(extrude_sheet6)
ProfilePram111.ProfileName="HK.Casing.Wall.Side.FR11.CDP"
ProfilePram111.MaterialName="SS400"
ProfilePram111.ProfileType=1002
ProfilePram111.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram111.Mold="+"
ProfilePram111.ReverseDir=False
ProfilePram111.ReverseAngle=True
ProfilePram111.CalcSnipOnlyAttachLines=False
ProfilePram111.AttachDirMethod=0
ProfilePram111.CCWDefAngle=False
ProfilePram111.AddEnd1Elements(extrude_sheet5)
ProfilePram111.End1Type=1102
ProfilePram111.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram111.AddEnd2Elements(extrude_sheet4)
ProfilePram111.End2Type=1102
ProfilePram111.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram111.End1ScallopType=1121
ProfilePram111.End1ScallopTypeParams=["35","40"]
ProfilePram111.End2ScallopType=1121
ProfilePram111.End2ScallopTypeParams=["35","40"]
profile111 = part.CreateProfile(ProfilePram111,False)
part.SetElementColor(profile111[0],"255","0","0","0.19999998807907104")
mirror_copied42 = part.MirrorCopy([profile67[0]],"PL,Y","")
part.SetElementColor(mirror_copied42[0],"255","0","0","0.19999998807907104")
ProfilePram112 = part.CreateProfileParam()
ProfilePram112.DefinitionType=1
ProfilePram112.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram112.AddAttachSurfaces(extrude_sheet1)
ProfilePram112.ProfileName="HK.Casing.Deck.B.FR09P"
ProfilePram112.MaterialName="SS400"
ProfilePram112.ProfileType=1003
ProfilePram112.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram112.Mold="+"
ProfilePram112.ReverseDir=True
ProfilePram112.ReverseAngle=False
ProfilePram112.CalcSnipOnlyAttachLines=False
ProfilePram112.AttachDirMethod=0
ProfilePram112.CCWDefAngle=False
ProfilePram112.AddEnd1Elements(profile30[0])
ProfilePram112.End1Type=1113
ProfilePram112.End1TypeParams=["0","79"]
ProfilePram112.AddEnd2Elements(profile106[0])
ProfilePram112.End2Type=1102
ProfilePram112.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram112.End1ScallopType=1120
ProfilePram112.End1ScallopTypeParams=["50"]
ProfilePram112.End2ScallopType=1120
ProfilePram112.End2ScallopTypeParams=["50"]
profile112 = part.CreateProfile(ProfilePram112,False)
part.SetElementColor(profile112[0],"148","0","211","0.39999997615814209")
mirror_copied43 = part.MirrorCopy([profile9[0]],"PL,Y","")
part.SetElementColor(mirror_copied43[0],"255","0","0","0.19999998807907104")
mirror_copied46 = part.MirrorCopy([profile91[0]],"PL,Y","")
part.SetElementColor(mirror_copied46[0],"255","0","0","0.19999998807907104")
mirror_copied50 = part.MirrorCopy([profile107[0]],"PL,Y","")
part.SetElementColor(mirror_copied50[0],"255","0","0","0.19999998807907104")
extrudePram44 = part.CreateLinearSweepParam()
extrudePram44.Name="積-押し出し22"
extrudePram44.AddProfile(extrude_sheet4)
extrudePram44.DirectionType="N"
extrudePram44.DirectionParameter1="50000"
extrudePram44.SweepDirection="+Z"
extrudePram44.RefByGeometricMethod=True
extrude35 = part.CreateLinearSweep(solid5,"*",extrudePram44,False)
ProfilePram113 = part.CreateProfileParam()
ProfilePram113.DefinitionType=1
ProfilePram113.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram113.AddAttachSurfaces(extrude_sheet6)
ProfilePram113.ProfileName="HK.Casing.Wall.Side.FR14.CDP"
ProfilePram113.MaterialName="SS400"
ProfilePram113.ProfileType=1002
ProfilePram113.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram113.Mold="+"
ProfilePram113.ReverseDir=False
ProfilePram113.ReverseAngle=True
ProfilePram113.CalcSnipOnlyAttachLines=False
ProfilePram113.AttachDirMethod=0
ProfilePram113.CCWDefAngle=False
ProfilePram113.AddEnd1Elements(extrude_sheet5)
ProfilePram113.End1Type=1102
ProfilePram113.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram113.AddEnd2Elements(extrude_sheet4)
ProfilePram113.End2Type=1102
ProfilePram113.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram113.End1ScallopType=1121
ProfilePram113.End1ScallopTypeParams=["35","40"]
ProfilePram113.End2ScallopType=1121
ProfilePram113.End2ScallopTypeParams=["35","40"]
profile113 = part.CreateProfile(ProfilePram113,False)
part.SetElementColor(profile113[0],"255","0","0","0.19999998807907104")
mirror_copied52 = part.MirrorCopy([profile90[0]],"PL,Y","")
part.SetElementColor(mirror_copied52[0],"148","0","211","0.39999997615814209")
ProfilePram114 = part.CreateProfileParam()
ProfilePram114.DefinitionType=1
ProfilePram114.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram114.AddAttachSurfaces(extrude_sheet1)
ProfilePram114.ProfileName="HK.Casing.Deck.B.DL03.FP"
ProfilePram114.MaterialName="SS400"
ProfilePram114.ProfileType=1002
ProfilePram114.ProfileParams=["125","75","7","10","5"]
ProfilePram114.Mold="+"
ProfilePram114.ReverseDir=True
ProfilePram114.ReverseAngle=True
ProfilePram114.CalcSnipOnlyAttachLines=False
ProfilePram114.AttachDirMethod=0
ProfilePram114.CCWDefAngle=False
ProfilePram114.AddEnd1Elements(profile70[0])
ProfilePram114.End1Type=1102
ProfilePram114.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram114.AddEnd2Elements(profile25[0])
ProfilePram114.End2Type=1102
ProfilePram114.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram114.End1ScallopType=1121
ProfilePram114.End1ScallopTypeParams=["25","40"]
ProfilePram114.End2ScallopType=1121
ProfilePram114.End2ScallopTypeParams=["25","40"]
profile114 = part.CreateProfile(ProfilePram114,False)
part.SetElementColor(profile114[0],"255","0","0","0.19999998807907104")
mirror_copied54 = part.MirrorCopy([profile51[0]],"PL,Y","")
part.SetElementColor(mirror_copied54[0],"255","0","0","0.19999998807907104")
ProfilePram115 = part.CreateProfileParam()
ProfilePram115.DefinitionType=1
ProfilePram115.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram115.AddAttachSurfaces(extrude_sheet3)
ProfilePram115.ProfileName="HK.Casing.Wall.Aft.DL01.ABP"
ProfilePram115.MaterialName="SS400"
ProfilePram115.ProfileType=1002
ProfilePram115.ProfileParams=["125","75","7","10","5"]
ProfilePram115.Mold="+"
ProfilePram115.ReverseDir=False
ProfilePram115.ReverseAngle=True
ProfilePram115.CalcSnipOnlyAttachLines=False
ProfilePram115.AttachDirMethod=0
ProfilePram115.CCWDefAngle=False
ProfilePram115.AddEnd1Elements(extrude_sheet1)
ProfilePram115.End1Type=1102
ProfilePram115.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram115.AddEnd2Elements(extrude_sheet2)
ProfilePram115.End2Type=1102
ProfilePram115.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram115.End1ScallopType=1121
ProfilePram115.End1ScallopTypeParams=["25","40"]
ProfilePram115.End2ScallopType=1121
ProfilePram115.End2ScallopTypeParams=["25","40"]
profile115 = part.CreateProfile(ProfilePram115,False)
part.SetElementColor(profile115[0],"255","0","0","0.19999998807907104")
mirror_copied58 = part.MirrorCopy([profile25[0]],"PL,Y","")
part.SetElementColor(mirror_copied58[0],"255","0","0","0.19999998807907104")
ProfilePram116 = part.CreateProfileParam()
ProfilePram116.DefinitionType=1
ProfilePram116.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram116.AddAttachSurfaces(extrude_sheet6)
ProfilePram116.ProfileName="HK.Casing.Wall.Side.FR11.OAP"
ProfilePram116.MaterialName="SS400"
ProfilePram116.ProfileType=1002
ProfilePram116.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram116.Mold="+"
ProfilePram116.ReverseDir=False
ProfilePram116.ReverseAngle=True
ProfilePram116.CalcSnipOnlyAttachLines=False
ProfilePram116.AttachDirMethod=0
ProfilePram116.CCWDefAngle=False
ProfilePram116.AddEnd1Elements(extrude_sheet2)
ProfilePram116.End1Type=1102
ProfilePram116.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram116.AddEnd2Elements(extrude_sheet7)
ProfilePram116.End2Type=1102
ProfilePram116.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram116.End1ScallopType=1121
ProfilePram116.End1ScallopTypeParams=["35","40"]
ProfilePram116.End2ScallopType=1121
ProfilePram116.End2ScallopTypeParams=["35","40"]
profile116 = part.CreateProfile(ProfilePram116,False)
part.SetElementColor(profile116[0],"255","0","0","0.19999998807907104")
mirror_copied59 = part.MirrorCopy([profile45[0]],"PL,Y","")
part.SetElementColor(mirror_copied59[0],"255","0","0","0.19999998807907104")
ProfilePram117 = part.CreateProfileParam()
ProfilePram117.DefinitionType=1
ProfilePram117.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram117.AddAttachSurfaces(extrude_sheet8)
ProfilePram117.ProfileName="HK.Casing.Wall.Fore.DL03.CDP"
ProfilePram117.MaterialName="SS400"
ProfilePram117.ProfileType=1002
ProfilePram117.ProfileParams=["125","75","7","10","5"]
ProfilePram117.Mold="+"
ProfilePram117.ReverseDir=True
ProfilePram117.ReverseAngle=True
ProfilePram117.CalcSnipOnlyAttachLines=False
ProfilePram117.AttachDirMethod=0
ProfilePram117.CCWDefAngle=False
ProfilePram117.AddEnd1Elements(profile35[0])
ProfilePram117.End1Type=1102
ProfilePram117.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram117.AddEnd2Elements(extrude_sheet4)
ProfilePram117.End2Type=1102
ProfilePram117.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram117.End1ScallopType=1120
ProfilePram117.End1ScallopTypeParams=["50"]
ProfilePram117.End2ScallopType=1120
ProfilePram117.End2ScallopTypeParams=["50"]
profile117 = part.CreateProfile(ProfilePram117,False)
part.SetElementColor(profile117[0],"255","0","0","0.19999998807907104")
mirror_copied60 = part.MirrorCopy([profile16[0]],"PL,Y","")
part.SetElementColor(mirror_copied60[0],"255","0","0","0.19999998807907104")
mirror_copied62 = part.MirrorCopy([profile65[0]],"PL,Y","")
part.SetElementColor(mirror_copied62[0],"148","0","211","0.39999997615814209")
mirror_copied63 = part.MirrorCopy([profile53[0]],"PL,Y","")
part.SetElementColor(mirror_copied63[0],"255","0","0","0.19999998807907104")
mirror_copied64 = part.MirrorCopy([profile46[0]],"PL,Y","")
part.SetElementColor(mirror_copied64[0],"255","0","0","0.19999998807907104")
ProfilePram118 = part.CreateProfileParam()
ProfilePram118.DefinitionType=1
ProfilePram118.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram118.AddAttachSurfaces(extrude_sheet6)
ProfilePram118.ProfileName="HK.Casing.Wall.Side.FR15.OAP"
ProfilePram118.MaterialName="SS400"
ProfilePram118.ProfileType=1002
ProfilePram118.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram118.Mold="+"
ProfilePram118.ReverseDir=False
ProfilePram118.ReverseAngle=True
ProfilePram118.CalcSnipOnlyAttachLines=False
ProfilePram118.AttachDirMethod=0
ProfilePram118.CCWDefAngle=False
ProfilePram118.AddEnd1Elements(extrude_sheet2)
ProfilePram118.End1Type=1102
ProfilePram118.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram118.AddEnd2Elements(extrude_sheet7)
ProfilePram118.End2Type=1102
ProfilePram118.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram118.End1ScallopType=1121
ProfilePram118.End1ScallopTypeParams=["35","40"]
ProfilePram118.End2ScallopType=1121
ProfilePram118.End2ScallopTypeParams=["35","40"]
profile118 = part.CreateProfile(ProfilePram118,False)
part.SetElementColor(profile118[0],"255","0","0","0.19999998807907104")
mirror_copied66 = part.MirrorCopy([profile64[0]],"PL,Y","")
part.SetElementColor(mirror_copied66[0],"148","0","211","0.39999997615814209")
ProfilePram119 = part.CreateProfileParam()
ProfilePram119.DefinitionType=1
ProfilePram119.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfilePram119.AddAttachSurfaces(extrude_sheet3)
ProfilePram119.ProfileName="HK.Casing.Wall.Aft.DL03.OAP"
ProfilePram119.MaterialName="SS400"
ProfilePram119.ProfileType=1002
ProfilePram119.ProfileParams=["125","75","7","10","5"]
ProfilePram119.Mold="+"
ProfilePram119.ReverseDir=False
ProfilePram119.ReverseAngle=True
ProfilePram119.CalcSnipOnlyAttachLines=False
ProfilePram119.AttachDirMethod=0
ProfilePram119.CCWDefAngle=False
ProfilePram119.AddEnd1Elements(extrude_sheet2)
ProfilePram119.End1Type=1102
ProfilePram119.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram119.AddEnd2Elements(extrude_sheet7)
ProfilePram119.End2Type=1102
ProfilePram119.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram119.End1ScallopType=1121
ProfilePram119.End1ScallopTypeParams=["25","40"]
ProfilePram119.End2ScallopType=1121
ProfilePram119.End2ScallopTypeParams=["25","40"]
profile119 = part.CreateProfile(ProfilePram119,False)
part.SetElementColor(profile119[0],"255","0","0","0.19999998807907104")
mirror_copied67 = part.MirrorCopy([profile119[0]],"PL,Y","")
part.SetElementColor(mirror_copied67[0],"255","0","0","0.19999998807907104")
mirror_copied68 = part.MirrorCopy([profile13[0]],"PL,Y","")
part.SetElementColor(mirror_copied68[0],"148","0","211","0.39999997615814209")
mirror_copied69 = part.MirrorCopy([profile106[0]],"PL,Y","")
part.SetElementColor(mirror_copied69[0],"148","0","211","0.39999997615814209")
ProfilePram120 = part.CreateProfileParam()
ProfilePram120.DefinitionType=1
ProfilePram120.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram120.AddAttachSurfaces(extrude_sheet3)
ProfilePram120.ProfileName="HK.Casing.Wall.Aft.DL02.ABP"
ProfilePram120.MaterialName="SS400"
ProfilePram120.FlangeName="HK.Casing.Wall.Aft.DL02.ABP"
ProfilePram120.FlangeMaterialName="SS400"
ProfilePram120.ProfileType=1201
ProfilePram120.ProfileParams=["150","12","388","10"]
ProfilePram120.Mold="-"
ProfilePram120.ReverseDir=False
ProfilePram120.ReverseAngle=False
ProfilePram120.CalcSnipOnlyAttachLines=False
ProfilePram120.AttachDirMethod=0
ProfilePram120.CCWDefAngle=False
ProfilePram120.AddEnd1Elements(extrude_sheet1)
ProfilePram120.End1Type=1103
ProfilePram120.End1TypeParams=["0"]
ProfilePram120.AddEnd2Elements(extrude_sheet2)
ProfilePram120.End2Type=1103
ProfilePram120.End2TypeParams=["0"]
ProfilePram120.End1ScallopType=1120
ProfilePram120.End1ScallopTypeParams=["50"]
ProfilePram120.End2ScallopType=1120
ProfilePram120.End2ScallopTypeParams=["50"]
profile120 = part.CreateProfile(ProfilePram120,False)
part.SetElementColor(profile120[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile120[1],"148","0","211","0.39999997615814209")
extrudePram45 = part.CreateLinearSweepParam()
extrudePram45.Name="積-押し出し7"
extrudePram45.AddProfile(skt_pl4+",Edge00")
extrudePram45.DirectionType="N"
extrudePram45.DirectionParameter1="50000"
extrudePram45.SweepDirection="+Z"
extrudePram45.RefByGeometricMethod=True
extrude36 = part.CreateLinearSweep(solid12,"*",extrudePram45,False)
extrudePram46 = part.CreateLinearSweepParam()
extrudePram46.Name="積-押し出し8"
extrudePram46.AddProfile(extrude_sheet5)
extrudePram46.DirectionType="R"
extrudePram46.DirectionParameter1="50000"
extrudePram46.SweepDirection="+Z"
extrudePram46.RefByGeometricMethod=True
extrude37 = part.CreateLinearSweep(solid12,"*",extrudePram46,False)
extrudePram47 = part.CreateLinearSweepParam()
extrudePram47.Name="積-押し出し9"
extrudePram47.AddProfile(extrude_sheet4)
extrudePram47.DirectionType="N"
extrudePram47.DirectionParameter1="50000"
extrudePram47.SweepDirection="+Z"
extrudePram47.RefByGeometricMethod=True
extrude38 = part.CreateLinearSweep(solid12,"*",extrudePram47,False)
mirror_copied72 = part.MirrorCopy([profile97[1]],"PL,Y","")
part.SetElementColor(mirror_copied72[0],"148","0","211","0.39999997615814209")
mirror_copied73 = part.MirrorCopy([profile118[0]],"PL,Y","")
part.SetElementColor(mirror_copied73[0],"255","0","0","0.19999998807907104")
extrudePram48 = part.CreateLinearSweepParam()
extrudePram48.Name="積-押し出し25"
extrudePram48.AddProfile(extrude_sheet4)
extrudePram48.DirectionType="R"
extrudePram48.DirectionParameter1="50000"
extrudePram48.SweepDirection="+Z"
extrudePram48.RefByGeometricMethod=True
extrude39 = part.CreateLinearSweep(solid13,"*",extrudePram48,False)
extrudePram49 = part.CreateLinearSweepParam()
extrudePram49.Name="積-押し出し26"
extrudePram49.AddProfile(extrude_sheet1)
extrudePram49.DirectionType="N"
extrudePram49.DirectionParameter1="50000"
extrudePram49.SweepDirection="+Z"
extrudePram49.RefByGeometricMethod=True
extrude40 = part.CreateLinearSweep(solid13,"*",extrudePram49,False)
mirror_copied75 = part.MirrorCopy([profile2[1]],"PL,Y","")
part.SetElementColor(mirror_copied75[0],"148","0","211","0.39999997615814209")
mirror_copied76 = part.MirrorCopy([profile36[0]],"PL,Y","")
part.SetElementColor(mirror_copied76[0],"255","0","0","0.19999998807907104")
mirror_copied77 = part.MirrorCopy([profile43[0]],"PL,Y","")
part.SetElementColor(mirror_copied77[0],"148","0","211","0.39999997615814209")
mirror_copied78 = part.MirrorCopy([profile86[0]],"PL,Y","")
part.SetElementColor(mirror_copied78[0],"255","0","0","0.19999998807907104")
mirror_copied79 = part.MirrorCopy([profile92[0]],"PL,Y","")
part.SetElementColor(mirror_copied79[0],"255","0","0","0.19999998807907104")
ProfilePram121 = part.CreateProfileParam()
ProfilePram121.DefinitionType=1
ProfilePram121.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram121.AddAttachSurfaces(extrude_sheet3)
ProfilePram121.ProfileName="HK.Casing.Wall.Aft.DL00.CD"
ProfilePram121.MaterialName="SS400"
ProfilePram121.ProfileType=1002
ProfilePram121.ProfileParams=["125","75","7","10","5"]
ProfilePram121.ReverseDir=False
ProfilePram121.ReverseAngle=True
ProfilePram121.CalcSnipOnlyAttachLines=False
ProfilePram121.AttachDirMethod=0
ProfilePram121.CCWDefAngle=False
ProfilePram121.AddEnd1Elements(profile33[0])
ProfilePram121.End1Type=1102
ProfilePram121.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram121.AddEnd2Elements(extrude_sheet4)
ProfilePram121.End2Type=1102
ProfilePram121.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram121.End1ScallopType=1120
ProfilePram121.End1ScallopTypeParams=["50"]
ProfilePram121.End2ScallopType=1120
ProfilePram121.End2ScallopTypeParams=["50"]
profile121 = part.CreateProfile(ProfilePram121,False)
part.SetElementColor(profile121[0],"255","0","0","0.19999998807907104")
mirror_copied81 = part.MirrorCopy([profile110[0]],"PL,Y","")
part.SetElementColor(mirror_copied81[0],"148","0","211","0.39999997615814209")
mirror_copied83 = part.MirrorCopy([profile54[0]],"PL,Y","")
part.SetElementColor(mirror_copied83[0],"255","0","0","0.19999998807907104")
mirror_copied84 = part.MirrorCopy([profile71[0]],"PL,Y","")
part.SetElementColor(mirror_copied84[0],"255","0","0","0.19999998807907104")
mirror_copied86 = part.MirrorCopy([profile88[0]],"PL,Y","")
part.SetElementColor(mirror_copied86[0],"148","0","211","0.39999997615814209")
mirror_copied88 = part.MirrorCopy([profile29[0]],"PL,Y","")
part.SetElementColor(mirror_copied88[0],"148","0","211","0.39999997615814209")
mirror_copied89 = part.MirrorCopy([profile62[0]],"PL,Y","")
part.SetElementColor(mirror_copied89[0],"255","0","0","0.19999998807907104")
mirror_copied92 = part.MirrorCopy([profile59[1]],"PL,Y","")
part.SetElementColor(mirror_copied92[0],"148","0","211","0.39999997615814209")
mirror_copied93 = part.MirrorCopy([profile88[1]],"PL,Y","")
part.SetElementColor(mirror_copied93[0],"148","0","211","0.39999997615814209")
ProfilePram122 = part.CreateProfileParam()
ProfilePram122.DefinitionType=1
ProfilePram122.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram122.AddAttachSurfaces(extrude_sheet6)
ProfilePram122.ProfileName="HK.Casing.Wall.Side.FR12.ABP"
ProfilePram122.MaterialName="SS400"
ProfilePram122.ProfileType=1002
ProfilePram122.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram122.Mold="+"
ProfilePram122.ReverseDir=False
ProfilePram122.ReverseAngle=True
ProfilePram122.CalcSnipOnlyAttachLines=False
ProfilePram122.AttachDirMethod=0
ProfilePram122.CCWDefAngle=False
ProfilePram122.AddEnd1Elements(extrude_sheet1)
ProfilePram122.End1Type=1102
ProfilePram122.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram122.AddEnd2Elements(extrude_sheet2)
ProfilePram122.End2Type=1102
ProfilePram122.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram122.End1ScallopType=1121
ProfilePram122.End1ScallopTypeParams=["35","40"]
ProfilePram122.End2ScallopType=1121
ProfilePram122.End2ScallopTypeParams=["35","40"]
profile122 = part.CreateProfile(ProfilePram122,False)
part.SetElementColor(profile122[0],"255","0","0","0.19999998807907104")
mirror_copied94 = part.MirrorCopy([profile122[0]],"PL,Y","")
part.SetElementColor(mirror_copied94[0],"255","0","0","0.19999998807907104")
solid15 = part.CreateSolid("HK.Casing.Wall.Side.BCP","","SS400")
part.SetElementColor(solid15,"139","69","19","0.79999995231628418")
thicken15 = part.CreateThicken("厚み付け8",solid15,"+",[extrude_sheet6],"-","10","0","0",False,False)
extrudePram50 = part.CreateLinearSweepParam()
extrudePram50.Name="積-押し出し10"
extrudePram50.AddProfile(skt_pl4+",Edge00")
extrudePram50.DirectionType="N"
extrudePram50.DirectionParameter1="50000"
extrudePram50.SweepDirection="+Z"
extrudePram50.RefByGeometricMethod=True
extrude41 = part.CreateLinearSweep(solid15,"*",extrudePram50,False)
extrudePram51 = part.CreateLinearSweepParam()
extrudePram51.Name="積-押し出し11"
extrudePram51.AddProfile(extrude_sheet4)
extrudePram51.DirectionType="R"
extrudePram51.DirectionParameter1="50000"
extrudePram51.SweepDirection="+Z"
extrudePram51.RefByGeometricMethod=True
extrude42 = part.CreateLinearSweep(solid15,"*",extrudePram51,False)
extrudePram52 = part.CreateLinearSweepParam()
extrudePram52.Name="積-押し出し12"
extrudePram52.AddProfile(extrude_sheet1)
extrudePram52.DirectionType="N"
extrudePram52.DirectionParameter1="50000"
extrudePram52.SweepDirection="+Z"
extrudePram52.RefByGeometricMethod=True
extrude43 = part.CreateLinearSweep(solid15,"*",extrudePram52,False)
mirror_copied96 = part.MirrorCopy([solid15],"PL,Y","")
part.SetElementColor(mirror_copied96[0],"139","69","19","0.79999995231628418")
mirror_copied97 = part.MirrorCopy([profile11[1]],"PL,Y","")
part.SetElementColor(mirror_copied97[0],"148","0","211","0.39999997615814209")
mirror_copied99 = part.MirrorCopy([profile41[0]],"PL,Y","")
part.SetElementColor(mirror_copied99[0],"148","0","211","0.39999997615814209")
mirror_copied100 = part.MirrorCopy([profile76[0]],"PL,Y","")
part.SetElementColor(mirror_copied100[0],"255","0","0","0.19999998807907104")
mirror_copied101 = part.MirrorCopy([profile19[0]],"PL,Y","")
part.SetElementColor(mirror_copied101[0],"148","0","211","0.39999997615814209")
mirror_copied102 = part.MirrorCopy([profile112[0]],"PL,Y","")
part.SetElementColor(mirror_copied102[0],"148","0","211","0.39999997615814209")
mirror_copied105 = part.MirrorCopy([profile47[0]],"PL,Y","")
part.SetElementColor(mirror_copied105[0],"255","0","0","0.19999998807907104")
mirror_copied106 = part.MirrorCopy([profile23[0]],"PL,Y","")
part.SetElementColor(mirror_copied106[0],"255","0","0","0.19999998807907104")
mirror_copied108 = part.MirrorCopy([profile18[1]],"PL,Y","")
part.SetElementColor(mirror_copied108[0],"148","0","211","0.39999997615814209")
mirror_copied109 = part.MirrorCopy([profile79[0]],"PL,Y","")
part.SetElementColor(mirror_copied109[0],"255","0","0","0.19999998807907104")
mirror_copied110 = part.MirrorCopy([profile35[0]],"PL,Y","")
part.SetElementColor(mirror_copied110[0],"255","0","0","0.19999998807907104")
mirror_copied111 = part.MirrorCopy([profile19[1]],"PL,Y","")
part.SetElementColor(mirror_copied111[0],"148","0","211","0.38999998569488525")
mirror_copied113 = part.MirrorCopy([profile82[0]],"PL,Y","")
part.SetElementColor(mirror_copied113[0],"255","0","0","0.19999998807907104")
mirror_copied114 = part.MirrorCopy([profile17[0]],"PL,Y","")
part.SetElementColor(mirror_copied114[0],"255","0","0","0.19999998807907104")
mirror_copied115 = part.MirrorCopy([profile6[0]],"PL,Y","")
part.SetElementColor(mirror_copied115[0],"255","0","0","0.19999998807907104")
mirror_copied116 = part.MirrorCopy([profile61[0]],"PL,Y","")
part.SetElementColor(mirror_copied116[0],"255","0","0","0.19999998807907104")
mirror_copied117 = part.MirrorCopy([profile10[0]],"PL,Y","")
part.SetElementColor(mirror_copied117[0],"255","0","0","0.19999998807907104")
mirror_copied120 = part.MirrorCopy([profile114[0]],"PL,Y","")
part.SetElementColor(mirror_copied120[0],"255","0","0","0.19999998807907104")
mirror_copied121 = part.MirrorCopy([profile116[0]],"PL,Y","")
part.SetElementColor(mirror_copied121[0],"255","0","0","0.19999998807907104")
mirror_copied122 = part.MirrorCopy([profile98[0]],"PL,Y","")
part.SetElementColor(mirror_copied122[0],"148","0","211","0.39999997615814209")
mirror_copied123 = part.MirrorCopy([profile113[0]],"PL,Y","")
part.SetElementColor(mirror_copied123[0],"255","0","0","0.19999998807907104")
ProfilePram123 = part.CreateProfileParam()
ProfilePram123.DefinitionType=1
ProfilePram123.BasePlane="PL,O,"+var_elm14+","+"Y"
ProfilePram123.AddAttachSurfaces(extrude_sheet3)
ProfilePram123.ProfileName="HK.Casing.Wall.Aft.DL00.OA"
ProfilePram123.MaterialName="SS400"
ProfilePram123.ProfileType=1002
ProfilePram123.ProfileParams=["125","75","7","10","5"]
ProfilePram123.ReverseDir=False
ProfilePram123.ReverseAngle=True
ProfilePram123.CalcSnipOnlyAttachLines=False
ProfilePram123.AttachDirMethod=0
ProfilePram123.CCWDefAngle=False
ProfilePram123.AddEnd1Elements(extrude_sheet2)
ProfilePram123.End1Type=1102
ProfilePram123.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram123.AddEnd2Elements(extrude_sheet7)
ProfilePram123.End2Type=1102
ProfilePram123.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram123.End1ScallopType=1121
ProfilePram123.End1ScallopTypeParams=["25","40"]
ProfilePram123.End2ScallopType=1121
ProfilePram123.End2ScallopTypeParams=["25","40"]
profile123 = part.CreateProfile(ProfilePram123,False)
part.SetElementColor(profile123[0],"255","0","0","0.19999998807907104")
mirror_copied128 = part.MirrorCopy([profile115[0]],"PL,Y","")
part.SetElementColor(mirror_copied128[0],"255","0","0","0.19999998807907104")
extrudePram53 = part.CreateLinearSweepParam()
extrudePram53.Name="積-押し出し43"
extrudePram53.AddProfile(extrude_sheet6)
extrudePram53.DirectionType="R"
extrudePram53.DirectionParameter1="50000"
extrudePram53.SweepDirection="+Y"
extrudePram53.RefByGeometricMethod=True
extrude44 = part.CreateLinearSweep(solid6,"*",extrudePram53,False)
extrudePram54 = part.CreateLinearSweepParam()
extrudePram54.Name="積-押し出し44"
extrudePram54.AddProfile(extrude_sheet9)
extrudePram54.DirectionType="N"
extrudePram54.DirectionParameter1="50000"
extrudePram54.SweepDirection="+Y"
extrudePram54.RefByGeometricMethod=True
extrude45 = part.CreateLinearSweep(solid6,"*",extrudePram54,False)
extrudePram55 = part.CreateLinearSweepParam()
extrudePram55.Name="積-押し出し45"
extrudePram55.AddProfile(extrude_sheet1)
extrudePram55.DirectionType="R"
extrudePram55.DirectionParameter1="50000"
extrudePram55.SweepDirection="+Z"
extrudePram55.RefByGeometricMethod=True
extrude46 = part.CreateLinearSweep(solid6,"*",extrudePram55,False)
extrudePram56 = part.CreateLinearSweepParam()
extrudePram56.Name="積-押し出し46"
extrudePram56.AddProfile(extrude_sheet2)
extrudePram56.DirectionType="N"
extrudePram56.DirectionParameter1="50000"
extrudePram56.SweepDirection="+Z"
extrudePram56.RefByGeometricMethod=True
extrude47 = part.CreateLinearSweep(solid6,"*",extrudePram56,False)
extrudePram57 = part.CreateLinearSweepParam()
extrudePram57.Name="積-押し出し41"
extrudePram57.AddProfile(extrude_sheet4)
extrudePram57.DirectionType="R"
extrudePram57.DirectionParameter1="50000"
extrudePram57.SweepDirection="+Z"
extrudePram57.RefByGeometricMethod=True
extrude48 = part.CreateLinearSweep(solid14,"*",extrudePram57,False)
extrudePram58 = part.CreateLinearSweepParam()
extrudePram58.Name="積-押し出し42"
extrudePram58.AddProfile(extrude_sheet1)
extrudePram58.DirectionType="N"
extrudePram58.DirectionParameter1="50000"
extrudePram58.SweepDirection="+Z"
extrudePram58.RefByGeometricMethod=True
extrude49 = part.CreateLinearSweep(solid14,"*",extrudePram58,False)
mirror_copied131 = part.MirrorCopy([profile72[0]],"PL,Y","")
part.SetElementColor(mirror_copied131[0],"255","0","0","0.19999998807907104")
mirror_copied132 = part.MirrorCopy([profile26[0]],"PL,Y","")
part.SetElementColor(mirror_copied132[0],"255","0","0","0.19999998807907104")
mirror_copied133 = part.MirrorCopy([profile66[0]],"PL,Y","")
part.SetElementColor(mirror_copied133[0],"255","0","0","0.19999998807907104")
solid16 = part.CreateSolid("HK.Casing.Wall.Side.ABP","","SS400")
part.SetElementColor(solid16,"139","69","19","0.79999995231628418")
thicken16 = part.CreateThicken("厚み付け9",solid16,"+",[extrude_sheet6],"-","10","0","0",False,False)
extrudePram59 = part.CreateLinearSweepParam()
extrudePram59.Name="積-押し出し13"
extrudePram59.AddProfile(skt_pl4+",Edge00")
extrudePram59.DirectionType="N"
extrudePram59.DirectionParameter1="50000"
extrudePram59.SweepDirection="+Z"
extrudePram59.RefByGeometricMethod=True
extrude50 = part.CreateLinearSweep(solid16,"*",extrudePram59,False)
extrudePram60 = part.CreateLinearSweepParam()
extrudePram60.Name="積-押し出し14"
extrudePram60.AddProfile(extrude_sheet1)
extrudePram60.DirectionType="R"
extrudePram60.DirectionParameter1="50000"
extrudePram60.SweepDirection="+Z"
extrudePram60.RefByGeometricMethod=True
extrude51 = part.CreateLinearSweep(solid16,"*",extrudePram60,False)
extrudePram61 = part.CreateLinearSweepParam()
extrudePram61.Name="積-押し出し15"
extrudePram61.AddProfile(extrude_sheet2)
extrudePram61.DirectionType="N"
extrudePram61.DirectionParameter1="50000"
extrudePram61.SweepDirection="+Z"
extrudePram61.RefByGeometricMethod=True
extrude52 = part.CreateLinearSweep(solid16,"*",extrudePram61,False)
mirror_copied135 = part.MirrorCopy([profile7[0]],"PL,Y","")
part.SetElementColor(mirror_copied135[0],"255","0","0","0.19999998807907104")
mirror_copied136 = part.MirrorCopy([profile52[0]],"PL,Y","")
part.SetElementColor(mirror_copied136[0],"255","0","0","0.19999998807907104")
mirror_copied137 = part.MirrorCopy([profile120[0]],"PL,Y","")
part.SetElementColor(mirror_copied137[0],"148","0","211","0.39999997615814209")
mirror_copied138 = part.MirrorCopy([profile111[0]],"PL,Y","")
part.SetElementColor(mirror_copied138[0],"255","0","0","0.19999998807907104")
mirror_copied139 = part.MirrorCopy([profile100[0]],"PL,Y","")
part.SetElementColor(mirror_copied139[0],"255","0","0","0.19999998807907104")
mirror_copied141 = part.MirrorCopy([profile42[0]],"PL,Y","")
part.SetElementColor(mirror_copied141[0],"148","0","211","0.39999997615814209")
mirror_copied146 = part.MirrorCopy([profile39[0]],"PL,Y","")
part.SetElementColor(mirror_copied146[0],"148","0","211","0.39999997615814209")
mirror_copied147 = part.MirrorCopy([profile98[1]],"PL,Y","")
part.SetElementColor(mirror_copied147[0],"148","0","211","0.39999997615814209")
mirror_copied149 = part.MirrorCopy([profile55[0]],"PL,Y","")
part.SetElementColor(mirror_copied149[0],"255","0","0","0.19999998807907104")
mirror_copied153 = part.MirrorCopy([profile117[0]],"PL,Y","")
part.SetElementColor(mirror_copied153[0],"255","0","0","0.19999998807907104")
mirror_copied154 = part.MirrorCopy([profile8[0]],"PL,Y","")
part.SetElementColor(mirror_copied154[0],"255","0","0","0.19999998807907104")
mirror_copied155 = part.MirrorCopy([solid12],"PL,Y","")
part.SetElementColor(mirror_copied155[0],"139","69","19","0.79999995231628418")
mirror_copied158 = part.MirrorCopy([profile37[0]],"PL,Y","")
part.SetElementColor(mirror_copied158[0],"148","0","211","0.39999997615814209")
mirror_copied160 = part.MirrorCopy([profile96[0]],"PL,Y","")
part.SetElementColor(mirror_copied160[0],"148","0","211","0.39999997615814209")
mirror_copied161 = part.MirrorCopy([profile108[0]],"PL,Y","")
part.SetElementColor(mirror_copied161[0],"255","0","0","0.19999998807907104")
mirror_copied162 = part.MirrorCopy([profile120[1]],"PL,Y","")
part.SetElementColor(mirror_copied162[0],"148","0","211","0.39999997615814209")
mirror_copied166 = part.MirrorCopy([profile89[0]],"PL,Y","")
part.SetElementColor(mirror_copied166[0],"255","0","0","0.19999998807907104")
mirror_copied167 = part.MirrorCopy([profile105[0]],"PL,Y","")
part.SetElementColor(mirror_copied167[0],"255","0","0","0.19999998807907104")
mirror_copied171 = part.MirrorCopy([profile109[0]],"PL,Y","")
part.SetElementColor(mirror_copied171[0],"255","0","0","0.19999998807907104")
mirror_copied173 = part.MirrorCopy([profile59[0]],"PL,Y","")
part.SetElementColor(mirror_copied173[0],"148","0","211","0.39999997615814209")
mirror_copied174 = part.MirrorCopy([profile103[0]],"PL,Y","")
part.SetElementColor(mirror_copied174[0],"255","0","0","0.19999998807907104")
mirror_copied175 = part.MirrorCopy([profile20[0]],"PL,Y","")
part.SetElementColor(mirror_copied175[0],"255","0","0","0.19999998807907104")
mirror_copied176 = part.MirrorCopy([profile14[0]],"PL,Y","")
part.SetElementColor(mirror_copied176[0],"148","0","211","0.39999997615814209")
mirror_copied177 = part.MirrorCopy([profile4[0]],"PL,Y","")
part.SetElementColor(mirror_copied177[0],"255","0","0","0.19999998807907104")
mirror_copied179 = part.MirrorCopy([profile77[0]],"PL,Y","")
part.SetElementColor(mirror_copied179[0],"148","0","211","0.39999997615814209")
mirror_copied180 = part.MirrorCopy([profile104[0]],"PL,Y","")
part.SetElementColor(mirror_copied180[0],"255","0","0","0.19999998807907104")
mirror_copied183 = part.MirrorCopy([profile28[0]],"PL,Y","")
part.SetElementColor(mirror_copied183[0],"255","0","0","0.19999998807907104")
mirror_copied184 = part.MirrorCopy([profile1[0]],"PL,Y","")
part.SetElementColor(mirror_copied184[0],"148","0","211","0.39999997615814209")
mirror_copied185 = part.MirrorCopy([profile32[0]],"PL,Y","")
part.SetElementColor(mirror_copied185[0],"255","0","0","0.19999998807907104")
mirror_copied187 = part.MirrorCopy([solid16],"PL,Y","")
part.SetElementColor(mirror_copied187[0],"139","69","19","0.79999995231628418")
mirror_copied190 = part.MirrorCopy([profile69[0]],"PL,Y","")
part.SetElementColor(mirror_copied190[0],"255","0","0","0.19999998807907104")