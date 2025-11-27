import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("HK.Az.Wall","","PL,Z","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","作図","0,-18500","0,18500",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","作図","-50000,15500","250000,15500",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","作図","-50000,-15500","250000,-15500",False)
skt_layer1 = part.CreateSketchLayer("Casing.Fore",skt_pl1)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","Casing.Fore","11370.000000000002,-10394.984078409721","11370.000000000002,9605.0159215902786",False)
skt_layer2 = part.CreateSketchLayer("Casing.Aft",skt_pl1)
skt_ln5 = part.CreateSketchLine(skt_pl1,"","Casing.Aft","4019.9999999999995,-10394.984078409721","4019.9999999999995,9605.0159215902786",False)
skt_layer3 = part.CreateSketchLayer("Casing.Side.P",skt_pl1)
skt_ln6 = part.CreateSketchLine(skt_pl1,"","Casing.Side.P","-1500,4800","18500,4800",False)
skt_layer4 = part.CreateSketchLayer("Casing.Side.S",skt_pl1)
skt_ln7 = part.CreateSketchLine(skt_pl1,"","Casing.Side.S","-1500,-4800","18500,-4800",False)
skt_layer5 = part.CreateSketchLayer("Dim.CenterLine",skt_pl1)
skt_ln8 = part.CreateSketchLine(skt_pl1,"","Dim.CenterLine","-50000,0","250000,0",False)
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.AddProfile(skt_pl1+",Casing.Fore")
extrudePram1.DirectionType="2"
extrudePram1.DirectionParameter1="50000"
extrudePram1.DirectionParameter2="10000"
extrudePram1.SweepDirection="+Z"
extrudePram1.Name="HK.Casing.Wall.Fore"
extrudePram1.MaterialName="SS400"
extrudePram1.IntervalSweep=False
extrude_sheet1 = part.CreateLinearSweepSheet(extrudePram1,False)
part.SheetAlignNormal(extrude_sheet1,1,0,0)
part.BlankElement(extrude_sheet1,True)
part.SetElementColor(extrude_sheet1,"225","225","225","1")
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.AddProfile(skt_pl1+",Casing.Aft")
extrudePram2.DirectionType="2"
extrudePram2.DirectionParameter1="50000"
extrudePram2.DirectionParameter2="10000"
extrudePram2.SweepDirection="+Z"
extrudePram2.Name="HK.Casing.Wall.Aft"
extrudePram2.MaterialName="SS400"
extrudePram2.IntervalSweep=False
extrude_sheet2 = part.CreateLinearSweepSheet(extrudePram2,False)
part.SheetAlignNormal(extrude_sheet2,1,0,0)
part.BlankElement(extrude_sheet2,True)
part.SetElementColor(extrude_sheet2,"225","225","225","1")
skt_pl2 = part.CreateSketchPlane("HK.Ax.Deck","","PL,X","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl2,True)
skt_ln9 = part.CreateSketchLine(skt_pl2,"","作図","15500,31800","15500,-2999.9999999999964",False)
skt_ln10 = part.CreateSketchLine(skt_pl2,"","作図","-15499.999999999996,31800","-15500,-2999.9999999999964",False)
skt_ln11 = part.CreateSketchLine(skt_pl2,"","作図","0,-3000","0,31799.999999999996",False)
skt_layer6 = part.CreateSketchLayer("General.Deck.UpperDeck",skt_pl2)
skt_ln12 = part.CreateSketchLine(skt_pl2,"","General.Deck.UpperDeck","2000,15300","18500,14933.333333333334",False)
skt_ln13 = part.CreateSketchLine(skt_pl2,"","General.Deck.UpperDeck","2000,15300","-2000,15300",False)
skt_ln14 = part.CreateSketchLine(skt_pl2,"","General.Deck.UpperDeck","-2000,15300","-18500,14933.333333333336",False)
skt_layer7 = part.CreateSketchLayer("Casing.Deck.A",skt_pl2)
skt_ln15 = part.CreateSketchLine(skt_pl2,"","Casing.Deck.A","18500,18300","-18500,18300",False)
skt_layer8 = part.CreateSketchLayer("Casing.Deck.B",skt_pl2)
skt_ln16 = part.CreateSketchLine(skt_pl2,"","Casing.Deck.B","18500,21300","-18500,21300",False)
skt_layer9 = part.CreateSketchLayer("Casing.Deck.C",skt_pl2)
skt_ln17 = part.CreateSketchLine(skt_pl2,"","Casing.Deck.C","18500,24300","-18500,24300",False)
skt_layer10 = part.CreateSketchLayer("Casing.Deck.D",skt_pl2)
skt_ln18 = part.CreateSketchLine(skt_pl2,"","Casing.Deck.D","18500,27300","-18500,27300",False)
extrudePram3 = part.CreateLinearSweepParam()
extrudePram3.AddProfile(skt_pl2+",Casing.Deck.D")
extrudePram3.DirectionType="2"
extrudePram3.DirectionParameter1="50000"
extrudePram3.DirectionParameter2="10000"
extrudePram3.SweepDirection="+X"
extrudePram3.Name="HK.Casing.Deck.D"
extrudePram3.MaterialName="SS400"
extrudePram3.IntervalSweep=False
extrude_sheet3 = part.CreateLinearSweepSheet(extrudePram3,False)
part.SheetAlignNormal(extrude_sheet3,-0,0,1)
part.BlankElement(extrude_sheet3,True)
part.SetElementColor(extrude_sheet3,"225","225","225","1")
var_elm1 = part.CreateVariable("Casing.DL05","4000","mm","")
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType=1
ProfilePram1.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfilePram1.AddAttachSurfaces(extrude_sheet3)
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
ProfilePram1.AddEnd1Elements(extrude_sheet2)
ProfilePram1.End1Type=1102
ProfilePram1.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram1.AddEnd2Elements(extrude_sheet1)
ProfilePram1.End2Type=1102
ProfilePram1.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram1.End1ScallopType=1120
ProfilePram1.End1ScallopTypeParams=["50"]
ProfilePram1.End2ScallopType=1120
ProfilePram1.End2ScallopTypeParams=["50"]
profile1 = part.CreateProfile(ProfilePram1,False)
part.SetElementColor(profile1[0],"255","0","0","0.19999998807907104")
extrudePram4 = part.CreateLinearSweepParam()
extrudePram4.AddProfile(skt_pl2+",Casing.Deck.C")
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
extrudePram5 = part.CreateLinearSweepParam()
extrudePram5.AddProfile(skt_pl1+",Casing.Side.P")
extrudePram5.DirectionType="2"
extrudePram5.DirectionParameter1="50000"
extrudePram5.DirectionParameter2="10000"
extrudePram5.SweepDirection="+Z"
extrudePram5.Name="HK.Casing.Wall.SideP"
extrudePram5.MaterialName="SS400"
extrudePram5.IntervalSweep=False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudePram5,False)
part.SheetAlignNormal(extrude_sheet5,0,-1,0)
part.BlankElement(extrude_sheet5,True)
part.SetElementColor(extrude_sheet5,"225","225","225","1")
var_elm2 = part.CreateVariable("FR12","8170","mm","")
skt_pl3 = part.CreateSketchPlane("HK.Az.Deck.D","","PL,Z","0",False,False,False,"","","",True,False)
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
ProfilePram2 = part.CreateProfileParam()
ProfilePram2.DefinitionType=1
ProfilePram2.BasePlane="PL,O,"+var_elm2+","+"X"
ProfilePram2.AddAttachSurfaces(extrude_sheet5)
ProfilePram2.ProfileName="HK.Casing.Wall.Side.FR12.CDP"
ProfilePram2.MaterialName="SS400"
ProfilePram2.ProfileType=1002
ProfilePram2.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfilePram2.Mold="+"
ProfilePram2.ReverseDir=False
ProfilePram2.ReverseAngle=True
ProfilePram2.CalcSnipOnlyAttachLines=False
ProfilePram2.AttachDirMethod=0
ProfilePram2.CCWDefAngle=False
ProfilePram2.AddEnd1Elements(extrude_sheet3)
ProfilePram2.End1Type=1102
ProfilePram2.End1TypeParams=["25","29.999999999999996","0","0"]
ProfilePram2.AddEnd2Elements(extrude_sheet4)
ProfilePram2.End2Type=1102
ProfilePram2.End2TypeParams=["25","29.999999999999996","0","0"]
ProfilePram2.End1ScallopType=1121
ProfilePram2.End1ScallopTypeParams=["35","40"]
ProfilePram2.End2ScallopType=1121
ProfilePram2.End2ScallopTypeParams=["35","40"]
profile2 = part.CreateProfile(ProfilePram2,False)
part.SetElementColor(profile2[0],"255","0","0","0.19999998807907104")
solid1 = part.CreateSolid("HK.Casing.Deck.D","","SS400")
part.SetElementColor(solid1,"139","69","19","0.78999996185302734")
thicken1 = part.CreateThicken("厚み付け3",solid1,"+",[extrude_sheet3],"+","10","0","0",False,False)
extrudePram6 = part.CreateLinearSweepParam()
extrudePram6.Name="積-押し出し3"
extrudePram6.AddProfile(skt_pl3+",Edge00")
extrudePram6.DirectionType="N"
extrudePram6.DirectionParameter1="50000"
extrudePram6.SweepDirection="+Z"
extrudePram6.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid1,"*",extrudePram6,False)
extrudePram7 = part.CreateLinearSweepParam()
extrudePram7.Name="削除-押し出し1"
extrudePram7.AddProfile(skt_pl3+",Edge01")
extrudePram7.DirectionType="T"
extrudePram7.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"-",extrudePram7,False)
bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=1
bracketPram1.BracketName="HK.Casing.Wall.Side.FR12.Deck.DP"
bracketPram1.MaterialName="SS400"
bracketPram1.BaseElement=profile2[0]
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="+"
bracketPram1.Thickness="9.9999999999999982"
bracketPram1.BracketType=1505
bracketPram1.BracketParams=["200"]
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=-1
bracketPram1.Surfaces1=["PLS","False","False","0","-0","-1",solid1]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=[profile2[0]+",FL"]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1541
bracketPram1.Sf1DimensonParams=["0","100"]
bracketPram1.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile1[0]]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["200","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"0","255","255","0.19999998807907104")

