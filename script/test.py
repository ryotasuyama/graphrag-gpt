import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("HK.Ax.Deck","","PL,X","0",False,False,False,"","","",True,False)
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
var_elm1 = part.CreateVariable("Casing.DL03","2400","mm","")
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
extrudePram3.AddProfile(skt_pl2+",Casing.Fore")
extrudePram3.DirectionType="2"
extrudePram3.DirectionParameter1="50000"
extrudePram3.DirectionParameter2="10000"
extrudePram3.SweepDirection="+Z"
extrudePram3.Name="HK.Casing.Wall.Fore"
extrudePram3.MaterialName="SS400"
extrudePram3.IntervalSweep=False
extrude_sheet3 = part.CreateLinearSweepSheet(extrudePram3,False)
part.SheetAlignNormal(extrude_sheet3,1,0,0)
part.BlankElement(extrude_sheet3,True)
part.SetElementColor(extrude_sheet3,"225","225","225","1")
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType=1
ProfilePram1.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram1.AddAttachSurfaces(extrude_sheet3)
ProfilePram1.ProfileName="HK.Casing.Wall.Fore.DL03.ABP"
ProfilePram1.MaterialName="SS400"
ProfilePram1.ProfileType=1002
ProfilePram1.ProfileParams=["125","75","7","10","5"]
ProfilePram1.Mold="+"
ProfilePram1.ReverseDir=True
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
ProfilePram1.End1ScallopType=1121
ProfilePram1.End1ScallopTypeParams=["25","40"]
ProfilePram1.End2ScallopType=1121
ProfilePram1.End2ScallopTypeParams=["25","40"]
profile1 = part.CreateProfile(ProfilePram1,False)
part.SetElementColor(profile1[0],"255","0","0","0.19999998807907104")
var_elm2 = part.CreateVariable("Casing.DL04","3200","mm","")
ProfilePram2 = part.CreateProfileParam()
ProfilePram2.DefinitionType=1
ProfilePram2.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram2.AddAttachSurfaces(extrude_sheet3)
ProfilePram2.ProfileName="HK.Casing.Wall.Fore.DL04.ABP"
ProfilePram2.MaterialName="SS400"
ProfilePram2.ProfileType=1003
ProfilePram2.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram2.Mold="+"
ProfilePram2.ReverseDir=True
ProfilePram2.ReverseAngle=True
ProfilePram2.CalcSnipOnlyAttachLines=False
ProfilePram2.AttachDirMethod=0
ProfilePram2.CCWDefAngle=False
ProfilePram2.AddEnd1Elements(extrude_sheet1)
ProfilePram2.End1Type=1102
ProfilePram2.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram2.AddEnd2Elements(extrude_sheet2)
ProfilePram2.End2Type=1102
ProfilePram2.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram2.End1ScallopType=1120
ProfilePram2.End1ScallopTypeParams=["50"]
ProfilePram2.End2ScallopType=1120
ProfilePram2.End2ScallopTypeParams=["50"]
profile2 = part.CreateProfile(ProfilePram2,False)
part.SetElementColor(profile2[0],"148","0","211","0.39999997615814209")
extrudePram4 = part.CreateLinearSweepParam()
extrudePram4.AddProfile(skt_pl2+",Casing.Aft")
extrudePram4.DirectionType="2"
extrudePram4.DirectionParameter1="50000"
extrudePram4.DirectionParameter2="10000"
extrudePram4.SweepDirection="+Z"
extrudePram4.Name="HK.Casing.Wall.Aft"
extrudePram4.MaterialName="SS400"
extrudePram4.IntervalSweep=False
extrude_sheet4 = part.CreateLinearSweepSheet(extrudePram4,False)
part.SheetAlignNormal(extrude_sheet4,1,0,0)
part.BlankElement(extrude_sheet4,True)
part.SetElementColor(extrude_sheet4,"225","225","225","1")
ProfilePram3 = part.CreateProfileParam()
ProfilePram3.DefinitionType=1
ProfilePram3.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram3.AddAttachSurfaces(extrude_sheet4)
ProfilePram3.ProfileName="HK.Casing.Wall.Aft.DL04.ABP"
ProfilePram3.MaterialName="SS400"
ProfilePram3.ProfileType=1003
ProfilePram3.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram3.Mold="+"
ProfilePram3.ReverseDir=False
ProfilePram3.ReverseAngle=True
ProfilePram3.CalcSnipOnlyAttachLines=False
ProfilePram3.AttachDirMethod=0
ProfilePram3.CCWDefAngle=False
ProfilePram3.AddEnd1Elements(extrude_sheet1)
ProfilePram3.End1Type=1102
ProfilePram3.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.AddEnd2Elements(extrude_sheet2)
ProfilePram3.End2Type=1102
ProfilePram3.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.End1ScallopType=1120
ProfilePram3.End1ScallopTypeParams=["50"]
ProfilePram3.End2ScallopType=1120
ProfilePram3.End2ScallopTypeParams=["50"]
profile3 = part.CreateProfile(ProfilePram3,False)
part.SetElementColor(profile3[0],"148","0","211","0.39999997615814209")
ProfilePram4 = part.CreateProfileParam()
ProfilePram4.DefinitionType=1
ProfilePram4.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram4.AddAttachSurfaces(extrude_sheet1)
ProfilePram4.ProfileName="HK.Casing.Deck.B.DL04P"
ProfilePram4.MaterialName="SS400"
ProfilePram4.ProfileType=1003
ProfilePram4.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram4.Mold="-"
ProfilePram4.ReverseDir=True
ProfilePram4.ReverseAngle=False
ProfilePram4.CalcSnipOnlyAttachLines=False
ProfilePram4.AttachDirMethod=0
ProfilePram4.CCWDefAngle=False
ProfilePram4.AddEnd1Elements(profile3[0])
ProfilePram4.End1Type=1102
ProfilePram4.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.AddEnd2Elements(profile2[0])
ProfilePram4.End2Type=1102
ProfilePram4.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.End1ScallopType=0
ProfilePram4.End2ScallopType=0
profile4 = part.CreateProfile(ProfilePram4,False)
part.SetElementColor(profile4[0],"148","0","211","0.39999997615814209")
mirror_copied1 = part.MirrorCopy([profile4[0]],"PL,Y","")
part.SetElementColor(mirror_copied1[0],"148","0","211","0.39999997615814209")
var_elm3 = part.CreateVariable("FR14","9770","mm","")
ProfilePram5 = part.CreateProfileParam()
ProfilePram5.DefinitionType=1
ProfilePram5.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram5.AddAttachSurfaces(extrude_sheet1)
ProfilePram5.ProfileName="HK.Casing.Deck.B.FR14F415"
ProfilePram5.MaterialName="SS400"
ProfilePram5.ProfileType=1003
ProfilePram5.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram5.Mold="+"
ProfilePram5.ReverseDir=True
ProfilePram5.ReverseAngle=True
ProfilePram5.CalcSnipOnlyAttachLines=False
ProfilePram5.AttachDirMethod=0
ProfilePram5.CCWDefAngle=False
ProfilePram5.AddEnd1Elements(mirror_copied1[0])
ProfilePram5.End1Type=1111
ProfilePram5.End1TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram5.AddEnd2Elements(profile4[0])
ProfilePram5.End2Type=1111
ProfilePram5.End2TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram5.End1ScallopType=1120
ProfilePram5.End1ScallopTypeParams=["50"]
ProfilePram5.End2ScallopType=1120
ProfilePram5.End2ScallopTypeParams=["50"]
profile5 = part.CreateProfile(ProfilePram5,False)
part.SetElementColor(profile5[0],"255","0","0","0.19999998807907104")
ProfilePram6 = part.CreateProfileParam()
ProfilePram6.DefinitionType=1
ProfilePram6.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram6.AddAttachSurfaces(extrude_sheet1)
ProfilePram6.ProfileName="HK.Casing.Deck.B.DL03.FP"
ProfilePram6.MaterialName="SS400"
ProfilePram6.ProfileType=1002
ProfilePram6.ProfileParams=["125","75","7","10","5"]
ProfilePram6.Mold="+"
ProfilePram6.ReverseDir=True
ProfilePram6.ReverseAngle=True
ProfilePram6.CalcSnipOnlyAttachLines=False
ProfilePram6.AttachDirMethod=0
ProfilePram6.CCWDefAngle=False
ProfilePram6.AddEnd1Elements(profile5[0])
ProfilePram6.End1Type=1102
ProfilePram6.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram6.AddEnd2Elements(profile1[0])
ProfilePram6.End2Type=1102
ProfilePram6.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram6.End1ScallopType=1121
ProfilePram6.End1ScallopTypeParams=["25","40"]
ProfilePram6.End2ScallopType=1121
ProfilePram6.End2ScallopTypeParams=["25","40"]
profile6 = part.CreateProfile(ProfilePram6,False)
part.SetElementColor(profile6[0],"255","0","0","0.19999998807907104")
extrudePram5 = part.CreateLinearSweepParam()
extrudePram5.AddProfile(skt_pl1+",Casing.Deck.C")
extrudePram5.DirectionType="2"
extrudePram5.DirectionParameter1="50000"
extrudePram5.DirectionParameter2="10000"
extrudePram5.SweepDirection="+X"
extrudePram5.Name="HK.Casing.Deck.C"
extrudePram5.MaterialName="SS400"
extrudePram5.IntervalSweep=False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudePram5,False)
part.SheetAlignNormal(extrude_sheet5,-0,0,1)
part.BlankElement(extrude_sheet5,True)
part.SetElementColor(extrude_sheet5,"225","225","225","1")
extrudePram6 = part.CreateLinearSweepParam()
extrudePram6.AddProfile(skt_pl1+",Casing.Deck.D")
extrudePram6.DirectionType="2"
extrudePram6.DirectionParameter1="50000"
extrudePram6.DirectionParameter2="10000"
extrudePram6.SweepDirection="+X"
extrudePram6.Name="HK.Casing.Deck.D"
extrudePram6.MaterialName="SS400"
extrudePram6.IntervalSweep=False
extrude_sheet6 = part.CreateLinearSweepSheet(extrudePram6,False)
part.SheetAlignNormal(extrude_sheet6,-0,0,1)
part.BlankElement(extrude_sheet6,True)
part.SetElementColor(extrude_sheet6,"225","225","225","1")
ProfilePram7 = part.CreateProfileParam()
ProfilePram7.DefinitionType=1
ProfilePram7.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram7.AddAttachSurfaces(extrude_sheet6)
ProfilePram7.ProfileName="HK.Casing.Deck.D.DL04P"
ProfilePram7.MaterialName="SS400"
ProfilePram7.ProfileType=1002
ProfilePram7.ProfileParams=["125","75","7","10","5"]
ProfilePram7.Mold="+"
ProfilePram7.ReverseDir=True
ProfilePram7.ReverseAngle=True
ProfilePram7.CalcSnipOnlyAttachLines=False
ProfilePram7.AttachDirMethod=0
ProfilePram7.CCWDefAngle=False
ProfilePram7.AddEnd1Elements(extrude_sheet4)
ProfilePram7.End1Type=1102
ProfilePram7.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.AddEnd2Elements(extrude_sheet3)
ProfilePram7.End2Type=1102
ProfilePram7.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.End1ScallopType=1120
ProfilePram7.End1ScallopTypeParams=["50"]
ProfilePram7.End2ScallopType=1120
ProfilePram7.End2ScallopTypeParams=["50"]
profile7 = part.CreateProfile(ProfilePram7,False)
part.SetElementColor(profile7[0],"255","0","0","0.19999998807907104")
ProfilePram8 = part.CreateProfileParam()
ProfilePram8.DefinitionType=1
ProfilePram8.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram8.AddAttachSurfaces(extrude_sheet4)
ProfilePram8.ProfileName="HK.Casing.Wall.Aft.DL04.CDP"
ProfilePram8.MaterialName="SS400"
ProfilePram8.ProfileType=1002
ProfilePram8.ProfileParams=["125","75","7","10","5"]
ProfilePram8.Mold="+"
ProfilePram8.ReverseDir=False
ProfilePram8.ReverseAngle=True
ProfilePram8.CalcSnipOnlyAttachLines=False
ProfilePram8.AttachDirMethod=0
ProfilePram8.CCWDefAngle=False
ProfilePram8.AddEnd1Elements(profile7[0])
ProfilePram8.End1Type=1102
ProfilePram8.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram8.AddEnd2Elements(extrude_sheet5)
ProfilePram8.End2Type=1102
ProfilePram8.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram8.End1ScallopType=1120
ProfilePram8.End1ScallopTypeParams=["50"]
ProfilePram8.End2ScallopType=1120
ProfilePram8.End2ScallopTypeParams=["50"]
profile8 = part.CreateProfile(ProfilePram8,False)
part.SetElementColor(profile8[0],"255","0","0","0.19999998807907104")
mirror_copied2 = part.MirrorCopy([profile8[0]],"PL,Y","")
part.SetElementColor(mirror_copied2[0],"255","0","0","0.19999998807907104")
ProfilePram9 = part.CreateProfileParam()
ProfilePram9.DefinitionType=1
ProfilePram9.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram9.AddAttachSurfaces(extrude_sheet6)
ProfilePram9.ProfileName="HK.Casing.Deck.D.DL03P"
ProfilePram9.MaterialName="SS400"
ProfilePram9.ProfileType=1002
ProfilePram9.ProfileParams=["125","75","7","10","5"]
ProfilePram9.Mold="+"
ProfilePram9.ReverseDir=True
ProfilePram9.ReverseAngle=True
ProfilePram9.CalcSnipOnlyAttachLines=False
ProfilePram9.AttachDirMethod=0
ProfilePram9.CCWDefAngle=False
ProfilePram9.AddEnd1Elements(extrude_sheet4)
ProfilePram9.End1Type=1102
ProfilePram9.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.AddEnd2Elements(extrude_sheet3)
ProfilePram9.End2Type=1102
ProfilePram9.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.End1ScallopType=1120
ProfilePram9.End1ScallopTypeParams=["50"]
ProfilePram9.End2ScallopType=1120
ProfilePram9.End2ScallopTypeParams=["50"]
profile9 = part.CreateProfile(ProfilePram9,False)
part.SetElementColor(profile9[0],"255","0","0","0.19999998807907104")
ProfilePram10 = part.CreateProfileParam()
ProfilePram10.DefinitionType=1
ProfilePram10.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram10.AddAttachSurfaces(extrude_sheet3)
ProfilePram10.ProfileName="HK.Casing.Wall.Fore.DL04.BCP"
ProfilePram10.MaterialName="SS400"
ProfilePram10.ProfileType=1003
ProfilePram10.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram10.Mold="+"
ProfilePram10.ReverseDir=True
ProfilePram10.ReverseAngle=True
ProfilePram10.CalcSnipOnlyAttachLines=False
ProfilePram10.AttachDirMethod=0
ProfilePram10.CCWDefAngle=False
ProfilePram10.AddEnd1Elements(extrude_sheet5)
ProfilePram10.End1Type=1102
ProfilePram10.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram10.AddEnd2Elements(extrude_sheet1)
ProfilePram10.End2Type=1102
ProfilePram10.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram10.End1ScallopType=1120
ProfilePram10.End1ScallopTypeParams=["50"]
ProfilePram10.End2ScallopType=1120
ProfilePram10.End2ScallopTypeParams=["50"]
profile10 = part.CreateProfile(ProfilePram10,False)
part.SetElementColor(profile10[0],"148","0","211","0.39999997615814209")
ProfilePram11 = part.CreateProfileParam()
ProfilePram11.DefinitionType=1
ProfilePram11.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram11.AddAttachSurfaces(extrude_sheet4)
ProfilePram11.ProfileName="HK.Casing.Wall.Aft.DL04.BCP"
ProfilePram11.MaterialName="SS400"
ProfilePram11.ProfileType=1003
ProfilePram11.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram11.Mold="+"
ProfilePram11.ReverseDir=False
ProfilePram11.ReverseAngle=True
ProfilePram11.CalcSnipOnlyAttachLines=False
ProfilePram11.AttachDirMethod=0
ProfilePram11.CCWDefAngle=False
ProfilePram11.AddEnd1Elements(extrude_sheet5)
ProfilePram11.End1Type=1102
ProfilePram11.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram11.AddEnd2Elements(extrude_sheet1)
ProfilePram11.End2Type=1102
ProfilePram11.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram11.End1ScallopType=1120
ProfilePram11.End1ScallopTypeParams=["50"]
ProfilePram11.End2ScallopType=1120
ProfilePram11.End2ScallopTypeParams=["50"]
profile11 = part.CreateProfile(ProfilePram11,False)
part.SetElementColor(profile11[0],"148","0","211","0.39999997615814209")
ProfilePram12 = part.CreateProfileParam()
ProfilePram12.DefinitionType=1
ProfilePram12.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram12.AddAttachSurfaces(extrude_sheet5)
ProfilePram12.ProfileName="HK.Casing.Deck.C.DL04P"
ProfilePram12.MaterialName="SS400"
ProfilePram12.ProfileType=1003
ProfilePram12.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram12.Mold="-"
ProfilePram12.ReverseDir=True
ProfilePram12.ReverseAngle=False
ProfilePram12.CalcSnipOnlyAttachLines=False
ProfilePram12.AttachDirMethod=0
ProfilePram12.CCWDefAngle=False
ProfilePram12.AddEnd1Elements(profile11[0])
ProfilePram12.End1Type=1102
ProfilePram12.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.AddEnd2Elements(profile10[0])
ProfilePram12.End2Type=1102
ProfilePram12.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.End1ScallopType=0
ProfilePram12.End2ScallopType=0
profile12 = part.CreateProfile(ProfilePram12,False)
part.SetElementColor(profile12[0],"148","0","211","0.39999997615814209")
mirror_copied3 = part.MirrorCopy([profile12[0]],"PL,Y","")
part.SetElementColor(mirror_copied3[0],"148","0","211","0.39999997615814209")
ProfilePram13 = part.CreateProfileParam()
ProfilePram13.DefinitionType=1
ProfilePram13.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram13.AddAttachSurfaces(extrude_sheet5)
ProfilePram13.ProfileName="HK.Casing.Deck.C.FR14F415"
ProfilePram13.MaterialName="SS400"
ProfilePram13.ProfileType=1003
ProfilePram13.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram13.Mold="+"
ProfilePram13.ReverseDir=True
ProfilePram13.ReverseAngle=True
ProfilePram13.CalcSnipOnlyAttachLines=False
ProfilePram13.AttachDirMethod=0
ProfilePram13.CCWDefAngle=False
ProfilePram13.AddEnd1Elements(mirror_copied3[0])
ProfilePram13.End1Type=1111
ProfilePram13.End1TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram13.AddEnd2Elements(profile12[0])
ProfilePram13.End2Type=1111
ProfilePram13.End2TypeParams=["0","35","50","50","25","29.999999999999996","0"]
ProfilePram13.End1ScallopType=1120
ProfilePram13.End1ScallopTypeParams=["50"]
ProfilePram13.End2ScallopType=1120
ProfilePram13.End2ScallopTypeParams=["50"]
profile13 = part.CreateProfile(ProfilePram13,False)
part.SetElementColor(profile13[0],"255","0","0","0.19999998807907104")
ProfilePram14 = part.CreateProfileParam()
ProfilePram14.DefinitionType=1
ProfilePram14.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram14.AddAttachSurfaces(extrude_sheet3)
ProfilePram14.ProfileName="HK.Casing.Wall.Fore.DL03.BCP"
ProfilePram14.MaterialName="SS400"
ProfilePram14.ProfileType=1002
ProfilePram14.ProfileParams=["125","75","7","10","5"]
ProfilePram14.Mold="+"
ProfilePram14.ReverseDir=True
ProfilePram14.ReverseAngle=True
ProfilePram14.CalcSnipOnlyAttachLines=False
ProfilePram14.AttachDirMethod=0
ProfilePram14.CCWDefAngle=False
ProfilePram14.AddEnd1Elements(extrude_sheet5)
ProfilePram14.End1Type=1102
ProfilePram14.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.AddEnd2Elements(extrude_sheet1)
ProfilePram14.End2Type=1102
ProfilePram14.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.End1ScallopType=1121
ProfilePram14.End1ScallopTypeParams=["25","40"]
ProfilePram14.End2ScallopType=1121
ProfilePram14.End2ScallopTypeParams=["25","40"]
profile14 = part.CreateProfile(ProfilePram14,False)
part.SetElementColor(profile14[0],"255","0","0","0.19999998807907104")
ProfilePram15 = part.CreateProfileParam()
ProfilePram15.DefinitionType=1
ProfilePram15.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram15.AddAttachSurfaces(extrude_sheet5)
ProfilePram15.ProfileName="HK.Casing.Deck.C.DL03.FP"
ProfilePram15.MaterialName="SS400"
ProfilePram15.ProfileType=1002
ProfilePram15.ProfileParams=["125","75","7","10","5"]
ProfilePram15.Mold="+"
ProfilePram15.ReverseDir=True
ProfilePram15.ReverseAngle=True
ProfilePram15.CalcSnipOnlyAttachLines=False
ProfilePram15.AttachDirMethod=0
ProfilePram15.CCWDefAngle=False
ProfilePram15.AddEnd1Elements(profile13[0])
ProfilePram15.End1Type=1102
ProfilePram15.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram15.AddEnd2Elements(profile14[0])
ProfilePram15.End2Type=1102
ProfilePram15.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram15.End1ScallopType=1121
ProfilePram15.End1ScallopTypeParams=["25","40"]
ProfilePram15.End2ScallopType=1121
ProfilePram15.End2ScallopTypeParams=["25","40"]
profile15 = part.CreateProfile(ProfilePram15,False)
part.SetElementColor(profile15[0],"255","0","0","0.19999998807907104")
mirror_copied4 = part.MirrorCopy([profile15[0]],"PL,Y","")
part.SetElementColor(mirror_copied4[0],"255","0","0","0.19999998807907104")
extrudePram7 = part.CreateLinearSweepParam()
extrudePram7.AddProfile(skt_pl2+",Casing.Side.P")
extrudePram7.DirectionType="2"
extrudePram7.DirectionParameter1="50000"
extrudePram7.DirectionParameter2="10000"
extrudePram7.SweepDirection="+Z"
extrudePram7.Name="HK.Casing.Wall.SideP"
extrudePram7.MaterialName="SS400"
extrudePram7.IntervalSweep=False
extrude_sheet7 = part.CreateLinearSweepSheet(extrudePram7,False)
part.SheetAlignNormal(extrude_sheet7,0,-1,0)
part.BlankElement(extrude_sheet7,True)
part.SetElementColor(extrude_sheet7,"225","225","225","1")
var_elm4 = part.CreateVariable("FR12","8170","mm","")
ProfilePram16 = part.CreateProfileParam()
ProfilePram16.DefinitionType=1
ProfilePram16.BasePlane="PL,O,"+var_elm4+","+"X"
ProfilePram16.AddAttachSurfaces(extrude_sheet7)
ProfilePram16.ProfileName="HK.Casing.Wall.Side.FR12.CDP"
ProfilePram16.MaterialName="SS400"
ProfilePram16.ProfileType=1002
ProfilePram16.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram16.Mold="+"
ProfilePram16.ReverseDir=False
ProfilePram16.ReverseAngle=True
ProfilePram16.CalcSnipOnlyAttachLines=False
ProfilePram16.AttachDirMethod=0
ProfilePram16.CCWDefAngle=False
ProfilePram16.AddEnd1Elements(extrude_sheet6)
ProfilePram16.End1Type=1102
ProfilePram16.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.AddEnd2Elements(extrude_sheet5)
ProfilePram16.End2Type=1102
ProfilePram16.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.End1ScallopType=1121
ProfilePram16.End1ScallopTypeParams=["35","40"]
ProfilePram16.End2ScallopType=1121
ProfilePram16.End2ScallopTypeParams=["35","40"]
profile16 = part.CreateProfile(ProfilePram16,False)
part.SetElementColor(profile16[0],"255","0","0","0.19999998807907104")
mirror_copied5 = part.MirrorCopy([profile16[0]],"PL,Y","")
part.SetElementColor(mirror_copied5[0],"255","0","0","0.19999998807907104")
solid1 = part.CreateSolid("HK.Casing.Deck.C","","SS400")
part.SetElementColor(solid1,"139","69","19","0.78999996185302734")
thicken1 = part.CreateThicken("厚み付け4",solid1,"+",[extrude_sheet5],"+","10","0","0",False,False)
skt_pl3 = part.CreateSketchPlane("HK.Az.Deck.D","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl3,True)
skt_layer11 = part.CreateSketchLayer("Edge00",skt_pl3)
skt_ln19 = part.CreateSketchLine(skt_pl3,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln20 = part.CreateSketchLine(skt_pl3,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln21 = part.CreateSketchLine(skt_pl3,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln22 = part.CreateSketchLine(skt_pl3,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer12 = part.CreateSketchLayer("Edge01",skt_pl3)
skt_arc1 = part.CreateSketchArc(skt_pl3,"","Edge01","6345.0000000000009,1195.0000000000002","6345,1495.0000000000002","6045.0000000000009,1195",True,False)
skt_ln23 = part.CreateSketchLine(skt_pl3,"","Edge01","8580,1495","6345,1495",False)
skt_arc2 = part.CreateSketchArc(skt_pl3,"","Edge01","8580,1195","8880,1195.0000000000002","8580,1495.0000000000007",True,False)
skt_ln24 = part.CreateSketchLine(skt_pl3,"","Edge01","8880,-1195","8880,1195.0000000000005",False)
skt_arc3 = part.CreateSketchArc(skt_pl3,"","Edge01","8580,-1195.0000000000002","8580,-1495.0000000000002","8880,-1195",True,False)
skt_ln25 = part.CreateSketchLine(skt_pl3,"","Edge01","6345,-1495","8580,-1495",False)
skt_arc4 = part.CreateSketchArc(skt_pl3,"","Edge01","6345.0000000000009,-1195","6045.0000000000009,-1195.0000000000002","6345,-1494.9999999999998",True,False)
skt_ln26 = part.CreateSketchLine(skt_pl3,"","Edge01","6045,1195","6045,-1195.0000000000005",False)
var_elm5 = part.CreateVariable("Casing.DL00","0","mm","")
ProfilePram17 = part.CreateProfileParam()
ProfilePram17.DefinitionType=1
ProfilePram17.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram17.AddAttachSurfaces(extrude_sheet3)
ProfilePram17.ProfileName="HK.Casing.Wall.Fore.DL00.AB"
ProfilePram17.MaterialName="SS400"
ProfilePram17.ProfileType=1002
ProfilePram17.ProfileParams=["125","75","7","10","5"]
ProfilePram17.Mold="+"
ProfilePram17.ReverseDir=True
ProfilePram17.ReverseAngle=True
ProfilePram17.CalcSnipOnlyAttachLines=False
ProfilePram17.AttachDirMethod=0
ProfilePram17.CCWDefAngle=False
ProfilePram17.AddEnd1Elements(extrude_sheet1)
ProfilePram17.End1Type=1102
ProfilePram17.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.AddEnd2Elements(extrude_sheet2)
ProfilePram17.End2Type=1102
ProfilePram17.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.End1ScallopType=1121
ProfilePram17.End1ScallopTypeParams=["25","40"]
ProfilePram17.End2ScallopType=1121
ProfilePram17.End2ScallopTypeParams=["25","40"]
profile17 = part.CreateProfile(ProfilePram17,False)
part.SetElementColor(profile17[0],"255","0","0","0.19999998807907104")
ProfilePram18 = part.CreateProfileParam()
ProfilePram18.DefinitionType=1
ProfilePram18.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram18.AddAttachSurfaces(extrude_sheet3)
ProfilePram18.ProfileName="HK.Casing.Wall.Fore.DL03.CDP"
ProfilePram18.MaterialName="SS400"
ProfilePram18.ProfileType=1002
ProfilePram18.ProfileParams=["125","75","7","10","5"]
ProfilePram18.Mold="+"
ProfilePram18.ReverseDir=True
ProfilePram18.ReverseAngle=True
ProfilePram18.CalcSnipOnlyAttachLines=False
ProfilePram18.AttachDirMethod=0
ProfilePram18.CCWDefAngle=False
ProfilePram18.AddEnd1Elements(profile9[0])
ProfilePram18.End1Type=1102
ProfilePram18.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram18.AddEnd2Elements(extrude_sheet5)
ProfilePram18.End2Type=1102
ProfilePram18.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram18.End1ScallopType=1120
ProfilePram18.End1ScallopTypeParams=["50"]
ProfilePram18.End2ScallopType=1120
ProfilePram18.End2ScallopTypeParams=["50"]
profile18 = part.CreateProfile(ProfilePram18,False)
part.SetElementColor(profile18[0],"255","0","0","0.19999998807907104")
var_elm6 = part.CreateVariable("FR11","7370","mm","")
ProfilePram19 = part.CreateProfileParam()
ProfilePram19.DefinitionType=1
ProfilePram19.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram19.AddAttachSurfaces(extrude_sheet7)
ProfilePram19.ProfileName="HK.Casing.Wall.Side.FR11.CDP"
ProfilePram19.MaterialName="SS400"
ProfilePram19.ProfileType=1002
ProfilePram19.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram19.Mold="+"
ProfilePram19.ReverseDir=False
ProfilePram19.ReverseAngle=True
ProfilePram19.CalcSnipOnlyAttachLines=False
ProfilePram19.AttachDirMethod=0
ProfilePram19.CCWDefAngle=False
ProfilePram19.AddEnd1Elements(extrude_sheet6)
ProfilePram19.End1Type=1102
ProfilePram19.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram19.AddEnd2Elements(extrude_sheet5)
ProfilePram19.End2Type=1102
ProfilePram19.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram19.End1ScallopType=1121
ProfilePram19.End1ScallopTypeParams=["35","40"]
ProfilePram19.End2ScallopType=1121
ProfilePram19.End2ScallopTypeParams=["35","40"]
profile19 = part.CreateProfile(ProfilePram19,False)
part.SetElementColor(profile19[0],"255","0","0","0.19999998807907104")
var_elm7 = part.CreateVariable("FR15","10570","mm","")
ProfilePram20 = part.CreateProfileParam()
ProfilePram20.DefinitionType=1
ProfilePram20.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram20.AddAttachSurfaces(extrude_sheet7)
ProfilePram20.ProfileName="HK.Casing.Wall.Side.FR15.CDP"
ProfilePram20.MaterialName="SS400"
ProfilePram20.ProfileType=1002
ProfilePram20.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram20.Mold="+"
ProfilePram20.ReverseDir=False
ProfilePram20.ReverseAngle=True
ProfilePram20.CalcSnipOnlyAttachLines=False
ProfilePram20.AttachDirMethod=0
ProfilePram20.CCWDefAngle=False
ProfilePram20.AddEnd1Elements(extrude_sheet6)
ProfilePram20.End1Type=1102
ProfilePram20.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.AddEnd2Elements(extrude_sheet5)
ProfilePram20.End2Type=1102
ProfilePram20.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.End1ScallopType=1121
ProfilePram20.End1ScallopTypeParams=["35","40"]
ProfilePram20.End2ScallopType=1121
ProfilePram20.End2ScallopTypeParams=["35","40"]
profile20 = part.CreateProfile(ProfilePram20,False)
part.SetElementColor(profile20[0],"255","0","0","0.19999998807907104")
var_elm8 = part.CreateVariable("Casing.DL02","1600","mm","")
ProfilePram21 = part.CreateProfileParam()
ProfilePram21.DefinitionType=1
ProfilePram21.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram21.AddAttachSurfaces(extrude_sheet6)
ProfilePram21.ProfileName="HK.Casing.Deck.D.DL02P"
ProfilePram21.MaterialName="SS400"
ProfilePram21.FlangeName="HK.Casing.Deck.D.DL02P"
ProfilePram21.FlangeMaterialName="SS400"
ProfilePram21.ProfileType=1201
ProfilePram21.ProfileParams=["200","14","900","10"]
ProfilePram21.Mold="-"
ProfilePram21.ReverseDir=True
ProfilePram21.ReverseAngle=False
ProfilePram21.CalcSnipOnlyAttachLines=False
ProfilePram21.AttachDirMethod=0
ProfilePram21.CCWDefAngle=False
ProfilePram21.AddEnd1Elements(extrude_sheet4)
ProfilePram21.End1Type=1102
ProfilePram21.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram21.AddEnd2Elements(extrude_sheet3)
ProfilePram21.End2Type=1102
ProfilePram21.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram21.End1ScallopType=1120
ProfilePram21.End1ScallopTypeParams=["50"]
ProfilePram21.End2ScallopType=1120
ProfilePram21.End2ScallopTypeParams=["50"]
profile21 = part.CreateProfile(ProfilePram21,False)
part.SetElementColor(profile21[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile21[1],"148","0","211","0.39999997615814209")
ProfilePram22 = part.CreateProfileParam()
ProfilePram22.DefinitionType=1
ProfilePram22.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram22.AddAttachSurfaces(extrude_sheet4)
ProfilePram22.ProfileName="HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram22.MaterialName="SS400"
ProfilePram22.FlangeName="HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram22.FlangeMaterialName="SS400"
ProfilePram22.ProfileType=1201
ProfilePram22.ProfileParams=["150","12","388","10"]
ProfilePram22.Mold="-"
ProfilePram22.ReverseDir=False
ProfilePram22.ReverseAngle=False
ProfilePram22.CalcSnipOnlyAttachLines=False
ProfilePram22.AttachDirMethod=0
ProfilePram22.CCWDefAngle=False
ProfilePram22.AddEnd1Elements(extrude_sheet5)
ProfilePram22.End1Type=1103
ProfilePram22.End1TypeParams=["0"]
ProfilePram22.AddEnd2Elements(extrude_sheet1)
ProfilePram22.End2Type=1103
ProfilePram22.End2TypeParams=["0"]
ProfilePram22.End1ScallopType=1120
ProfilePram22.End1ScallopTypeParams=["50"]
ProfilePram22.End2ScallopType=1120
ProfilePram22.End2ScallopTypeParams=["50"]
profile22 = part.CreateProfile(ProfilePram22,False)
part.SetElementColor(profile22[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile22[1],"148","0","211","0.39999997615814209")
extrudePram8 = part.CreateLinearSweepParam()
extrudePram8.AddProfile(skt_pl1+",General.Deck.UpperDeck")
extrudePram8.DirectionType="2"
extrudePram8.DirectionParameter1="190000"
extrudePram8.DirectionParameter2="10000"
extrudePram8.SweepDirection="+X"
extrudePram8.Name="HK.General.Deck.UpperDeck"
extrudePram8.MaterialName="SS400"
extrudePram8.IntervalSweep=False
extrude_sheet8 = part.CreateLinearSweepSheet(extrudePram8,False)
part.SheetAlignNormal(extrude_sheet8,0,0,-1)
part.BlankElement(extrude_sheet8,True)
part.SetElementColor(extrude_sheet8,"225","225","225","1")
ProfilePram23 = part.CreateProfileParam()
ProfilePram23.DefinitionType=1
ProfilePram23.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram23.AddAttachSurfaces(extrude_sheet3)
ProfilePram23.ProfileName="HK.Casing.Wall.Fore.DL03.OAP"
ProfilePram23.MaterialName="SS400"
ProfilePram23.ProfileType=1002
ProfilePram23.ProfileParams=["125","75","7","10","5"]
ProfilePram23.Mold="+"
ProfilePram23.ReverseDir=True
ProfilePram23.ReverseAngle=True
ProfilePram23.CalcSnipOnlyAttachLines=False
ProfilePram23.AttachDirMethod=0
ProfilePram23.CCWDefAngle=False
ProfilePram23.AddEnd1Elements(extrude_sheet2)
ProfilePram23.End1Type=1102
ProfilePram23.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram23.AddEnd2Elements(extrude_sheet8)
ProfilePram23.End2Type=1102
ProfilePram23.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram23.End1ScallopType=1121
ProfilePram23.End1ScallopTypeParams=["25","40"]
ProfilePram23.End2ScallopType=1121
ProfilePram23.End2ScallopTypeParams=["25","40"]
profile23 = part.CreateProfile(ProfilePram23,False)
part.SetElementColor(profile23[0],"255","0","0","0.19999998807907104")
ProfilePram24 = part.CreateProfileParam()
ProfilePram24.DefinitionType=1
ProfilePram24.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram24.AddAttachSurfaces(extrude_sheet3)
ProfilePram24.ProfileName="HK.Casing.Wall.Fore.DL04.OAP"
ProfilePram24.MaterialName="SS400"
ProfilePram24.ProfileType=1003
ProfilePram24.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram24.Mold="+"
ProfilePram24.ReverseDir=True
ProfilePram24.ReverseAngle=True
ProfilePram24.CalcSnipOnlyAttachLines=False
ProfilePram24.AttachDirMethod=0
ProfilePram24.CCWDefAngle=False
ProfilePram24.AddEnd1Elements(extrude_sheet2)
ProfilePram24.End1Type=1102
ProfilePram24.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.AddEnd2Elements(extrude_sheet8)
ProfilePram24.End2Type=1102
ProfilePram24.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.End1ScallopType=1120
ProfilePram24.End1ScallopTypeParams=["50"]
ProfilePram24.End2ScallopType=1120
ProfilePram24.End2ScallopTypeParams=["50"]
profile24 = part.CreateProfile(ProfilePram24,False)
part.SetElementColor(profile24[0],"148","0","211","0.39999997615814209")
ProfilePram25 = part.CreateProfileParam()
ProfilePram25.DefinitionType=1
ProfilePram25.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram25.AddAttachSurfaces(extrude_sheet4)
ProfilePram25.ProfileName="HK.Casing.Wall.Aft.DL04.OAP"
ProfilePram25.MaterialName="SS400"
ProfilePram25.ProfileType=1003
ProfilePram25.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram25.Mold="+"
ProfilePram25.ReverseDir=False
ProfilePram25.ReverseAngle=True
ProfilePram25.CalcSnipOnlyAttachLines=False
ProfilePram25.AttachDirMethod=0
ProfilePram25.CCWDefAngle=False
ProfilePram25.AddEnd1Elements(extrude_sheet2)
ProfilePram25.End1Type=1102
ProfilePram25.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.AddEnd2Elements(extrude_sheet8)
ProfilePram25.End2Type=1102
ProfilePram25.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.End1ScallopType=1120
ProfilePram25.End1ScallopTypeParams=["50"]
ProfilePram25.End2ScallopType=1120
ProfilePram25.End2ScallopTypeParams=["50"]
profile25 = part.CreateProfile(ProfilePram25,False)
part.SetElementColor(profile25[0],"148","0","211","0.39999997615814209")
ProfilePram26 = part.CreateProfileParam()
ProfilePram26.DefinitionType=1
ProfilePram26.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram26.AddAttachSurfaces(extrude_sheet2)
ProfilePram26.ProfileName="HK.Casing.Deck.A.DL04P"
ProfilePram26.MaterialName="SS400"
ProfilePram26.ProfileType=1003
ProfilePram26.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram26.Mold="-"
ProfilePram26.ReverseDir=True
ProfilePram26.ReverseAngle=False
ProfilePram26.CalcSnipOnlyAttachLines=False
ProfilePram26.AttachDirMethod=0
ProfilePram26.CCWDefAngle=False
ProfilePram26.AddEnd1Elements(profile25[0])
ProfilePram26.End1Type=1102
ProfilePram26.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram26.AddEnd2Elements(profile24[0])
ProfilePram26.End2Type=1102
ProfilePram26.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram26.End1ScallopType=0
ProfilePram26.End2ScallopType=0
profile26 = part.CreateProfile(ProfilePram26,False)
part.SetElementColor(profile26[0],"148","0","211","0.39999997615814209")
mirror_copied6 = part.MirrorCopy([profile26[0]],"PL,Y","")
part.SetElementColor(mirror_copied6[0],"148","0","211","0.39999997615814209")
ProfilePram27 = part.CreateProfileParam()
ProfilePram27.DefinitionType=1
ProfilePram27.BasePlane="PL,O,"+"FR14 + 415 mm"+","+"X"
ProfilePram27.AddAttachSurfaces(extrude_sheet2)
ProfilePram27.ProfileName="HK.Casing.Deck.A.FR14F415"
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
ProfilePram27.AddEnd2Elements(profile26[0])
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
ProfilePram28.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram28.AddAttachSurfaces(extrude_sheet2)
ProfilePram28.ProfileName="HK.Casing.Deck.A.DL03.FP"
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
ProfilePram28.AddEnd2Elements(profile23[0])
ProfilePram28.End2Type=1102
ProfilePram28.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram28.End1ScallopType=1121
ProfilePram28.End1ScallopTypeParams=["25","40"]
ProfilePram28.End2ScallopType=1121
ProfilePram28.End2ScallopTypeParams=["25","40"]
profile28 = part.CreateProfile(ProfilePram28,False)
part.SetElementColor(profile28[0],"255","0","0","0.19999998807907104")
mirror_copied7 = part.MirrorCopy([profile28[0]],"PL,Y","")
part.SetElementColor(mirror_copied7[0],"255","0","0","0.19999998807907104")
var_elm9 = part.CreateVariable("FR8","5360","mm","")
ProfilePram29 = part.CreateProfileParam()
ProfilePram29.DefinitionType=1
ProfilePram29.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram29.AddAttachSurfaces(extrude_sheet7)
ProfilePram29.ProfileName="HK.Casing.Wall.Side.FR08.CDP"
ProfilePram29.MaterialName="SS400"
ProfilePram29.ProfileType=1002
ProfilePram29.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram29.Mold="+"
ProfilePram29.ReverseDir=False
ProfilePram29.ReverseAngle=True
ProfilePram29.CalcSnipOnlyAttachLines=False
ProfilePram29.AttachDirMethod=0
ProfilePram29.CCWDefAngle=False
ProfilePram29.AddEnd1Elements(extrude_sheet6)
ProfilePram29.End1Type=1102
ProfilePram29.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.AddEnd2Elements(extrude_sheet5)
ProfilePram29.End2Type=1102
ProfilePram29.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.End1ScallopType=1121
ProfilePram29.End1ScallopTypeParams=["35","40"]
ProfilePram29.End2ScallopType=1121
ProfilePram29.End2ScallopTypeParams=["35","40"]
profile29 = part.CreateProfile(ProfilePram29,False)
part.SetElementColor(profile29[0],"255","0","0","0.19999998807907104")
mirror_copied8 = part.MirrorCopy([profile29[0]],"PL,Y","")
part.SetElementColor(mirror_copied8[0],"255","0","0","0.19999998807907104")
var_elm10 = part.CreateVariable("FR9","6030","mm","")
ProfilePram30 = part.CreateProfileParam()
ProfilePram30.DefinitionType=1
ProfilePram30.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram30.AddAttachSurfaces(extrude_sheet6)
ProfilePram30.ProfileName="HK.Casing.Deck.D.FR09P"
ProfilePram30.MaterialName="SS400"
ProfilePram30.ProfileType=1003
ProfilePram30.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram30.Mold="+"
ProfilePram30.ReverseDir=True
ProfilePram30.ReverseAngle=False
ProfilePram30.CalcSnipOnlyAttachLines=False
ProfilePram30.AttachDirMethod=0
ProfilePram30.CCWDefAngle=False
ProfilePram30.AddEnd1Elements(profile21[0])
ProfilePram30.End1Type=1102
ProfilePram30.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram30.AddEnd2Elements(extrude_sheet7)
ProfilePram30.End2Type=1102
ProfilePram30.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram30.End1ScallopType=1120
ProfilePram30.End1ScallopTypeParams=["50"]
ProfilePram30.End2ScallopType=1120
ProfilePram30.End2ScallopTypeParams=["50"]
profile30 = part.CreateProfile(ProfilePram30,False)
part.SetElementColor(profile30[0],"148","0","211","0.39999997615814209")
mirror_copied9 = part.MirrorCopy([profile30[0]],"PL,Y","")
part.SetElementColor(mirror_copied9[0],"148","0","211","0.39999997615814209")
var_elm11 = part.CreateVariable("Casing.DL05","4000","mm","")
ProfilePram31 = part.CreateProfileParam()
ProfilePram31.DefinitionType=1
ProfilePram31.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram31.AddAttachSurfaces(extrude_sheet4)
ProfilePram31.ProfileName="HK.Casing.Wall.Aft.DL05.BCP"
ProfilePram31.MaterialName="SS400"
ProfilePram31.ProfileType=1002
ProfilePram31.ProfileParams=["125","75","7","10","5"]
ProfilePram31.Mold="+"
ProfilePram31.ReverseDir=False
ProfilePram31.ReverseAngle=True
ProfilePram31.CalcSnipOnlyAttachLines=False
ProfilePram31.AttachDirMethod=0
ProfilePram31.CCWDefAngle=False
ProfilePram31.AddEnd1Elements(extrude_sheet5)
ProfilePram31.End1Type=1102
ProfilePram31.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram31.AddEnd2Elements(extrude_sheet1)
ProfilePram31.End2Type=1102
ProfilePram31.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram31.End1ScallopType=1121
ProfilePram31.End1ScallopTypeParams=["25","40"]
ProfilePram31.End2ScallopType=1121
ProfilePram31.End2ScallopTypeParams=["25","40"]
profile31 = part.CreateProfile(ProfilePram31,False)
part.SetElementColor(profile31[0],"255","0","0","0.19999998807907104")
var_elm12 = part.CreateVariable("FR13","8970","mm","")
ProfilePram32 = part.CreateProfileParam()
ProfilePram32.DefinitionType=1
ProfilePram32.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram32.AddAttachSurfaces(extrude_sheet7)
ProfilePram32.ProfileName="HK.Casing.Wall.Side.FR13.ABP"
ProfilePram32.MaterialName="SS400"
ProfilePram32.ProfileType=1003
ProfilePram32.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram32.Mold="+"
ProfilePram32.ReverseDir=False
ProfilePram32.ReverseAngle=True
ProfilePram32.CalcSnipOnlyAttachLines=False
ProfilePram32.AttachDirMethod=0
ProfilePram32.CCWDefAngle=False
ProfilePram32.AddEnd1Elements(extrude_sheet1)
ProfilePram32.End1Type=1103
ProfilePram32.End1TypeParams=["0"]
ProfilePram32.AddEnd2Elements(extrude_sheet2)
ProfilePram32.End2Type=1103
ProfilePram32.End2TypeParams=["0"]
ProfilePram32.End1ScallopType=1120
ProfilePram32.End1ScallopTypeParams=["50"]
ProfilePram32.End2ScallopType=1120
ProfilePram32.End2ScallopTypeParams=["50"]
profile32 = part.CreateProfile(ProfilePram32,False)
part.SetElementColor(profile32[0],"148","0","211","0.39999997615814209")
var_elm13 = part.CreateVariable("Casing.DL01","800","mm","")
ProfilePram33 = part.CreateProfileParam()
ProfilePram33.DefinitionType=1
ProfilePram33.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram33.AddAttachSurfaces(extrude_sheet4)
ProfilePram33.ProfileName="HK.Casing.Wall.Aft.DL01.ABP"
ProfilePram33.MaterialName="SS400"
ProfilePram33.ProfileType=1002
ProfilePram33.ProfileParams=["125","75","7","10","5"]
ProfilePram33.Mold="+"
ProfilePram33.ReverseDir=False
ProfilePram33.ReverseAngle=True
ProfilePram33.CalcSnipOnlyAttachLines=False
ProfilePram33.AttachDirMethod=0
ProfilePram33.CCWDefAngle=False
ProfilePram33.AddEnd1Elements(extrude_sheet1)
ProfilePram33.End1Type=1102
ProfilePram33.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram33.AddEnd2Elements(extrude_sheet2)
ProfilePram33.End2Type=1102
ProfilePram33.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram33.End1ScallopType=1121
ProfilePram33.End1ScallopTypeParams=["25","40"]
ProfilePram33.End2ScallopType=1121
ProfilePram33.End2ScallopTypeParams=["25","40"]
profile33 = part.CreateProfile(ProfilePram33,False)
part.SetElementColor(profile33[0],"255","0","0","0.19999998807907104")
solid2 = part.CreateSolid("HK.Casing.Wall.Side.ABP","","SS400")
part.SetElementColor(solid2,"139","69","19","0.79999995231628418")
thicken2 = part.CreateThicken("厚み付け9",solid2,"+",[extrude_sheet7],"-","10","0","0",False,False)
extrudePram9 = part.CreateLinearSweepParam()
extrudePram9.Name="積-押し出し13"
extrudePram9.AddProfile(skt_pl3+",Edge00")
extrudePram9.DirectionType="N"
extrudePram9.DirectionParameter1="50000"
extrudePram9.SweepDirection="+Z"
extrudePram9.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid2,"*",extrudePram9,False)
skt_pl4 = part.CreateSketchPlane("HK.Az.Deck.C","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl4,True)
skt_layer13 = part.CreateSketchLayer("Edge00",skt_pl4)
skt_ln27 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln28 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln29 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln30 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer14 = part.CreateSketchLayer("Edge01",skt_pl4)
skt_ln31 = part.CreateSketchLine(skt_pl4,"","Edge01","9770,3125","4835.0000000000009,3125",False)
skt_ln32 = part.CreateSketchLine(skt_pl4,"","Edge01","10170,-2725","10170,2725",False)
skt_ln33 = part.CreateSketchLine(skt_pl4,"","Edge01","4835.0000000000009,-3125","9770,-3125",False)
skt_ln34 = part.CreateSketchLine(skt_pl4,"","Edge01","4435.0000000000009,2725","4435.0000000000009,-2724.9999999999991",False)
skt_arc5 = part.CreateSketchArc(skt_pl4,"","Edge01","4835.0000000000009,2724.9999999999995","4835.0000000000009,3124.9999999999995","4435.0000000000009,2725",True,False)
skt_arc6 = part.CreateSketchArc(skt_pl4,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3125",True,False)
skt_arc7 = part.CreateSketchArc(skt_pl4,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc8 = part.CreateSketchArc(skt_pl4,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125.0000000000005",True,False)
extrudePram10 = part.CreateLinearSweepParam()
extrudePram10.Name="積-押し出し4"
extrudePram10.AddProfile(skt_pl4+",Edge00")
extrudePram10.DirectionType="N"
extrudePram10.DirectionParameter1="50000"
extrudePram10.SweepDirection="+Z"
extrudePram10.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"*",extrudePram10,False)
var_elm14 = part.CreateVariable("FR6","4019.9999999999995","mm","")
ProfilePram34 = part.CreateProfileParam()
ProfilePram34.DefinitionType=1
ProfilePram34.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram34.AddAttachSurfaces(extrude_sheet5)
ProfilePram34.ProfileName="HK.Casing.Deck.C.FR06F400"
ProfilePram34.MaterialName="SS400"
ProfilePram34.ProfileType=1007
ProfilePram34.ProfileParams=["150","12"]
ProfilePram34.Mold="+"
ProfilePram34.ReverseDir=True
ProfilePram34.ReverseAngle=False
ProfilePram34.CalcSnipOnlyAttachLines=False
ProfilePram34.AttachDirMethod=0
ProfilePram34.CCWDefAngle=False
ProfilePram34.AddEnd1Elements(mirror_copied3[0])
ProfilePram34.End1Type=1102
ProfilePram34.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram34.AddEnd2Elements(profile12[0])
ProfilePram34.End2Type=1102
ProfilePram34.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram34.End1ScallopType=0
ProfilePram34.End2ScallopType=0
profile34 = part.CreateProfile(ProfilePram34,False)
part.SetElementColor(profile34[0],"255","0","0","0.19999998807907104")
mirror_copied10 = part.MirrorCopy([profile23[0]],"PL,Y","")
part.SetElementColor(mirror_copied10[0],"255","0","0","0.19999998807907104")
ProfilePram35 = part.CreateProfileParam()
ProfilePram35.DefinitionType=1
ProfilePram35.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram35.AddAttachSurfaces(extrude_sheet3)
ProfilePram35.ProfileName="HK.Casing.Wall.Fore.DL04.CDP"
ProfilePram35.MaterialName="SS400"
ProfilePram35.ProfileType=1002
ProfilePram35.ProfileParams=["125","75","7","10","5"]
ProfilePram35.Mold="+"
ProfilePram35.ReverseDir=True
ProfilePram35.ReverseAngle=True
ProfilePram35.CalcSnipOnlyAttachLines=False
ProfilePram35.AttachDirMethod=0
ProfilePram35.CCWDefAngle=False
ProfilePram35.AddEnd1Elements(profile7[0])
ProfilePram35.End1Type=1102
ProfilePram35.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram35.AddEnd2Elements(extrude_sheet5)
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
ProfilePram36.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram36.AddAttachSurfaces(extrude_sheet3)
ProfilePram36.ProfileName="HK.Casing.Wall.Fore.DL05.BCP"
ProfilePram36.MaterialName="SS400"
ProfilePram36.ProfileType=1002
ProfilePram36.ProfileParams=["125","75","7","10","5"]
ProfilePram36.Mold="+"
ProfilePram36.ReverseDir=True
ProfilePram36.ReverseAngle=True
ProfilePram36.CalcSnipOnlyAttachLines=False
ProfilePram36.AttachDirMethod=0
ProfilePram36.CCWDefAngle=False
ProfilePram36.AddEnd1Elements(extrude_sheet5)
ProfilePram36.End1Type=1102
ProfilePram36.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram36.AddEnd2Elements(extrude_sheet1)
ProfilePram36.End2Type=1102
ProfilePram36.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram36.End1ScallopType=1121
ProfilePram36.End1ScallopTypeParams=["25","40"]
ProfilePram36.End2ScallopType=1121
ProfilePram36.End2ScallopTypeParams=["25","40"]
profile36 = part.CreateProfile(ProfilePram36,False)
part.SetElementColor(profile36[0],"255","0","0","0.19999998807907104")
ProfilePram37 = part.CreateProfileParam()
ProfilePram37.DefinitionType=1
ProfilePram37.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram37.AddAttachSurfaces(extrude_sheet3)
ProfilePram37.ProfileName="HK.Casing.Wall.Fore.DL01.ABP"
ProfilePram37.MaterialName="SS400"
ProfilePram37.ProfileType=1002
ProfilePram37.ProfileParams=["125","75","7","10","5"]
ProfilePram37.Mold="+"
ProfilePram37.ReverseDir=True
ProfilePram37.ReverseAngle=True
ProfilePram37.CalcSnipOnlyAttachLines=False
ProfilePram37.AttachDirMethod=0
ProfilePram37.CCWDefAngle=False
ProfilePram37.AddEnd1Elements(extrude_sheet1)
ProfilePram37.End1Type=1102
ProfilePram37.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram37.AddEnd2Elements(extrude_sheet2)
ProfilePram37.End2Type=1102
ProfilePram37.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram37.End1ScallopType=1121
ProfilePram37.End1ScallopTypeParams=["25","40"]
ProfilePram37.End2ScallopType=1121
ProfilePram37.End2ScallopTypeParams=["25","40"]
profile37 = part.CreateProfile(ProfilePram37,False)
part.SetElementColor(profile37[0],"255","0","0","0.19999998807907104")
mirror_copied11 = part.MirrorCopy([profile37[0]],"PL,Y","")
part.SetElementColor(mirror_copied11[0],"255","0","0","0.19999998807907104")
ProfilePram38 = part.CreateProfileParam()
ProfilePram38.DefinitionType=1
ProfilePram38.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram38.AddAttachSurfaces(extrude_sheet4)
ProfilePram38.ProfileName="HK.Casing.Wall.Aft.DL02.ABP"
ProfilePram38.MaterialName="SS400"
ProfilePram38.FlangeName="HK.Casing.Wall.Aft.DL02.ABP"
ProfilePram38.FlangeMaterialName="SS400"
ProfilePram38.ProfileType=1201
ProfilePram38.ProfileParams=["150","12","388","10"]
ProfilePram38.Mold="-"
ProfilePram38.ReverseDir=False
ProfilePram38.ReverseAngle=False
ProfilePram38.CalcSnipOnlyAttachLines=False
ProfilePram38.AttachDirMethod=0
ProfilePram38.CCWDefAngle=False
ProfilePram38.AddEnd1Elements(extrude_sheet1)
ProfilePram38.End1Type=1103
ProfilePram38.End1TypeParams=["0"]
ProfilePram38.AddEnd2Elements(extrude_sheet2)
ProfilePram38.End2Type=1103
ProfilePram38.End2TypeParams=["0"]
ProfilePram38.End1ScallopType=1120
ProfilePram38.End1ScallopTypeParams=["50"]
ProfilePram38.End2ScallopType=1120
ProfilePram38.End2ScallopTypeParams=["50"]
profile38 = part.CreateProfile(ProfilePram38,False)
part.SetElementColor(profile38[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile38[1],"148","0","211","0.39999997615814209")
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
skt_arc10 = part.CreateSketchArc(skt_pl5,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3125",True,False)
skt_arc11 = part.CreateSketchArc(skt_pl5,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc12 = part.CreateSketchArc(skt_pl5,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125.0000000000005",True,False)
mirror_copied12 = part.MirrorCopy([profile11[0]],"PL,Y","")
part.SetElementColor(mirror_copied12[0],"148","0","211","0.39999997615814209")
ProfilePram39 = part.CreateProfileParam()
ProfilePram39.DefinitionType=1
ProfilePram39.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram39.AddAttachSurfaces(extrude_sheet3)
ProfilePram39.ProfileName="HK.Casing.Wall.Fore.DL01.OAP"
ProfilePram39.MaterialName="SS400"
ProfilePram39.ProfileType=1002
ProfilePram39.ProfileParams=["125","75","7","10","5"]
ProfilePram39.Mold="+"
ProfilePram39.ReverseDir=True
ProfilePram39.ReverseAngle=True
ProfilePram39.CalcSnipOnlyAttachLines=False
ProfilePram39.AttachDirMethod=0
ProfilePram39.CCWDefAngle=False
ProfilePram39.AddEnd1Elements(extrude_sheet2)
ProfilePram39.End1Type=1102
ProfilePram39.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram39.AddEnd2Elements(extrude_sheet8)
ProfilePram39.End2Type=1102
ProfilePram39.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram39.End1ScallopType=1121
ProfilePram39.End1ScallopTypeParams=["25","40"]
ProfilePram39.End2ScallopType=1121
ProfilePram39.End2ScallopTypeParams=["25","40"]
profile39 = part.CreateProfile(ProfilePram39,False)
part.SetElementColor(profile39[0],"255","0","0","0.19999998807907104")
ProfilePram40 = part.CreateProfileParam()
ProfilePram40.DefinitionType=1
ProfilePram40.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram40.AddAttachSurfaces(extrude_sheet2)
ProfilePram40.ProfileName="HK.Casing.Deck.A.DL01.FP"
ProfilePram40.MaterialName="SS400"
ProfilePram40.ProfileType=1002
ProfilePram40.ProfileParams=["125","75","7","10","5"]
ProfilePram40.Mold="+"
ProfilePram40.ReverseDir=True
ProfilePram40.ReverseAngle=True
ProfilePram40.CalcSnipOnlyAttachLines=False
ProfilePram40.AttachDirMethod=0
ProfilePram40.CCWDefAngle=False
ProfilePram40.AddEnd1Elements(profile27[0])
ProfilePram40.End1Type=1102
ProfilePram40.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram40.AddEnd2Elements(profile39[0])
ProfilePram40.End2Type=1102
ProfilePram40.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram40.End1ScallopType=1121
ProfilePram40.End1ScallopTypeParams=["25","40"]
ProfilePram40.End2ScallopType=1121
ProfilePram40.End2ScallopTypeParams=["25","40"]
profile40 = part.CreateProfile(ProfilePram40,False)
part.SetElementColor(profile40[0],"255","0","0","0.19999998807907104")
mirror_copied13 = part.MirrorCopy([profile40[0]],"PL,Y","")
part.SetElementColor(mirror_copied13[0],"255","0","0","0.19999998807907104")
ProfilePram41 = part.CreateProfileParam()
ProfilePram41.DefinitionType=1
ProfilePram41.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram41.AddAttachSurfaces(extrude_sheet4)
ProfilePram41.ProfileName="HK.Casing.Wall.Aft.DL05.OAP"
ProfilePram41.MaterialName="SS400"
ProfilePram41.ProfileType=1002
ProfilePram41.ProfileParams=["125","75","7","10","5"]
ProfilePram41.Mold="+"
ProfilePram41.ReverseDir=False
ProfilePram41.ReverseAngle=True
ProfilePram41.CalcSnipOnlyAttachLines=False
ProfilePram41.AttachDirMethod=0
ProfilePram41.CCWDefAngle=False
ProfilePram41.AddEnd1Elements(extrude_sheet2)
ProfilePram41.End1Type=1102
ProfilePram41.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram41.AddEnd2Elements(extrude_sheet8)
ProfilePram41.End2Type=1102
ProfilePram41.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram41.End1ScallopType=1121
ProfilePram41.End1ScallopTypeParams=["25","40"]
ProfilePram41.End2ScallopType=1121
ProfilePram41.End2ScallopTypeParams=["25","40"]
profile41 = part.CreateProfile(ProfilePram41,False)
part.SetElementColor(profile41[0],"255","0","0","0.19999998807907104")
mirror_copied14 = part.MirrorCopy([profile41[0]],"PL,Y","")
part.SetElementColor(mirror_copied14[0],"255","0","0","0.19999998807907104")
solid3 = part.CreateSolid("HK.Casing.Wall.Side.BCP","","SS400")
part.SetElementColor(solid3,"139","69","19","0.79999995231628418")
thicken3 = part.CreateThicken("厚み付け8",solid3,"+",[extrude_sheet7],"-","10","0","0",False,False)
extrudePram11 = part.CreateLinearSweepParam()
extrudePram11.Name="積-押し出し10"
extrudePram11.AddProfile(skt_pl3+",Edge00")
extrudePram11.DirectionType="N"
extrudePram11.DirectionParameter1="50000"
extrudePram11.SweepDirection="+Z"
extrudePram11.RefByGeometricMethod=False
extrude3 = part.CreateLinearSweep(solid3,"*",extrudePram11,False)
extrudePram12 = part.CreateLinearSweepParam()
extrudePram12.Name="積-押し出し11"
extrudePram12.AddProfile(extrude_sheet5)
extrudePram12.DirectionType="R"
extrudePram12.DirectionParameter1="50000"
extrudePram12.SweepDirection="+Z"
extrudePram12.RefByGeometricMethod=False
extrude4 = part.CreateLinearSweep(solid3,"*",extrudePram12,False)
extrudePram13 = part.CreateLinearSweepParam()
extrudePram13.Name="積-押し出し12"
extrudePram13.AddProfile(extrude_sheet1)
extrudePram13.DirectionType="N"
extrudePram13.DirectionParameter1="50000"
extrudePram13.SweepDirection="+Z"
extrudePram13.RefByGeometricMethod=False
extrude5 = part.CreateLinearSweep(solid3,"*",extrudePram13,False)
mirror_copied15 = part.MirrorCopy([solid3],"PL,Y","")
part.SetElementColor(mirror_copied15[0],"139","69","19","0.79999995231628418")
extrudePram14 = part.CreateLinearSweepParam()
extrudePram14.AddProfile(skt_pl2+",Casing.Side.S")
extrudePram14.DirectionType="2"
extrudePram14.DirectionParameter1="50000"
extrudePram14.DirectionParameter2="10000"
extrudePram14.SweepDirection="+Z"
extrudePram14.Name="HK.Casing.Wall.SideS"
extrudePram14.MaterialName="SS400"
extrudePram14.IntervalSweep=False
extrude_sheet9 = part.CreateLinearSweepSheet(extrudePram14,False)
part.SheetAlignNormal(extrude_sheet9,0,-1,0)
part.BlankElement(extrude_sheet9,True)
part.SetElementColor(extrude_sheet9,"225","225","225","1")
ProfilePram42 = part.CreateProfileParam()
ProfilePram42.DefinitionType=1
ProfilePram42.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram42.AddAttachSurfaces(extrude_sheet7)
ProfilePram42.ProfileName="HK.Casing.Wall.Side.FR13.BCP"
ProfilePram42.MaterialName="SS400"
ProfilePram42.ProfileType=1003
ProfilePram42.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram42.Mold="+"
ProfilePram42.ReverseDir=False
ProfilePram42.ReverseAngle=True
ProfilePram42.CalcSnipOnlyAttachLines=False
ProfilePram42.AttachDirMethod=0
ProfilePram42.CCWDefAngle=False
ProfilePram42.AddEnd1Elements(extrude_sheet5)
ProfilePram42.End1Type=1103
ProfilePram42.End1TypeParams=["0"]
ProfilePram42.AddEnd2Elements(extrude_sheet1)
ProfilePram42.End2Type=1103
ProfilePram42.End2TypeParams=["0"]
ProfilePram42.End1ScallopType=1120
ProfilePram42.End1ScallopTypeParams=["50"]
ProfilePram42.End2ScallopType=1120
ProfilePram42.End2ScallopTypeParams=["50"]
profile42 = part.CreateProfile(ProfilePram42,False)
part.SetElementColor(profile42[0],"148","0","211","0.39999997615814209")
ProfilePram43 = part.CreateProfileParam()
ProfilePram43.DefinitionType=1
ProfilePram43.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram43.AddAttachSurfaces(extrude_sheet7)
ProfilePram43.ProfileName="HK.Casing.Wall.Side.FR13.OAP"
ProfilePram43.MaterialName="SS400"
ProfilePram43.ProfileType=1003
ProfilePram43.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram43.Mold="+"
ProfilePram43.ReverseDir=False
ProfilePram43.ReverseAngle=True
ProfilePram43.CalcSnipOnlyAttachLines=False
ProfilePram43.AttachDirMethod=0
ProfilePram43.CCWDefAngle=False
ProfilePram43.AddEnd1Elements(extrude_sheet2)
ProfilePram43.End1Type=1103
ProfilePram43.End1TypeParams=["0"]
ProfilePram43.AddEnd2Elements(extrude_sheet8)
ProfilePram43.End2Type=1103
ProfilePram43.End2TypeParams=["0"]
ProfilePram43.End1ScallopType=1120
ProfilePram43.End1ScallopTypeParams=["50"]
ProfilePram43.End2ScallopType=1120
ProfilePram43.End2ScallopTypeParams=["50"]
profile43 = part.CreateProfile(ProfilePram43,False)
part.SetElementColor(profile43[0],"148","0","211","0.39999997615814209")
ProfilePram44 = part.CreateProfileParam()
ProfilePram44.DefinitionType=1
ProfilePram44.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram44.AddAttachSurfaces(extrude_sheet2)
ProfilePram44.ProfileName="HK.Casing.Deck.A.FR13P"
ProfilePram44.MaterialName="SS400"
ProfilePram44.ProfileType=1003
ProfilePram44.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram44.Mold="+"
ProfilePram44.ReverseDir=True
ProfilePram44.ReverseAngle=False
ProfilePram44.CalcSnipOnlyAttachLines=False
ProfilePram44.AttachDirMethod=0
ProfilePram44.CCWDefAngle=False
ProfilePram44.AddEnd1Elements(profile26[0])
ProfilePram44.End1Type=1113
ProfilePram44.End1TypeParams=["0","79"]
ProfilePram44.AddEnd2Elements(profile43[0])
ProfilePram44.End2Type=1102
ProfilePram44.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram44.End1ScallopType=1120
ProfilePram44.End1ScallopTypeParams=["50"]
ProfilePram44.End2ScallopType=1120
ProfilePram44.End2ScallopTypeParams=["50"]
profile44 = part.CreateProfile(ProfilePram44,False)
part.SetElementColor(profile44[0],"148","0","211","0.39999997615814209")
ProfilePram45 = part.CreateProfileParam()
ProfilePram45.DefinitionType=1
ProfilePram45.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram45.AddAttachSurfaces(extrude_sheet3)
ProfilePram45.ProfileName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram45.MaterialName="SS400"
ProfilePram45.FlangeName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram45.FlangeMaterialName="SS400"
ProfilePram45.ProfileType=1201
ProfilePram45.ProfileParams=["150","12","388","10"]
ProfilePram45.Mold="-"
ProfilePram45.ReverseDir=True
ProfilePram45.ReverseAngle=False
ProfilePram45.CalcSnipOnlyAttachLines=False
ProfilePram45.AttachDirMethod=0
ProfilePram45.CCWDefAngle=False
ProfilePram45.AddEnd1Elements(profile21[1])
ProfilePram45.End1Type=1102
ProfilePram45.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram45.AddEnd2Elements(extrude_sheet5)
ProfilePram45.End2Type=1102
ProfilePram45.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram45.End1ScallopType=1120
ProfilePram45.End1ScallopTypeParams=["50"]
ProfilePram45.End2ScallopType=1120
ProfilePram45.End2ScallopTypeParams=["50"]
profile45 = part.CreateProfile(ProfilePram45,False)
part.SetElementColor(profile45[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile45[1],"148","0","211","0.39999997615814209")
ProfilePram46 = part.CreateProfileParam()
ProfilePram46.DefinitionType=1
ProfilePram46.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram46.AddAttachSurfaces(extrude_sheet3)
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
ProfilePram46.AddEnd2Elements(extrude_sheet8)
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
ProfilePram47.BasePlane="PL,O,"+var_elm11+","+"Y"
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
ProfilePram47.AddEnd1Elements(profile41[0])
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
ProfilePram48 = part.CreateProfileParam()
ProfilePram48.DefinitionType=1
ProfilePram48.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram48.AddAttachSurfaces(extrude_sheet7)
ProfilePram48.ProfileName="HK.Casing.Wall.Side.FR15.ABP"
ProfilePram48.MaterialName="SS400"
ProfilePram48.ProfileType=1002
ProfilePram48.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram48.Mold="+"
ProfilePram48.ReverseDir=False
ProfilePram48.ReverseAngle=True
ProfilePram48.CalcSnipOnlyAttachLines=False
ProfilePram48.AttachDirMethod=0
ProfilePram48.CCWDefAngle=False
ProfilePram48.AddEnd1Elements(extrude_sheet1)
ProfilePram48.End1Type=1102
ProfilePram48.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram48.AddEnd2Elements(extrude_sheet2)
ProfilePram48.End2Type=1102
ProfilePram48.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram48.End1ScallopType=1121
ProfilePram48.End1ScallopTypeParams=["35","40"]
ProfilePram48.End2ScallopType=1121
ProfilePram48.End2ScallopTypeParams=["35","40"]
profile48 = part.CreateProfile(ProfilePram48,False)
part.SetElementColor(profile48[0],"255","0","0","0.19999998807907104")
mirror_copied16 = part.MirrorCopy([profile48[0]],"PL,Y","")
part.SetElementColor(mirror_copied16[0],"255","0","0","0.19999998807907104")
mirror_copied17 = part.MirrorCopy([profile21[0]],"PL,Y","")
part.SetElementColor(mirror_copied17[0],"148","0","211","0.39999997615814209")
ProfilePram49 = part.CreateProfileParam()
ProfilePram49.DefinitionType=1
ProfilePram49.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram49.AddAttachSurfaces(extrude_sheet7)
ProfilePram49.ProfileName="HK.Casing.Wall.Side.FR09.CDP"
ProfilePram49.MaterialName="SS400"
ProfilePram49.ProfileType=1003
ProfilePram49.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram49.Mold="+"
ProfilePram49.ReverseDir=False
ProfilePram49.ReverseAngle=True
ProfilePram49.CalcSnipOnlyAttachLines=False
ProfilePram49.AttachDirMethod=0
ProfilePram49.CCWDefAngle=False
ProfilePram49.AddEnd1Elements(profile30[0])
ProfilePram49.End1Type=1102
ProfilePram49.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram49.AddEnd2Elements(extrude_sheet5)
ProfilePram49.End2Type=1103
ProfilePram49.End2TypeParams=["0"]
ProfilePram49.End1ScallopType=1120
ProfilePram49.End1ScallopTypeParams=["50"]
ProfilePram49.End2ScallopType=1120
ProfilePram49.End2ScallopTypeParams=["50"]
profile49 = part.CreateProfile(ProfilePram49,False)
part.SetElementColor(profile49[0],"148","0","211","0.39999997615814209")
var_elm15 = part.CreateVariable("FR10","6700","mm","")
var_elm16 = part.CreateVariable("FR7","4690","mm","")
ProfilePram50 = part.CreateProfileParam()
ProfilePram50.DefinitionType=1
ProfilePram50.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram50.AddAttachSurfaces(extrude_sheet7)
ProfilePram50.ProfileName="HK.Casing.Wall.Side.FR07.CDP"
ProfilePram50.MaterialName="SS400"
ProfilePram50.ProfileType=1002
ProfilePram50.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram50.Mold="+"
ProfilePram50.ReverseDir=False
ProfilePram50.ReverseAngle=True
ProfilePram50.CalcSnipOnlyAttachLines=False
ProfilePram50.AttachDirMethod=0
ProfilePram50.CCWDefAngle=False
ProfilePram50.AddEnd1Elements(extrude_sheet6)
ProfilePram50.End1Type=1102
ProfilePram50.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram50.AddEnd2Elements(extrude_sheet5)
ProfilePram50.End2Type=1102
ProfilePram50.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram50.End1ScallopType=1121
ProfilePram50.End1ScallopTypeParams=["35","40"]
ProfilePram50.End2ScallopType=1121
ProfilePram50.End2ScallopTypeParams=["35","40"]
profile50 = part.CreateProfile(ProfilePram50,False)
part.SetElementColor(profile50[0],"255","0","0","0.19999998807907104")
mirror_copied18 = part.MirrorCopy([profile50[0]],"PL,Y","")
part.SetElementColor(mirror_copied18[0],"255","0","0","0.19999998807907104")
ProfilePram51 = part.CreateProfileParam()
ProfilePram51.DefinitionType=1
ProfilePram51.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram51.AddAttachSurfaces(extrude_sheet4)
ProfilePram51.ProfileName="HK.Casing.Wall.Aft.DL03.BCP"
ProfilePram51.MaterialName="SS400"
ProfilePram51.ProfileType=1002
ProfilePram51.ProfileParams=["125","75","7","10","5"]
ProfilePram51.Mold="+"
ProfilePram51.ReverseDir=False
ProfilePram51.ReverseAngle=True
ProfilePram51.CalcSnipOnlyAttachLines=False
ProfilePram51.AttachDirMethod=0
ProfilePram51.CCWDefAngle=False
ProfilePram51.AddEnd1Elements(extrude_sheet5)
ProfilePram51.End1Type=1102
ProfilePram51.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram51.AddEnd2Elements(extrude_sheet1)
ProfilePram51.End2Type=1102
ProfilePram51.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram51.End1ScallopType=1121
ProfilePram51.End1ScallopTypeParams=["25","40"]
ProfilePram51.End2ScallopType=1121
ProfilePram51.End2ScallopTypeParams=["25","40"]
profile51 = part.CreateProfile(ProfilePram51,False)
part.SetElementColor(profile51[0],"255","0","0","0.19999998807907104")
mirror_copied19 = part.MirrorCopy([profile51[0]],"PL,Y","")
part.SetElementColor(mirror_copied19[0],"255","0","0","0.19999998807907104")
ProfilePram52 = part.CreateProfileParam()
ProfilePram52.DefinitionType=1
ProfilePram52.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram52.AddAttachSurfaces(extrude_sheet3)
ProfilePram52.ProfileName="HK.Casing.Wall.Fore.DL02.ABP"
ProfilePram52.MaterialName="SS400"
ProfilePram52.FlangeName="HK.Casing.Wall.Fore.DL02.ABP"
ProfilePram52.FlangeMaterialName="SS400"
ProfilePram52.ProfileType=1201
ProfilePram52.ProfileParams=["150","12","388","10"]
ProfilePram52.Mold="-"
ProfilePram52.ReverseDir=True
ProfilePram52.ReverseAngle=False
ProfilePram52.CalcSnipOnlyAttachLines=False
ProfilePram52.AttachDirMethod=0
ProfilePram52.CCWDefAngle=False
ProfilePram52.AddEnd1Elements(extrude_sheet1)
ProfilePram52.End1Type=1102
ProfilePram52.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram52.AddEnd2Elements(extrude_sheet2)
ProfilePram52.End2Type=1102
ProfilePram52.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram52.End1ScallopType=1120
ProfilePram52.End1ScallopTypeParams=["50"]
ProfilePram52.End2ScallopType=1120
ProfilePram52.End2ScallopTypeParams=["50"]
profile52 = part.CreateProfile(ProfilePram52,False)
part.SetElementColor(profile52[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile52[1],"148","0","211","0.39999997615814209")
ProfilePram53 = part.CreateProfileParam()
ProfilePram53.DefinitionType=1
ProfilePram53.BasePlane="PL,O,"+var_elm4+","+"X"
ProfilePram53.AddAttachSurfaces(extrude_sheet7)
ProfilePram53.ProfileName="HK.Casing.Wall.Side.FR12.BCP"
ProfilePram53.MaterialName="SS400"
ProfilePram53.ProfileType=1002
ProfilePram53.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram53.Mold="+"
ProfilePram53.ReverseDir=False
ProfilePram53.ReverseAngle=True
ProfilePram53.CalcSnipOnlyAttachLines=False
ProfilePram53.AttachDirMethod=0
ProfilePram53.CCWDefAngle=False
ProfilePram53.AddEnd1Elements(extrude_sheet5)
ProfilePram53.End1Type=1102
ProfilePram53.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram53.AddEnd2Elements(extrude_sheet1)
ProfilePram53.End2Type=1102
ProfilePram53.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram53.End1ScallopType=1121
ProfilePram53.End1ScallopTypeParams=["35","40"]
ProfilePram53.End2ScallopType=1121
ProfilePram53.End2ScallopTypeParams=["35","40"]
profile53 = part.CreateProfile(ProfilePram53,False)
part.SetElementColor(profile53[0],"255","0","0","0.19999998807907104")
mirror_copied20 = part.MirrorCopy([profile53[0]],"PL,Y","")
part.SetElementColor(mirror_copied20[0],"255","0","0","0.19999998807907104")
ProfilePram54 = part.CreateProfileParam()
ProfilePram54.DefinitionType=1
ProfilePram54.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram54.AddAttachSurfaces(extrude_sheet6)
ProfilePram54.ProfileName="HK.Casing.Deck.D.FR09C"
ProfilePram54.MaterialName="SS400"
ProfilePram54.ProfileType=1003
ProfilePram54.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram54.Mold="+"
ProfilePram54.ReverseDir=True
ProfilePram54.ReverseAngle=False
ProfilePram54.CalcSnipOnlyAttachLines=False
ProfilePram54.AttachDirMethod=0
ProfilePram54.CCWDefAngle=False
ProfilePram54.AddEnd1Elements(mirror_copied17[0])
ProfilePram54.End1Type=1102
ProfilePram54.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram54.AddEnd2Elements(profile21[0])
ProfilePram54.End2Type=1102
ProfilePram54.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram54.End1ScallopType=1120
ProfilePram54.End1ScallopTypeParams=["50"]
ProfilePram54.End2ScallopType=1120
ProfilePram54.End2ScallopTypeParams=["50"]
profile54 = part.CreateProfile(ProfilePram54,False)
part.SetElementColor(profile54[0],"148","0","211","0.39999997615814209")
ProfilePram55 = part.CreateProfileParam()
ProfilePram55.DefinitionType=1
ProfilePram55.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram55.AddAttachSurfaces(extrude_sheet6)
ProfilePram55.ProfileName="HK.Casing.Deck.D.DL00.A"
ProfilePram55.MaterialName="SS400"
ProfilePram55.ProfileType=1002
ProfilePram55.ProfileParams=["125","75","7","10","5"]
ProfilePram55.Mold="+"
ProfilePram55.ReverseDir=True
ProfilePram55.ReverseAngle=True
ProfilePram55.CalcSnipOnlyAttachLines=False
ProfilePram55.AttachDirMethod=0
ProfilePram55.CCWDefAngle=False
ProfilePram55.AddEnd1Elements(extrude_sheet4)
ProfilePram55.End1Type=1102
ProfilePram55.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram55.AddEnd2Elements(profile54[0])
ProfilePram55.End2Type=1102
ProfilePram55.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram55.End1ScallopType=1120
ProfilePram55.End1ScallopTypeParams=["50"]
ProfilePram55.End2ScallopType=1120
ProfilePram55.End2ScallopTypeParams=["50"]
profile55 = part.CreateProfile(ProfilePram55,False)
part.SetElementColor(profile55[0],"255","0","0","0.19999998807907104")
ProfilePram56 = part.CreateProfileParam()
ProfilePram56.DefinitionType=1
ProfilePram56.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram56.AddAttachSurfaces(extrude_sheet4)
ProfilePram56.ProfileName="HK.Casing.Wall.Aft.DL00.CD"
ProfilePram56.MaterialName="SS400"
ProfilePram56.ProfileType=1002
ProfilePram56.ProfileParams=["125","75","7","10","5"]
ProfilePram56.Mold="+"
ProfilePram56.ReverseDir=False
ProfilePram56.ReverseAngle=True
ProfilePram56.CalcSnipOnlyAttachLines=False
ProfilePram56.AttachDirMethod=0
ProfilePram56.CCWDefAngle=False
ProfilePram56.AddEnd1Elements(profile55[0])
ProfilePram56.End1Type=1102
ProfilePram56.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram56.AddEnd2Elements(extrude_sheet5)
ProfilePram56.End2Type=1102
ProfilePram56.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram56.End1ScallopType=1120
ProfilePram56.End1ScallopTypeParams=["50"]
ProfilePram56.End2ScallopType=1120
ProfilePram56.End2ScallopTypeParams=["50"]
profile56 = part.CreateProfile(ProfilePram56,False)
part.SetElementColor(profile56[0],"255","0","0","0.19999998807907104")
ProfilePram57 = part.CreateProfileParam()
ProfilePram57.DefinitionType=1
ProfilePram57.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram57.AddAttachSurfaces(extrude_sheet7)
ProfilePram57.ProfileName="HK.Casing.Wall.Side.FR09.BCP"
ProfilePram57.MaterialName="SS400"
ProfilePram57.ProfileType=1003
ProfilePram57.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram57.Mold="+"
ProfilePram57.ReverseDir=False
ProfilePram57.ReverseAngle=True
ProfilePram57.CalcSnipOnlyAttachLines=False
ProfilePram57.AttachDirMethod=0
ProfilePram57.CCWDefAngle=False
ProfilePram57.AddEnd1Elements(extrude_sheet5)
ProfilePram57.End1Type=1103
ProfilePram57.End1TypeParams=["0"]
ProfilePram57.AddEnd2Elements(extrude_sheet1)
ProfilePram57.End2Type=1103
ProfilePram57.End2TypeParams=["0"]
ProfilePram57.End1ScallopType=1120
ProfilePram57.End1ScallopTypeParams=["50"]
ProfilePram57.End2ScallopType=1120
ProfilePram57.End2ScallopTypeParams=["50"]
profile57 = part.CreateProfile(ProfilePram57,False)
part.SetElementColor(profile57[0],"148","0","211","0.39999997615814209")
ProfilePram58 = part.CreateProfileParam()
ProfilePram58.DefinitionType=1
ProfilePram58.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram58.AddAttachSurfaces(extrude_sheet5)
ProfilePram58.ProfileName="HK.Casing.Deck.C.FR09P"
ProfilePram58.MaterialName="SS400"
ProfilePram58.ProfileType=1003
ProfilePram58.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram58.Mold="+"
ProfilePram58.ReverseDir=True
ProfilePram58.ReverseAngle=False
ProfilePram58.CalcSnipOnlyAttachLines=False
ProfilePram58.AttachDirMethod=0
ProfilePram58.CCWDefAngle=False
ProfilePram58.AddEnd1Elements(profile12[0])
ProfilePram58.End1Type=1113
ProfilePram58.End1TypeParams=["0","79"]
ProfilePram58.AddEnd2Elements(profile57[0])
ProfilePram58.End2Type=1102
ProfilePram58.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram58.End1ScallopType=1120
ProfilePram58.End1ScallopTypeParams=["50"]
ProfilePram58.End2ScallopType=1120
ProfilePram58.End2ScallopTypeParams=["50"]
profile58 = part.CreateProfile(ProfilePram58,False)
part.SetElementColor(profile58[0],"148","0","211","0.39999997615814209")
ProfilePram59 = part.CreateProfileParam()
ProfilePram59.DefinitionType=1
ProfilePram59.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram59.AddAttachSurfaces(extrude_sheet6)
ProfilePram59.ProfileName="HK.Casing.Deck.D.DL05P"
ProfilePram59.MaterialName="SS400"
ProfilePram59.ProfileType=1002
ProfilePram59.ProfileParams=["125","75","7","10","5"]
ProfilePram59.Mold="+"
ProfilePram59.ReverseDir=True
ProfilePram59.ReverseAngle=True
ProfilePram59.CalcSnipOnlyAttachLines=False
ProfilePram59.AttachDirMethod=0
ProfilePram59.CCWDefAngle=False
ProfilePram59.AddEnd1Elements(extrude_sheet4)
ProfilePram59.End1Type=1102
ProfilePram59.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram59.AddEnd2Elements(extrude_sheet3)
ProfilePram59.End2Type=1102
ProfilePram59.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram59.End1ScallopType=1120
ProfilePram59.End1ScallopTypeParams=["50"]
ProfilePram59.End2ScallopType=1120
ProfilePram59.End2ScallopTypeParams=["50"]
profile59 = part.CreateProfile(ProfilePram59,False)
part.SetElementColor(profile59[0],"255","0","0","0.19999998807907104")
ProfilePram60 = part.CreateProfileParam()
ProfilePram60.DefinitionType=1
ProfilePram60.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram60.AddAttachSurfaces(extrude_sheet3)
ProfilePram60.ProfileName="HK.Casing.Wall.Fore.DL05.CDP"
ProfilePram60.MaterialName="SS400"
ProfilePram60.ProfileType=1002
ProfilePram60.ProfileParams=["125","75","7","10","5"]
ProfilePram60.Mold="+"
ProfilePram60.ReverseDir=True
ProfilePram60.ReverseAngle=True
ProfilePram60.CalcSnipOnlyAttachLines=False
ProfilePram60.AttachDirMethod=0
ProfilePram60.CCWDefAngle=False
ProfilePram60.AddEnd1Elements(profile59[0])
ProfilePram60.End1Type=1102
ProfilePram60.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram60.AddEnd2Elements(extrude_sheet5)
ProfilePram60.End2Type=1102
ProfilePram60.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram60.End1ScallopType=1120
ProfilePram60.End1ScallopTypeParams=["50"]
ProfilePram60.End2ScallopType=1120
ProfilePram60.End2ScallopTypeParams=["50"]
profile60 = part.CreateProfile(ProfilePram60,False)
part.SetElementColor(profile60[0],"255","0","0","0.19999998807907104")
ProfilePram61 = part.CreateProfileParam()
ProfilePram61.DefinitionType=1
ProfilePram61.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram61.AddAttachSurfaces(extrude_sheet4)
ProfilePram61.ProfileName="HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram61.MaterialName="SS400"
ProfilePram61.FlangeName="HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram61.FlangeMaterialName="SS400"
ProfilePram61.ProfileType=1201
ProfilePram61.ProfileParams=["150","12","388","10"]
ProfilePram61.Mold="-"
ProfilePram61.ReverseDir=False
ProfilePram61.ReverseAngle=False
ProfilePram61.CalcSnipOnlyAttachLines=False
ProfilePram61.AttachDirMethod=0
ProfilePram61.CCWDefAngle=False
ProfilePram61.AddEnd1Elements(extrude_sheet2)
ProfilePram61.End1Type=1103
ProfilePram61.End1TypeParams=["0"]
ProfilePram61.AddEnd2Elements(extrude_sheet8)
ProfilePram61.End2Type=1103
ProfilePram61.End2TypeParams=["0"]
ProfilePram61.End1ScallopType=1120
ProfilePram61.End1ScallopTypeParams=["50"]
ProfilePram61.End2ScallopType=1120
ProfilePram61.End2ScallopTypeParams=["50"]
profile61 = part.CreateProfile(ProfilePram61,False)
part.SetElementColor(profile61[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile61[1],"148","0","211","0.39999997615814209")
solid4 = part.CreateSolid("HK.Casing.Wall.Fore.BC","","SS400")
part.SetElementColor(solid4,"139","69","19","0.79999995231628418")
thicken4 = part.CreateThicken("厚み付け16",solid4,"+",[extrude_sheet3],"+","10","0","0",False,False)
extrudePram15 = part.CreateLinearSweepParam()
extrudePram15.Name="積-押し出し39"
extrudePram15.AddProfile(extrude_sheet7)
extrudePram15.DirectionType="R"
extrudePram15.DirectionParameter1="50000"
extrudePram15.SweepDirection="+Y"
extrudePram15.RefByGeometricMethod=False
extrude6 = part.CreateLinearSweep(solid4,"*",extrudePram15,False)
extrudePram16 = part.CreateLinearSweepParam()
extrudePram16.Name="積-押し出し40"
extrudePram16.AddProfile(extrude_sheet9)
extrudePram16.DirectionType="N"
extrudePram16.DirectionParameter1="50000"
extrudePram16.SweepDirection="+Y"
extrudePram16.RefByGeometricMethod=False
extrude7 = part.CreateLinearSweep(solid4,"*",extrudePram16,False)
extrudePram17 = part.CreateLinearSweepParam()
extrudePram17.Name="積-押し出し41"
extrudePram17.AddProfile(extrude_sheet5)
extrudePram17.DirectionType="R"
extrudePram17.DirectionParameter1="50000"
extrudePram17.SweepDirection="+Z"
extrudePram17.RefByGeometricMethod=False
extrude8 = part.CreateLinearSweep(solid4,"*",extrudePram17,False)
extrudePram18 = part.CreateLinearSweepParam()
extrudePram18.Name="積-押し出し42"
extrudePram18.AddProfile(extrude_sheet1)
extrudePram18.DirectionType="N"
extrudePram18.DirectionParameter1="50000"
extrudePram18.SweepDirection="+Z"
extrudePram18.RefByGeometricMethod=False
extrude9 = part.CreateLinearSweep(solid4,"*",extrudePram18,False)
ProfilePram62 = part.CreateProfileParam()
ProfilePram62.DefinitionType=1
ProfilePram62.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram62.AddAttachSurfaces(extrude_sheet7)
ProfilePram62.ProfileName="HK.Casing.Wall.Side.FR08.BCP"
ProfilePram62.MaterialName="SS400"
ProfilePram62.ProfileType=1002
ProfilePram62.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram62.Mold="+"
ProfilePram62.ReverseDir=False
ProfilePram62.ReverseAngle=True
ProfilePram62.CalcSnipOnlyAttachLines=False
ProfilePram62.AttachDirMethod=0
ProfilePram62.CCWDefAngle=False
ProfilePram62.AddEnd1Elements(extrude_sheet5)
ProfilePram62.End1Type=1102
ProfilePram62.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram62.AddEnd2Elements(extrude_sheet1)
ProfilePram62.End2Type=1102
ProfilePram62.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram62.End1ScallopType=1121
ProfilePram62.End1ScallopTypeParams=["35","40"]
ProfilePram62.End2ScallopType=1121
ProfilePram62.End2ScallopTypeParams=["35","40"]
profile62 = part.CreateProfile(ProfilePram62,False)
part.SetElementColor(profile62[0],"255","0","0","0.19999998807907104")
solid5 = part.CreateSolid("HK.Casing.Deck.B","","SS400")
part.SetElementColor(solid5,"139","69","19","0.78999996185302734")
thicken5 = part.CreateThicken("厚み付け5",solid5,"+",[extrude_sheet1],"+","10","0","0",False,False)
extrudePram19 = part.CreateLinearSweepParam()
extrudePram19.Name="積-押し出し5"
extrudePram19.AddProfile(skt_pl5+",Edge00")
extrudePram19.DirectionType="N"
extrudePram19.DirectionParameter1="50000"
extrudePram19.SweepDirection="+Z"
extrudePram19.RefByGeometricMethod=False
extrude10 = part.CreateLinearSweep(solid5,"*",extrudePram19,False)
extrudePram20 = part.CreateLinearSweepParam()
extrudePram20.Name="削除-押し出し3"
extrudePram20.AddProfile(skt_pl5+",Edge01")
extrudePram20.DirectionType="T"
extrudePram20.RefByGeometricMethod=False
extrude11 = part.CreateLinearSweep(solid5,"-",extrudePram20,False)
ProfilePram63 = part.CreateProfileParam()
ProfilePram63.DefinitionType=1
ProfilePram63.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram63.AddAttachSurfaces(extrude_sheet4)
ProfilePram63.ProfileName="HK.Casing.Wall.Aft.DL03.ABP"
ProfilePram63.MaterialName="SS400"
ProfilePram63.ProfileType=1002
ProfilePram63.ProfileParams=["125","75","7","10","5"]
ProfilePram63.Mold="+"
ProfilePram63.ReverseDir=False
ProfilePram63.ReverseAngle=True
ProfilePram63.CalcSnipOnlyAttachLines=False
ProfilePram63.AttachDirMethod=0
ProfilePram63.CCWDefAngle=False
ProfilePram63.AddEnd1Elements(extrude_sheet1)
ProfilePram63.End1Type=1102
ProfilePram63.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram63.AddEnd2Elements(extrude_sheet2)
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
ProfilePram64.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram64.AddAttachSurfaces(extrude_sheet3)
ProfilePram64.ProfileName="HK.Casing.Wall.Fore.DL02.OAP"
ProfilePram64.MaterialName="SS400"
ProfilePram64.FlangeName="HK.Casing.Wall.Fore.DL02.OAP"
ProfilePram64.FlangeMaterialName="SS400"
ProfilePram64.ProfileType=1201
ProfilePram64.ProfileParams=["150","12","388","10"]
ProfilePram64.Mold="-"
ProfilePram64.ReverseDir=True
ProfilePram64.ReverseAngle=False
ProfilePram64.CalcSnipOnlyAttachLines=False
ProfilePram64.AttachDirMethod=0
ProfilePram64.CCWDefAngle=False
ProfilePram64.AddEnd1Elements(extrude_sheet2)
ProfilePram64.End1Type=1102
ProfilePram64.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram64.AddEnd2Elements(extrude_sheet8)
ProfilePram64.End2Type=1102
ProfilePram64.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram64.End1ScallopType=1120
ProfilePram64.End1ScallopTypeParams=["50"]
ProfilePram64.End2ScallopType=1120
ProfilePram64.End2ScallopTypeParams=["50"]
profile64 = part.CreateProfile(ProfilePram64,False)
part.SetElementColor(profile64[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile64[1],"148","0","211","0.39999997615814209")
ProfilePram65 = part.CreateProfileParam()
ProfilePram65.DefinitionType=1
ProfilePram65.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram65.AddAttachSurfaces(extrude_sheet4)
ProfilePram65.ProfileName="HK.Casing.Wall.Aft.DL03.OAP"
ProfilePram65.MaterialName="SS400"
ProfilePram65.ProfileType=1002
ProfilePram65.ProfileParams=["125","75","7","10","5"]
ProfilePram65.Mold="+"
ProfilePram65.ReverseDir=False
ProfilePram65.ReverseAngle=True
ProfilePram65.CalcSnipOnlyAttachLines=False
ProfilePram65.AttachDirMethod=0
ProfilePram65.CCWDefAngle=False
ProfilePram65.AddEnd1Elements(extrude_sheet2)
ProfilePram65.End1Type=1102
ProfilePram65.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram65.AddEnd2Elements(extrude_sheet8)
ProfilePram65.End2Type=1102
ProfilePram65.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram65.End1ScallopType=1121
ProfilePram65.End1ScallopTypeParams=["25","40"]
ProfilePram65.End2ScallopType=1121
ProfilePram65.End2ScallopTypeParams=["25","40"]
profile65 = part.CreateProfile(ProfilePram65,False)
part.SetElementColor(profile65[0],"255","0","0","0.19999998807907104")
ProfilePram66 = part.CreateProfileParam()
ProfilePram66.DefinitionType=1
ProfilePram66.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram66.AddAttachSurfaces(extrude_sheet6)
ProfilePram66.ProfileName="HK.Casing.Deck.D.FR13P"
ProfilePram66.MaterialName="SS400"
ProfilePram66.ProfileType=1003
ProfilePram66.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram66.Mold="+"
ProfilePram66.ReverseDir=True
ProfilePram66.ReverseAngle=False
ProfilePram66.CalcSnipOnlyAttachLines=False
ProfilePram66.AttachDirMethod=0
ProfilePram66.CCWDefAngle=False
ProfilePram66.AddEnd1Elements(profile21[0])
ProfilePram66.End1Type=1102
ProfilePram66.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram66.AddEnd2Elements(extrude_sheet7)
ProfilePram66.End2Type=1102
ProfilePram66.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram66.End1ScallopType=1120
ProfilePram66.End1ScallopTypeParams=["50"]
ProfilePram66.End2ScallopType=1120
ProfilePram66.End2ScallopTypeParams=["50"]
profile66 = part.CreateProfile(ProfilePram66,False)
part.SetElementColor(profile66[0],"148","0","211","0.39999997615814209")
ProfilePram67 = part.CreateProfileParam()
ProfilePram67.DefinitionType=1
ProfilePram67.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram67.AddAttachSurfaces(extrude_sheet7)
ProfilePram67.ProfileName="HK.Casing.Wall.Side.FR13.CDP"
ProfilePram67.MaterialName="SS400"
ProfilePram67.ProfileType=1003
ProfilePram67.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram67.Mold="+"
ProfilePram67.ReverseDir=False
ProfilePram67.ReverseAngle=True
ProfilePram67.CalcSnipOnlyAttachLines=False
ProfilePram67.AttachDirMethod=0
ProfilePram67.CCWDefAngle=False
ProfilePram67.AddEnd1Elements(profile66[0])
ProfilePram67.End1Type=1102
ProfilePram67.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram67.AddEnd2Elements(extrude_sheet5)
ProfilePram67.End2Type=1103
ProfilePram67.End2TypeParams=["0"]
ProfilePram67.End1ScallopType=1120
ProfilePram67.End1ScallopTypeParams=["50"]
ProfilePram67.End2ScallopType=1120
ProfilePram67.End2ScallopTypeParams=["50"]
profile67 = part.CreateProfile(ProfilePram67,False)
part.SetElementColor(profile67[0],"148","0","211","0.39999997615814209")
mirror_copied21 = part.MirrorCopy([profile67[0]],"PL,Y","")
part.SetElementColor(mirror_copied21[0],"148","0","211","0.39999997615814209")
mirror_copied22 = part.MirrorCopy([profile38[0]],"PL,Y","")
part.SetElementColor(mirror_copied22[0],"148","0","211","0.39999997615814209")
ProfilePram68 = part.CreateProfileParam()
ProfilePram68.DefinitionType=1
ProfilePram68.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram68.AddAttachSurfaces(extrude_sheet5)
ProfilePram68.ProfileName="HK.Casing.Deck.C.FR13P"
ProfilePram68.MaterialName="SS400"
ProfilePram68.ProfileType=1003
ProfilePram68.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram68.Mold="+"
ProfilePram68.ReverseDir=True
ProfilePram68.ReverseAngle=False
ProfilePram68.CalcSnipOnlyAttachLines=False
ProfilePram68.AttachDirMethod=0
ProfilePram68.CCWDefAngle=False
ProfilePram68.AddEnd1Elements(profile12[0])
ProfilePram68.End1Type=1113
ProfilePram68.End1TypeParams=["0","79"]
ProfilePram68.AddEnd2Elements(profile42[0])
ProfilePram68.End2Type=1102
ProfilePram68.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram68.End1ScallopType=1120
ProfilePram68.End1ScallopTypeParams=["50"]
ProfilePram68.End2ScallopType=1120
ProfilePram68.End2ScallopTypeParams=["50"]
profile68 = part.CreateProfile(ProfilePram68,False)
part.SetElementColor(profile68[0],"148","0","211","0.39999997615814209")
ProfilePram69 = part.CreateProfileParam()
ProfilePram69.DefinitionType=1
ProfilePram69.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram69.AddAttachSurfaces(extrude_sheet5)
ProfilePram69.ProfileName="HK.Casing.Deck.C.DL05P"
ProfilePram69.MaterialName="SS400"
ProfilePram69.ProfileType=1002
ProfilePram69.ProfileParams=["125","75","7","10","5"]
ProfilePram69.Mold="+"
ProfilePram69.ReverseDir=True
ProfilePram69.ReverseAngle=True
ProfilePram69.CalcSnipOnlyAttachLines=False
ProfilePram69.AttachDirMethod=0
ProfilePram69.CCWDefAngle=False
ProfilePram69.AddEnd1Elements(profile31[0])
ProfilePram69.End1Type=1102
ProfilePram69.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram69.AddEnd2Elements(profile36[0])
ProfilePram69.End2Type=1102
ProfilePram69.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram69.End1ScallopType=1120
ProfilePram69.End1ScallopTypeParams=["50"]
ProfilePram69.End2ScallopType=1120
ProfilePram69.End2ScallopTypeParams=["50"]
profile69 = part.CreateProfile(ProfilePram69,False)
part.SetElementColor(profile69[0],"255","0","0","0.19999998807907104")
ProfilePram70 = part.CreateProfileParam()
ProfilePram70.DefinitionType=1
ProfilePram70.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram70.AddAttachSurfaces(extrude_sheet7)
ProfilePram70.ProfileName="HK.Casing.Wall.Side.FR15.OAP"
ProfilePram70.MaterialName="SS400"
ProfilePram70.ProfileType=1002
ProfilePram70.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram70.Mold="+"
ProfilePram70.ReverseDir=False
ProfilePram70.ReverseAngle=True
ProfilePram70.CalcSnipOnlyAttachLines=False
ProfilePram70.AttachDirMethod=0
ProfilePram70.CCWDefAngle=False
ProfilePram70.AddEnd1Elements(extrude_sheet2)
ProfilePram70.End1Type=1102
ProfilePram70.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram70.AddEnd2Elements(extrude_sheet8)
ProfilePram70.End2Type=1102
ProfilePram70.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram70.End1ScallopType=1121
ProfilePram70.End1ScallopTypeParams=["35","40"]
ProfilePram70.End2ScallopType=1121
ProfilePram70.End2ScallopTypeParams=["35","40"]
profile70 = part.CreateProfile(ProfilePram70,False)
part.SetElementColor(profile70[0],"255","0","0","0.19999998807907104")
ProfilePram71 = part.CreateProfileParam()
ProfilePram71.DefinitionType=1
ProfilePram71.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram71.AddAttachSurfaces(extrude_sheet4)
ProfilePram71.ProfileName="HK.Casing.Wall.Aft.DL05.ABP"
ProfilePram71.MaterialName="SS400"
ProfilePram71.ProfileType=1002
ProfilePram71.ProfileParams=["125","75","7","10","5"]
ProfilePram71.Mold="+"
ProfilePram71.ReverseDir=False
ProfilePram71.ReverseAngle=True
ProfilePram71.CalcSnipOnlyAttachLines=False
ProfilePram71.AttachDirMethod=0
ProfilePram71.CCWDefAngle=False
ProfilePram71.AddEnd1Elements(extrude_sheet1)
ProfilePram71.End1Type=1102
ProfilePram71.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram71.AddEnd2Elements(extrude_sheet2)
ProfilePram71.End2Type=1102
ProfilePram71.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram71.End1ScallopType=1121
ProfilePram71.End1ScallopTypeParams=["25","40"]
ProfilePram71.End2ScallopType=1121
ProfilePram71.End2ScallopTypeParams=["25","40"]
profile71 = part.CreateProfile(ProfilePram71,False)
part.SetElementColor(profile71[0],"255","0","0","0.19999998807907104")
mirror_copied23 = part.MirrorCopy([profile71[0]],"PL,Y","")
part.SetElementColor(mirror_copied23[0],"255","0","0","0.19999998807907104")
ProfilePram72 = part.CreateProfileParam()
ProfilePram72.DefinitionType=1
ProfilePram72.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram72.AddAttachSurfaces(extrude_sheet4)
ProfilePram72.ProfileName="HK.Casing.Wall.Aft.DL03.CDP"
ProfilePram72.MaterialName="SS400"
ProfilePram72.ProfileType=1002
ProfilePram72.ProfileParams=["125","75","7","10","5"]
ProfilePram72.Mold="+"
ProfilePram72.ReverseDir=False
ProfilePram72.ReverseAngle=True
ProfilePram72.CalcSnipOnlyAttachLines=False
ProfilePram72.AttachDirMethod=0
ProfilePram72.CCWDefAngle=False
ProfilePram72.AddEnd1Elements(profile9[0])
ProfilePram72.End1Type=1102
ProfilePram72.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram72.AddEnd2Elements(extrude_sheet5)
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
ProfilePram73.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram73.AddAttachSurfaces(extrude_sheet6)
ProfilePram73.ProfileName="HK.Casing.Deck.D.DL01.AP"
ProfilePram73.MaterialName="SS400"
ProfilePram73.ProfileType=1002
ProfilePram73.ProfileParams=["125","75","7","10","5"]
ProfilePram73.Mold="+"
ProfilePram73.ReverseDir=True
ProfilePram73.ReverseAngle=True
ProfilePram73.CalcSnipOnlyAttachLines=False
ProfilePram73.AttachDirMethod=0
ProfilePram73.CCWDefAngle=False
ProfilePram73.AddEnd1Elements(extrude_sheet4)
ProfilePram73.End1Type=1102
ProfilePram73.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram73.AddEnd2Elements(profile54[0])
ProfilePram73.End2Type=1102
ProfilePram73.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram73.End1ScallopType=1120
ProfilePram73.End1ScallopTypeParams=["50"]
ProfilePram73.End2ScallopType=1120
ProfilePram73.End2ScallopTypeParams=["50"]
profile73 = part.CreateProfile(ProfilePram73,False)
part.SetElementColor(profile73[0],"255","0","0","0.19999998807907104")
mirror_copied24 = part.MirrorCopy([profile73[0]],"PL,Y","")
part.SetElementColor(mirror_copied24[0],"255","0","0","0.19999998807907104")
bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=1
bracketPram1.BracketName="HK.Casing.Wall.Fore.DL03.Deck.DP"
bracketPram1.MaterialName="SS400"
bracketPram1.BaseElement=profile18[0]
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="+"
bracketPram1.Thickness="7.9999999999999964"
bracketPram1.BracketType=1501
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=-1
bracketPram1.Surfaces1=[profile18[0]+",FL"]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=[profile9[0]+",FL"]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1531
bracketPram1.Sf1DimensonParams=["200","15"]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["200","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"0","255","255","0.19999998807907104")
ProfilePram74 = part.CreateProfileParam()
ProfilePram74.DefinitionType=1
ProfilePram74.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram74.AddAttachSurfaces(extrude_sheet7)
ProfilePram74.ProfileName="HK.Casing.Wall.Side.FR10.CDP"
ProfilePram74.MaterialName="SS400"
ProfilePram74.ProfileType=1002
ProfilePram74.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram74.Mold="+"
ProfilePram74.ReverseDir=False
ProfilePram74.ReverseAngle=True
ProfilePram74.CalcSnipOnlyAttachLines=False
ProfilePram74.AttachDirMethod=0
ProfilePram74.CCWDefAngle=False
ProfilePram74.AddEnd1Elements(extrude_sheet6)
ProfilePram74.End1Type=1102
ProfilePram74.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram74.AddEnd2Elements(extrude_sheet5)
ProfilePram74.End2Type=1102
ProfilePram74.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram74.End1ScallopType=1121
ProfilePram74.End1ScallopTypeParams=["35","40"]
ProfilePram74.End2ScallopType=1121
ProfilePram74.End2ScallopTypeParams=["35","40"]
profile74 = part.CreateProfile(ProfilePram74,False)
part.SetElementColor(profile74[0],"255","0","0","0.19999998807907104")
mirror_copied25 = part.MirrorCopy([profile74[0]],"PL,Y","")
part.SetElementColor(mirror_copied25[0],"255","0","0","0.19999998807907104")
ProfilePram75 = part.CreateProfileParam()
ProfilePram75.DefinitionType=1
ProfilePram75.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram75.AddAttachSurfaces(extrude_sheet7)
ProfilePram75.ProfileName="HK.Casing.Wall.Side.FR14.OAP"
ProfilePram75.MaterialName="SS400"
ProfilePram75.ProfileType=1002
ProfilePram75.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram75.Mold="+"
ProfilePram75.ReverseDir=False
ProfilePram75.ReverseAngle=True
ProfilePram75.CalcSnipOnlyAttachLines=False
ProfilePram75.AttachDirMethod=0
ProfilePram75.CCWDefAngle=False
ProfilePram75.AddEnd1Elements(extrude_sheet2)
ProfilePram75.End1Type=1102
ProfilePram75.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram75.AddEnd2Elements(extrude_sheet8)
ProfilePram75.End2Type=1102
ProfilePram75.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram75.End1ScallopType=1121
ProfilePram75.End1ScallopTypeParams=["35","40"]
ProfilePram75.End2ScallopType=1121
ProfilePram75.End2ScallopTypeParams=["35","40"]
profile75 = part.CreateProfile(ProfilePram75,False)
part.SetElementColor(profile75[0],"255","0","0","0.19999998807907104")
mirror_copied26 = part.MirrorCopy([profile38[1]],"PL,Y","")
part.SetElementColor(mirror_copied26[0],"148","0","211","0.39999997615814209")
ProfilePram76 = part.CreateProfileParam()
ProfilePram76.DefinitionType=1
ProfilePram76.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram76.AddAttachSurfaces(extrude_sheet3)
ProfilePram76.ProfileName="HK.Casing.Wall.Fore.DL05.ABP"
ProfilePram76.MaterialName="SS400"
ProfilePram76.ProfileType=1002
ProfilePram76.ProfileParams=["125","75","7","10","5"]
ProfilePram76.Mold="+"
ProfilePram76.ReverseDir=True
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
ProfilePram76.End1ScallopTypeParams=["25","40"]
ProfilePram76.End2ScallopType=1121
ProfilePram76.End2ScallopTypeParams=["25","40"]
profile76 = part.CreateProfile(ProfilePram76,False)
part.SetElementColor(profile76[0],"255","0","0","0.19999998807907104")
ProfilePram77 = part.CreateProfileParam()
ProfilePram77.DefinitionType=1
ProfilePram77.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram77.AddAttachSurfaces(extrude_sheet3)
ProfilePram77.ProfileName="HK.Casing.Wall.Fore.DL01.BCP"
ProfilePram77.MaterialName="SS400"
ProfilePram77.ProfileType=1002
ProfilePram77.ProfileParams=["125","75","7","10","5"]
ProfilePram77.Mold="+"
ProfilePram77.ReverseDir=True
ProfilePram77.ReverseAngle=True
ProfilePram77.CalcSnipOnlyAttachLines=False
ProfilePram77.AttachDirMethod=0
ProfilePram77.CCWDefAngle=False
ProfilePram77.AddEnd1Elements(extrude_sheet5)
ProfilePram77.End1Type=1102
ProfilePram77.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram77.AddEnd2Elements(extrude_sheet1)
ProfilePram77.End2Type=1102
ProfilePram77.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram77.End1ScallopType=1121
ProfilePram77.End1ScallopTypeParams=["25","40"]
ProfilePram77.End2ScallopType=1121
ProfilePram77.End2ScallopTypeParams=["25","40"]
profile77 = part.CreateProfile(ProfilePram77,False)
part.SetElementColor(profile77[0],"255","0","0","0.19999998807907104")
ProfilePram78 = part.CreateProfileParam()
ProfilePram78.DefinitionType=1
ProfilePram78.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram78.AddAttachSurfaces(extrude_sheet7)
ProfilePram78.ProfileName="HK.Casing.Wall.Side.FR08.ABP"
ProfilePram78.MaterialName="SS400"
ProfilePram78.ProfileType=1002
ProfilePram78.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram78.Mold="+"
ProfilePram78.ReverseDir=False
ProfilePram78.ReverseAngle=True
ProfilePram78.CalcSnipOnlyAttachLines=False
ProfilePram78.AttachDirMethod=0
ProfilePram78.CCWDefAngle=False
ProfilePram78.AddEnd1Elements(extrude_sheet1)
ProfilePram78.End1Type=1102
ProfilePram78.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram78.AddEnd2Elements(extrude_sheet2)
ProfilePram78.End2Type=1102
ProfilePram78.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram78.End1ScallopType=1121
ProfilePram78.End1ScallopTypeParams=["35","40"]
ProfilePram78.End2ScallopType=1121
ProfilePram78.End2ScallopTypeParams=["35","40"]
profile78 = part.CreateProfile(ProfilePram78,False)
part.SetElementColor(profile78[0],"255","0","0","0.19999998807907104")
mirror_copied27 = part.MirrorCopy([profile78[0]],"PL,Y","")
part.SetElementColor(mirror_copied27[0],"255","0","0","0.19999998807907104")
mirror_copied28 = part.MirrorCopy([profile68[0]],"PL,Y","")
part.SetElementColor(mirror_copied28[0],"148","0","211","0.39999997615814209")
solid6 = part.CreateSolid("HK.Casing.Wall.Aft.CD","","SS400")
part.SetElementColor(solid6,"139","69","19","0.79999995231628418")
thicken6 = part.CreateThicken("厚み付け11",solid6,"+",[extrude_sheet4],"-","10","0","0",False,False)
extrudePram21 = part.CreateLinearSweepParam()
extrudePram21.Name="積-押し出し19"
extrudePram21.AddProfile(extrude_sheet7)
extrudePram21.DirectionType="R"
extrudePram21.DirectionParameter1="50000"
extrudePram21.SweepDirection="+Y"
extrudePram21.RefByGeometricMethod=False
extrude12 = part.CreateLinearSweep(solid6,"*",extrudePram21,False)
extrudePram22 = part.CreateLinearSweepParam()
extrudePram22.Name="積-押し出し20"
extrudePram22.AddProfile(extrude_sheet9)
extrudePram22.DirectionType="N"
extrudePram22.DirectionParameter1="50000"
extrudePram22.SweepDirection="+Y"
extrudePram22.RefByGeometricMethod=False
extrude13 = part.CreateLinearSweep(solid6,"*",extrudePram22,False)
mirror_copied29 = part.MirrorCopy([profile77[0]],"PL,Y","")
part.SetElementColor(mirror_copied29[0],"255","0","0","0.19999998807907104")
mirror_copied30 = part.MirrorCopy([profile3[0]],"PL,Y","")
part.SetElementColor(mirror_copied30[0],"148","0","211","0.39999997615814209")
mirror_copied31 = part.MirrorCopy([profile64[1]],"PL,Y","")
part.SetElementColor(mirror_copied31[0],"148","0","211","0.39999997615814209")
mirror_copied32 = part.MirrorCopy([profile45[0]],"PL,Y","")
part.SetElementColor(mirror_copied32[0],"148","0","211","0.39999997615814209")
ProfilePram79 = part.CreateProfileParam()
ProfilePram79.DefinitionType=1
ProfilePram79.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram79.AddAttachSurfaces(extrude_sheet7)
ProfilePram79.ProfileName="HK.Casing.Wall.Side.FR09.ABP"
ProfilePram79.MaterialName="SS400"
ProfilePram79.ProfileType=1003
ProfilePram79.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram79.Mold="+"
ProfilePram79.ReverseDir=False
ProfilePram79.ReverseAngle=True
ProfilePram79.CalcSnipOnlyAttachLines=False
ProfilePram79.AttachDirMethod=0
ProfilePram79.CCWDefAngle=False
ProfilePram79.AddEnd1Elements(extrude_sheet1)
ProfilePram79.End1Type=1103
ProfilePram79.End1TypeParams=["0"]
ProfilePram79.AddEnd2Elements(extrude_sheet2)
ProfilePram79.End2Type=1103
ProfilePram79.End2TypeParams=["0"]
ProfilePram79.End1ScallopType=1120
ProfilePram79.End1ScallopTypeParams=["50"]
ProfilePram79.End2ScallopType=1120
ProfilePram79.End2ScallopTypeParams=["50"]
profile79 = part.CreateProfile(ProfilePram79,False)
part.SetElementColor(profile79[0],"148","0","211","0.39999997615814209")
ProfilePram80 = part.CreateProfileParam()
ProfilePram80.DefinitionType=1
ProfilePram80.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram80.AddAttachSurfaces(extrude_sheet1)
ProfilePram80.ProfileName="HK.Casing.Deck.B.FR09P"
ProfilePram80.MaterialName="SS400"
ProfilePram80.ProfileType=1003
ProfilePram80.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram80.Mold="+"
ProfilePram80.ReverseDir=True
ProfilePram80.ReverseAngle=False
ProfilePram80.CalcSnipOnlyAttachLines=False
ProfilePram80.AttachDirMethod=0
ProfilePram80.CCWDefAngle=False
ProfilePram80.AddEnd1Elements(profile4[0])
ProfilePram80.End1Type=1113
ProfilePram80.End1TypeParams=["0","79"]
ProfilePram80.AddEnd2Elements(profile79[0])
ProfilePram80.End2Type=1102
ProfilePram80.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram80.End1ScallopType=1120
ProfilePram80.End1ScallopTypeParams=["50"]
ProfilePram80.End2ScallopType=1120
ProfilePram80.End2ScallopTypeParams=["50"]
profile80 = part.CreateProfile(ProfilePram80,False)
part.SetElementColor(profile80[0],"148","0","211","0.39999997615814209")
mirror_copied33 = part.MirrorCopy([profile80[0]],"PL,Y","")
part.SetElementColor(mirror_copied33[0],"148","0","211","0.39999997615814209")
ProfilePram81 = part.CreateProfileParam()
ProfilePram81.DefinitionType=1
ProfilePram81.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram81.AddAttachSurfaces(extrude_sheet4)
ProfilePram81.ProfileName="HK.Casing.Wall.Aft.DL01.BCP"
ProfilePram81.MaterialName="SS400"
ProfilePram81.ProfileType=1002
ProfilePram81.ProfileParams=["125","75","7","10","5"]
ProfilePram81.Mold="+"
ProfilePram81.ReverseDir=False
ProfilePram81.ReverseAngle=True
ProfilePram81.CalcSnipOnlyAttachLines=False
ProfilePram81.AttachDirMethod=0
ProfilePram81.CCWDefAngle=False
ProfilePram81.AddEnd1Elements(extrude_sheet5)
ProfilePram81.End1Type=1102
ProfilePram81.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram81.AddEnd2Elements(extrude_sheet1)
ProfilePram81.End2Type=1102
ProfilePram81.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram81.End1ScallopType=1121
ProfilePram81.End1ScallopTypeParams=["25","40"]
ProfilePram81.End2ScallopType=1121
ProfilePram81.End2ScallopTypeParams=["25","40"]
profile81 = part.CreateProfile(ProfilePram81,False)
part.SetElementColor(profile81[0],"255","0","0","0.19999998807907104")
bracketPram2 = part.CreateBracketParam()
bracketPram2.DefinitionType=1
bracketPram2.BracketName="HK.Casing.Wall.Aft.DL03.Deck.DP"
bracketPram2.MaterialName="SS400"
bracketPram2.BaseElement=profile72[0]
bracketPram2.UseSideSheetForPlane=False
bracketPram2.Mold="+"
bracketPram2.Thickness="7.9999999999999964"
bracketPram2.BracketType=1501
bracketPram2.Scallop1Type=1801
bracketPram2.Scallop1Params=["0"]
bracketPram2.Scallop2Type=-1
bracketPram2.Surfaces1=[profile72[0]+",FL"]
bracketPram2.RevSf1=False
bracketPram2.Surfaces2=[profile9[0]+",FL"]
bracketPram2.RevSf2=False
bracketPram2.RevSf3=False
bracketPram2.Sf1DimensionType=1531
bracketPram2.Sf1DimensonParams=["200","15"]
bracketPram2.Sf2DimensionType=1531
bracketPram2.Sf2DimensonParams=["200","15"]
bracket2 = part.CreateBracket(bracketPram2,False)
part.SetElementColor(bracket2,"0","255","255","0.19999998807907104")
ProfilePram82 = part.CreateProfileParam()
ProfilePram82.DefinitionType=1
ProfilePram82.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram82.AddAttachSurfaces(extrude_sheet3)
ProfilePram82.ProfileName="HK.Casing.Wall.Fore.DL02.BCP"
ProfilePram82.MaterialName="SS400"
ProfilePram82.FlangeName="HK.Casing.Wall.Fore.DL02.BCP"
ProfilePram82.FlangeMaterialName="SS400"
ProfilePram82.ProfileType=1201
ProfilePram82.ProfileParams=["150","12","388","10"]
ProfilePram82.Mold="-"
ProfilePram82.ReverseDir=True
ProfilePram82.ReverseAngle=False
ProfilePram82.CalcSnipOnlyAttachLines=False
ProfilePram82.AttachDirMethod=0
ProfilePram82.CCWDefAngle=False
ProfilePram82.AddEnd1Elements(extrude_sheet5)
ProfilePram82.End1Type=1102
ProfilePram82.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram82.AddEnd2Elements(extrude_sheet1)
ProfilePram82.End2Type=1102
ProfilePram82.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram82.End1ScallopType=1120
ProfilePram82.End1ScallopTypeParams=["50"]
ProfilePram82.End2ScallopType=1120
ProfilePram82.End2ScallopTypeParams=["50"]
profile82 = part.CreateProfile(ProfilePram82,False)
part.SetElementColor(profile82[0],"148","0","211","0.39999997615814209")
part.SetElementColor(profile82[1],"148","0","211","0.39999997615814209")
ProfilePram83 = part.CreateProfileParam()
ProfilePram83.DefinitionType=1
ProfilePram83.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram83.AddAttachSurfaces(extrude_sheet7)
ProfilePram83.ProfileName="HK.Casing.Wall.Side.FR07.BCP"
ProfilePram83.MaterialName="SS400"
ProfilePram83.ProfileType=1002
ProfilePram83.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram83.Mold="+"
ProfilePram83.ReverseDir=False
ProfilePram83.ReverseAngle=True
ProfilePram83.CalcSnipOnlyAttachLines=False
ProfilePram83.AttachDirMethod=0
ProfilePram83.CCWDefAngle=False
ProfilePram83.AddEnd1Elements(extrude_sheet5)
ProfilePram83.End1Type=1102
ProfilePram83.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram83.AddEnd2Elements(extrude_sheet1)
ProfilePram83.End2Type=1102
ProfilePram83.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram83.End1ScallopType=1121
ProfilePram83.End1ScallopTypeParams=["35","40"]
ProfilePram83.End2ScallopType=1121
ProfilePram83.End2ScallopTypeParams=["35","40"]
profile83 = part.CreateProfile(ProfilePram83,False)
part.SetElementColor(profile83[0],"255","0","0","0.19999998807907104")
solid7 = part.CreateSolid("HK.Casing.Wall.Aft.BC","","SS400")
part.SetElementColor(solid7,"139","69","19","0.79999995231628418")
thicken7 = part.CreateThicken("厚み付け12",solid7,"+",[extrude_sheet4],"-","10","0","0",False,False)
extrudePram23 = part.CreateLinearSweepParam()
extrudePram23.Name="積-押し出し23"
extrudePram23.AddProfile(extrude_sheet7)
extrudePram23.DirectionType="R"
extrudePram23.DirectionParameter1="50000"
extrudePram23.SweepDirection="+Y"
extrudePram23.RefByGeometricMethod=False
extrude14 = part.CreateLinearSweep(solid7,"*",extrudePram23,False)
extrudePram24 = part.CreateLinearSweepParam()
extrudePram24.Name="積-押し出し24"
extrudePram24.AddProfile(extrude_sheet9)
extrudePram24.DirectionType="N"
extrudePram24.DirectionParameter1="50000"
extrudePram24.SweepDirection="+Y"
extrudePram24.RefByGeometricMethod=False
extrude15 = part.CreateLinearSweep(solid7,"*",extrudePram24,False)
extrudePram25 = part.CreateLinearSweepParam()
extrudePram25.Name="積-押し出し25"
extrudePram25.AddProfile(extrude_sheet5)
extrudePram25.DirectionType="R"
extrudePram25.DirectionParameter1="50000"
extrudePram25.SweepDirection="+Z"
extrudePram25.RefByGeometricMethod=False
extrude16 = part.CreateLinearSweep(solid7,"*",extrudePram25,False)
ProfilePram84 = part.CreateProfileParam()
ProfilePram84.DefinitionType=1
ProfilePram84.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram84.AddAttachSurfaces(extrude_sheet5)
ProfilePram84.ProfileName="HK.Casing.Deck.C.DL01.FP"
ProfilePram84.MaterialName="SS400"
ProfilePram84.ProfileType=1002
ProfilePram84.ProfileParams=["125","75","7","10","5"]
ProfilePram84.Mold="+"
ProfilePram84.ReverseDir=True
ProfilePram84.ReverseAngle=True
ProfilePram84.CalcSnipOnlyAttachLines=False
ProfilePram84.AttachDirMethod=0
ProfilePram84.CCWDefAngle=False
ProfilePram84.AddEnd1Elements(profile13[0])
ProfilePram84.End1Type=1102
ProfilePram84.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram84.AddEnd2Elements(profile77[0])
ProfilePram84.End2Type=1102
ProfilePram84.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram84.End1ScallopType=1121
ProfilePram84.End1ScallopTypeParams=["25","40"]
ProfilePram84.End2ScallopType=1121
ProfilePram84.End2ScallopTypeParams=["25","40"]
profile84 = part.CreateProfile(ProfilePram84,False)
part.SetElementColor(profile84[0],"255","0","0","0.19999998807907104")
solid8 = part.CreateSolid("HK.Casing.Wall.Side.OAP","","SS400")
part.SetElementColor(solid8,"139","69","19","0.79999995231628418")
thicken8 = part.CreateThicken("厚み付け10",solid8,"+",[extrude_sheet7],"-","10","0","0",False,False)
extrudePram26 = part.CreateLinearSweepParam()
extrudePram26.Name="積-押し出し16"
extrudePram26.AddProfile(skt_pl3+",Edge00")
extrudePram26.DirectionType="N"
extrudePram26.DirectionParameter1="50000"
extrudePram26.SweepDirection="+Z"
extrudePram26.RefByGeometricMethod=False
extrude17 = part.CreateLinearSweep(solid8,"*",extrudePram26,False)
extrudePram27 = part.CreateLinearSweepParam()
extrudePram27.Name="積-押し出し17"
extrudePram27.AddProfile(extrude_sheet2)
extrudePram27.DirectionType="R"
extrudePram27.DirectionParameter1="50000"
extrudePram27.SweepDirection="+Z"
extrudePram27.RefByGeometricMethod=False
extrude18 = part.CreateLinearSweep(solid8,"*",extrudePram27,False)
extrudePram28 = part.CreateLinearSweepParam()
extrudePram28.Name="積-押し出し18"
extrudePram28.AddProfile(extrude_sheet8)
extrudePram28.DirectionType="N"
extrudePram28.DirectionParameter1="50000"
extrudePram28.SweepDirection="+Z"
extrudePram28.RefByGeometricMethod=False
extrude19 = part.CreateLinearSweep(solid8,"*",extrudePram28,False)
extrudePram29 = part.CreateLinearSweepParam()
extrudePram29.Name="積-押し出し14"
extrudePram29.AddProfile(extrude_sheet1)
extrudePram29.DirectionType="R"
extrudePram29.DirectionParameter1="50000"
extrudePram29.SweepDirection="+Z"
extrudePram29.RefByGeometricMethod=False
extrude20 = part.CreateLinearSweep(solid2,"*",extrudePram29,False)
extrudePram30 = part.CreateLinearSweepParam()
extrudePram30.Name="積-押し出し15"
extrudePram30.AddProfile(extrude_sheet2)
extrudePram30.DirectionType="N"
extrudePram30.DirectionParameter1="50000"
extrudePram30.SweepDirection="+Z"
extrudePram30.RefByGeometricMethod=False
extrude21 = part.CreateLinearSweep(solid2,"*",extrudePram30,False)
mirror_copied34 = part.MirrorCopy([solid2],"PL,Y","")
part.SetElementColor(mirror_copied34[0],"139","69","19","0.79999995231628418")
ProfilePram85 = part.CreateProfileParam()
ProfilePram85.DefinitionType=1
ProfilePram85.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram85.AddAttachSurfaces(extrude_sheet1)
ProfilePram85.ProfileName="HK.Casing.Deck.B.FR13P"
ProfilePram85.MaterialName="SS400"
ProfilePram85.ProfileType=1003
ProfilePram85.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram85.Mold="+"
ProfilePram85.ReverseDir=True
ProfilePram85.ReverseAngle=False
ProfilePram85.CalcSnipOnlyAttachLines=False
ProfilePram85.AttachDirMethod=0
ProfilePram85.CCWDefAngle=False
ProfilePram85.AddEnd1Elements(profile4[0])
ProfilePram85.End1Type=1113
ProfilePram85.End1TypeParams=["0","79"]
ProfilePram85.AddEnd2Elements(profile32[0])
ProfilePram85.End2Type=1102
ProfilePram85.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram85.End1ScallopType=1120
ProfilePram85.End1ScallopTypeParams=["50"]
ProfilePram85.End2ScallopType=1120
ProfilePram85.End2ScallopTypeParams=["50"]
profile85 = part.CreateProfile(ProfilePram85,False)
part.SetElementColor(profile85[0],"148","0","211","0.39999997615814209")
ProfilePram86 = part.CreateProfileParam()
ProfilePram86.DefinitionType=1
ProfilePram86.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram86.AddAttachSurfaces(extrude_sheet7)
ProfilePram86.ProfileName="HK.Casing.Wall.Side.FR14.BCP"
ProfilePram86.MaterialName="SS400"
ProfilePram86.ProfileType=1002
ProfilePram86.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram86.Mold="+"
ProfilePram86.ReverseDir=False
ProfilePram86.ReverseAngle=True
ProfilePram86.CalcSnipOnlyAttachLines=False
ProfilePram86.AttachDirMethod=0
ProfilePram86.CCWDefAngle=False
ProfilePram86.AddEnd1Elements(extrude_sheet5)
ProfilePram86.End1Type=1102
ProfilePram86.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram86.AddEnd2Elements(extrude_sheet1)
ProfilePram86.End2Type=1102
ProfilePram86.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram86.End1ScallopType=1121
ProfilePram86.End1ScallopTypeParams=["35","40"]
ProfilePram86.End2ScallopType=1121
ProfilePram86.End2ScallopTypeParams=["35","40"]
profile86 = part.CreateProfile(ProfilePram86,False)
part.SetElementColor(profile86[0],"255","0","0","0.19999998807907104")
mirror_copied35 = part.MirrorCopy([profile86[0]],"PL,Y","")
part.SetElementColor(mirror_copied35[0],"255","0","0","0.19999998807907104")
ProfilePram87 = part.CreateProfileParam()
ProfilePram87.DefinitionType=1
ProfilePram87.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram87.AddAttachSurfaces(extrude_sheet7)
ProfilePram87.ProfileName="HK.Casing.Wall.Side.FR14.ABP"
ProfilePram87.MaterialName="SS400"
ProfilePram87.ProfileType=1002
ProfilePram87.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram87.Mold="+"
ProfilePram87.ReverseDir=False
ProfilePram87.ReverseAngle=True
ProfilePram87.CalcSnipOnlyAttachLines=False
ProfilePram87.AttachDirMethod=0
ProfilePram87.CCWDefAngle=False
ProfilePram87.AddEnd1Elements(extrude_sheet1)
ProfilePram87.End1Type=1102
ProfilePram87.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram87.AddEnd2Elements(extrude_sheet2)
ProfilePram87.End2Type=1102
ProfilePram87.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram87.End1ScallopType=1121
ProfilePram87.End1ScallopTypeParams=["35","40"]
ProfilePram87.End2ScallopType=1121
ProfilePram87.End2ScallopTypeParams=["35","40"]
profile87 = part.CreateProfile(ProfilePram87,False)
part.SetElementColor(profile87[0],"255","0","0","0.19999998807907104")
ProfilePram88 = part.CreateProfileParam()
ProfilePram88.DefinitionType=1
ProfilePram88.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram88.AddAttachSurfaces(extrude_sheet7)
ProfilePram88.ProfileName="HK.Casing.Wall.Side.FR10.BCP"
ProfilePram88.MaterialName="SS400"
ProfilePram88.ProfileType=1002
ProfilePram88.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram88.Mold="+"
ProfilePram88.ReverseDir=False
ProfilePram88.ReverseAngle=True
ProfilePram88.CalcSnipOnlyAttachLines=False
ProfilePram88.AttachDirMethod=0
ProfilePram88.CCWDefAngle=False
ProfilePram88.AddEnd1Elements(extrude_sheet5)
ProfilePram88.End1Type=1102
ProfilePram88.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram88.AddEnd2Elements(extrude_sheet1)
ProfilePram88.End2Type=1102
ProfilePram88.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram88.End1ScallopType=1121
ProfilePram88.End1ScallopTypeParams=["35","40"]
ProfilePram88.End2ScallopType=1121
ProfilePram88.End2ScallopTypeParams=["35","40"]
profile88 = part.CreateProfile(ProfilePram88,False)
part.SetElementColor(profile88[0],"255","0","0","0.19999998807907104")
mirror_copied36 = part.MirrorCopy([profile88[0]],"PL,Y","")
part.SetElementColor(mirror_copied36[0],"255","0","0","0.19999998807907104")
mirror_copied37 = part.MirrorCopy([profile2[0]],"PL,Y","")
part.SetElementColor(mirror_copied37[0],"148","0","211","0.39999997615814209")
extrudePram31 = part.CreateLinearSweepParam()
extrudePram31.Name="削除-押し出し2"
extrudePram31.AddProfile(skt_pl4+",Edge01")
extrudePram31.DirectionType="T"
extrudePram31.RefByGeometricMethod=False
extrude22 = part.CreateLinearSweep(solid1,"-",extrudePram31,False)
ProfilePram89 = part.CreateProfileParam()
ProfilePram89.DefinitionType=1
ProfilePram89.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram89.AddAttachSurfaces(extrude_sheet7)
ProfilePram89.ProfileName="HK.Casing.Wall.Side.FR11.BCP"
ProfilePram89.MaterialName="SS400"
ProfilePram89.ProfileType=1002
ProfilePram89.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram89.Mold="+"
ProfilePram89.ReverseDir=False
ProfilePram89.ReverseAngle=True
ProfilePram89.CalcSnipOnlyAttachLines=False
ProfilePram89.AttachDirMethod=0
ProfilePram89.CCWDefAngle=False
ProfilePram89.AddEnd1Elements(extrude_sheet5)
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
solid9 = part.CreateSolid("HK.Casing.Deck.A","","SS400")
part.SetElementColor(solid9,"139","69","19","0.78999996185302734")
thicken9 = part.CreateThicken("厚み付け6",solid9,"+",[extrude_sheet2],"+","10","0","0",False,False)
skt_pl6 = part.CreateSketchPlane("HK.Az.Deck.A","","PL,Z","0",False,False,False,"","","",False,False)
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
skt_arc14 = part.CreateSketchArc(skt_pl6,"","Edge01","9770,2724.9999999999995","10170,2725","9770,3125",True,False)
skt_arc15 = part.CreateSketchArc(skt_pl6,"","Edge01","9770,-2724.9999999999995","9770,-3124.9999999999995","10170,-2725",True,False)
skt_arc16 = part.CreateSketchArc(skt_pl6,"","Edge01","4835.0000000000009,-2725","4435.0000000000009,-2724.9999999999995","4835.0000000000009,-3125.0000000000005",True,False)
extrudePram32 = part.CreateLinearSweepParam()
extrudePram32.Name="積-押し出し6"
extrudePram32.AddProfile(skt_pl6+",Edge00")
extrudePram32.DirectionType="N"
extrudePram32.DirectionParameter1="50000"
extrudePram32.SweepDirection="+Z"
extrudePram32.RefByGeometricMethod=False
extrude23 = part.CreateLinearSweep(solid9,"*",extrudePram32,False)
extrudePram33 = part.CreateLinearSweepParam()
extrudePram33.Name="削除-押し出し4"
extrudePram33.AddProfile(skt_pl6+",Edge01")
extrudePram33.DirectionType="T"
extrudePram33.RefByGeometricMethod=False
extrude24 = part.CreateLinearSweep(solid9,"-",extrudePram33,False)
ProfilePram90 = part.CreateProfileParam()
ProfilePram90.DefinitionType=1
ProfilePram90.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram90.AddAttachSurfaces(extrude_sheet4)
ProfilePram90.ProfileName="HK.Casing.Wall.Aft.DL05.CDP"
ProfilePram90.MaterialName="SS400"
ProfilePram90.ProfileType=1002
ProfilePram90.ProfileParams=["125","75","7","10","5"]
ProfilePram90.Mold="+"
ProfilePram90.ReverseDir=False
ProfilePram90.ReverseAngle=True
ProfilePram90.CalcSnipOnlyAttachLines=False
ProfilePram90.AttachDirMethod=0
ProfilePram90.CCWDefAngle=False
ProfilePram90.AddEnd1Elements(profile59[0])
ProfilePram90.End1Type=1102
ProfilePram90.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram90.AddEnd2Elements(extrude_sheet5)
ProfilePram90.End2Type=1102
ProfilePram90.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram90.End1ScallopType=1120
ProfilePram90.End1ScallopTypeParams=["50"]
ProfilePram90.End2ScallopType=1120
ProfilePram90.End2ScallopTypeParams=["50"]
profile90 = part.CreateProfile(ProfilePram90,False)
part.SetElementColor(profile90[0],"255","0","0","0.19999998807907104")
bracketPram3 = part.CreateBracketParam()
bracketPram3.DefinitionType=1
bracketPram3.BracketName="HK.Casing.Wall.Aft.DL05.Deck.DP"
bracketPram3.MaterialName="SS400"
bracketPram3.BaseElement=profile90[0]
bracketPram3.UseSideSheetForPlane=False
bracketPram3.Mold="+"
bracketPram3.Thickness="7.9999999999999964"
bracketPram3.BracketType=1501
bracketPram3.Scallop1Type=1801
bracketPram3.Scallop1Params=["0"]
bracketPram3.Scallop2Type=-1
bracketPram3.Surfaces1=[profile90[0]+",FL"]
bracketPram3.RevSf1=False
bracketPram3.Surfaces2=[profile59[0]+",FL"]
bracketPram3.RevSf2=False
bracketPram3.RevSf3=False
bracketPram3.Sf1DimensionType=1531
bracketPram3.Sf1DimensonParams=["200","15"]
bracketPram3.Sf2DimensionType=1531
bracketPram3.Sf2DimensonParams=["200","15"]
bracket3 = part.CreateBracket(bracketPram3,False)
part.SetElementColor(bracket3,"0","255","255","0.19999998807907104")
ProfilePram91 = part.CreateProfileParam()
ProfilePram91.DefinitionType=1
ProfilePram91.BasePlane="PL,O,"+var_elm4+","+"X"
ProfilePram91.AddAttachSurfaces(extrude_sheet7)
ProfilePram91.ProfileName="HK.Casing.Wall.Side.FR12.ABP"
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
mirror_copied38 = part.MirrorCopy([profile91[0]],"PL,Y","")
part.SetElementColor(mirror_copied38[0],"255","0","0","0.19999998807907104")
solid10 = part.CreateSolid("HK.Casing.Wall.Fore.CD","","SS400")
part.SetElementColor(solid10,"139","69","19","0.79999995231628418")
thicken10 = part.CreateThicken("厚み付け15",solid10,"+",[extrude_sheet3],"+","10","0","0",False,False)
extrudePram34 = part.CreateLinearSweepParam()
extrudePram34.Name="積-押し出し35"
extrudePram34.AddProfile(extrude_sheet7)
extrudePram34.DirectionType="R"
extrudePram34.DirectionParameter1="50000"
extrudePram34.SweepDirection="+Y"
extrudePram34.RefByGeometricMethod=False
extrude25 = part.CreateLinearSweep(solid10,"*",extrudePram34,False)
extrudePram35 = part.CreateLinearSweepParam()
extrudePram35.Name="積-押し出し36"
extrudePram35.AddProfile(extrude_sheet9)
extrudePram35.DirectionType="N"
extrudePram35.DirectionParameter1="50000"
extrudePram35.SweepDirection="+Y"
extrudePram35.RefByGeometricMethod=False
extrude26 = part.CreateLinearSweep(solid10,"*",extrudePram35,False)
mirror_copied39 = part.MirrorCopy([profile52[1]],"PL,Y","")
part.SetElementColor(mirror_copied39[0],"148","0","211","0.39999997615814209")
ProfilePram92 = part.CreateProfileParam()
ProfilePram92.DefinitionType=1
ProfilePram92.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram92.AddAttachSurfaces(extrude_sheet4)
ProfilePram92.ProfileName="HK.Casing.Wall.Aft.DL00.AB"
ProfilePram92.MaterialName="SS400"
ProfilePram92.ProfileType=1002
ProfilePram92.ProfileParams=["125","75","7","10","5"]
ProfilePram92.Mold="+"
ProfilePram92.ReverseDir=False
ProfilePram92.ReverseAngle=True
ProfilePram92.CalcSnipOnlyAttachLines=False
ProfilePram92.AttachDirMethod=0
ProfilePram92.CCWDefAngle=False
ProfilePram92.AddEnd1Elements(extrude_sheet1)
ProfilePram92.End1Type=1102
ProfilePram92.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram92.AddEnd2Elements(extrude_sheet2)
ProfilePram92.End2Type=1102
ProfilePram92.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram92.End1ScallopType=1121
ProfilePram92.End1ScallopTypeParams=["25","40"]
ProfilePram92.End2ScallopType=1121
ProfilePram92.End2ScallopTypeParams=["25","40"]
profile92 = part.CreateProfile(ProfilePram92,False)
part.SetElementColor(profile92[0],"255","0","0","0.19999998807907104")
mirror_copied40 = part.MirrorCopy([solid8],"PL,Y","")
part.SetElementColor(mirror_copied40[0],"139","69","19","0.79999995231628418")
mirror_copied41 = part.MirrorCopy([profile49[0]],"PL,Y","")
part.SetElementColor(mirror_copied41[0],"148","0","211","0.39999997615814209")
ProfilePram93 = part.CreateProfileParam()
ProfilePram93.DefinitionType=1
ProfilePram93.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram93.AddAttachSurfaces(extrude_sheet7)
ProfilePram93.ProfileName="HK.Casing.Wall.Side.FR11.OAP"
ProfilePram93.MaterialName="SS400"
ProfilePram93.ProfileType=1002
ProfilePram93.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram93.Mold="+"
ProfilePram93.ReverseDir=False
ProfilePram93.ReverseAngle=True
ProfilePram93.CalcSnipOnlyAttachLines=False
ProfilePram93.AttachDirMethod=0
ProfilePram93.CCWDefAngle=False
ProfilePram93.AddEnd1Elements(extrude_sheet2)
ProfilePram93.End1Type=1102
ProfilePram93.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram93.AddEnd2Elements(extrude_sheet8)
ProfilePram93.End2Type=1102
ProfilePram93.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram93.End1ScallopType=1121
ProfilePram93.End1ScallopTypeParams=["35","40"]
ProfilePram93.End2ScallopType=1121
ProfilePram93.End2ScallopTypeParams=["35","40"]
profile93 = part.CreateProfile(ProfilePram93,False)
part.SetElementColor(profile93[0],"255","0","0","0.19999998807907104")
ProfilePram94 = part.CreateProfileParam()
ProfilePram94.DefinitionType=1
ProfilePram94.BasePlane="PL,O,"+var_elm4+","+"X"
ProfilePram94.AddAttachSurfaces(extrude_sheet7)
ProfilePram94.ProfileName="HK.Casing.Wall.Side.FR12.OAP"
ProfilePram94.MaterialName="SS400"
ProfilePram94.ProfileType=1002
ProfilePram94.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram94.Mold="+"
ProfilePram94.ReverseDir=False
ProfilePram94.ReverseAngle=True
ProfilePram94.CalcSnipOnlyAttachLines=False
ProfilePram94.AttachDirMethod=0
ProfilePram94.CCWDefAngle=False
ProfilePram94.AddEnd1Elements(extrude_sheet2)
ProfilePram94.End1Type=1102
ProfilePram94.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram94.AddEnd2Elements(extrude_sheet8)
ProfilePram94.End2Type=1102
ProfilePram94.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram94.End1ScallopType=1121
ProfilePram94.End1ScallopTypeParams=["35","40"]
ProfilePram94.End2ScallopType=1121
ProfilePram94.End2ScallopTypeParams=["35","40"]
profile94 = part.CreateProfile(ProfilePram94,False)
part.SetElementColor(profile94[0],"255","0","0","0.19999998807907104")
ProfilePram95 = part.CreateProfileParam()
ProfilePram95.DefinitionType=1
ProfilePram95.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram95.AddAttachSurfaces(extrude_sheet4)
ProfilePram95.ProfileName="HK.Casing.Wall.Aft.DL00.BC"
ProfilePram95.MaterialName="SS400"
ProfilePram95.ProfileType=1002
ProfilePram95.ProfileParams=["125","75","7","10","5"]
ProfilePram95.Mold="+"
ProfilePram95.ReverseDir=False
ProfilePram95.ReverseAngle=True
ProfilePram95.CalcSnipOnlyAttachLines=False
ProfilePram95.AttachDirMethod=0
ProfilePram95.CCWDefAngle=False
ProfilePram95.AddEnd1Elements(extrude_sheet5)
ProfilePram95.End1Type=1102
ProfilePram95.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram95.AddEnd2Elements(extrude_sheet1)
ProfilePram95.End2Type=1102
ProfilePram95.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram95.End1ScallopType=1121
ProfilePram95.End1ScallopTypeParams=["25","40"]
ProfilePram95.End2ScallopType=1121
ProfilePram95.End2ScallopTypeParams=["25","40"]
profile95 = part.CreateProfile(ProfilePram95,False)
part.SetElementColor(profile95[0],"255","0","0","0.19999998807907104")
solid11 = part.CreateSolid("HK.Casing.Deck.D","","SS400")
part.SetElementColor(solid11,"139","69","19","0.78999996185302734")
thicken11 = part.CreateThicken("厚み付け3",solid11,"+",[extrude_sheet6],"+","10","0","0",False,False)
extrudePram36 = part.CreateLinearSweepParam()
extrudePram36.Name="積-押し出し3"
extrudePram36.AddProfile(skt_pl3+",Edge00")
extrudePram36.DirectionType="N"
extrudePram36.DirectionParameter1="50000"
extrudePram36.SweepDirection="+Z"
extrudePram36.RefByGeometricMethod=False
extrude27 = part.CreateLinearSweep(solid11,"*",extrudePram36,False)
extrudePram37 = part.CreateLinearSweepParam()
extrudePram37.Name="削除-押し出し1"
extrudePram37.AddProfile(skt_pl3+",Edge01")
extrudePram37.DirectionType="T"
extrudePram37.RefByGeometricMethod=False
extrude28 = part.CreateLinearSweep(solid11,"-",extrudePram37,False)
bracketPram4 = part.CreateBracketParam()
bracketPram4.DefinitionType=1
bracketPram4.BracketName="HK.Casing.Wall.Side.FR10.Deck.DP"
bracketPram4.MaterialName="SS400"
bracketPram4.BaseElement=profile74[0]
bracketPram4.UseSideSheetForPlane=False
bracketPram4.Mold="+"
bracketPram4.Thickness="9.9999999999999982"
bracketPram4.BracketType=1505
bracketPram4.BracketParams=["200"]
bracketPram4.Scallop1Type=1801
bracketPram4.Scallop1Params=["0"]
bracketPram4.Scallop2Type=-1
bracketPram4.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram4.RevSf1=False
bracketPram4.Surfaces2=[profile74[0]+",FL"]
bracketPram4.RevSf2=False
bracketPram4.RevSf3=False
bracketPram4.Sf1DimensionType=1541
bracketPram4.Sf1DimensonParams=["0","100"]
bracketPram4.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram4.Sf2DimensionType=1531
bracketPram4.Sf2DimensonParams=["200","15"]
bracket4 = part.CreateBracket(bracketPram4,False)
part.SetElementColor(bracket4,"0","255","255","0.19999998807907104")
solid12 = part.CreateSolid("HK.Casing.Wall.Fore.AB","","SS400")
part.SetElementColor(solid12,"139","69","19","0.79999995231628418")
thicken12 = part.CreateThicken("厚み付け17",solid12,"+",[extrude_sheet3],"+","10","0","0",False,False)
solid13 = part.CreateSolid("HK.Casing.Wall.Aft.AB","","SS400")
part.SetElementColor(solid13,"139","69","19","0.79999995231628418")
thicken13 = part.CreateThicken("厚み付け13",solid13,"+",[extrude_sheet4],"-","10","0","0",False,False)
extrudePram38 = part.CreateLinearSweepParam()
extrudePram38.Name="積-押し出し27"
extrudePram38.AddProfile(extrude_sheet7)
extrudePram38.DirectionType="R"
extrudePram38.DirectionParameter1="50000"
extrudePram38.SweepDirection="+Y"
extrudePram38.RefByGeometricMethod=False
extrude29 = part.CreateLinearSweep(solid13,"*",extrudePram38,False)
extrudePram39 = part.CreateLinearSweepParam()
extrudePram39.Name="積-押し出し28"
extrudePram39.AddProfile(extrude_sheet9)
extrudePram39.DirectionType="N"
extrudePram39.DirectionParameter1="50000"
extrudePram39.SweepDirection="+Y"
extrudePram39.RefByGeometricMethod=False
extrude30 = part.CreateLinearSweep(solid13,"*",extrudePram39,False)
mirror_copied42 = part.MirrorCopy([profile46[0]],"PL,Y","")
part.SetElementColor(mirror_copied42[0],"255","0","0","0.19999998807907104")
solid14 = part.CreateSolid("HK.Casing.Wall.Side.CDP","","SS400")
part.SetElementColor(solid14,"139","69","19","0.79999995231628418")
thicken14 = part.CreateThicken("厚み付け7",solid14,"+",[extrude_sheet7],"-","10","0","0",False,False)
extrudePram40 = part.CreateLinearSweepParam()
extrudePram40.Name="積-押し出し7"
extrudePram40.AddProfile(skt_pl3+",Edge00")
extrudePram40.DirectionType="N"
extrudePram40.DirectionParameter1="50000"
extrudePram40.SweepDirection="+Z"
extrudePram40.RefByGeometricMethod=False
extrude31 = part.CreateLinearSweep(solid14,"*",extrudePram40,False)
extrudePram41 = part.CreateLinearSweepParam()
extrudePram41.Name="積-押し出し8"
extrudePram41.AddProfile(extrude_sheet6)
extrudePram41.DirectionType="R"
extrudePram41.DirectionParameter1="50000"
extrudePram41.SweepDirection="+Z"
extrudePram41.RefByGeometricMethod=False
extrude32 = part.CreateLinearSweep(solid14,"*",extrudePram41,False)
extrudePram42 = part.CreateLinearSweepParam()
extrudePram42.Name="積-押し出し9"
extrudePram42.AddProfile(extrude_sheet5)
extrudePram42.DirectionType="N"
extrudePram42.DirectionParameter1="50000"
extrudePram42.SweepDirection="+Z"
extrudePram42.RefByGeometricMethod=False
extrude33 = part.CreateLinearSweep(solid14,"*",extrudePram42,False)
mirror_copied43 = part.MirrorCopy([solid14],"PL,Y","")
part.SetElementColor(mirror_copied43[0],"139","69","19","0.79999995231628418")
ProfilePram96 = part.CreateProfileParam()
ProfilePram96.DefinitionType=1
ProfilePram96.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram96.AddAttachSurfaces(extrude_sheet4)
ProfilePram96.ProfileName="HK.Casing.Wall.Aft.DL01.CDP"
ProfilePram96.MaterialName="SS400"
ProfilePram96.ProfileType=1002
ProfilePram96.ProfileParams=["125","75","7","10","5"]
ProfilePram96.Mold="+"
ProfilePram96.ReverseDir=False
ProfilePram96.ReverseAngle=True
ProfilePram96.CalcSnipOnlyAttachLines=False
ProfilePram96.AttachDirMethod=0
ProfilePram96.CCWDefAngle=False
ProfilePram96.AddEnd1Elements(profile73[0])
ProfilePram96.End1Type=1102
ProfilePram96.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram96.AddEnd2Elements(extrude_sheet5)
ProfilePram96.End2Type=1102
ProfilePram96.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram96.End1ScallopType=1120
ProfilePram96.End1ScallopTypeParams=["50"]
ProfilePram96.End2ScallopType=1120
ProfilePram96.End2ScallopTypeParams=["50"]
profile96 = part.CreateProfile(ProfilePram96,False)
part.SetElementColor(profile96[0],"255","0","0","0.19999998807907104")
mirror_copied44 = part.MirrorCopy([profile96[0]],"PL,Y","")
part.SetElementColor(mirror_copied44[0],"255","0","0","0.19999998807907104")
ProfilePram97 = part.CreateProfileParam()
ProfilePram97.DefinitionType=1
ProfilePram97.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram97.AddAttachSurfaces(extrude_sheet7)
ProfilePram97.ProfileName="HK.Casing.Wall.Side.FR08.OAP"
ProfilePram97.MaterialName="SS400"
ProfilePram97.ProfileType=1002
ProfilePram97.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram97.Mold="+"
ProfilePram97.ReverseDir=False
ProfilePram97.ReverseAngle=True
ProfilePram97.CalcSnipOnlyAttachLines=False
ProfilePram97.AttachDirMethod=0
ProfilePram97.CCWDefAngle=False
ProfilePram97.AddEnd1Elements(extrude_sheet2)
ProfilePram97.End1Type=1102
ProfilePram97.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram97.AddEnd2Elements(extrude_sheet8)
ProfilePram97.End2Type=1102
ProfilePram97.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram97.End1ScallopType=1121
ProfilePram97.End1ScallopTypeParams=["35","40"]
ProfilePram97.End2ScallopType=1121
ProfilePram97.End2ScallopTypeParams=["35","40"]
profile97 = part.CreateProfile(ProfilePram97,False)
part.SetElementColor(profile97[0],"255","0","0","0.19999998807907104")
mirror_copied45 = part.MirrorCopy([profile79[0]],"PL,Y","")
part.SetElementColor(mirror_copied45[0],"148","0","211","0.39999997615814209")
ProfilePram98 = part.CreateProfileParam()
ProfilePram98.DefinitionType=1
ProfilePram98.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram98.AddAttachSurfaces(extrude_sheet6)
ProfilePram98.ProfileName="HK.Casing.Deck.D.FR13C"
ProfilePram98.MaterialName="SS400"
ProfilePram98.ProfileType=1003
ProfilePram98.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram98.Mold="+"
ProfilePram98.ReverseDir=True
ProfilePram98.ReverseAngle=False
ProfilePram98.CalcSnipOnlyAttachLines=False
ProfilePram98.AttachDirMethod=0
ProfilePram98.CCWDefAngle=False
ProfilePram98.AddEnd1Elements(mirror_copied17[0])
ProfilePram98.End1Type=1102
ProfilePram98.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram98.AddEnd2Elements(profile21[0])
ProfilePram98.End2Type=1102
ProfilePram98.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram98.End1ScallopType=1120
ProfilePram98.End1ScallopTypeParams=["50"]
ProfilePram98.End2ScallopType=1120
ProfilePram98.End2ScallopTypeParams=["50"]
profile98 = part.CreateProfile(ProfilePram98,False)
part.SetElementColor(profile98[0],"148","0","211","0.39999997615814209")
ProfilePram99 = part.CreateProfileParam()
ProfilePram99.DefinitionType=1
ProfilePram99.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram99.AddAttachSurfaces(extrude_sheet7)
ProfilePram99.ProfileName="HK.Casing.Wall.Side.FR11.ABP"
ProfilePram99.MaterialName="SS400"
ProfilePram99.ProfileType=1002
ProfilePram99.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram99.Mold="+"
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
ProfilePram99.End1ScallopTypeParams=["35","40"]
ProfilePram99.End2ScallopType=1121
ProfilePram99.End2ScallopTypeParams=["35","40"]
profile99 = part.CreateProfile(ProfilePram99,False)
part.SetElementColor(profile99[0],"255","0","0","0.19999998807907104")
mirror_copied46 = part.MirrorCopy([profile99[0]],"PL,Y","")
part.SetElementColor(mirror_copied46[0],"255","0","0","0.19999998807907104")
mirror_copied47 = part.MirrorCopy([profile61[0]],"PL,Y","")
part.SetElementColor(mirror_copied47[0],"148","0","211","0.39999997615814209")
mirror_copied48 = part.MirrorCopy([profile39[0]],"PL,Y","")
part.SetElementColor(mirror_copied48[0],"255","0","0","0.19999998807907104")
ProfilePram100 = part.CreateProfileParam()
ProfilePram100.DefinitionType=1
ProfilePram100.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram100.AddAttachSurfaces(extrude_sheet3)
ProfilePram100.ProfileName="HK.Casing.Wall.Fore.DL00.OA"
ProfilePram100.MaterialName="SS400"
ProfilePram100.ProfileType=1002
ProfilePram100.ProfileParams=["125","75","7","10","5"]
ProfilePram100.Mold="+"
ProfilePram100.ReverseDir=True
ProfilePram100.ReverseAngle=True
ProfilePram100.CalcSnipOnlyAttachLines=False
ProfilePram100.AttachDirMethod=0
ProfilePram100.CCWDefAngle=False
ProfilePram100.AddEnd1Elements(extrude_sheet2)
ProfilePram100.End1Type=1102
ProfilePram100.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram100.AddEnd2Elements(extrude_sheet8)
ProfilePram100.End2Type=1102
ProfilePram100.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram100.End1ScallopType=1121
ProfilePram100.End1ScallopTypeParams=["25","40"]
ProfilePram100.End2ScallopType=1121
ProfilePram100.End2ScallopTypeParams=["25","40"]
profile100 = part.CreateProfile(ProfilePram100,False)
part.SetElementColor(profile100[0],"255","0","0","0.19999998807907104")
mirror_copied49 = part.MirrorCopy([profile22[0]],"PL,Y","")
part.SetElementColor(mirror_copied49[0],"148","0","211","0.39999997615814209")
extrudePram43 = part.CreateLinearSweepParam()
extrudePram43.Name="積-押し出し43"
extrudePram43.AddProfile(extrude_sheet7)
extrudePram43.DirectionType="R"
extrudePram43.DirectionParameter1="50000"
extrudePram43.SweepDirection="+Y"
extrudePram43.RefByGeometricMethod=False
extrude34 = part.CreateLinearSweep(solid12,"*",extrudePram43,False)
ProfilePram101 = part.CreateProfileParam()
ProfilePram101.DefinitionType=1
ProfilePram101.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram101.AddAttachSurfaces(extrude_sheet4)
ProfilePram101.ProfileName="HK.Casing.Wall.Aft.DL01.OAP"
ProfilePram101.MaterialName="SS400"
ProfilePram101.ProfileType=1002
ProfilePram101.ProfileParams=["125","75","7","10","5"]
ProfilePram101.Mold="+"
ProfilePram101.ReverseDir=False
ProfilePram101.ReverseAngle=True
ProfilePram101.CalcSnipOnlyAttachLines=False
ProfilePram101.AttachDirMethod=0
ProfilePram101.CCWDefAngle=False
ProfilePram101.AddEnd1Elements(extrude_sheet2)
ProfilePram101.End1Type=1102
ProfilePram101.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram101.AddEnd2Elements(extrude_sheet8)
ProfilePram101.End2Type=1102
ProfilePram101.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram101.End1ScallopType=1121
ProfilePram101.End1ScallopTypeParams=["25","40"]
ProfilePram101.End2ScallopType=1121
ProfilePram101.End2ScallopTypeParams=["25","40"]
profile101 = part.CreateProfile(ProfilePram101,False)
part.SetElementColor(profile101[0],"255","0","0","0.19999998807907104")
mirror_copied50 = part.MirrorCopy([profile82[1]],"PL,Y","")
part.SetElementColor(mirror_copied50[0],"148","0","211","0.39999997615814209")
mirror_copied51 = part.MirrorCopy([profile72[0]],"PL,Y","")
part.SetElementColor(mirror_copied51[0],"255","0","0","0.19999998807907104")
mirror_copied52 = part.MirrorCopy([profile93[0]],"PL,Y","")
part.SetElementColor(mirror_copied52[0],"255","0","0","0.19999998807907104")
ProfilePram102 = part.CreateProfileParam()
ProfilePram102.DefinitionType=1
ProfilePram102.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram102.AddAttachSurfaces(extrude_sheet1)
ProfilePram102.ProfileName="HK.Casing.Deck.B.DL05P"
ProfilePram102.MaterialName="SS400"
ProfilePram102.ProfileType=1002
ProfilePram102.ProfileParams=["125","75","7","10","5"]
ProfilePram102.Mold="+"
ProfilePram102.ReverseDir=True
ProfilePram102.ReverseAngle=True
ProfilePram102.CalcSnipOnlyAttachLines=False
ProfilePram102.AttachDirMethod=0
ProfilePram102.CCWDefAngle=False
ProfilePram102.AddEnd1Elements(profile71[0])
ProfilePram102.End1Type=1102
ProfilePram102.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram102.AddEnd2Elements(profile76[0])
ProfilePram102.End2Type=1102
ProfilePram102.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram102.End1ScallopType=1120
ProfilePram102.End1ScallopTypeParams=["50"]
ProfilePram102.End2ScallopType=1120
ProfilePram102.End2ScallopTypeParams=["50"]
profile102 = part.CreateProfile(ProfilePram102,False)
part.SetElementColor(profile102[0],"255","0","0","0.19999998807907104")
bracketPram5 = part.CreateBracketParam()
bracketPram5.DefinitionType=1
bracketPram5.BracketName="HK.Casing.Wall.Side.FR08.Deck.DP"
bracketPram5.MaterialName="SS400"
bracketPram5.BaseElement=profile29[0]
bracketPram5.UseSideSheetForPlane=False
bracketPram5.Mold="+"
bracketPram5.Thickness="9.9999999999999982"
bracketPram5.BracketType=1505
bracketPram5.BracketParams=["200"]
bracketPram5.Scallop1Type=1801
bracketPram5.Scallop1Params=["0"]
bracketPram5.Scallop2Type=-1
bracketPram5.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram5.RevSf1=False
bracketPram5.Surfaces2=[profile29[0]+",FL"]
bracketPram5.RevSf2=False
bracketPram5.RevSf3=False
bracketPram5.Sf1DimensionType=1541
bracketPram5.Sf1DimensonParams=["0","100"]
bracketPram5.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram5.Sf2DimensionType=1531
bracketPram5.Sf2DimensonParams=["200","15"]
bracket5 = part.CreateBracket(bracketPram5,False)
part.SetElementColor(bracket5,"0","255","255","0.19999998807907104")
mirror_copied53 = part.MirrorCopy([profile83[0]],"PL,Y","")
part.SetElementColor(mirror_copied53[0],"255","0","0","0.19999998807907104")
ProfilePram103 = part.CreateProfileParam()
ProfilePram103.DefinitionType=1
ProfilePram103.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram103.AddAttachSurfaces(extrude_sheet6)
ProfilePram103.ProfileName="HK.Casing.Deck.D.DL01.FP"
ProfilePram103.MaterialName="SS400"
ProfilePram103.ProfileType=1002
ProfilePram103.ProfileParams=["125","75","7","10","5"]
ProfilePram103.Mold="+"
ProfilePram103.ReverseDir=True
ProfilePram103.ReverseAngle=True
ProfilePram103.CalcSnipOnlyAttachLines=False
ProfilePram103.AttachDirMethod=0
ProfilePram103.CCWDefAngle=False
ProfilePram103.AddEnd1Elements(profile98[0])
ProfilePram103.End1Type=1102
ProfilePram103.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram103.AddEnd2Elements(extrude_sheet3)
ProfilePram103.End2Type=1102
ProfilePram103.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram103.End1ScallopType=1121
ProfilePram103.End1ScallopTypeParams=["25","40"]
ProfilePram103.End2ScallopType=1121
ProfilePram103.End2ScallopTypeParams=["25","40"]
profile103 = part.CreateProfile(ProfilePram103,False)
part.SetElementColor(profile103[0],"255","0","0","0.19999998807907104")
ProfilePram104 = part.CreateProfileParam()
ProfilePram104.DefinitionType=1
ProfilePram104.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram104.AddAttachSurfaces(extrude_sheet3)
ProfilePram104.ProfileName="HK.Casing.Wall.Fore.DL01.CDP"
ProfilePram104.MaterialName="SS400"
ProfilePram104.ProfileType=1002
ProfilePram104.ProfileParams=["125","75","7","10","5"]
ProfilePram104.Mold="+"
ProfilePram104.ReverseDir=True
ProfilePram104.ReverseAngle=True
ProfilePram104.CalcSnipOnlyAttachLines=False
ProfilePram104.AttachDirMethod=0
ProfilePram104.CCWDefAngle=False
ProfilePram104.AddEnd1Elements(profile103[0])
ProfilePram104.End1Type=1102
ProfilePram104.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram104.AddEnd2Elements(extrude_sheet5)
ProfilePram104.End2Type=1102
ProfilePram104.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram104.End1ScallopType=1120
ProfilePram104.End1ScallopTypeParams=["50"]
ProfilePram104.End2ScallopType=1120
ProfilePram104.End2ScallopTypeParams=["50"]
profile104 = part.CreateProfile(ProfilePram104,False)
part.SetElementColor(profile104[0],"255","0","0","0.19999998807907104")
mirror_copied54 = part.MirrorCopy([profile104[0]],"PL,Y","")
part.SetElementColor(mirror_copied54[0],"255","0","0","0.19999998807907104")
mirror_copied55 = part.MirrorCopy([profile90[0]],"PL,Y","")
part.SetElementColor(mirror_copied55[0],"255","0","0","0.19999998807907104")
ProfilePram105 = part.CreateProfileParam()
ProfilePram105.DefinitionType=1
ProfilePram105.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram105.AddAttachSurfaces(extrude_sheet7)
ProfilePram105.ProfileName="HK.Casing.Wall.Side.FR10.OAP"
ProfilePram105.MaterialName="SS400"
ProfilePram105.ProfileType=1002
ProfilePram105.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram105.Mold="+"
ProfilePram105.ReverseDir=False
ProfilePram105.ReverseAngle=True
ProfilePram105.CalcSnipOnlyAttachLines=False
ProfilePram105.AttachDirMethod=0
ProfilePram105.CCWDefAngle=False
ProfilePram105.AddEnd1Elements(extrude_sheet2)
ProfilePram105.End1Type=1102
ProfilePram105.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram105.AddEnd2Elements(extrude_sheet8)
ProfilePram105.End2Type=1102
ProfilePram105.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram105.End1ScallopType=1121
ProfilePram105.End1ScallopTypeParams=["35","40"]
ProfilePram105.End2ScallopType=1121
ProfilePram105.End2ScallopTypeParams=["35","40"]
profile105 = part.CreateProfile(ProfilePram105,False)
part.SetElementColor(profile105[0],"255","0","0","0.19999998807907104")
ProfilePram106 = part.CreateProfileParam()
ProfilePram106.DefinitionType=1
ProfilePram106.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram106.AddAttachSurfaces(extrude_sheet1)
ProfilePram106.ProfileName="HK.Casing.Deck.B.FR06F400"
ProfilePram106.MaterialName="SS400"
ProfilePram106.ProfileType=1007
ProfilePram106.ProfileParams=["150","12"]
ProfilePram106.Mold="+"
ProfilePram106.ReverseDir=True
ProfilePram106.ReverseAngle=False
ProfilePram106.CalcSnipOnlyAttachLines=False
ProfilePram106.AttachDirMethod=0
ProfilePram106.CCWDefAngle=False
ProfilePram106.AddEnd1Elements(mirror_copied1[0])
ProfilePram106.End1Type=1102
ProfilePram106.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram106.AddEnd2Elements(profile4[0])
ProfilePram106.End2Type=1102
ProfilePram106.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram106.End1ScallopType=0
ProfilePram106.End2ScallopType=0
profile106 = part.CreateProfile(ProfilePram106,False)
part.SetElementColor(profile106[0],"255","0","0","0.19999998807907104")
ProfilePram107 = part.CreateProfileParam()
ProfilePram107.DefinitionType=1
ProfilePram107.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram107.AddAttachSurfaces(extrude_sheet7)
ProfilePram107.ProfileName="HK.Casing.Wall.Side.FR14.CDP"
ProfilePram107.MaterialName="SS400"
ProfilePram107.ProfileType=1002
ProfilePram107.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram107.Mold="+"
ProfilePram107.ReverseDir=False
ProfilePram107.ReverseAngle=True
ProfilePram107.CalcSnipOnlyAttachLines=False
ProfilePram107.AttachDirMethod=0
ProfilePram107.CCWDefAngle=False
ProfilePram107.AddEnd1Elements(extrude_sheet6)
ProfilePram107.End1Type=1102
ProfilePram107.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram107.AddEnd2Elements(extrude_sheet5)
ProfilePram107.End2Type=1102
ProfilePram107.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram107.End1ScallopType=1121
ProfilePram107.End1ScallopTypeParams=["35","40"]
ProfilePram107.End2ScallopType=1121
ProfilePram107.End2ScallopTypeParams=["35","40"]
profile107 = part.CreateProfile(ProfilePram107,False)
part.SetElementColor(profile107[0],"255","0","0","0.19999998807907104")
mirror_copied56 = part.MirrorCopy([profile103[0]],"PL,Y","")
part.SetElementColor(mirror_copied56[0],"255","0","0","0.19999998807907104")
ProfilePram108 = part.CreateProfileParam()
ProfilePram108.DefinitionType=1
ProfilePram108.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram108.AddAttachSurfaces(extrude_sheet7)
ProfilePram108.ProfileName="HK.Casing.Wall.Side.FR07.ABP"
ProfilePram108.MaterialName="SS400"
ProfilePram108.ProfileType=1002
ProfilePram108.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram108.Mold="+"
ProfilePram108.ReverseDir=False
ProfilePram108.ReverseAngle=True
ProfilePram108.CalcSnipOnlyAttachLines=False
ProfilePram108.AttachDirMethod=0
ProfilePram108.CCWDefAngle=False
ProfilePram108.AddEnd1Elements(extrude_sheet1)
ProfilePram108.End1Type=1102
ProfilePram108.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram108.AddEnd2Elements(extrude_sheet2)
ProfilePram108.End2Type=1102
ProfilePram108.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram108.End1ScallopType=1121
ProfilePram108.End1ScallopTypeParams=["35","40"]
ProfilePram108.End2ScallopType=1121
ProfilePram108.End2ScallopTypeParams=["35","40"]
profile108 = part.CreateProfile(ProfilePram108,False)
part.SetElementColor(profile108[0],"255","0","0","0.19999998807907104")
mirror_copied57 = part.MirrorCopy([profile85[0]],"PL,Y","")
part.SetElementColor(mirror_copied57[0],"148","0","211","0.39999997615814209")
ProfilePram109 = part.CreateProfileParam()
ProfilePram109.DefinitionType=1
ProfilePram109.BasePlane="PL,O,"+var_elm16+","+"X"
ProfilePram109.AddAttachSurfaces(extrude_sheet7)
ProfilePram109.ProfileName="HK.Casing.Wall.Side.FR07.OAP"
ProfilePram109.MaterialName="SS400"
ProfilePram109.ProfileType=1002
ProfilePram109.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram109.Mold="+"
ProfilePram109.ReverseDir=False
ProfilePram109.ReverseAngle=True
ProfilePram109.CalcSnipOnlyAttachLines=False
ProfilePram109.AttachDirMethod=0
ProfilePram109.CCWDefAngle=False
ProfilePram109.AddEnd1Elements(extrude_sheet2)
ProfilePram109.End1Type=1102
ProfilePram109.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram109.AddEnd2Elements(extrude_sheet8)
ProfilePram109.End2Type=1102
ProfilePram109.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram109.End1ScallopType=1121
ProfilePram109.End1ScallopTypeParams=["35","40"]
ProfilePram109.End2ScallopType=1121
ProfilePram109.End2ScallopTypeParams=["35","40"]
profile109 = part.CreateProfile(ProfilePram109,False)
part.SetElementColor(profile109[0],"255","0","0","0.19999998807907104")
mirror_copied58 = part.MirrorCopy([profile82[0]],"PL,Y","")
part.SetElementColor(mirror_copied58[0],"148","0","211","0.39999997615814209")
mirror_copied59 = part.MirrorCopy([profile7[0]],"PL,Y","")
part.SetElementColor(mirror_copied59[0],"255","0","0","0.19999998807907104")
solid15 = part.CreateSolid("HK.Casing.Wall.Fore.OA","","SS400")
part.SetElementColor(solid15,"139","69","19","0.79999995231628418")
thicken15 = part.CreateThicken("厚み付け18",solid15,"+",[extrude_sheet3],"+","10","0","0",False,False)
extrudePram44 = part.CreateLinearSweepParam()
extrudePram44.Name="積-押し出し47"
extrudePram44.AddProfile(extrude_sheet7)
extrudePram44.DirectionType="R"
extrudePram44.DirectionParameter1="50000"
extrudePram44.SweepDirection="+Y"
extrudePram44.RefByGeometricMethod=False
extrude35 = part.CreateLinearSweep(solid15,"*",extrudePram44,False)
extrudePram45 = part.CreateLinearSweepParam()
extrudePram45.Name="積-押し出し48"
extrudePram45.AddProfile(extrude_sheet9)
extrudePram45.DirectionType="N"
extrudePram45.DirectionParameter1="50000"
extrudePram45.SweepDirection="+Y"
extrudePram45.RefByGeometricMethod=False
extrude36 = part.CreateLinearSweep(solid15,"*",extrudePram45,False)
extrudePram46 = part.CreateLinearSweepParam()
extrudePram46.Name="積-押し出し49"
extrudePram46.AddProfile(extrude_sheet2)
extrudePram46.DirectionType="R"
extrudePram46.DirectionParameter1="50000"
extrudePram46.SweepDirection="+Z"
extrudePram46.RefByGeometricMethod=False
extrude37 = part.CreateLinearSweep(solid15,"*",extrudePram46,False)
mirror_copied60 = part.MirrorCopy([profile35[0]],"PL,Y","")
part.SetElementColor(mirror_copied60[0],"255","0","0","0.19999998807907104")
mirror_copied61 = part.MirrorCopy([profile64[0]],"PL,Y","")
part.SetElementColor(mirror_copied61[0],"148","0","211","0.39999997615814209")
mirror_copied62 = part.MirrorCopy([profile14[0]],"PL,Y","")
part.SetElementColor(mirror_copied62[0],"255","0","0","0.19999998807907104")
ProfilePram110 = part.CreateProfileParam()
ProfilePram110.DefinitionType=1
ProfilePram110.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfilePram110.AddAttachSurfaces(extrude_sheet4)
ProfilePram110.ProfileName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram110.MaterialName="SS400"
ProfilePram110.FlangeName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram110.FlangeMaterialName="SS400"
ProfilePram110.ProfileType=1201
ProfilePram110.ProfileParams=["150","12","388","10"]
ProfilePram110.Mold="-"
ProfilePram110.ReverseDir=False
ProfilePram110.ReverseAngle=False
ProfilePram110.CalcSnipOnlyAttachLines=False
ProfilePram110.AttachDirMethod=0
ProfilePram110.CCWDefAngle=False
ProfilePram110.AddEnd1Elements(profile21[1])
ProfilePram110.End1Type=1102
ProfilePram110.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram110.AddEnd2Elements(extrude_sheet5)
ProfilePram110.End2Type=1103
ProfilePram110.End2TypeParams=["0"]
ProfilePram110.End1ScallopType=1120
ProfilePram110.End1ScallopTypeParams=["50"]
ProfilePram110.End2ScallopType=1120
ProfilePram110.End2ScallopTypeParams=["50"]
profile110 = part.CreateProfile(ProfilePram110,False)
part.SetElementColor(profile110[0],"148","0","211","0.38999998569488525")
part.SetElementColor(profile110[1],"148","0","211","0.38999998569488525")
bracketPram6 = part.CreateBracketParam()
bracketPram6.DefinitionType=1
bracketPram6.BracketName="HK.Casing.Wall.Side.FR07.Deck.DP"
bracketPram6.MaterialName="SS400"
bracketPram6.BaseElement=profile50[0]
bracketPram6.UseSideSheetForPlane=False
bracketPram6.Mold="+"
bracketPram6.Thickness="9.9999999999999982"
bracketPram6.BracketType=1505
bracketPram6.BracketParams=["200"]
bracketPram6.Scallop1Type=1801
bracketPram6.Scallop1Params=["0"]
bracketPram6.Scallop2Type=-1
bracketPram6.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram6.RevSf1=False
bracketPram6.Surfaces2=[profile50[0]+",FL"]
bracketPram6.RevSf2=False
bracketPram6.RevSf3=False
bracketPram6.Sf1DimensionType=1541
bracketPram6.Sf1DimensonParams=["0","100"]
bracketPram6.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram6.Sf2DimensionType=1531
bracketPram6.Sf2DimensonParams=["200","15"]
bracket6 = part.CreateBracket(bracketPram6,False)
part.SetElementColor(bracket6,"0","255","255","0.19999998807907104")
mirror_copied63 = part.MirrorCopy([profile101[0]],"PL,Y","")
part.SetElementColor(mirror_copied63[0],"255","0","0","0.19999998807907104")
extrudePram47 = part.CreateLinearSweepParam()
extrudePram47.Name="積-押し出し26"
extrudePram47.AddProfile(extrude_sheet1)
extrudePram47.DirectionType="N"
extrudePram47.DirectionParameter1="50000"
extrudePram47.SweepDirection="+Z"
extrudePram47.RefByGeometricMethod=False
extrude38 = part.CreateLinearSweep(solid7,"*",extrudePram47,False)
mirror_copied64 = part.MirrorCopy([profile18[0]],"PL,Y","")
part.SetElementColor(mirror_copied64[0],"255","0","0","0.19999998807907104")
mirror_copied65 = part.MirrorCopy([profile1[0]],"PL,Y","")
part.SetElementColor(mirror_copied65[0],"255","0","0","0.19999998807907104")
ProfilePram111 = part.CreateProfileParam()
ProfilePram111.DefinitionType=1
ProfilePram111.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram111.AddAttachSurfaces(extrude_sheet7)
ProfilePram111.ProfileName="HK.Casing.Wall.Side.FR09.OAP"
ProfilePram111.MaterialName="SS400"
ProfilePram111.ProfileType=1003
ProfilePram111.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram111.Mold="+"
ProfilePram111.ReverseDir=False
ProfilePram111.ReverseAngle=True
ProfilePram111.CalcSnipOnlyAttachLines=False
ProfilePram111.AttachDirMethod=0
ProfilePram111.CCWDefAngle=False
ProfilePram111.AddEnd1Elements(extrude_sheet2)
ProfilePram111.End1Type=1103
ProfilePram111.End1TypeParams=["0"]
ProfilePram111.AddEnd2Elements(extrude_sheet8)
ProfilePram111.End2Type=1103
ProfilePram111.End2TypeParams=["0"]
ProfilePram111.End1ScallopType=1120
ProfilePram111.End1ScallopTypeParams=["50"]
ProfilePram111.End2ScallopType=1120
ProfilePram111.End2ScallopTypeParams=["50"]
profile111 = part.CreateProfile(ProfilePram111,False)
part.SetElementColor(profile111[0],"148","0","211","0.39999997615814209")
mirror_copied66 = part.MirrorCopy([profile111[0]],"PL,Y","")
part.SetElementColor(mirror_copied66[0],"148","0","211","0.39999997615814209")
ProfilePram112 = part.CreateProfileParam()
ProfilePram112.DefinitionType=1
ProfilePram112.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram112.AddAttachSurfaces(extrude_sheet3)
ProfilePram112.ProfileName="HK.Casing.Wall.Fore.DL00.BC"
ProfilePram112.MaterialName="SS400"
ProfilePram112.ProfileType=1002
ProfilePram112.ProfileParams=["125","75","7","10","5"]
ProfilePram112.Mold="+"
ProfilePram112.ReverseDir=True
ProfilePram112.ReverseAngle=True
ProfilePram112.CalcSnipOnlyAttachLines=False
ProfilePram112.AttachDirMethod=0
ProfilePram112.CCWDefAngle=False
ProfilePram112.AddEnd1Elements(extrude_sheet5)
ProfilePram112.End1Type=1102
ProfilePram112.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram112.AddEnd2Elements(extrude_sheet1)
ProfilePram112.End2Type=1102
ProfilePram112.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram112.End1ScallopType=1121
ProfilePram112.End1ScallopTypeParams=["25","40"]
ProfilePram112.End2ScallopType=1121
ProfilePram112.End2ScallopTypeParams=["25","40"]
profile112 = part.CreateProfile(ProfilePram112,False)
part.SetElementColor(profile112[0],"255","0","0","0.19999998807907104")
ProfilePram113 = part.CreateProfileParam()
ProfilePram113.DefinitionType=1
ProfilePram113.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram113.AddAttachSurfaces(extrude_sheet5)
ProfilePram113.ProfileName="HK.Casing.Deck.C.DL00.F"
ProfilePram113.MaterialName="SS400"
ProfilePram113.ProfileType=1002
ProfilePram113.ProfileParams=["125","75","7","10","5"]
ProfilePram113.Mold="+"
ProfilePram113.ReverseDir=True
ProfilePram113.ReverseAngle=True
ProfilePram113.CalcSnipOnlyAttachLines=False
ProfilePram113.AttachDirMethod=0
ProfilePram113.CCWDefAngle=False
ProfilePram113.AddEnd1Elements(profile13[0])
ProfilePram113.End1Type=1102
ProfilePram113.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram113.AddEnd2Elements(profile112[0])
ProfilePram113.End2Type=1102
ProfilePram113.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram113.End1ScallopType=1121
ProfilePram113.End1ScallopTypeParams=["25","40"]
ProfilePram113.End2ScallopType=1121
ProfilePram113.End2ScallopTypeParams=["25","40"]
profile113 = part.CreateProfile(ProfilePram113,False)
part.SetElementColor(profile113[0],"255","0","0","0.19999998807907104")
ProfilePram114 = part.CreateProfileParam()
ProfilePram114.DefinitionType=1
ProfilePram114.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram114.AddAttachSurfaces(extrude_sheet6)
ProfilePram114.ProfileName="HK.Casing.Deck.D.DL00.F"
ProfilePram114.MaterialName="SS400"
ProfilePram114.ProfileType=1002
ProfilePram114.ProfileParams=["125","75","7","10","5"]
ProfilePram114.Mold="+"
ProfilePram114.ReverseDir=True
ProfilePram114.ReverseAngle=True
ProfilePram114.CalcSnipOnlyAttachLines=False
ProfilePram114.AttachDirMethod=0
ProfilePram114.CCWDefAngle=False
ProfilePram114.AddEnd1Elements(profile98[0])
ProfilePram114.End1Type=1102
ProfilePram114.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram114.AddEnd2Elements(extrude_sheet3)
ProfilePram114.End2Type=1102
ProfilePram114.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram114.End1ScallopType=1121
ProfilePram114.End1ScallopTypeParams=["25","40"]
ProfilePram114.End2ScallopType=1121
ProfilePram114.End2ScallopTypeParams=["25","40"]
profile114 = part.CreateProfile(ProfilePram114,False)
part.SetElementColor(profile114[0],"255","0","0","0.19999998807907104")
ProfilePram115 = part.CreateProfileParam()
ProfilePram115.DefinitionType=1
ProfilePram115.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram115.AddAttachSurfaces(extrude_sheet4)
ProfilePram115.ProfileName="HK.Casing.Wall.Aft.DL00.OA"
ProfilePram115.MaterialName="SS400"
ProfilePram115.ProfileType=1002
ProfilePram115.ProfileParams=["125","75","7","10","5"]
ProfilePram115.Mold="+"
ProfilePram115.ReverseDir=False
ProfilePram115.ReverseAngle=True
ProfilePram115.CalcSnipOnlyAttachLines=False
ProfilePram115.AttachDirMethod=0
ProfilePram115.CCWDefAngle=False
ProfilePram115.AddEnd1Elements(extrude_sheet2)
ProfilePram115.End1Type=1102
ProfilePram115.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram115.AddEnd2Elements(extrude_sheet8)
ProfilePram115.End2Type=1102
ProfilePram115.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram115.End1ScallopType=1121
ProfilePram115.End1ScallopTypeParams=["25","40"]
ProfilePram115.End2ScallopType=1121
ProfilePram115.End2ScallopTypeParams=["25","40"]
profile115 = part.CreateProfile(ProfilePram115,False)
part.SetElementColor(profile115[0],"255","0","0","0.19999998807907104")
solid16 = part.CreateSolid("HK.Casing.Wall.Aft.OA","","SS400")
part.SetElementColor(solid16,"139","69","19","0.79999995231628418")
thicken16 = part.CreateThicken("厚み付け14",solid16,"+",[extrude_sheet4],"-","10","0","0",False,False)
extrudePram48 = part.CreateLinearSweepParam()
extrudePram48.Name="積-押し出し31"
extrudePram48.AddProfile(extrude_sheet7)
extrudePram48.DirectionType="R"
extrudePram48.DirectionParameter1="50000"
extrudePram48.SweepDirection="+Y"
extrudePram48.RefByGeometricMethod=False
extrude39 = part.CreateLinearSweep(solid16,"*",extrudePram48,False)
extrudePram49 = part.CreateLinearSweepParam()
extrudePram49.Name="積-押し出し32"
extrudePram49.AddProfile(extrude_sheet9)
extrudePram49.DirectionType="N"
extrudePram49.DirectionParameter1="50000"
extrudePram49.SweepDirection="+Y"
extrudePram49.RefByGeometricMethod=False
extrude40 = part.CreateLinearSweep(solid16,"*",extrudePram49,False)
extrudePram50 = part.CreateLinearSweepParam()
extrudePram50.Name="積-押し出し33"
extrudePram50.AddProfile(extrude_sheet2)
extrudePram50.DirectionType="R"
extrudePram50.DirectionParameter1="50000"
extrudePram50.SweepDirection="+Z"
extrudePram50.RefByGeometricMethod=False
extrude41 = part.CreateLinearSweep(solid16,"*",extrudePram50,False)
extrudePram51 = part.CreateLinearSweepParam()
extrudePram51.Name="積-押し出し34"
extrudePram51.AddProfile(extrude_sheet8)
extrudePram51.DirectionType="N"
extrudePram51.DirectionParameter1="50000"
extrudePram51.SweepDirection="+Z"
extrudePram51.RefByGeometricMethod=False
extrude42 = part.CreateLinearSweep(solid16,"*",extrudePram51,False)
extrudePram52 = part.CreateLinearSweepParam()
extrudePram52.Name="積-押し出し37"
extrudePram52.AddProfile(extrude_sheet6)
extrudePram52.DirectionType="R"
extrudePram52.DirectionParameter1="50000"
extrudePram52.SweepDirection="+Z"
extrudePram52.RefByGeometricMethod=False
extrude43 = part.CreateLinearSweep(solid10,"*",extrudePram52,False)
mirror_copied67 = part.MirrorCopy([profile32[0]],"PL,Y","")
part.SetElementColor(mirror_copied67[0],"148","0","211","0.39999997615814209")
mirror_copied68 = part.MirrorCopy([profile89[0]],"PL,Y","")
part.SetElementColor(mirror_copied68[0],"255","0","0","0.19999998807907104")
mirror_copied69 = part.MirrorCopy([profile69[0]],"PL,Y","")
part.SetElementColor(mirror_copied69[0],"255","0","0","0.19999998807907104")
mirror_copied70 = part.MirrorCopy([profile59[0]],"PL,Y","")
part.SetElementColor(mirror_copied70[0],"255","0","0","0.19999998807907104")
ProfilePram116 = part.CreateProfileParam()
ProfilePram116.DefinitionType=1
ProfilePram116.BasePlane="PL,O,"+var_elm13+","+"Y"
ProfilePram116.AddAttachSurfaces(extrude_sheet1)
ProfilePram116.ProfileName="HK.Casing.Deck.B.DL01.FP"
ProfilePram116.MaterialName="SS400"
ProfilePram116.ProfileType=1002
ProfilePram116.ProfileParams=["125","75","7","10","5"]
ProfilePram116.Mold="+"
ProfilePram116.ReverseDir=True
ProfilePram116.ReverseAngle=True
ProfilePram116.CalcSnipOnlyAttachLines=False
ProfilePram116.AttachDirMethod=0
ProfilePram116.CCWDefAngle=False
ProfilePram116.AddEnd1Elements(profile5[0])
ProfilePram116.End1Type=1102
ProfilePram116.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram116.AddEnd2Elements(profile37[0])
ProfilePram116.End2Type=1102
ProfilePram116.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram116.End1ScallopType=1121
ProfilePram116.End1ScallopTypeParams=["25","40"]
ProfilePram116.End2ScallopType=1121
ProfilePram116.End2ScallopTypeParams=["25","40"]
profile116 = part.CreateProfile(ProfilePram116,False)
part.SetElementColor(profile116[0],"255","0","0","0.19999998807907104")
mirror_copied71 = part.MirrorCopy([profile116[0]],"PL,Y","")
part.SetElementColor(mirror_copied71[0],"255","0","0","0.19999998807907104")
mirror_copied72 = part.MirrorCopy([profile60[0]],"PL,Y","")
part.SetElementColor(mirror_copied72[0],"255","0","0","0.19999998807907104")
mirror_copied73 = part.MirrorCopy([profile75[0]],"PL,Y","")
part.SetElementColor(mirror_copied73[0],"255","0","0","0.19999998807907104")
mirror_copied74 = part.MirrorCopy([profile70[0]],"PL,Y","")
part.SetElementColor(mirror_copied74[0],"255","0","0","0.19999998807907104")
ProfilePram117 = part.CreateProfileParam()
ProfilePram117.DefinitionType=1
ProfilePram117.BasePlane="PL,O,"+var_elm7+","+"X"
ProfilePram117.AddAttachSurfaces(extrude_sheet7)
ProfilePram117.ProfileName="HK.Casing.Wall.Side.FR15.BCP"
ProfilePram117.MaterialName="SS400"
ProfilePram117.ProfileType=1002
ProfilePram117.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram117.Mold="+"
ProfilePram117.ReverseDir=False
ProfilePram117.ReverseAngle=True
ProfilePram117.CalcSnipOnlyAttachLines=False
ProfilePram117.AttachDirMethod=0
ProfilePram117.CCWDefAngle=False
ProfilePram117.AddEnd1Elements(extrude_sheet5)
ProfilePram117.End1Type=1102
ProfilePram117.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram117.AddEnd2Elements(extrude_sheet1)
ProfilePram117.End2Type=1102
ProfilePram117.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram117.End1ScallopType=1121
ProfilePram117.End1ScallopTypeParams=["35","40"]
ProfilePram117.End2ScallopType=1121
ProfilePram117.End2ScallopTypeParams=["35","40"]
profile117 = part.CreateProfile(ProfilePram117,False)
part.SetElementColor(profile117[0],"255","0","0","0.19999998807907104")
mirror_copied75 = part.MirrorCopy([profile110[0]],"PL,Y","")
part.SetElementColor(mirror_copied75[0],"148","0","211","0.39999997615814209")
ProfilePram118 = part.CreateProfileParam()
ProfilePram118.DefinitionType=1
ProfilePram118.BasePlane="PL,O,"+"FR6 + 400 mm"+","+"X"
ProfilePram118.AddAttachSurfaces(extrude_sheet2)
ProfilePram118.ProfileName="HK.Casing.Deck.A.FR06F400"
ProfilePram118.MaterialName="SS400"
ProfilePram118.ProfileType=1007
ProfilePram118.ProfileParams=["150","12"]
ProfilePram118.Mold="+"
ProfilePram118.ReverseDir=True
ProfilePram118.ReverseAngle=False
ProfilePram118.CalcSnipOnlyAttachLines=False
ProfilePram118.AttachDirMethod=0
ProfilePram118.CCWDefAngle=False
ProfilePram118.AddEnd1Elements(mirror_copied6[0])
ProfilePram118.End1Type=1102
ProfilePram118.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram118.AddEnd2Elements(profile26[0])
ProfilePram118.End2Type=1102
ProfilePram118.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram118.End1ScallopType=0
ProfilePram118.End2ScallopType=0
profile118 = part.CreateProfile(ProfilePram118,False)
part.SetElementColor(profile118[0],"255","0","0","0.19999998807907104")
mirror_copied76 = part.MirrorCopy([profile61[1]],"PL,Y","")
part.SetElementColor(mirror_copied76[0],"148","0","211","0.39999997615814209")
extrudePram53 = part.CreateLinearSweepParam()
extrudePram53.Name="積-押し出し29"
extrudePram53.AddProfile(extrude_sheet1)
extrudePram53.DirectionType="R"
extrudePram53.DirectionParameter1="50000"
extrudePram53.SweepDirection="+Z"
extrudePram53.RefByGeometricMethod=False
extrude44 = part.CreateLinearSweep(solid13,"*",extrudePram53,False)
extrudePram54 = part.CreateLinearSweepParam()
extrudePram54.Name="積-押し出し30"
extrudePram54.AddProfile(extrude_sheet2)
extrudePram54.DirectionType="N"
extrudePram54.DirectionParameter1="50000"
extrudePram54.SweepDirection="+Z"
extrudePram54.RefByGeometricMethod=False
extrude45 = part.CreateLinearSweep(solid13,"*",extrudePram54,False)
mirror_copied77 = part.MirrorCopy([profile57[0]],"PL,Y","")
part.SetElementColor(mirror_copied77[0],"148","0","211","0.39999997615814209")
mirror_copied78 = part.MirrorCopy([profile76[0]],"PL,Y","")
part.SetElementColor(mirror_copied78[0],"255","0","0","0.19999998807907104")
mirror_copied79 = part.MirrorCopy([profile108[0]],"PL,Y","")
part.SetElementColor(mirror_copied79[0],"255","0","0","0.19999998807907104")
mirror_copied80 = part.MirrorCopy([profile21[1]],"PL,Y","")
part.SetElementColor(mirror_copied80[0],"148","0","211","0.39999997615814209")
mirror_copied81 = part.MirrorCopy([profile42[0]],"PL,Y","")
part.SetElementColor(mirror_copied81[0],"148","0","211","0.39999997615814209")
extrudePram55 = part.CreateLinearSweepParam()
extrudePram55.Name="積-押し出し44"
extrudePram55.AddProfile(extrude_sheet9)
extrudePram55.DirectionType="N"
extrudePram55.DirectionParameter1="50000"
extrudePram55.SweepDirection="+Y"
extrudePram55.RefByGeometricMethod=False
extrude46 = part.CreateLinearSweep(solid12,"*",extrudePram55,False)
extrudePram56 = part.CreateLinearSweepParam()
extrudePram56.Name="積-押し出し45"
extrudePram56.AddProfile(extrude_sheet1)
extrudePram56.DirectionType="R"
extrudePram56.DirectionParameter1="50000"
extrudePram56.SweepDirection="+Z"
extrudePram56.RefByGeometricMethod=False
extrude47 = part.CreateLinearSweep(solid12,"*",extrudePram56,False)
extrudePram57 = part.CreateLinearSweepParam()
extrudePram57.Name="積-押し出し46"
extrudePram57.AddProfile(extrude_sheet2)
extrudePram57.DirectionType="N"
extrudePram57.DirectionParameter1="50000"
extrudePram57.SweepDirection="+Z"
extrudePram57.RefByGeometricMethod=False
extrude48 = part.CreateLinearSweep(solid12,"*",extrudePram57,False)
ProfilePram119 = part.CreateProfileParam()
ProfilePram119.DefinitionType=1
ProfilePram119.BasePlane="PL,O,"+var_elm15+","+"X"
ProfilePram119.AddAttachSurfaces(extrude_sheet7)
ProfilePram119.ProfileName="HK.Casing.Wall.Side.FR10.ABP"
ProfilePram119.MaterialName="SS400"
ProfilePram119.ProfileType=1002
ProfilePram119.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram119.Mold="+"
ProfilePram119.ReverseDir=False
ProfilePram119.ReverseAngle=True
ProfilePram119.CalcSnipOnlyAttachLines=False
ProfilePram119.AttachDirMethod=0
ProfilePram119.CCWDefAngle=False
ProfilePram119.AddEnd1Elements(extrude_sheet1)
ProfilePram119.End1Type=1102
ProfilePram119.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram119.AddEnd2Elements(extrude_sheet2)
ProfilePram119.End2Type=1102
ProfilePram119.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram119.End1ScallopType=1121
ProfilePram119.End1ScallopTypeParams=["35","40"]
ProfilePram119.End2ScallopType=1121
ProfilePram119.End2ScallopTypeParams=["35","40"]
profile119 = part.CreateProfile(ProfilePram119,False)
part.SetElementColor(profile119[0],"255","0","0","0.19999998807907104")
mirror_copied82 = part.MirrorCopy([profile22[1]],"PL,Y","")
part.SetElementColor(mirror_copied82[0],"148","0","211","0.39999997615814209")
mirror_copied83 = part.MirrorCopy([profile84[0]],"PL,Y","")
part.SetElementColor(mirror_copied83[0],"255","0","0","0.19999998807907104")
mirror_copied84 = part.MirrorCopy([profile6[0]],"PL,Y","")
part.SetElementColor(mirror_copied84[0],"255","0","0","0.19999998807907104")
mirror_copied85 = part.MirrorCopy([profile31[0]],"PL,Y","")
part.SetElementColor(mirror_copied85[0],"255","0","0","0.19999998807907104")
mirror_copied86 = part.MirrorCopy([profile102[0]],"PL,Y","")
part.SetElementColor(mirror_copied86[0],"255","0","0","0.19999998807907104")
mirror_copied87 = part.MirrorCopy([profile107[0]],"PL,Y","")
part.SetElementColor(mirror_copied87[0],"255","0","0","0.19999998807907104")
mirror_copied88 = part.MirrorCopy([profile33[0]],"PL,Y","")
part.SetElementColor(mirror_copied88[0],"255","0","0","0.19999998807907104")
mirror_copied89 = part.MirrorCopy([profile87[0]],"PL,Y","")
part.SetElementColor(mirror_copied89[0],"255","0","0","0.19999998807907104")
mirror_copied90 = part.MirrorCopy([profile97[0]],"PL,Y","")
part.SetElementColor(mirror_copied90[0],"255","0","0","0.19999998807907104")
ProfilePram120 = part.CreateProfileParam()
ProfilePram120.DefinitionType=1
ProfilePram120.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram120.AddAttachSurfaces(extrude_sheet2)
ProfilePram120.ProfileName="HK.Casing.Deck.A.FR09P"
ProfilePram120.MaterialName="SS400"
ProfilePram120.ProfileType=1003
ProfilePram120.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram120.Mold="+"
ProfilePram120.ReverseDir=True
ProfilePram120.ReverseAngle=False
ProfilePram120.CalcSnipOnlyAttachLines=False
ProfilePram120.AttachDirMethod=0
ProfilePram120.CCWDefAngle=False
ProfilePram120.AddEnd1Elements(profile26[0])
ProfilePram120.End1Type=1113
ProfilePram120.End1TypeParams=["0","79"]
ProfilePram120.AddEnd2Elements(profile111[0])
ProfilePram120.End2Type=1102
ProfilePram120.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram120.End1ScallopType=1120
ProfilePram120.End1ScallopTypeParams=["50"]
ProfilePram120.End2ScallopType=1120
ProfilePram120.End2ScallopTypeParams=["50"]
profile120 = part.CreateProfile(ProfilePram120,False)
part.SetElementColor(profile120[0],"148","0","211","0.39999997615814209")
ProfilePram121 = part.CreateProfileParam()
ProfilePram121.DefinitionType=1
ProfilePram121.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram121.AddAttachSurfaces(extrude_sheet3)
ProfilePram121.ProfileName="HK.Casing.Wall.Fore.DL00.CD"
ProfilePram121.MaterialName="SS400"
ProfilePram121.ProfileType=1002
ProfilePram121.ProfileParams=["125","75","7","10","5"]
ProfilePram121.Mold="+"
ProfilePram121.ReverseDir=True
ProfilePram121.ReverseAngle=True
ProfilePram121.CalcSnipOnlyAttachLines=False
ProfilePram121.AttachDirMethod=0
ProfilePram121.CCWDefAngle=False
ProfilePram121.AddEnd1Elements(profile114[0])
ProfilePram121.End1Type=1102
ProfilePram121.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram121.AddEnd2Elements(extrude_sheet5)
ProfilePram121.End2Type=1102
ProfilePram121.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram121.End1ScallopType=1120
ProfilePram121.End1ScallopTypeParams=["50"]
ProfilePram121.End2ScallopType=1120
ProfilePram121.End2ScallopTypeParams=["50"]
profile121 = part.CreateProfile(ProfilePram121,False)
part.SetElementColor(profile121[0],"255","0","0","0.19999998807907104")
mirror_copied91 = part.MirrorCopy([profile94[0]],"PL,Y","")
part.SetElementColor(mirror_copied91[0],"255","0","0","0.19999998807907104")
bracketPram7 = part.CreateBracketParam()
bracketPram7.DefinitionType=1
bracketPram7.BracketName="HK.Casing.Wall.Aft.DL01.Deck.DP"
bracketPram7.MaterialName="SS400"
bracketPram7.BaseElement=profile96[0]
bracketPram7.UseSideSheetForPlane=False
bracketPram7.Mold="+"
bracketPram7.Thickness="7.9999999999999964"
bracketPram7.BracketType=1501
bracketPram7.Scallop1Type=1801
bracketPram7.Scallop1Params=["0"]
bracketPram7.Scallop2Type=-1
bracketPram7.Surfaces1=[profile96[0]+",FL"]
bracketPram7.RevSf1=False
bracketPram7.Surfaces2=[profile73[0]+",FL"]
bracketPram7.RevSf2=False
bracketPram7.RevSf3=False
bracketPram7.Sf1DimensionType=1531
bracketPram7.Sf1DimensonParams=["200","15"]
bracketPram7.Sf2DimensionType=1531
bracketPram7.Sf2DimensonParams=["200","15"]
bracket7 = part.CreateBracket(bracketPram7,False)
part.SetElementColor(bracket7,"0","255","255","0.19999998807907104")
mirror_copied92 = part.MirrorCopy([profile19[0]],"PL,Y","")
part.SetElementColor(mirror_copied92[0],"255","0","0","0.19999998807907104")
mirror_copied93 = part.MirrorCopy([profile120[0]],"PL,Y","")
part.SetElementColor(mirror_copied93[0],"148","0","211","0.39999997615814209")
ProfilePram122 = part.CreateProfileParam()
ProfilePram122.DefinitionType=1
ProfilePram122.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram122.AddAttachSurfaces(extrude_sheet2)
ProfilePram122.ProfileName="HK.Casing.Deck.A.DL00.F"
ProfilePram122.MaterialName="SS400"
ProfilePram122.ProfileType=1002
ProfilePram122.ProfileParams=["125","75","7","10","5"]
ProfilePram122.Mold="+"
ProfilePram122.ReverseDir=True
ProfilePram122.ReverseAngle=True
ProfilePram122.CalcSnipOnlyAttachLines=False
ProfilePram122.AttachDirMethod=0
ProfilePram122.CCWDefAngle=False
ProfilePram122.AddEnd1Elements(profile27[0])
ProfilePram122.End1Type=1102
ProfilePram122.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram122.AddEnd2Elements(profile100[0])
ProfilePram122.End2Type=1102
ProfilePram122.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram122.End1ScallopType=1121
ProfilePram122.End1ScallopTypeParams=["25","40"]
ProfilePram122.End2ScallopType=1121
ProfilePram122.End2ScallopTypeParams=["25","40"]
profile122 = part.CreateProfile(ProfilePram122,False)
part.SetElementColor(profile122[0],"255","0","0","0.19999998807907104")
bracketPram8 = part.CreateBracketParam()
bracketPram8.DefinitionType=1
bracketPram8.BracketName="HK.Casing.Wall.Side.FR15.Deck.DP"
bracketPram8.MaterialName="SS400"
bracketPram8.BaseElement=profile20[0]
bracketPram8.UseSideSheetForPlane=False
bracketPram8.Mold="+"
bracketPram8.Thickness="9.9999999999999982"
bracketPram8.BracketType=1505
bracketPram8.BracketParams=["200"]
bracketPram8.Scallop1Type=1801
bracketPram8.Scallop1Params=["0"]
bracketPram8.Scallop2Type=-1
bracketPram8.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram8.RevSf1=False
bracketPram8.Surfaces2=[profile20[0]+",FL"]
bracketPram8.RevSf2=False
bracketPram8.RevSf3=False
bracketPram8.Sf1DimensionType=1541
bracketPram8.Sf1DimensonParams=["0","100"]
bracketPram8.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram8.Sf2DimensionType=1531
bracketPram8.Sf2DimensonParams=["200","15"]
bracket8 = part.CreateBracket(bracketPram8,False)
part.SetElementColor(bracket8,"0","255","255","0.19999998807907104")
mirror_copied94 = part.MirrorCopy([profile81[0]],"PL,Y","")
part.SetElementColor(mirror_copied94[0],"255","0","0","0.19999998807907104")
mirror_copied95 = part.MirrorCopy([profile36[0]],"PL,Y","")
part.SetElementColor(mirror_copied95[0],"255","0","0","0.19999998807907104")
mirror_copied96 = part.MirrorCopy([profile119[0]],"PL,Y","")
part.SetElementColor(mirror_copied96[0],"255","0","0","0.19999998807907104")
mirror_copied97 = part.MirrorCopy([profile110[1]],"PL,Y","")
part.SetElementColor(mirror_copied97[0],"148","0","211","0.38999998569488525")
mirror_copied98 = part.MirrorCopy([profile10[0]],"PL,Y","")
part.SetElementColor(mirror_copied98[0],"148","0","211","0.39999997615814209")
mirror_copied99 = part.MirrorCopy([profile105[0]],"PL,Y","")
part.SetElementColor(mirror_copied99[0],"255","0","0","0.19999998807907104")
bracketPram9 = part.CreateBracketParam()
bracketPram9.DefinitionType=1
bracketPram9.BracketName="HK.Casing.Wall.Fore.DL02.Deck.DP"
bracketPram9.MaterialName="SS400"
bracketPram9.BaseElement=profile45[0]
bracketPram9.UseSideSheetForPlane=False
bracketPram9.Mold="-"
bracketPram9.Thickness="12"
bracketPram9.BracketType=1501
bracketPram9.Scallop1Type=1801
bracketPram9.Scallop1Params=["50"]
bracketPram9.Scallop2Type=-1
bracketPram9.Surfaces1=["PLS","False","False","-1","-0","0",profile45[1]]
bracketPram9.RevSf1=False
bracketPram9.Surfaces2=["PLS","False","False","-0","-0","-1",profile21[1]]
bracketPram9.RevSf2=False
bracketPram9.RevSf3=False
bracketPram9.FlangeType=262
bracketPram9.FlangeParams=["100","30","29.999999999999996","30","30","1"]
bracketPram9.RevFlange=False
bracketPram9.Sf1DimensionType=1531
bracketPram9.Sf1DimensonParams=["800","15"]
bracketPram9.Sf2DimensionType=1531
bracketPram9.Sf2DimensonParams=["800","15"]
bracket9 = part.CreateBracket(bracketPram9,False)
part.SetElementColor(bracket9,"0","255","255","0.19999998807907104")
bracketPram10 = part.CreateBracketParam()
bracketPram10.DefinitionType=1
bracketPram10.BracketName="HK.Casing.Wall.Side.FR12.Deck.DP"
bracketPram10.MaterialName="SS400"
bracketPram10.BaseElement=profile16[0]
bracketPram10.UseSideSheetForPlane=False
bracketPram10.Mold="+"
bracketPram10.Thickness="9.9999999999999982"
bracketPram10.BracketType=1505
bracketPram10.BracketParams=["200"]
bracketPram10.Scallop1Type=1801
bracketPram10.Scallop1Params=["0"]
bracketPram10.Scallop2Type=-1
bracketPram10.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram10.RevSf1=False
bracketPram10.Surfaces2=[profile16[0]+",FL"]
bracketPram10.RevSf2=False
bracketPram10.RevSf3=False
bracketPram10.Sf1DimensionType=1541
bracketPram10.Sf1DimensonParams=["0","100"]
bracketPram10.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram10.Sf2DimensionType=1531
bracketPram10.Sf2DimensonParams=["200","15"]
bracket10 = part.CreateBracket(bracketPram10,False)
part.SetElementColor(bracket10,"0","255","255","0.19999998807907104")
mirror_copied100 = part.MirrorCopy([profile62[0]],"PL,Y","")
part.SetElementColor(mirror_copied100[0],"255","0","0","0.19999998807907104")
bracketPram11 = part.CreateBracketParam()
bracketPram11.DefinitionType=1
bracketPram11.BracketName="HK.Casing.Wall.Fore.DL05.Deck.DP"
bracketPram11.MaterialName="SS400"
bracketPram11.BaseElement=profile60[0]
bracketPram11.UseSideSheetForPlane=False
bracketPram11.Mold="+"
bracketPram11.Thickness="7.9999999999999964"
bracketPram11.BracketType=1501
bracketPram11.Scallop1Type=1801
bracketPram11.Scallop1Params=["0"]
bracketPram11.Scallop2Type=-1
bracketPram11.Surfaces1=[profile60[0]+",FL"]
bracketPram11.RevSf1=False
bracketPram11.Surfaces2=[profile59[0]+",FL"]
bracketPram11.RevSf2=False
bracketPram11.RevSf3=False
bracketPram11.Sf1DimensionType=1531
bracketPram11.Sf1DimensonParams=["200","15"]
bracketPram11.Sf2DimensionType=1531
bracketPram11.Sf2DimensonParams=["200","15"]
bracket11 = part.CreateBracket(bracketPram11,False)
part.SetElementColor(bracket11,"0","255","255","0.19999998807907104")
mirror_copied101 = part.MirrorCopy([profile20[0]],"PL,Y","")
part.SetElementColor(mirror_copied101[0],"255","0","0","0.19999998807907104")
mirror_copied102 = part.MirrorCopy([profile117[0]],"PL,Y","")
part.SetElementColor(mirror_copied102[0],"255","0","0","0.19999998807907104")
mirror_copied103 = part.MirrorCopy([profile58[0]],"PL,Y","")
part.SetElementColor(mirror_copied103[0],"148","0","211","0.39999997615814209")
mirror_copied104 = part.MirrorCopy([profile44[0]],"PL,Y","")
part.SetElementColor(mirror_copied104[0],"148","0","211","0.39999997615814209")
mirror_copied105 = part.MirrorCopy([profile65[0]],"PL,Y","")
part.SetElementColor(mirror_copied105[0],"255","0","0","0.19999998807907104")
mirror_copied106 = part.MirrorCopy([profile24[0]],"PL,Y","")
part.SetElementColor(mirror_copied106[0],"148","0","211","0.39999997615814209")
bracketPram12 = part.CreateBracketParam()
bracketPram12.DefinitionType=1
bracketPram12.BracketName="HK.Casing.Wall.Fore.DL04.Deck.DP"
bracketPram12.MaterialName="SS400"
bracketPram12.BaseElement=profile35[0]
bracketPram12.UseSideSheetForPlane=False
bracketPram12.Mold="+"
bracketPram12.Thickness="7.9999999999999964"
bracketPram12.BracketType=1501
bracketPram12.Scallop1Type=1801
bracketPram12.Scallop1Params=["0"]
bracketPram12.Scallop2Type=-1
bracketPram12.Surfaces1=[profile35[0]+",FL"]
bracketPram12.RevSf1=False
bracketPram12.Surfaces2=[profile7[0]+",FL"]
bracketPram12.RevSf2=False
bracketPram12.RevSf3=False
bracketPram12.Sf1DimensionType=1531
bracketPram12.Sf1DimensonParams=["200","15"]
bracketPram12.Sf2DimensionType=1531
bracketPram12.Sf2DimensonParams=["200","15"]
bracket12 = part.CreateBracket(bracketPram12,False)
part.SetElementColor(bracket12,"0","255","255","0.19999998807907104")
mirror_copied107 = part.MirrorCopy([profile47[0]],"PL,Y","")
part.SetElementColor(mirror_copied107[0],"255","0","0","0.19999998807907104")
mirror_copied108 = part.MirrorCopy([profile25[0]],"PL,Y","")
part.SetElementColor(mirror_copied108[0],"148","0","211","0.39999997615814209")
mirror_copied109 = part.MirrorCopy([profile9[0]],"PL,Y","")
part.SetElementColor(mirror_copied109[0],"255","0","0","0.19999998807907104")
extrudePram58 = part.CreateLinearSweepParam()
extrudePram58.Name="積-押し出し50"
extrudePram58.AddProfile(extrude_sheet8)
extrudePram58.DirectionType="N"
extrudePram58.DirectionParameter1="50000"
extrudePram58.SweepDirection="+Z"
extrudePram58.RefByGeometricMethod=False
extrude49 = part.CreateLinearSweep(solid15,"*",extrudePram58,False)
mirror_copied110 = part.MirrorCopy([profile52[0]],"PL,Y","")
part.SetElementColor(mirror_copied110[0],"148","0","211","0.39999997615814209")
bracketPram13 = part.CreateBracketParam()
bracketPram13.DefinitionType=1
bracketPram13.BracketName="HK.Casing.Wall.Aft.DL04.Deck.DP"
bracketPram13.MaterialName="SS400"
bracketPram13.BaseElement=profile8[0]
bracketPram13.UseSideSheetForPlane=False
bracketPram13.Mold="+"
bracketPram13.Thickness="7.9999999999999964"
bracketPram13.BracketType=1501
bracketPram13.Scallop1Type=1801
bracketPram13.Scallop1Params=["0"]
bracketPram13.Scallop2Type=-1
bracketPram13.Surfaces1=[profile8[0]+",FL"]
bracketPram13.RevSf1=False
bracketPram13.Surfaces2=[profile7[0]+",FL"]
bracketPram13.RevSf2=False
bracketPram13.RevSf3=False
bracketPram13.Sf1DimensionType=1531
bracketPram13.Sf1DimensonParams=["200","15"]
bracketPram13.Sf2DimensionType=1531
bracketPram13.Sf2DimensonParams=["200","15"]
bracket13 = part.CreateBracket(bracketPram13,False)
part.SetElementColor(bracket13,"0","255","255","0.19999998807907104")
bracketPram14 = part.CreateBracketParam()
bracketPram14.DefinitionType=1
bracketPram14.BracketName="HK.Casing.Wall.Fore.DL01.Deck.DP"
bracketPram14.MaterialName="SS400"
bracketPram14.BaseElement=profile104[0]
bracketPram14.UseSideSheetForPlane=False
bracketPram14.Mold="+"
bracketPram14.Thickness="7.9999999999999964"
bracketPram14.BracketType=1501
bracketPram14.Scallop1Type=1801
bracketPram14.Scallop1Params=["0"]
bracketPram14.Scallop2Type=-1
bracketPram14.Surfaces1=[profile104[0]+",FL"]
bracketPram14.RevSf1=False
bracketPram14.Surfaces2=[profile103[0]+",FL"]
bracketPram14.RevSf2=False
bracketPram14.RevSf3=False
bracketPram14.Sf1DimensionType=1531
bracketPram14.Sf1DimensonParams=["200","15"]
bracketPram14.Sf2DimensionType=1531
bracketPram14.Sf2DimensonParams=["200","15"]
bracket14 = part.CreateBracket(bracketPram14,False)
part.SetElementColor(bracket14,"0","255","255","0.19999998807907104")
ProfilePram123 = part.CreateProfileParam()
ProfilePram123.DefinitionType=1
ProfilePram123.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram123.AddAttachSurfaces(extrude_sheet1)
ProfilePram123.ProfileName="HK.Casing.Deck.B.DL00.F"
ProfilePram123.MaterialName="SS400"
ProfilePram123.ProfileType=1002
ProfilePram123.ProfileParams=["125","75","7","10","5"]
ProfilePram123.Mold="+"
ProfilePram123.ReverseDir=True
ProfilePram123.ReverseAngle=True
ProfilePram123.CalcSnipOnlyAttachLines=False
ProfilePram123.AttachDirMethod=0
ProfilePram123.CCWDefAngle=False
ProfilePram123.AddEnd1Elements(profile5[0])
ProfilePram123.End1Type=1102
ProfilePram123.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram123.AddEnd2Elements(profile17[0])
ProfilePram123.End2Type=1102
ProfilePram123.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram123.End1ScallopType=1121
ProfilePram123.End1ScallopTypeParams=["25","40"]
ProfilePram123.End2ScallopType=1121
ProfilePram123.End2ScallopTypeParams=["25","40"]
profile123 = part.CreateProfile(ProfilePram123,False)
part.SetElementColor(profile123[0],"255","0","0","0.19999998807907104")
mirror_copied111 = part.MirrorCopy([profile45[1]],"PL,Y","")
part.SetElementColor(mirror_copied111[0],"148","0","211","0.39999997615814209")
extrudePram59 = part.CreateLinearSweepParam()
extrudePram59.Name="積-押し出し21"
extrudePram59.AddProfile(extrude_sheet6)
extrudePram59.DirectionType="R"
extrudePram59.DirectionParameter1="50000"
extrudePram59.SweepDirection="+Z"
extrudePram59.RefByGeometricMethod=False
extrude50 = part.CreateLinearSweep(solid6,"*",extrudePram59,False)
extrudePram60 = part.CreateLinearSweepParam()
extrudePram60.Name="積-押し出し22"
extrudePram60.AddProfile(extrude_sheet5)
extrudePram60.DirectionType="N"
extrudePram60.DirectionParameter1="50000"
extrudePram60.SweepDirection="+Z"
extrudePram60.RefByGeometricMethod=False
extrude51 = part.CreateLinearSweep(solid6,"*",extrudePram60,False)
mirror_copied112 = part.MirrorCopy([profile63[0]],"PL,Y","")
part.SetElementColor(mirror_copied112[0],"255","0","0","0.19999998807907104")
bracketPram15 = part.CreateBracketParam()
bracketPram15.DefinitionType=1
bracketPram15.BracketName="HK.Casing.Wall.Side.FR11.Deck.DP"
bracketPram15.MaterialName="SS400"
bracketPram15.BaseElement=profile19[0]
bracketPram15.UseSideSheetForPlane=False
bracketPram15.Mold="+"
bracketPram15.Thickness="9.9999999999999982"
bracketPram15.BracketType=1505
bracketPram15.BracketParams=["200"]
bracketPram15.Scallop1Type=1801
bracketPram15.Scallop1Params=["0"]
bracketPram15.Scallop2Type=-1
bracketPram15.Surfaces1=["PLS","False","False","0","-0","-1",solid11]
bracketPram15.RevSf1=False
bracketPram15.Surfaces2=[profile19[0]+",FL"]
bracketPram15.RevSf2=False
bracketPram15.RevSf3=False
bracketPram15.Sf1DimensionType=1541
bracketPram15.Sf1DimensonParams=["0","100"]
bracketPram15.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile59[0]]
bracketPram15.Sf2DimensionType=1531
bracketPram15.Sf2DimensonParams=["200","15"]
bracket15 = part.CreateBracket(bracketPram15,False)
part.SetElementColor(bracket15,"0","255","255","0.19999998807907104")
extrudePram61 = part.CreateLinearSweepParam()
extrudePram61.Name="積-押し出し38"
extrudePram61.AddProfile(extrude_sheet5)
extrudePram61.DirectionType="N"
extrudePram61.DirectionParameter1="50000"
extrudePram61.SweepDirection="+Z"
extrudePram61.RefByGeometricMethod=False
extrude52 = part.CreateLinearSweep(solid10,"*",extrudePram61,False)
mirror_copied113 = part.MirrorCopy([profile109[0]],"PL,Y","")
part.SetElementColor(mirror_copied113[0],"255","0","0","0.19999998807907104")
mirror_copied114 = part.MirrorCopy([profile43[0]],"PL,Y","")
part.SetElementColor(mirror_copied114[0],"148","0","211","0.39999997615814209")
mirror_copied115 = part.MirrorCopy([profile66[0]],"PL,Y","")
part.SetElementColor(mirror_copied115[0],"148","0","211","0.39999997615814209")

