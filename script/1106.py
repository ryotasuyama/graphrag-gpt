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
extrudePram1.AddProfile(skt_pl1+",Casing.Deck.C")
extrudePram1.DirectionType="2"
extrudePram1.DirectionParameter1="50000"
extrudePram1.DirectionParameter2="10000"
extrudePram1.SweepDirection="+X"
extrudePram1.Name="HK.Casing.Deck.C"
extrudePram1.MaterialName="SS400"
extrudePram1.IntervalSweep=False
extrude_sheet1 = part.CreateLinearSweepSheet(extrudePram1,False)
part.SheetAlignNormal(extrude_sheet1,-0,0,1)
part.BlankElement(extrude_sheet1,True)
part.SetElementColor(extrude_sheet1,"225","225","225","1")
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
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.AddProfile(skt_pl2+",Casing.Fore")
extrudePram2.DirectionType="2"
extrudePram2.DirectionParameter1="50000"
extrudePram2.DirectionParameter2="10000"
extrudePram2.SweepDirection="+Z"
extrudePram2.Name="HK.Casing.Wall.Fore"
extrudePram2.MaterialName="SS400"
extrudePram2.IntervalSweep=False
extrude_sheet2 = part.CreateLinearSweepSheet(extrudePram2,False)
part.SheetAlignNormal(extrude_sheet2,1,0,0)
part.BlankElement(extrude_sheet2,True)
part.SetElementColor(extrude_sheet2,"225","225","225","1")
var_elm1 = part.CreateVariable("Casing.DL05","4000","mm","")
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
extrudePram4 = part.CreateLinearSweepParam()
extrudePram4.AddProfile(skt_pl1+",Casing.Deck.D")
extrudePram4.DirectionType="2"
extrudePram4.DirectionParameter1="50000"
extrudePram4.DirectionParameter2="10000"
extrudePram4.SweepDirection="+X"
extrudePram4.Name="HK.Casing.Deck.D"
extrudePram4.MaterialName="SS400"
extrudePram4.IntervalSweep=False
extrude_sheet4 = part.CreateLinearSweepSheet(extrudePram4,False)
part.SheetAlignNormal(extrude_sheet4,-0,0,1)
part.BlankElement(extrude_sheet4,True)
part.SetElementColor(extrude_sheet4,"225","225","225","1")
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType=1
ProfilePram1.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram1.AddAttachSurfaces(extrude_sheet4)
ProfilePram1.ProfileName="HK.Casing.Deck.D.DL05P"
ProfilePram1.MaterialName="SS400"
ProfilePram1.ProfileType=1002
ProfilePram1.ProfileParams=["125","75","7","10","5"]
ProfilePram1.Mold="+"
ProfilePram1.ReverseDir=True
ProfilePram1.ReverseAngle=True
ProfilePram1.CalcSnipOnlyAttachLines=False
ProfilePram1.AttachDirMethod=0
ProfilePram1.CCWDefAngle=False
ProfilePram1.AddEnd1Elements(extrude_sheet3)
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
part.BlankElement(profile1[0],True)
part.SetElementColor(profile1[0],"255","0","0","0.19999998807907104")
extrudePram5 = part.CreateLinearSweepParam()
extrudePram5.AddProfile(skt_pl2+",Casing.Side.S")
extrudePram5.DirectionType="2"
extrudePram5.DirectionParameter1="50000"
extrudePram5.DirectionParameter2="10000"
extrudePram5.SweepDirection="+Z"
extrudePram5.Name="HK.Casing.Wall.SideS"
extrudePram5.MaterialName="SS400"
extrudePram5.IntervalSweep=False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudePram5,False)
part.SheetAlignNormal(extrude_sheet5,0,-1,0)
part.BlankElement(extrude_sheet5,True)
part.SetElementColor(extrude_sheet5,"225","225","225","1")
solid1 = part.CreateSolid("HK.Casing.Wall.Fore.CD","","SS400")
part.BlankElement(solid1,True)
part.SetElementColor(solid1,"139","69","19","0.79999995231628418")
thicken1 = part.CreateThicken("厚み付け15",solid1,"+",[extrude_sheet2],"+","10","0","0",False,False)
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
extrudePram7 = part.CreateLinearSweepParam()
extrudePram7.Name="積-押し出し35"
extrudePram7.AddProfile(extrude_sheet6)
extrudePram7.DirectionType="R"
extrudePram7.DirectionParameter1="50000"
extrudePram7.SweepDirection="+Y"
extrudePram7.RefByGeometricMethod=True
extrude1 = part.CreateLinearSweep(solid1,"*",extrudePram7,False)
extrudePram8 = part.CreateLinearSweepParam()
extrudePram8.Name="積-押し出し36"
extrudePram8.AddProfile(extrude_sheet5)
extrudePram8.DirectionType="N"
extrudePram8.DirectionParameter1="50000"
extrudePram8.SweepDirection="+Y"
extrudePram8.RefByGeometricMethod=True
extrude2 = part.CreateLinearSweep(solid1,"*",extrudePram8,False)
extrudePram9 = part.CreateLinearSweepParam()
extrudePram9.Name="積-押し出し37"
extrudePram9.AddProfile(extrude_sheet4)
extrudePram9.DirectionType="R"
extrudePram9.DirectionParameter1="50000"
extrudePram9.SweepDirection="+Z"
extrudePram9.RefByGeometricMethod=True
extrude3 = part.CreateLinearSweep(solid1,"*",extrudePram9,False)
extrudePram10 = part.CreateLinearSweepParam()
extrudePram10.Name="積-押し出し38"
extrudePram10.AddProfile(extrude_sheet1)
extrudePram10.DirectionType="N"
extrudePram10.DirectionParameter1="50000"
extrudePram10.SweepDirection="+Z"
extrudePram10.RefByGeometricMethod=True
extrude4 = part.CreateLinearSweep(solid1,"*",extrudePram10,False)
skt_pl3 = part.CreateSketchPlane("Sketch3","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl3,True)
skt_ln19 = part.CreateSketchLine(skt_pl3,"","Default Layer","2926.4779204678048,400","12241.442807836524,400",False)
var_elm2 = part.CreateVariable("Casing.DL04","3200","mm","")
ProfilePram2 = part.CreateProfileParam()
ProfilePram2.DefinitionType=1
ProfilePram2.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram2.AddAttachSurfaces(extrude_sheet4)
ProfilePram2.ProfileName="HK.Casing.Deck.D.DL04P"
ProfilePram2.MaterialName="SS400"
ProfilePram2.ProfileType=1002
ProfilePram2.ProfileParams=["125","75","7","10","5"]
ProfilePram2.Mold="+"
ProfilePram2.ReverseDir=True
ProfilePram2.ReverseAngle=True
ProfilePram2.CalcSnipOnlyAttachLines=False
ProfilePram2.AttachDirMethod=0
ProfilePram2.CCWDefAngle=False
ProfilePram2.AddEnd1Elements(extrude_sheet3)
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
part.BlankElement(profile2[0],True)
part.SetElementColor(profile2[0],"255","0","0","0.19999998807907104")
ProfilePram3 = part.CreateProfileParam()
ProfilePram3.DefinitionType=1
ProfilePram3.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram3.AddAttachSurfaces(extrude_sheet3)
ProfilePram3.ProfileName="HK.Casing.Wall.Aft.DL04.CDP"
ProfilePram3.MaterialName="SS400"
ProfilePram3.ProfileType=1002
ProfilePram3.ProfileParams=["125","75","7","10","5"]
ProfilePram3.Mold="+"
ProfilePram3.ReverseDir=False
ProfilePram3.ReverseAngle=True
ProfilePram3.CalcSnipOnlyAttachLines=False
ProfilePram3.AttachDirMethod=0
ProfilePram3.CCWDefAngle=False
ProfilePram3.AddEnd1Elements(profile2[0])
ProfilePram3.End1Type=1102
ProfilePram3.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.AddEnd2Elements(extrude_sheet1)
ProfilePram3.End2Type=1102
ProfilePram3.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram3.End1ScallopType=1120
ProfilePram3.End1ScallopTypeParams=["50"]
ProfilePram3.End2ScallopType=1120
ProfilePram3.End2ScallopTypeParams=["50"]
profile3 = part.CreateProfile(ProfilePram3,False)
part.BlankElement(profile3[0],True)
part.SetElementColor(profile3[0],"255","0","0","0.19999998807907104")
var_elm3 = part.CreateVariable("FR8","5360","mm","")
ProfilePram4 = part.CreateProfileParam()
ProfilePram4.DefinitionType=1
ProfilePram4.BasePlane="PL,O,"+var_elm3+","+"X"
ProfilePram4.AddAttachSurfaces(extrude_sheet6)
ProfilePram4.ProfileName="HK.Casing.Wall.Side.FR08.CDP"
ProfilePram4.MaterialName="SS400"
ProfilePram4.ProfileType=1002
ProfilePram4.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram4.Mold="+"
ProfilePram4.ReverseDir=False
ProfilePram4.ReverseAngle=True
ProfilePram4.CalcSnipOnlyAttachLines=False
ProfilePram4.AttachDirMethod=0
ProfilePram4.CCWDefAngle=False
ProfilePram4.AddEnd1Elements(extrude_sheet4)
ProfilePram4.End1Type=1102
ProfilePram4.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.AddEnd2Elements(extrude_sheet1)
ProfilePram4.End2Type=1102
ProfilePram4.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram4.End1ScallopType=1121
ProfilePram4.End1ScallopTypeParams=["35","40"]
ProfilePram4.End2ScallopType=1121
ProfilePram4.End2ScallopTypeParams=["35","40"]
profile4 = part.CreateProfile(ProfilePram4,False)
part.BlankElement(profile4[0],True)
part.SetElementColor(profile4[0],"255","0","0","0.19999998807907104")
skt_pl4 = part.CreateSketchPlane("HK.Az.Deck.D","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl4,True)
skt_layer11 = part.CreateSketchLayer("Edge00",skt_pl4)
skt_ln20 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln21 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln22 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln23 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer12 = part.CreateSketchLayer("Edge01",skt_pl4)
skt_arc1 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,1195.0000000000002","6345,1495.0000000000002","6045.0000000000009,1195",True,False)
skt_ln24 = part.CreateSketchLine(skt_pl4,"","Edge01","8580,1495","6345,1495",False)
skt_arc2 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,1195","8880,1195.0000000000002","8580,1495",True,False)
skt_ln25 = part.CreateSketchLine(skt_pl4,"","Edge01","8880,-1195","8880,1195.0000000000005",False)
skt_arc3 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,-1195.0000000000002","8580,-1495.0000000000002","8880,-1195",True,False)
skt_ln26 = part.CreateSketchLine(skt_pl4,"","Edge01","6345,-1495","8580,-1495",False)
skt_arc4 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,-1195","6045.0000000000009,-1195.0000000000002","6345,-1495",True,False)
skt_ln27 = part.CreateSketchLine(skt_pl4,"","Edge01","6045,1195","6045,-1195.0000000000005",False)
solid2 = part.CreateSolid("HK.Casing.Deck.D","","SS400")
part.BlankElement(solid2,True)
part.SetElementColor(solid2,"139","69","19","0.78999996185302734")
thicken2 = part.CreateThicken("厚み付け3",solid2,"+",[extrude_sheet4],"+","10","0","0",False,False)
extrudePram11 = part.CreateLinearSweepParam()
extrudePram11.Name="積-押し出し3"
extrudePram11.AddProfile(skt_pl4+",Edge00")
extrudePram11.DirectionType="N"
extrudePram11.DirectionParameter1="50000"
extrudePram11.SweepDirection="+Z"
extrudePram11.RefByGeometricMethod=True
extrude5 = part.CreateLinearSweep(solid2,"*",extrudePram11,False)
extrudePram12 = part.CreateLinearSweepParam()
extrudePram12.Name="削除-押し出し1"
extrudePram12.AddProfile(skt_pl4+",Edge01")
extrudePram12.DirectionType="T"
extrudePram12.RefByGeometricMethod=True
extrude6 = part.CreateLinearSweep(solid2,"-",extrudePram12,False)
var_elm4 = part.CreateVariable("FR7","4690","mm","")
ProfilePram5 = part.CreateProfileParam()
ProfilePram5.DefinitionType=1
ProfilePram5.BasePlane="PL,O,"+var_elm4+","+"X"
ProfilePram5.AddAttachSurfaces(extrude_sheet6)
ProfilePram5.ProfileName="HK.Casing.Wall.Side.FR07.CDP"
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
part.BlankElement(profile5[0],True)
part.SetElementColor(profile5[0],"255","0","0","0.19999998807907104")
var_elm5 = part.CreateVariable("Casing.DL01","800","mm","")
var_elm6 = part.CreateVariable("FR13","8970","mm","")
var_elm7 = part.CreateVariable("Casing.DL02","1600","mm","")
ProfilePram6 = part.CreateProfileParam()
ProfilePram6.DefinitionType=1
ProfilePram6.BasePlane="PL,O,"+var_elm7+","+"Y"
ProfilePram6.AddAttachSurfaces(extrude_sheet4)
ProfilePram6.ProfileName="HK.Casing.Deck.D.DL02P"
ProfilePram6.MaterialName="SS400"
ProfilePram6.FlangeName="HK.Casing.Deck.D.DL02P"
ProfilePram6.FlangeMaterialName="SS400"
ProfilePram6.ProfileType=1201
ProfilePram6.ProfileParams=["200","14","900","10"]
ProfilePram6.Mold="-"
ProfilePram6.ReverseDir=True
ProfilePram6.ReverseAngle=False
ProfilePram6.CalcSnipOnlyAttachLines=False
ProfilePram6.AttachDirMethod=0
ProfilePram6.CCWDefAngle=False
ProfilePram6.AddEnd1Elements(extrude_sheet3)
ProfilePram6.End1Type=1102
ProfilePram6.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram6.AddEnd2Elements(extrude_sheet2)
ProfilePram6.End2Type=1102
ProfilePram6.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram6.End1ScallopType=1120
ProfilePram6.End1ScallopTypeParams=["50"]
ProfilePram6.End2ScallopType=1120
ProfilePram6.End2ScallopTypeParams=["50"]
profile6 = part.CreateProfile(ProfilePram6,False)
part.BlankElement(profile6[0],True)
part.SetElementColor(profile6[0],"148","0","211","0.39999997615814209")
part.BlankElement(profile6[1],True)
part.SetElementColor(profile6[1],"148","0","211","0.39999997615814209")
mirror_copied1 = part.MirrorCopy([profile6[0]],"PL,Y","")
part.BlankElement(mirror_copied1[0],True)
part.SetElementColor(mirror_copied1[0],"148","0","211","0.39999997615814209")
ProfilePram7 = part.CreateProfileParam()
ProfilePram7.DefinitionType=1
ProfilePram7.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram7.AddAttachSurfaces(extrude_sheet4)
ProfilePram7.ProfileName="HK.Casing.Deck.D.FR13C"
ProfilePram7.MaterialName="SS400"
ProfilePram7.ProfileType=1003
ProfilePram7.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram7.Mold="+"
ProfilePram7.ReverseDir=True
ProfilePram7.ReverseAngle=False
ProfilePram7.CalcSnipOnlyAttachLines=False
ProfilePram7.AttachDirMethod=0
ProfilePram7.CCWDefAngle=False
ProfilePram7.AddEnd1Elements(mirror_copied1[0])
ProfilePram7.End1Type=1102
ProfilePram7.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.AddEnd2Elements(profile6[0])
ProfilePram7.End2Type=1102
ProfilePram7.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram7.End1ScallopType=1120
ProfilePram7.End1ScallopTypeParams=["50"]
ProfilePram7.End2ScallopType=1120
ProfilePram7.End2ScallopTypeParams=["50"]
profile7 = part.CreateProfile(ProfilePram7,False)
part.BlankElement(profile7[0],True)
part.SetElementColor(profile7[0],"148","0","211","0.39999997615814209")
ProfilePram8 = part.CreateProfileParam()
ProfilePram8.DefinitionType=1
ProfilePram8.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram8.AddAttachSurfaces(extrude_sheet4)
ProfilePram8.ProfileName="HK.Casing.Deck.D.DL01.FP"
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
ProfilePram8.AddEnd2Elements(extrude_sheet2)
ProfilePram8.End2Type=1102
ProfilePram8.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram8.End1ScallopType=1121
ProfilePram8.End1ScallopTypeParams=["25","40"]
ProfilePram8.End2ScallopType=1121
ProfilePram8.End2ScallopTypeParams=["25","40"]
profile8 = part.CreateProfile(ProfilePram8,False)
part.BlankElement(profile8[0],True)
part.SetElementColor(profile8[0],"255","0","0","0.19999998807907104")
ProfilePram9 = part.CreateProfileParam()
ProfilePram9.DefinitionType=1
ProfilePram9.BasePlane="PL,O,"+var_elm5+","+"Y"
ProfilePram9.AddAttachSurfaces(extrude_sheet2)
ProfilePram9.ProfileName="HK.Casing.Wall.Fore.DL01.CDP"
ProfilePram9.MaterialName="SS400"
ProfilePram9.ProfileType=1002
ProfilePram9.ProfileParams=["125","75","7","10","5"]
ProfilePram9.Mold="+"
ProfilePram9.ReverseDir=True
ProfilePram9.ReverseAngle=True
ProfilePram9.CalcSnipOnlyAttachLines=False
ProfilePram9.AttachDirMethod=0
ProfilePram9.CCWDefAngle=False
ProfilePram9.AddEnd1Elements(profile8[0])
ProfilePram9.End1Type=1102
ProfilePram9.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.AddEnd2Elements(extrude_sheet1)
ProfilePram9.End2Type=1102
ProfilePram9.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram9.End1ScallopType=1120
ProfilePram9.End1ScallopTypeParams=["50"]
ProfilePram9.End2ScallopType=1120
ProfilePram9.End2ScallopTypeParams=["50"]
profile9 = part.CreateProfile(ProfilePram9,False)
part.BlankElement(profile9[0],True)
part.SetElementColor(profile9[0],"255","0","0","0.19999998807907104")
ProfilePram10 = part.CreateProfileParam()
ProfilePram10.DefinitionType=1
ProfilePram10.BasePlane="PL,O,"+var_elm7+","+"Y"
ProfilePram10.AddAttachSurfaces(extrude_sheet3)
ProfilePram10.ProfileName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram10.MaterialName="SS400"
ProfilePram10.FlangeName="HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram10.FlangeMaterialName="SS400"
ProfilePram10.ProfileType=1201
ProfilePram10.ProfileParams=["150","12","388","10"]
ProfilePram10.Mold="-"
ProfilePram10.ReverseDir=False
ProfilePram10.ReverseAngle=False
ProfilePram10.CalcSnipOnlyAttachLines=False
ProfilePram10.AttachDirMethod=0
ProfilePram10.CCWDefAngle=False
ProfilePram10.AddEnd1Elements(profile6[1])
ProfilePram10.End1Type=1102
ProfilePram10.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram10.AddEnd2Elements(extrude_sheet1)
ProfilePram10.End2Type=1103
ProfilePram10.End2TypeParams=["0"]
ProfilePram10.End1ScallopType=1120
ProfilePram10.End1ScallopTypeParams=["50"]
ProfilePram10.End2ScallopType=1120
ProfilePram10.End2ScallopTypeParams=["50"]
profile10 = part.CreateProfile(ProfilePram10,False)
part.BlankElement(profile10[0],True)
part.SetElementColor(profile10[0],"148","0","211","0.38999998569488525")
part.BlankElement(profile10[1],True)
part.SetElementColor(profile10[1],"148","0","211","0.38999998569488525")
separated_bodies3 = part.BodyDivideByCurves("Separe body by curves5",profile7[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies3[1],"148","0","211","0.39999997615814209")
ProfilePram11 = part.CreateProfileParam()
ProfilePram11.DefinitionType=1
ProfilePram11.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram11.AddAttachSurfaces(extrude_sheet2)
ProfilePram11.ProfileName="HK.Casing.Wall.Fore.DL05.CDP"
ProfilePram11.MaterialName="SS400"
ProfilePram11.ProfileType=1002
ProfilePram11.ProfileParams=["125","75","7","10","5"]
ProfilePram11.Mold="+"
ProfilePram11.ReverseDir=True
ProfilePram11.ReverseAngle=True
ProfilePram11.CalcSnipOnlyAttachLines=False
ProfilePram11.AttachDirMethod=0
ProfilePram11.CCWDefAngle=False
ProfilePram11.AddEnd1Elements(profile1[0])
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
part.BlankElement(profile11[0],True)
part.SetElementColor(profile11[0],"255","0","0","0.19999998807907104")
var_elm8 = part.CreateVariable("FR11","7370","mm","")
ProfilePram12 = part.CreateProfileParam()
ProfilePram12.DefinitionType=1
ProfilePram12.BasePlane="PL,O,"+var_elm8+","+"X"
ProfilePram12.AddAttachSurfaces(extrude_sheet6)
ProfilePram12.ProfileName="HK.Casing.Wall.Side.FR11.CDP"
ProfilePram12.MaterialName="SS400"
ProfilePram12.ProfileType=1002
ProfilePram12.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram12.Mold="+"
ProfilePram12.ReverseDir=False
ProfilePram12.ReverseAngle=True
ProfilePram12.CalcSnipOnlyAttachLines=False
ProfilePram12.AttachDirMethod=0
ProfilePram12.CCWDefAngle=False
ProfilePram12.AddEnd1Elements(extrude_sheet4)
ProfilePram12.End1Type=1102
ProfilePram12.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.AddEnd2Elements(extrude_sheet1)
ProfilePram12.End2Type=1102
ProfilePram12.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram12.End1ScallopType=1121
ProfilePram12.End1ScallopTypeParams=["35","40"]
ProfilePram12.End2ScallopType=1121
ProfilePram12.End2ScallopTypeParams=["35","40"]
profile12 = part.CreateProfile(ProfilePram12,False)
part.BlankElement(profile12[0],True)
part.SetElementColor(profile12[0],"255","0","0","0.19999998807907104")
ProfilePram13 = part.CreateProfileParam()
ProfilePram13.DefinitionType=1
ProfilePram13.BasePlane="PL,O,"+var_elm7+","+"Y"
ProfilePram13.AddAttachSurfaces(extrude_sheet2)
ProfilePram13.ProfileName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram13.MaterialName="SS400"
ProfilePram13.FlangeName="HK.Casing.Wall.Fore.DL02.CDP"
ProfilePram13.FlangeMaterialName="SS400"
ProfilePram13.ProfileType=1201
ProfilePram13.ProfileParams=["150","12","388","10"]
ProfilePram13.Mold="-"
ProfilePram13.ReverseDir=True
ProfilePram13.ReverseAngle=False
ProfilePram13.CalcSnipOnlyAttachLines=False
ProfilePram13.AttachDirMethod=0
ProfilePram13.CCWDefAngle=False
ProfilePram13.AddEnd1Elements(profile6[1])
ProfilePram13.End1Type=1102
ProfilePram13.End1TypeParams=["25","14.999999999999998","0","0"]
ProfilePram13.AddEnd2Elements(extrude_sheet1)
ProfilePram13.End2Type=1102
ProfilePram13.End2TypeParams=["25","14.999999999999998","0","0"]
ProfilePram13.End1ScallopType=1120
ProfilePram13.End1ScallopTypeParams=["50"]
ProfilePram13.End2ScallopType=1120
ProfilePram13.End2ScallopTypeParams=["50"]
profile13 = part.CreateProfile(ProfilePram13,False)
part.BlankElement(profile13[0],True)
part.SetElementColor(profile13[0],"148","0","211","0.39999997615814209")
part.BlankElement(profile13[1],True)
part.SetElementColor(profile13[1],"148","0","211","0.39999997615814209")
ProfilePram14 = part.CreateProfileParam()
ProfilePram14.DefinitionType=1
ProfilePram14.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram14.AddAttachSurfaces(extrude_sheet4)
ProfilePram14.ProfileName="HK.Casing.Deck.D.FR13P"
ProfilePram14.MaterialName="SS400"
ProfilePram14.ProfileType=1003
ProfilePram14.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram14.Mold="+"
ProfilePram14.ReverseDir=True
ProfilePram14.ReverseAngle=False
ProfilePram14.CalcSnipOnlyAttachLines=False
ProfilePram14.AttachDirMethod=0
ProfilePram14.CCWDefAngle=False
ProfilePram14.AddEnd1Elements(profile6[0])
ProfilePram14.End1Type=1102
ProfilePram14.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.AddEnd2Elements(extrude_sheet6)
ProfilePram14.End2Type=1102
ProfilePram14.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram14.End1ScallopType=1120
ProfilePram14.End1ScallopTypeParams=["50"]
ProfilePram14.End2ScallopType=1120
ProfilePram14.End2ScallopTypeParams=["50"]
profile14 = part.CreateProfile(ProfilePram14,False)
part.BlankElement(profile14[0],True)
part.SetElementColor(profile14[0],"148","0","211","0.39999997615814209")
ProfilePram15 = part.CreateProfileParam()
ProfilePram15.DefinitionType=1
ProfilePram15.BasePlane="PL,O,"+var_elm6+","+"X"
ProfilePram15.AddAttachSurfaces(extrude_sheet6)
ProfilePram15.ProfileName="HK.Casing.Wall.Side.FR13.CDP"
ProfilePram15.MaterialName="SS400"
ProfilePram15.ProfileType=1003
ProfilePram15.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram15.Mold="+"
ProfilePram15.ReverseDir=False
ProfilePram15.ReverseAngle=True
ProfilePram15.CalcSnipOnlyAttachLines=False
ProfilePram15.AttachDirMethod=0
ProfilePram15.CCWDefAngle=False
ProfilePram15.AddEnd1Elements(profile14[0])
ProfilePram15.End1Type=1102
ProfilePram15.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram15.AddEnd2Elements(extrude_sheet1)
ProfilePram15.End2Type=1103
ProfilePram15.End2TypeParams=["0"]
ProfilePram15.End1ScallopType=1120
ProfilePram15.End1ScallopTypeParams=["50"]
ProfilePram15.End2ScallopType=1120
ProfilePram15.End2ScallopTypeParams=["50"]
profile15 = part.CreateProfile(ProfilePram15,False)
part.BlankElement(profile15[0],True)
part.SetElementColor(profile15[0],"148","0","211","0.39999997615814209")
var_elm9 = part.CreateVariable("FR10","6700","mm","")
ProfilePram16 = part.CreateProfileParam()
ProfilePram16.DefinitionType=1
ProfilePram16.BasePlane="PL,O,"+var_elm9+","+"X"
ProfilePram16.AddAttachSurfaces(extrude_sheet6)
ProfilePram16.ProfileName="HK.Casing.Wall.Side.FR10.CDP"
ProfilePram16.MaterialName="SS400"
ProfilePram16.ProfileType=1002
ProfilePram16.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram16.Mold="+"
ProfilePram16.ReverseDir=False
ProfilePram16.ReverseAngle=True
ProfilePram16.CalcSnipOnlyAttachLines=False
ProfilePram16.AttachDirMethod=0
ProfilePram16.CCWDefAngle=False
ProfilePram16.AddEnd1Elements(extrude_sheet4)
ProfilePram16.End1Type=1102
ProfilePram16.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.AddEnd2Elements(extrude_sheet1)
ProfilePram16.End2Type=1102
ProfilePram16.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram16.End1ScallopType=1121
ProfilePram16.End1ScallopTypeParams=["35","40"]
ProfilePram16.End2ScallopType=1121
ProfilePram16.End2ScallopTypeParams=["35","40"]
profile16 = part.CreateProfile(ProfilePram16,False)
part.BlankElement(profile16[0],True)
part.SetElementColor(profile16[0],"255","0","0","0.19999998807907104")
var_elm10 = part.CreateVariable("FR12","8170","mm","")
ProfilePram17 = part.CreateProfileParam()
ProfilePram17.DefinitionType=1
ProfilePram17.BasePlane="PL,O,"+var_elm10+","+"X"
ProfilePram17.AddAttachSurfaces(extrude_sheet6)
ProfilePram17.ProfileName="HK.Casing.Wall.Side.FR12.CDP"
ProfilePram17.MaterialName="SS400"
ProfilePram17.ProfileType=1002
ProfilePram17.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram17.Mold="+"
ProfilePram17.ReverseDir=False
ProfilePram17.ReverseAngle=True
ProfilePram17.CalcSnipOnlyAttachLines=False
ProfilePram17.AttachDirMethod=0
ProfilePram17.CCWDefAngle=False
ProfilePram17.AddEnd1Elements(extrude_sheet4)
ProfilePram17.End1Type=1102
ProfilePram17.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.AddEnd2Elements(extrude_sheet1)
ProfilePram17.End2Type=1102
ProfilePram17.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram17.End1ScallopType=1121
ProfilePram17.End1ScallopTypeParams=["35","40"]
ProfilePram17.End2ScallopType=1121
ProfilePram17.End2ScallopTypeParams=["35","40"]
profile17 = part.CreateProfile(ProfilePram17,False)
part.BlankElement(profile17[0],True)
part.SetElementColor(profile17[0],"255","0","0","0.19999998807907104")
var_elm11 = part.CreateVariable("Casing.DL03","2400","mm","")
ProfilePram18 = part.CreateProfileParam()
ProfilePram18.DefinitionType=1
ProfilePram18.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram18.AddAttachSurfaces(extrude_sheet4)
ProfilePram18.ProfileName="HK.Casing.Deck.D.DL03P"
ProfilePram18.MaterialName="SS400"
ProfilePram18.ProfileType=1002
ProfilePram18.ProfileParams=["125","75","7","10","5"]
ProfilePram18.Mold="+"
ProfilePram18.ReverseDir=True
ProfilePram18.ReverseAngle=True
ProfilePram18.CalcSnipOnlyAttachLines=False
ProfilePram18.AttachDirMethod=0
ProfilePram18.CCWDefAngle=False
ProfilePram18.AddEnd1Elements(extrude_sheet3)
ProfilePram18.End1Type=1102
ProfilePram18.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram18.AddEnd2Elements(extrude_sheet2)
ProfilePram18.End2Type=1102
ProfilePram18.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram18.End1ScallopType=1120
ProfilePram18.End1ScallopTypeParams=["50"]
ProfilePram18.End2ScallopType=1120
ProfilePram18.End2ScallopTypeParams=["50"]
profile18 = part.CreateProfile(ProfilePram18,False)
part.BlankElement(profile18[0],True)
part.SetElementColor(profile18[0],"255","0","0","0.19999998807907104")
ProfilePram19 = part.CreateProfileParam()
ProfilePram19.DefinitionType=1
ProfilePram19.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram19.AddAttachSurfaces(extrude_sheet3)
ProfilePram19.ProfileName="HK.Casing.Wall.Aft.DL03.CDP"
ProfilePram19.MaterialName="SS400"
ProfilePram19.ProfileType=1002
ProfilePram19.ProfileParams=["125","75","7","10","5"]
ProfilePram19.Mold="+"
ProfilePram19.ReverseDir=False
ProfilePram19.ReverseAngle=True
ProfilePram19.CalcSnipOnlyAttachLines=False
ProfilePram19.AttachDirMethod=0
ProfilePram19.CCWDefAngle=False
ProfilePram19.AddEnd1Elements(profile18[0])
ProfilePram19.End1Type=1102
ProfilePram19.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram19.AddEnd2Elements(extrude_sheet1)
ProfilePram19.End2Type=1102
ProfilePram19.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram19.End1ScallopType=1120
ProfilePram19.End1ScallopTypeParams=["50"]
ProfilePram19.End2ScallopType=1120
ProfilePram19.End2ScallopTypeParams=["50"]
profile19 = part.CreateProfile(ProfilePram19,False)
part.BlankElement(profile19[0],True)
part.SetElementColor(profile19[0],"255","0","0","0.19999998807907104")
separated_bodies4 = part.BodyDivideByCurves("Separe body by curves41",profile19[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies4[0],"255","0","0","0.19999998807907104")
ProfilePram20 = part.CreateProfileParam()
ProfilePram20.DefinitionType=1
ProfilePram20.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram20.AddAttachSurfaces(extrude_sheet3)
ProfilePram20.ProfileName="HK.Casing.Wall.Aft.DL05.CDP"
ProfilePram20.MaterialName="SS400"
ProfilePram20.ProfileType=1002
ProfilePram20.ProfileParams=["125","75","7","10","5"]
ProfilePram20.Mold="+"
ProfilePram20.ReverseDir=False
ProfilePram20.ReverseAngle=True
ProfilePram20.CalcSnipOnlyAttachLines=False
ProfilePram20.AttachDirMethod=0
ProfilePram20.CCWDefAngle=False
ProfilePram20.AddEnd1Elements(profile1[0])
ProfilePram20.End1Type=1102
ProfilePram20.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.AddEnd2Elements(extrude_sheet1)
ProfilePram20.End2Type=1102
ProfilePram20.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram20.End1ScallopType=1120
ProfilePram20.End1ScallopTypeParams=["50"]
ProfilePram20.End2ScallopType=1120
ProfilePram20.End2ScallopTypeParams=["50"]
profile20 = part.CreateProfile(ProfilePram20,False)
part.BlankElement(profile20[0],True)
part.SetElementColor(profile20[0],"255","0","0","0.19999998807907104")
solid3 = part.CreateSolid("HK.Casing.Wall.Aft.CD","","SS400")
part.BlankElement(solid3,True)
part.SetElementColor(solid3,"139","69","19","0.79999995231628418")
thicken3 = part.CreateThicken("厚み付け11",solid3,"+",[extrude_sheet3],"-","10","0","0",False,False)
extrudePram13 = part.CreateLinearSweepParam()
extrudePram13.Name="積-押し出し19"
extrudePram13.AddProfile(extrude_sheet6)
extrudePram13.DirectionType="R"
extrudePram13.DirectionParameter1="50000"
extrudePram13.SweepDirection="+Y"
extrudePram13.RefByGeometricMethod=True
extrude7 = part.CreateLinearSweep(solid3,"*",extrudePram13,False)
var_elm12 = part.CreateVariable("FR9","6030","mm","")
ProfilePram21 = part.CreateProfileParam()
ProfilePram21.DefinitionType=1
ProfilePram21.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram21.AddAttachSurfaces(extrude_sheet4)
ProfilePram21.ProfileName="HK.Casing.Deck.D.FR09P"
ProfilePram21.MaterialName="SS400"
ProfilePram21.ProfileType=1003
ProfilePram21.ProfileParams=["300","90","11","16","19","9.5"]
ProfilePram21.Mold="+"
ProfilePram21.ReverseDir=True
ProfilePram21.ReverseAngle=False
ProfilePram21.CalcSnipOnlyAttachLines=False
ProfilePram21.AttachDirMethod=0
ProfilePram21.CCWDefAngle=False
ProfilePram21.AddEnd1Elements(profile6[0])
ProfilePram21.End1Type=1102
ProfilePram21.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram21.AddEnd2Elements(extrude_sheet6)
ProfilePram21.End2Type=1102
ProfilePram21.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram21.End1ScallopType=1120
ProfilePram21.End1ScallopTypeParams=["50"]
ProfilePram21.End2ScallopType=1120
ProfilePram21.End2ScallopTypeParams=["50"]
profile21 = part.CreateProfile(ProfilePram21,False)
part.BlankElement(profile21[0],True)
part.SetElementColor(profile21[0],"148","0","211","0.39999997615814209")
ProfilePram22 = part.CreateProfileParam()
ProfilePram22.DefinitionType=1
ProfilePram22.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram22.AddAttachSurfaces(extrude_sheet4)
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
ProfilePram22.AddEnd1Elements(mirror_copied1[0])
ProfilePram22.End1Type=1102
ProfilePram22.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram22.AddEnd2Elements(profile6[0])
ProfilePram22.End2Type=1102
ProfilePram22.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram22.End1ScallopType=1120
ProfilePram22.End1ScallopTypeParams=["50"]
ProfilePram22.End2ScallopType=1120
ProfilePram22.End2ScallopTypeParams=["50"]
profile22 = part.CreateProfile(ProfilePram22,False)
part.BlankElement(profile22[0],True)
part.SetElementColor(profile22[0],"148","0","211","0.39999997615814209")
ProfilePram23 = part.CreateProfileParam()
ProfilePram23.DefinitionType=1
ProfilePram23.BasePlane="PL,O,"+var_elm12+","+"X"
ProfilePram23.AddAttachSurfaces(extrude_sheet6)
ProfilePram23.ProfileName="HK.Casing.Wall.Side.FR09.CDP"
ProfilePram23.MaterialName="SS400"
ProfilePram23.ProfileType=1003
ProfilePram23.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfilePram23.Mold="+"
ProfilePram23.ReverseDir=False
ProfilePram23.ReverseAngle=True
ProfilePram23.CalcSnipOnlyAttachLines=False
ProfilePram23.AttachDirMethod=0
ProfilePram23.CCWDefAngle=False
ProfilePram23.AddEnd1Elements(profile21[0])
ProfilePram23.End1Type=1102
ProfilePram23.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram23.AddEnd2Elements(extrude_sheet1)
ProfilePram23.End2Type=1103
ProfilePram23.End2TypeParams=["0"]
ProfilePram23.End1ScallopType=1120
ProfilePram23.End1ScallopTypeParams=["50"]
ProfilePram23.End2ScallopType=1120
ProfilePram23.End2ScallopTypeParams=["50"]
profile23 = part.CreateProfile(ProfilePram23,False)
part.BlankElement(profile23[0],True)
part.SetElementColor(profile23[0],"148","0","211","0.39999997615814209")
extrudePram14 = part.CreateLinearSweepParam()
extrudePram14.Name="積-押し出し20"
extrudePram14.AddProfile(extrude_sheet5)
extrudePram14.DirectionType="N"
extrudePram14.DirectionParameter1="50000"
extrudePram14.SweepDirection="+Y"
extrudePram14.RefByGeometricMethod=True
extrude8 = part.CreateLinearSweep(solid3,"*",extrudePram14,False)
extrudePram15 = part.CreateLinearSweepParam()
extrudePram15.Name="積-押し出し21"
extrudePram15.AddProfile(extrude_sheet4)
extrudePram15.DirectionType="R"
extrudePram15.DirectionParameter1="50000"
extrudePram15.SweepDirection="+Z"
extrudePram15.RefByGeometricMethod=True
extrude9 = part.CreateLinearSweep(solid3,"*",extrudePram15,False)
ProfilePram24 = part.CreateProfileParam()
ProfilePram24.DefinitionType=1
ProfilePram24.BasePlane="PL,O,"+var_elm11+","+"Y"
ProfilePram24.AddAttachSurfaces(extrude_sheet2)
ProfilePram24.ProfileName="HK.Casing.Wall.Fore.DL03.CDP"
ProfilePram24.MaterialName="SS400"
ProfilePram24.ProfileType=1002
ProfilePram24.ProfileParams=["125","75","7","10","5"]
ProfilePram24.Mold="+"
ProfilePram24.ReverseDir=True
ProfilePram24.ReverseAngle=True
ProfilePram24.CalcSnipOnlyAttachLines=False
ProfilePram24.AttachDirMethod=0
ProfilePram24.CCWDefAngle=False
ProfilePram24.AddEnd1Elements(profile18[0])
ProfilePram24.End1Type=1102
ProfilePram24.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.AddEnd2Elements(extrude_sheet1)
ProfilePram24.End2Type=1102
ProfilePram24.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram24.End1ScallopType=1120
ProfilePram24.End1ScallopTypeParams=["50"]
ProfilePram24.End2ScallopType=1120
ProfilePram24.End2ScallopTypeParams=["50"]
profile24 = part.CreateProfile(ProfilePram24,False)
part.BlankElement(profile24[0],True)
part.SetElementColor(profile24[0],"255","0","0","0.19999998807907104")
separated_bodies6 = part.BodyDivideByCurves("Separe body by curves31",profile24[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies6[0],"255","0","0","0.19999998807907104")
var_elm13 = part.CreateVariable("FR15","10570","mm","")
ProfilePram25 = part.CreateProfileParam()
ProfilePram25.DefinitionType=1
ProfilePram25.BasePlane="PL,O,"+var_elm13+","+"X"
ProfilePram25.AddAttachSurfaces(extrude_sheet6)
ProfilePram25.ProfileName="HK.Casing.Wall.Side.FR15.CDP"
ProfilePram25.MaterialName="SS400"
ProfilePram25.ProfileType=1002
ProfilePram25.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram25.Mold="+"
ProfilePram25.ReverseDir=False
ProfilePram25.ReverseAngle=True
ProfilePram25.CalcSnipOnlyAttachLines=False
ProfilePram25.AttachDirMethod=0
ProfilePram25.CCWDefAngle=False
ProfilePram25.AddEnd1Elements(extrude_sheet4)
ProfilePram25.End1Type=1102
ProfilePram25.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.AddEnd2Elements(extrude_sheet1)
ProfilePram25.End2Type=1102
ProfilePram25.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram25.End1ScallopType=1121
ProfilePram25.End1ScallopTypeParams=["35","40"]
ProfilePram25.End2ScallopType=1121
ProfilePram25.End2ScallopTypeParams=["35","40"]
profile25 = part.CreateProfile(ProfilePram25,False)
part.BlankElement(profile25[0],True)
part.SetElementColor(profile25[0],"255","0","0","0.19999998807907104")
separated_bodies2 = part.BodyDivideByCurves("Separe body by curves32",profile9[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies2[0],"0","255","255","0.19999998807907104")
separated_bodies9 = part.BodyDivideByCurves("Separe body by curves54",profile10[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies9[0],"148","0","211","0.38999998569488525")
separated_bodies10 = part.BodyDivideByCurves("Separe body by curves11",profile12[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies10[0],"255","0","0","0.19999998807907104")
solid4 = part.CreateSolid("HK.Casing.Wall.Side.CDP","","SS400")
part.BlankElement(solid4,True)
part.SetElementColor(solid4,"139","69","19","0.79999995231628418")
thicken4 = part.CreateThicken("厚み付け7",solid4,"+",[extrude_sheet6],"-","10","0","0",False,False)
ProfilePram28 = part.CreateProfileParam()
ProfilePram28.DefinitionType=1
ProfilePram28.BasePlane="PL,O,"+var_elm2+","+"Y"
ProfilePram28.AddAttachSurfaces(extrude_sheet2)
ProfilePram28.ProfileName="HK.Casing.Wall.Fore.DL04.CDP"
ProfilePram28.MaterialName="SS400"
ProfilePram28.ProfileType=1002
ProfilePram28.ProfileParams=["125","75","7","10","5"]
ProfilePram28.Mold="+"
ProfilePram28.ReverseDir=True
ProfilePram28.ReverseAngle=True
ProfilePram28.CalcSnipOnlyAttachLines=False
ProfilePram28.AttachDirMethod=0
ProfilePram28.CCWDefAngle=False
ProfilePram28.AddEnd1Elements(profile2[0])
ProfilePram28.End1Type=1102
ProfilePram28.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram28.AddEnd2Elements(extrude_sheet1)
ProfilePram28.End2Type=1102
ProfilePram28.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram28.End1ScallopType=1120
ProfilePram28.End1ScallopTypeParams=["50"]
ProfilePram28.End2ScallopType=1120
ProfilePram28.End2ScallopTypeParams=["50"]
profile28 = part.CreateProfile(ProfilePram28,False)
part.BlankElement(profile28[0],True)
part.SetElementColor(profile28[0],"255","0","0","0.19999998807907104")
separated_bodies12 = part.BodyDivideByCurves("Separe body by curves44",profile28[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies12[0],"255","0","0","0.19999998807907104")
extrudePram16 = part.CreateLinearSweepParam()
extrudePram16.Name="積-押し出し7"
extrudePram16.AddProfile(skt_pl4+",Edge00")
extrudePram16.DirectionType="N"
extrudePram16.DirectionParameter1="50000"
extrudePram16.SweepDirection="+Z"
extrudePram16.RefByGeometricMethod=True
extrude10 = part.CreateLinearSweep(solid4,"*",extrudePram16,False)
extrudePram17 = part.CreateLinearSweepParam()
extrudePram17.Name="積-押し出し8"
extrudePram17.AddProfile(extrude_sheet4)
extrudePram17.DirectionType="R"
extrudePram17.DirectionParameter1="50000"
extrudePram17.SweepDirection="+Z"
extrudePram17.RefByGeometricMethod=True
extrude11 = part.CreateLinearSweep(solid4,"*",extrudePram17,False)
extrudePram18 = part.CreateLinearSweepParam()
extrudePram18.Name="積-押し出し9"
extrudePram18.AddProfile(extrude_sheet1)
extrudePram18.DirectionType="N"
extrudePram18.DirectionParameter1="50000"
extrudePram18.SweepDirection="+Z"
extrudePram18.RefByGeometricMethod=True
extrude12 = part.CreateLinearSweep(solid4,"*",extrudePram18,False)
separated_bodies15 = part.BodyDivideByCurves("Separe body by curves49",profile15[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies15[0],"148","0","211","0.39999997615814209")
separated_bodies16 = part.BodyDivideByCurves("Separe body by curves39",profile28[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies16[0],"255","0","0","0.19999998807907104")
separated_bodies19 = part.BodyDivideByCurves("Separe body by curves23",profile1[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies19[0],"255","0","0","0.19999998807907104")
extrudePram19 = part.CreateLinearSweepParam()
extrudePram19.Name="積-押し出し22"
extrudePram19.AddProfile(extrude_sheet1)
extrudePram19.DirectionType="N"
extrudePram19.DirectionParameter1="50000"
extrudePram19.SweepDirection="+Z"
extrudePram19.RefByGeometricMethod=True
extrude13 = part.CreateLinearSweep(solid3,"*",extrudePram19,False)
var_elm14 = part.CreateVariable("FR14","9770","mm","")
ProfilePram29 = part.CreateProfileParam()
ProfilePram29.DefinitionType=1
ProfilePram29.BasePlane="PL,O,"+var_elm14+","+"X"
ProfilePram29.AddAttachSurfaces(extrude_sheet6)
ProfilePram29.ProfileName="HK.Casing.Wall.Side.FR14.CDP"
ProfilePram29.MaterialName="SS400"
ProfilePram29.ProfileType=1002
ProfilePram29.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram29.Mold="+"
ProfilePram29.ReverseDir=False
ProfilePram29.ReverseAngle=True
ProfilePram29.CalcSnipOnlyAttachLines=False
ProfilePram29.AttachDirMethod=0
ProfilePram29.CCWDefAngle=False
ProfilePram29.AddEnd1Elements(extrude_sheet4)
ProfilePram29.End1Type=1102
ProfilePram29.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.AddEnd2Elements(extrude_sheet1)
ProfilePram29.End2Type=1102
ProfilePram29.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram29.End1ScallopType=1121
ProfilePram29.End1ScallopTypeParams=["35","40"]
ProfilePram29.End2ScallopType=1121
ProfilePram29.End2ScallopTypeParams=["35","40"]
profile29 = part.CreateProfile(ProfilePram29,False)
part.BlankElement(profile29[0],True)
part.SetElementColor(profile29[0],"255","0","0","0.19999998807907104")
separated_bodies20 = part.BodyDivideByCurves("Separe body by curves1",solid2,[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies20[1],"139","69","19","0.78999996185302734")
separated_bodies22 = part.BodyDivideByCurves("Separe body by curves15",profile22[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies22[1],"148","0","211","0.39999997615814209")
separated_bodies23 = part.BodyDivideByCurves("Separe body by curves2",profile17[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies23[0],"255","0","0","0.19999998807907104")
separated_bodies25 = part.BodyDivideByCurves("Separe body by curves20",profile18[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies25[0],"255","0","0","0.19999998807907104")
separated_bodies26 = part.BodyDivideByCurves("Separe body by curves40",profile20[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies26[0],"255","0","0","0.19999998807907104")
separated_bodies27 = part.BodyDivideByCurves("Separe body by curves21",profile14[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies27[0],"148","0","211","0.39999997615814209")
separated_bodies28 = part.BodyDivideByCurves("Separe body by curves3",profile8[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies28[0],"255","0","0","0.19999998807907104")
separated_bodies30 = part.BodyDivideByCurves("Separe body by curves38",profile19[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies30[0],"0","255","255","0.19999998807907104")
separated_bodies33 = part.BodyDivideByCurves("Separe body by curves27",solid4,[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies33[0],"139","69","19","0.79999995231628418")
separated_bodies35 = part.BodyDivideByCurves("Separe body by curves19",profile6[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies35[0],"148","0","211","0.39999997615814209")
separated_bodies36 = part.BodyDivideByCurves("Separe body by curves14",profile16[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies36[0],"255","0","0","0.19999998807907104")
separated_bodies37 = part.BodyDivideByCurves("Separe body by curves7",profile4[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies37[0],"255","0","0","0.19999998807907104")
separated_bodies38 = part.BodyDivideByCurves("Separe body by curves37",profile9[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies38[0],"255","0","0","0.19999998807907104")
separated_bodies40 = part.BodyDivideByCurves("Separe body by curves28",solid1,[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies40[1],"139","69","19","0.79999995231628418")
separated_bodies41 = part.BodyDivideByCurves("Separe body by curves10",profile25[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies41[0],"0","255","255","0.19999998807907104")
separated_bodies42 = part.BodyDivideByCurves("Separe body by curves53",profile13[1],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies42[0],"148","0","211","0.39999997615814209")
separated_bodies43 = part.BodyDivideByCurves("Separe body by curves12",profile21[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies43[0],"148","0","211","0.39999997615814209")
separated_bodies44 = part.BodyDivideByCurves("Separe body by curves26",profile28[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies44[0],"255","0","0","0.19999998807907104")
separated_bodies46 = part.BodyDivideByCurves("Separe body by curves58",profile13[1],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies46[0],"148","0","211","0.39999997615814209")
separated_bodies47 = part.BodyDivideByCurves("Separe body by curves4",solid3,[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies47[1],"139","69","19","0.79999995231628418")
separated_bodies49 = part.BodyDivideByCurves("Separe body by curves58",profile10[1],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies49[0],"148","0","211","0.38999998569488525")
separated_bodies50 = part.BodyDivideByCurves("Separe body by curves25",profile5[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies50[0],"255","0","0","0.19999998807907104")
separated_bodies51 = part.BodyDivideByCurves("Separe body by curves22",profile2[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies51[0],"255","0","0","0.19999998807907104")
separated_bodies52 = part.BodyDivideByCurves("Separe body by curves24",profile29[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies52[0],"255","0","0","0.19999998807907104")
separated_bodies55 = part.BodyDivideByCurves("Separe body by curves9",profile25[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies55[0],"255","0","0","0.19999998807907104")
separated_bodies56 = part.BodyDivideByCurves("Separe body by curves51",profile23[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies56[0],"148","0","211","0.39999997615814209")
separated_bodies57 = part.BodyDivideByCurves("Separe body by curves34",profile3[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies57[0],"255","0","0","0.19999998807907104")
separated_bodies58 = part.BodyDivideByCurves("Separe body by curves30",profile11[0],[skt_pl3],False,"0","","",False)
part.SetElementColor(separated_bodies58[0],"255","0","0","0.19999998807907104")

# ========= ブラケット追加（指示に基づく6点） =========
# 共通設定
def make_bracket(name, base_element, surfaces1, surfaces2, bkt_type=1501, thickness="8", sf_dim=("250","15")):
    bparam = part.CreateBracketParam()
    bparam.DefinitionType = 1
    bparam.BracketName = name
    bparam.MaterialName = "SS400"
    bparam.BaseElement = base_element
    bparam.UseSideSheetForPlane = False
    bparam.Mold = "+"
    bparam.Thickness = thickness
    bparam.BracketType = bkt_type
    bparam.Scallop1Type = 1801
    bparam.Scallop1Params = ["0"]
    bparam.Scallop2Type = 0
    bparam.Surfaces1 = surfaces1
    bparam.RevSf1 = False
    bparam.Surfaces2 = surfaces2
    bparam.RevSf2 = False
    bparam.RevSf3 = False
    bparam.Sf1DimensionType = 1531
    bparam.Sf1DimensonParams = list(sf_dim)
    bparam.Sf2DimensionType = 1531
    bparam.Sf2DimensonParams = list(sf_dim)
    bkt = part.CreateBracket(bparam, False)
    part.BlankElement(bkt, True)
    part.SetElementColor(bkt, "0","255","255","0.19999998807907104")
    return bkt

# 1) bracket1: HK.Casing.Wall.Fore.DL01.Deck.DP
#   Base: HK.Casing.Wall.Fore.DL01.CDP -> profile9[0]
#   Connect: (base) FL <-> profile6 (Deck.D.DL02P) FL
bracket1 = make_bracket(
    "HK.Casing.Wall.Fore.DL01.Deck.DP",
    profile9[0],
    [profile9[0] + ",FL"],
    [profile6[0] + ",FL"],
    bkt_type=1501,
    thickness="8"
)

# 2) bracket2: HK.Casing.Wall.Fore.DL02.Deck.DP
#   Base: HK.Casing.Wall.Fore.DL02.CDP -> profile13[0]
#   Connect: profile13 の面 <-> profile4 の面
bracket2 = make_bracket(
    "HK.Casing.Wall.Fore.DL02.Deck.DP",
    profile13[0],
    [profile13[0]],
    [profile4[0]],
    bkt_type=1501,
    thickness="8"
)

# 3) bracket3: HK.Casing.Deck.D.FR13P
#   Base: HK.Casing.Deck.D.FR13P -> profile14[0]
#   Connect: profile4 のウェブ面(WF) <-> profile14 のフランジ面(FL)
bracket3 = make_bracket(
    "HK.Casing.Deck.D.FR13P",
    profile14[0],
    [profile4[0] + ",WF"],
    [profile14[0] + ",FL"],
    bkt_type=1501,
    thickness="8"
)

# 4) bracket4: HK.Casing.Wall.Side.FR10.Deck.DP
#   Base: HK.Casing.Wall.Side.FR10.CDP -> profile16[0]
#   Connect: solid1 の面(PLS指定) <-> profile16 のフランジ面(FL)
bracket4_param_surfaces2 = ["PLS","True","False","0","-0","1",solid1]
bracket4 = make_bracket(
    "HK.Casing.Wall.Side.FR10.Deck.DP",
    profile16[0],
    [profile16[0] + ",FL"],
    bracket4_param_surfaces2,
    bkt_type=1505,
    thickness="8"
)

# 5) bracket5: HK.Casing.Wall.Aft.DL02.Deck.DP
#   Base: HK.Casing.Wall.Aft.DL02.CDP -> profile10[0]
#   Connect: profile10 の面 <-> profile4 の面
bracket5 = make_bracket(
    "HK.Casing.Wall.Aft.DL02.Deck.DP",
    profile10[0],
    [profile10[0]],
    [profile4[0]],
    bkt_type=1501,
    thickness="8"
)

# 6) bracket6: HK.Casing.Wall.Aft.DL04.Deck.DP
#   Base: HK.Casing.Wall.Aft.DL04.CDP -> profile3[0]
#   Connect: profile3 のフランジ面(FL) <-> profile24 のフランジ面(FL)
bracket6 = make_bracket(
    "HK.Casing.Wall.Aft.DL04.Deck.DP",
    profile3[0],
    [profile3[0] + ",FL"],
    [profile24[0] + ",FL"],
    bkt_type=1501,
    thickness="8"
)
# ========= ブラケット追加 ここまで =========