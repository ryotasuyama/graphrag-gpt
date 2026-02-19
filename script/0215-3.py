import win32com.client

evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)

doc = evoship.Create3DDocument()
part = doc.GetPart()

skt_pl1 = part.CreateSketchPlane("HK.Ax.Deck", "", "PL,X", "0", False, False, False, "", "", "", False, False)
part.BlankElement(skt_pl1, True)
skt_ln1 = part.CreateSketchLine(skt_pl1, "", "作図", "15500,31800", "15500,-2999.9999999999964", False)
skt_ln2 = part.CreateSketchLine(skt_pl1, "", "作図", "-15499.999999999996,31800", "-15500,-2999.9999999999964", False)
skt_ln3 = part.CreateSketchLine(skt_pl1, "", "作図", "0,-3000", "0,31799.999999999996", False)

skt_layer1 = part.CreateSketchLayer("General.Deck.UpperDeck", skt_pl1)
skt_ln4 = part.CreateSketchLine(skt_pl1, "", "General.Deck.UpperDeck", "2000,15300", "18500,14933.333333333334", False)
skt_ln5 = part.CreateSketchLine(skt_pl1, "", "General.Deck.UpperDeck", "2000,15300", "-2000,15300", False)
skt_ln6 = part.CreateSketchLine(skt_pl1, "", "General.Deck.UpperDeck", "-2000,15300", "-18500,14933.333333333336", False)

skt_layer2 = part.CreateSketchLayer("Casing.Deck.A", skt_pl1)
skt_ln7 = part.CreateSketchLine(skt_pl1, "", "Casing.Deck.A", "18500,18300", "-18500,18300", False)

skt_layer3 = part.CreateSketchLayer("Casing.Deck.B", skt_pl1)
skt_ln8 = part.CreateSketchLine(skt_pl1, "", "Casing.Deck.B", "18500,21300", "-18500,21300", False)

skt_layer4 = part.CreateSketchLayer("Casing.Deck.C", skt_pl1)
skt_ln9 = part.CreateSketchLine(skt_pl1, "", "Casing.Deck.C", "18500,24300", "-18500,24300", False)

skt_layer5 = part.CreateSketchLayer("Casing.Deck.D", skt_pl1)
skt_ln10 = part.CreateSketchLine(skt_pl1, "", "Casing.Deck.D", "18500,27300", "-18500,27300", False)

extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.AddProfile(skt_pl1 + ",Casing.Deck.B")
extrudePram1.DirectionType = "2"
extrudePram1.DirectionParameter1 = "50000"
extrudePram1.DirectionParameter2 = "10000"
extrudePram1.SweepDirection = "+X"
extrudePram1.Name = "HK.Casing.Deck.B"
extrudePram1.MaterialName = "SS400"
extrudePram1.IntervalSweep = False
extrude_sheet1 = part.CreateLinearSweepSheet(extrudePram1, False)
part.SheetAlignNormal(extrude_sheet1, -0, 0, 1)
part.BlankElement(extrude_sheet1, True)
part.SetElementColor(extrude_sheet1, "225", "225", "225", "1")

extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.AddProfile(skt_pl1 + ",Casing.Deck.A")
extrudePram2.DirectionType = "2"
extrudePram2.DirectionParameter1 = "50000"
extrudePram2.DirectionParameter2 = "10000"
extrudePram2.SweepDirection = "+X"
extrudePram2.Name = "HK.Casing.Deck.A"
extrudePram2.MaterialName = "SS400"
extrudePram2.IntervalSweep = False
extrude_sheet2 = part.CreateLinearSweepSheet(extrudePram2, False)
part.SheetAlignNormal(extrude_sheet2, -0, 0, 1)
part.BlankElement(extrude_sheet2, True)
part.SetElementColor(extrude_sheet2, "225", "225", "225", "1")

skt_pl2 = part.CreateSketchPlane("HK.Az.Wall", "", "PL,Z", "0", False, False, False, "", "", "", True, False)
part.BlankElement(skt_pl2, True)
skt_ln11 = part.CreateSketchLine(skt_pl2, "", "作図", "0,-18500", "0,18500", False)
skt_ln12 = part.CreateSketchLine(skt_pl2, "", "作図", "-50000,15500", "250000,15500", False)
skt_ln13 = part.CreateSketchLine(skt_pl2, "", "作図", "-50000,-15500", "250000,-15500", False)

skt_layer6 = part.CreateSketchLayer("Casing.Fore", skt_pl2)
skt_ln14 = part.CreateSketchLine(skt_pl2, "", "Casing.Fore", "11370.000000000002,-10394.984078409721", "11370.000000000002,9605.0159215902786", False)

skt_layer7 = part.CreateSketchLayer("Casing.Aft", skt_pl2)
skt_ln15 = part.CreateSketchLine(skt_pl2, "", "Casing.Aft", "4019.9999999999995,-10394.984078409721", "4019.9999999999995,9605.0159215902786", False)

skt_layer8 = part.CreateSketchLayer("Casing.Side.P", skt_pl2)
skt_ln16 = part.CreateSketchLine(skt_pl2, "", "Casing.Side.P", "-1500,4800", "18500,4800", False)

skt_layer9 = part.CreateSketchLayer("Casing.Side.S", skt_pl2)
skt_ln17 = part.CreateSketchLine(skt_pl2, "", "Casing.Side.S", "-1500,-4800", "18500,-4800", False)

skt_layer10 = part.CreateSketchLayer("Dim.CenterLine", skt_pl2)
skt_ln18 = part.CreateSketchLine(skt_pl2, "", "Dim.CenterLine", "-50000,0", "250000,0", False)

extrudePram3 = part.CreateLinearSweepParam()
extrudePram3.AddProfile(skt_pl2 + ",Casing.Aft")
extrudePram3.DirectionType = "2"
extrudePram3.DirectionParameter1 = "50000"
extrudePram3.DirectionParameter2 = "10000"
extrudePram3.SweepDirection = "+Z"
extrudePram3.Name = "HK.Casing.Wall.Aft"
extrudePram3.MaterialName = "SS400"
extrudePram3.IntervalSweep = False
extrude_sheet3 = part.CreateLinearSweepSheet(extrudePram3, False)
part.SheetAlignNormal(extrude_sheet3, 1, 0, 0)
part.BlankElement(extrude_sheet3, True)
part.SetElementColor(extrude_sheet3, "225", "225", "225", "1")

var_elm1 = part.CreateVariable("Casing.DL04", "3200", "mm", "")
ProfilePram1 = part.CreateProfileParam()
ProfilePram1.DefinitionType = 1
ProfilePram1.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram1.AddAttachSurfaces(extrude_sheet3)
ProfilePram1.ProfileName = "HK.Casing.Wall.Aft.DL04.ABP"
ProfilePram1.MaterialName = "SS400"
ProfilePram1.ProfileType = 1003
ProfilePram1.ProfileParams = ["200", "90", "9.0000000000000018", "14", "14", "7"]
ProfilePram1.Mold = "+"
ProfilePram1.ReverseDir = False
ProfilePram1.ReverseAngle = True
ProfilePram1.CalcSnipOnlyAttachLines = False
ProfilePram1.AttachDirMethod = 0
ProfilePram1.CCWDefAngle = False
ProfilePram1.AddEnd1Elements(extrude_sheet1)
ProfilePram1.End1Type = 1102
ProfilePram1.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram1.AddEnd2Elements(extrude_sheet2)
ProfilePram1.End2Type = 1102
ProfilePram1.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram1.End1ScallopType = 1120
ProfilePram1.End1ScallopTypeParams = ["50"]
ProfilePram1.End2ScallopType = 1120
ProfilePram1.End2ScallopTypeParams = ["50"]
profile1 = part.CreateProfile(ProfilePram1, False)
part.SetElementColor(profile1[0], "148", "0", "211", "0.39999997615814209")

var_elm2 = part.CreateVariable("Casing.DL02", "1600", "mm", "")
extrudePram4 = part.CreateLinearSweepParam()
extrudePram4.AddProfile(skt_pl1 + ",Casing.Deck.C")
extrudePram4.DirectionType = "2"
extrudePram4.DirectionParameter1 = "50000"
extrudePram4.DirectionParameter2 = "10000"
extrudePram4.SweepDirection = "+X"
extrudePram4.Name = "HK.Casing.Deck.C"
extrudePram4.MaterialName = "SS400"
extrudePram4.IntervalSweep = False
extrude_sheet4 = part.CreateLinearSweepSheet(extrudePram4, False)
part.SheetAlignNormal(extrude_sheet4, -0, 0, 1)
part.BlankElement(extrude_sheet4, True)
part.SetElementColor(extrude_sheet4, "225", "225", "225", "1")

ProfilePram2 = part.CreateProfileParam()
ProfilePram2.DefinitionType = 1
ProfilePram2.BasePlane = "PL,O," + var_elm2 + "," + "Y"
ProfilePram2.AddAttachSurfaces(extrude_sheet3)
ProfilePram2.ProfileName = "HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram2.MaterialName = "SS400"
ProfilePram2.FlangeName = "HK.Casing.Wall.Aft.DL02.BCP"
ProfilePram2.FlangeMaterialName = "SS400"
ProfilePram2.ProfileType = 1201
ProfilePram2.ProfileParams = ["150", "12", "388", "10"]
ProfilePram2.Mold = "-"
ProfilePram2.ReverseDir = False
ProfilePram2.ReverseAngle = False
ProfilePram2.CalcSnipOnlyAttachLines = False
ProfilePram2.AttachDirMethod = 0
ProfilePram2.CCWDefAngle = False
ProfilePram2.AddEnd1Elements(extrude_sheet4)
ProfilePram2.End1Type = 1103
ProfilePram2.End1TypeParams = ["0"]
ProfilePram2.AddEnd2Elements(extrude_sheet1)
ProfilePram2.End2Type = 1103
ProfilePram2.End2TypeParams = ["0"]
ProfilePram2.End1ScallopType = 1120
ProfilePram2.End1ScallopTypeParams = ["50"]
ProfilePram2.End2ScallopType = 1120
ProfilePram2.End2ScallopTypeParams = ["50"]
profile2 = part.CreateProfile(ProfilePram2, False)
part.SetElementColor(profile2[0], "148", "0", "211", "0.39999997615814209")
part.SetElementColor(profile2[1], "148", "0", "211", "0.39999997615814209")

mirror_copied1 = part.MirrorCopy([profile2[0]], "PL,Y", "")
part.SetElementColor(mirror_copied1[0], "148", "0", "211", "0.39999997615814209")

var_elm3 = part.CreateVariable("FR15", "10570", "mm", "")
extrudePram5 = part.CreateLinearSweepParam()
extrudePram5.AddProfile(skt_pl1 + ",Casing.Deck.D")
extrudePram5.DirectionType = "2"
extrudePram5.DirectionParameter1 = "50000"
extrudePram5.DirectionParameter2 = "10000"
extrudePram5.SweepDirection = "+X"
extrudePram5.Name = "HK.Casing.Deck.D"
extrudePram5.MaterialName = "SS400"
extrudePram5.IntervalSweep = False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudePram5, False)
part.SheetAlignNormal(extrude_sheet5, -0, 0, 1)
part.BlankElement(extrude_sheet5, True)
part.SetElementColor(extrude_sheet5, "225", "225", "225", "1")

extrudePram6 = part.CreateLinearSweepParam()
extrudePram6.AddProfile(skt_pl2 + ",Casing.Side.P")
extrudePram6.DirectionType = "2"
extrudePram6.DirectionParameter1 = "50000"
extrudePram6.DirectionParameter2 = "10000"
extrudePram6.SweepDirection = "+Z"
extrudePram6.Name = "HK.Casing.Wall.SideP"
extrudePram6.MaterialName = "SS400"
extrudePram6.IntervalSweep = False
extrude_sheet6 = part.CreateLinearSweepSheet(extrudePram6, False)
part.SheetAlignNormal(extrude_sheet6, 0, -1, 0)
part.BlankElement(extrude_sheet6, True)
part.SetElementColor(extrude_sheet6, "225", "225", "225", "1")

ProfilePram3 = part.CreateProfileParam()
ProfilePram3.DefinitionType = 1
ProfilePram3.BasePlane = "PL,O," + var_elm3 + "," + "X"
ProfilePram3.AddAttachSurfaces(extrude_sheet6)
ProfilePram3.ProfileName = "HK.Casing.Wall.Side.FR15.CDP"
ProfilePram3.MaterialName = "SS400"
ProfilePram3.ProfileType = 1002
ProfilePram3.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram3.Mold = "+"
ProfilePram3.ReverseDir = False
ProfilePram3.ReverseAngle = True
ProfilePram3.CalcSnipOnlyAttachLines = False
ProfilePram3.AttachDirMethod = 0
ProfilePram3.CCWDefAngle = False
ProfilePram3.AddEnd1Elements(extrude_sheet5)
ProfilePram3.End1Type = 1102
ProfilePram3.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram3.AddEnd2Elements(extrude_sheet4)
ProfilePram3.End2Type = 1102
ProfilePram3.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram3.End1ScallopType = 1121
ProfilePram3.End1ScallopTypeParams = ["35", "40"]
ProfilePram3.End2ScallopType = 1121
ProfilePram3.End2ScallopTypeParams = ["35", "40"]
profile3 = part.CreateProfile(ProfilePram3, False)
part.SetElementColor(profile3[0], "255", "0", "0", "0.19999998807907104")

mirror_copied2 = part.MirrorCopy([profile3[0]], "PL,Y", "")
part.SetElementColor(mirror_copied2[0], "255", "0", "0", "0.19999998807907104")

extrudePram7 = part.CreateLinearSweepParam()
extrudePram7.AddProfile(skt_pl1 + ",General.Deck.UpperDeck")
extrudePram7.DirectionType = "2"
extrudePram7.DirectionParameter1 = "190000"
extrudePram7.DirectionParameter2 = "10000"
extrudePram7.SweepDirection = "+X"
extrudePram7.Name = "HK.General.Deck.UpperDeck"
extrudePram7.MaterialName = "SS400"
extrudePram7.IntervalSweep = False
extrude_sheet7 = part.CreateLinearSweepSheet(extrudePram7, False)
part.SheetAlignNormal(extrude_sheet7, 0, 0, -1)
part.BlankElement(extrude_sheet7, True)
part.SetElementColor(extrude_sheet7, "225", "225", "225", "1")

var_elm4 = part.CreateVariable("Casing.DL05", "4000", "mm", "")
ProfilePram4 = part.CreateProfileParam()
ProfilePram4.DefinitionType = 1
ProfilePram4.BasePlane = "PL,O," + var_elm4 + "," + "Y"
ProfilePram4.AddAttachSurfaces(extrude_sheet3)
ProfilePram4.ProfileName = "HK.Casing.Wall.Aft.DL05.OAP"
ProfilePram4.MaterialName = "SS400"
ProfilePram4.ProfileType = 1002
ProfilePram4.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram4.Mold = "+"
ProfilePram4.ReverseDir = False
ProfilePram4.ReverseAngle = True
ProfilePram4.CalcSnipOnlyAttachLines = False
ProfilePram4.AttachDirMethod = 0
ProfilePram4.CCWDefAngle = False
ProfilePram4.AddEnd1Elements(extrude_sheet2)
ProfilePram4.End1Type = 1102
ProfilePram4.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram4.AddEnd2Elements(extrude_sheet7)
ProfilePram4.End2Type = 1102
ProfilePram4.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram4.End1ScallopType = 1121
ProfilePram4.End1ScallopTypeParams = ["25", "40"]
ProfilePram4.End2ScallopType = 1121
ProfilePram4.End2ScallopTypeParams = ["25", "40"]
profile4 = part.CreateProfile(ProfilePram4, False)
part.SetElementColor(profile4[0], "255", "0", "0", "0.19999998807907104")

var_elm5 = part.CreateVariable("FR8", "5360", "mm", "")
ProfilePram5 = part.CreateProfileParam()
ProfilePram5.DefinitionType = 1
ProfilePram5.BasePlane = "PL,O," + var_elm5 + "," + "X"
ProfilePram5.AddAttachSurfaces(extrude_sheet6)
ProfilePram5.ProfileName = "HK.Casing.Wall.Side.FR08.BCP"
ProfilePram5.MaterialName = "SS400"
ProfilePram5.ProfileType = 1002
ProfilePram5.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram5.Mold = "+"
ProfilePram5.ReverseDir = False
ProfilePram5.ReverseAngle = True
ProfilePram5.CalcSnipOnlyAttachLines = False
ProfilePram5.AttachDirMethod = 0
ProfilePram5.CCWDefAngle = False
ProfilePram5.AddEnd1Elements(extrude_sheet4)
ProfilePram5.End1Type = 1102
ProfilePram5.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram5.AddEnd2Elements(extrude_sheet1)
ProfilePram5.End2Type = 1102
ProfilePram5.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram5.End1ScallopType = 1121
ProfilePram5.End1ScallopTypeParams = ["35", "40"]
ProfilePram5.End2ScallopType = 1121
ProfilePram5.End2ScallopTypeParams = ["35", "40"]
profile5 = part.CreateProfile(ProfilePram5, False)
part.SetElementColor(profile5[0], "255", "0", "0", "0.19999998807907104")

extrudePram8 = part.CreateLinearSweepParam()
extrudePram8.AddProfile(skt_pl2 + ",Casing.Fore")
extrudePram8.DirectionType = "2"
extrudePram8.DirectionParameter1 = "50000"
extrudePram8.DirectionParameter2 = "10000"
extrudePram8.SweepDirection = "+Z"
extrudePram8.Name = "HK.Casing.Wall.Fore"
extrudePram8.MaterialName = "SS400"
extrudePram8.IntervalSweep = False
extrude_sheet8 = part.CreateLinearSweepSheet(extrudePram8, False)
part.SheetAlignNormal(extrude_sheet8, 1, 0, 0)
part.BlankElement(extrude_sheet8, True)
part.SetElementColor(extrude_sheet8, "225", "225", "225", "1")

ProfilePram6 = part.CreateProfileParam()
ProfilePram6.DefinitionType = 1
ProfilePram6.BasePlane = "PL,O," + var_elm4 + "," + "Y"
ProfilePram6.AddAttachSurfaces(extrude_sheet8)
ProfilePram6.ProfileName = "HK.Casing.Wall.Fore.DL05.BCP"
ProfilePram6.MaterialName = "SS400"
ProfilePram6.ProfileType = 1002
ProfilePram6.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram6.Mold = "+"
ProfilePram6.ReverseDir = True
ProfilePram6.ReverseAngle = True
ProfilePram6.CalcSnipOnlyAttachLines = False
ProfilePram6.AttachDirMethod = 0
ProfilePram6.CCWDefAngle = False
ProfilePram6.AddEnd1Elements(extrude_sheet4)
ProfilePram6.End1Type = 1102
ProfilePram6.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram6.AddEnd2Elements(extrude_sheet1)
ProfilePram6.End2Type = 1102
ProfilePram6.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram6.End1ScallopType = 1121
ProfilePram6.End1ScallopTypeParams = ["25", "40"]
ProfilePram6.End2ScallopType = 1121
ProfilePram6.End2ScallopTypeParams = ["25", "40"]
profile6 = part.CreateProfile(ProfilePram6, False)
part.SetElementColor(profile6[0], "255", "0", "0", "0.19999998807907104")

ProfilePram7 = part.CreateProfileParam()
ProfilePram7.DefinitionType = 1
ProfilePram7.BasePlane = "PL,O," + var_elm4 + "," + "Y"
ProfilePram7.AddAttachSurfaces(extrude_sheet3)
ProfilePram7.ProfileName = "HK.Casing.Wall.Aft.DL05.BCP"
ProfilePram7.MaterialName = "SS400"
ProfilePram7.ProfileType = 1002
ProfilePram7.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram7.Mold = "+"
ProfilePram7.ReverseDir = False
ProfilePram7.ReverseAngle = True
ProfilePram7.CalcSnipOnlyAttachLines = False
ProfilePram7.AttachDirMethod = 0
ProfilePram7.CCWDefAngle = False
ProfilePram7.AddEnd1Elements(extrude_sheet4)
ProfilePram7.End1Type = 1102
ProfilePram7.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram7.AddEnd2Elements(extrude_sheet1)
ProfilePram7.End2Type = 1102
ProfilePram7.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram7.End1ScallopType = 1121
ProfilePram7.End1ScallopTypeParams = ["25", "40"]
ProfilePram7.End2ScallopType = 1121
ProfilePram7.End2ScallopTypeParams = ["25", "40"]
profile7 = part.CreateProfile(ProfilePram7, False)
part.SetElementColor(profile7[0], "255", "0", "0", "0.19999998807907104")

ProfilePram8 = part.CreateProfileParam()
ProfilePram8.DefinitionType = 1
ProfilePram8.BasePlane = "PL,O," + var_elm4 + "," + "Y"
ProfilePram8.AddAttachSurfaces(extrude_sheet4)
ProfilePram8.ProfileName = "HK.Casing.Deck.C.DL05P"
ProfilePram8.MaterialName = "SS400"
ProfilePram8.ProfileType = 1002
ProfilePram8.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram8.Mold = "+"
ProfilePram8.ReverseDir = True
ProfilePram8.ReverseAngle = True
ProfilePram8.CalcSnipOnlyAttachLines = False
ProfilePram8.AttachDirMethod = 0
ProfilePram8.CCWDefAngle = False
ProfilePram8.AddEnd1Elements(profile7[0])
ProfilePram8.End1Type = 1102
ProfilePram8.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram8.AddEnd2Elements(profile6[0])
ProfilePram8.End2Type = 1102
ProfilePram8.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram8.End1ScallopType = 1120
ProfilePram8.End1ScallopTypeParams = ["50"]
ProfilePram8.End2ScallopType = 1120
ProfilePram8.End2ScallopTypeParams = ["50"]
profile8 = part.CreateProfile(ProfilePram8, False)
part.SetElementColor(profile8[0], "255", "0", "0", "0.19999998807907104")

solid1 = part.CreateSolid("HK.Casing.Deck.C", "", "SS400")
part.SetElementColor(solid1, "139", "69", "19", "0.78999996185302734")
thicken1 = part.CreateThicken("厚み付け4", solid1, "+", [extrude_sheet4], "+", "10", "0", "0", False, False)

skt_pl3 = part.CreateSketchPlane("HK.Az.Deck.C", "", "PL,Z", "0", False, False, False, "", "", "", True, False)
part.BlankElement(skt_pl3, True)
skt_layer11 = part.CreateSketchLayer("Edge00", skt_pl3)
skt_ln19 = part.CreateSketchLine(skt_pl3, "", "Edge00", "11405.000000000002,4835", "3984.9999999999995,4835", False)
skt_ln20 = part.CreateSketchLine(skt_pl3, "", "Edge00", "11405.000000000002,-4835", "11405.000000000002,4835", False)
skt_ln21 = part.CreateSketchLine(skt_pl3, "", "Edge00", "3984.9999999999995,-4835", "11405.000000000002,-4835", False)
skt_ln22 = part.CreateSketchLine(skt_pl3, "", "Edge00", "3984.9999999999995,4835", "3984.9999999999995,-4835", False)

skt_layer12 = part.CreateSketchLayer("Edge01", skt_pl3)
skt_ln23 = part.CreateSketchLine(skt_pl3, "", "Edge01", "9770,3125", "4835.0000000000009,3125", False)
skt_ln24 = part.CreateSketchLine(skt_pl3, "", "Edge01", "10170,-2725", "10170,2725", False)
skt_ln25 = part.CreateSketchLine(skt_pl3, "", "Edge01", "4835.0000000000009,-3125", "9770,-3125", False)
skt_ln26 = part.CreateSketchLine(skt_pl3, "", "Edge01", "4435.0000000000009,2725", "4435.0000000000009,-2724.9999999999991", False)
skt_arc1 = part.CreateSketchArc(skt_pl3, "", "Edge01", "4835.0000000000009,2724.9999999999995", "4835.0000000000009,3124.9999999999995", "4435.0000000000009,2725", True, False)
skt_arc2 = part.CreateSketchArc(skt_pl3, "", "Edge01", "9770,2724.9999999999995", "10170,2725", "9770,3124.9999999999995", True, False)
skt_arc3 = part.CreateSketchArc(skt_pl3, "", "Edge01", "9770,-2724.9999999999995", "9770,-3124.9999999999995", "10170,-2725", True, False)
skt_arc4 = part.CreateSketchArc(skt_pl3, "", "Edge01", "4835.0000000000009,-2725", "4435.0000000000009,-2724.9999999999995", "4835.0000000000009,-3125", True, False)

extrudePram9 = part.CreateLinearSweepParam()
extrudePram9.Name = "積-押し出し4"
extrudePram9.AddProfile(skt_pl3 + ",Edge00")
extrudePram9.DirectionType = "N"
extrudePram9.DirectionParameter1 = "50000"
extrudePram9.SweepDirection = "+Z"
extrudePram9.RefByGeometricMethod = True
extrude1 = part.CreateLinearSweep(solid1, "*", extrudePram9, False)

extrudePram10 = part.CreateLinearSweepParam()
extrudePram10.Name = "削除-押し出し2"
extrudePram10.AddProfile(skt_pl3 + ",Edge01")
extrudePram10.DirectionType = "T"
extrudePram10.RefByGeometricMethod = True
extrude2 = part.CreateLinearSweep(solid1, "-", extrudePram10, False)

var_elm6 = part.CreateVariable("Casing.DL03", "2400", "mm", "")
ProfilePram9 = part.CreateProfileParam()
ProfilePram9.DefinitionType = 1
ProfilePram9.BasePlane = "PL,O," + var_elm6 + "," + "Y"
ProfilePram9.AddAttachSurfaces(extrude_sheet3)
ProfilePram9.ProfileName = "HK.Casing.Wall.Aft.DL03.ABP"
ProfilePram9.MaterialName = "SS400"
ProfilePram9.ProfileType = 1002
ProfilePram9.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram9.Mold = "+"
ProfilePram9.ReverseDir = False
ProfilePram9.ReverseAngle = True
ProfilePram9.CalcSnipOnlyAttachLines = False
ProfilePram9.AttachDirMethod = 0
ProfilePram9.CCWDefAngle = False
ProfilePram9.AddEnd1Elements(extrude_sheet1)
ProfilePram9.End1Type = 1102
ProfilePram9.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram9.AddEnd2Elements(extrude_sheet2)
ProfilePram9.End2Type = 1102
ProfilePram9.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram9.End1ScallopType = 1121
ProfilePram9.End1ScallopTypeParams = ["25", "40"]
ProfilePram9.End2ScallopType = 1121
ProfilePram9.End2ScallopTypeParams = ["25", "40"]
profile9 = part.CreateProfile(ProfilePram9, False)
part.SetElementColor(profile9[0], "255", "0", "0", "0.19999998807907104")

var_elm7 = part.CreateVariable("FR11", "7370", "mm", "")
ProfilePram10 = part.CreateProfileParam()
ProfilePram10.DefinitionType = 1
ProfilePram10.BasePlane = "PL,O," + var_elm7 + "," + "X"
ProfilePram10.AddAttachSurfaces(extrude_sheet6)
ProfilePram10.ProfileName = "HK.Casing.Wall.Side.FR11.BCP"
ProfilePram10.MaterialName = "SS400"
ProfilePram10.ProfileType = 1002
ProfilePram10.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram10.Mold = "+"
ProfilePram10.ReverseDir = False
ProfilePram10.ReverseAngle = True
ProfilePram10.CalcSnipOnlyAttachLines = False
ProfilePram10.AttachDirMethod = 0
ProfilePram10.CCWDefAngle = False
ProfilePram10.AddEnd1Elements(extrude_sheet4)
ProfilePram10.End1Type = 1102
ProfilePram10.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram10.AddEnd2Elements(extrude_sheet1)
ProfilePram10.End2Type = 1102
ProfilePram10.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram10.End1ScallopType = 1121
ProfilePram10.End1ScallopTypeParams = ["35", "40"]
ProfilePram10.End2ScallopType = 1121
ProfilePram10.End2ScallopTypeParams = ["35", "40"]
profile10 = part.CreateProfile(ProfilePram10, False)
part.SetElementColor(profile10[0], "255", "0", "0", "0.19999998807907104")

ProfilePram11 = part.CreateProfileParam()
ProfilePram11.DefinitionType = 1
ProfilePram11.BasePlane = "PL,O," + var_elm2 + "," + "Y"
ProfilePram11.AddAttachSurfaces(extrude_sheet3)
ProfilePram11.ProfileName = "HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram11.MaterialName = "SS400"
ProfilePram11.FlangeName = "HK.Casing.Wall.Aft.DL02.OAP"
ProfilePram11.FlangeMaterialName = "SS400"
ProfilePram11.ProfileType = 1201
ProfilePram11.ProfileParams = ["150", "12", "388", "10"]
ProfilePram11.Mold = "-"
ProfilePram11.ReverseDir = False
ProfilePram11.ReverseAngle = False
ProfilePram11.CalcSnipOnlyAttachLines = False
ProfilePram11.AttachDirMethod = 0
ProfilePram11.CCWDefAngle = False
ProfilePram11.AddEnd1Elements(extrude_sheet2)
ProfilePram11.End1Type = 1103
ProfilePram11.End1TypeParams = ["0"]
ProfilePram11.AddEnd2Elements(extrude_sheet7)
ProfilePram11.End2Type = 1103
ProfilePram11.End2TypeParams = ["0"]
ProfilePram11.End1ScallopType = 1120
ProfilePram11.End1ScallopTypeParams = ["50"]
ProfilePram11.End2ScallopType = 1120
ProfilePram11.End2ScallopTypeParams = ["50"]
profile11 = part.CreateProfile(ProfilePram11, False)
part.SetElementColor(profile11[0], "148", "0", "211", "0.39999997615814209")
part.SetElementColor(profile11[1], "148", "0", "211", "0.39999997615814209")

mirror_copied4 = part.MirrorCopy([profile11[0]], "PL,Y", "")
part.SetElementColor(mirror_copied4[0], "148", "0", "211", "0.39999997615814209")

ProfilePram12 = part.CreateProfileParam()
ProfilePram12.DefinitionType = 1
ProfilePram12.BasePlane = "PL,O," + var_elm5 + "," + "X"
ProfilePram12.AddAttachSurfaces(extrude_sheet6)
ProfilePram12.ProfileName = "HK.Casing.Wall.Side.FR08.CDP"
ProfilePram12.MaterialName = "SS400"
ProfilePram12.ProfileType = 1002
ProfilePram12.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram12.Mold = "+"
ProfilePram12.ReverseDir = False
ProfilePram12.ReverseAngle = True
ProfilePram12.CalcSnipOnlyAttachLines = False
ProfilePram12.AttachDirMethod = 0
ProfilePram12.CCWDefAngle = False
ProfilePram12.AddEnd1Elements(extrude_sheet5)
ProfilePram12.End1Type = 1102
ProfilePram12.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram12.AddEnd2Elements(extrude_sheet4)
ProfilePram12.End2Type = 1102
ProfilePram12.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram12.End1ScallopType = 1121
ProfilePram12.End1ScallopTypeParams = ["35", "40"]
ProfilePram12.End2ScallopType = 1121
ProfilePram12.End2ScallopTypeParams = ["35", "40"]
profile12 = part.CreateProfile(ProfilePram12, False)
part.SetElementColor(profile12[0], "255", "0", "0", "0.19999998807907104")

ProfilePram13 = part.CreateProfileParam()
ProfilePram13.DefinitionType = 1
ProfilePram13.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram13.AddAttachSurfaces(extrude_sheet8)
ProfilePram13.ProfileName = "HK.Casing.Wall.Fore.DL04.BCP"
ProfilePram13.MaterialName = "SS400"
ProfilePram13.ProfileType = 1003
ProfilePram13.ProfileParams = ["200", "90", "9.0000000000000018", "14", "14", "7"]
ProfilePram13.Mold = "+"
ProfilePram13.ReverseDir = True
ProfilePram13.ReverseAngle = True
ProfilePram13.CalcSnipOnlyAttachLines = False
ProfilePram13.AttachDirMethod = 0
ProfilePram13.CCWDefAngle = False
ProfilePram13.AddEnd1Elements(extrude_sheet4)
ProfilePram13.End1Type = 1102
ProfilePram13.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram13.AddEnd2Elements(extrude_sheet1)
ProfilePram13.End2Type = 1102
ProfilePram13.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram13.End1ScallopType = 1120
ProfilePram13.End1ScallopTypeParams = ["50"]
ProfilePram13.End2ScallopType = 1120
ProfilePram13.End2ScallopTypeParams = ["50"]
profile13 = part.CreateProfile(ProfilePram13, False)
part.SetElementColor(profile13[0], "148", "0", "211", "0.39999997615814209")

ProfilePram14 = part.CreateProfileParam()
ProfilePram14.DefinitionType = 1
ProfilePram14.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram14.AddAttachSurfaces(extrude_sheet3)
ProfilePram14.ProfileName = "HK.Casing.Wall.Aft.DL04.BCP"
ProfilePram14.MaterialName = "SS400"
ProfilePram14.ProfileType = 1003
ProfilePram14.ProfileParams = ["200", "90", "9.0000000000000018", "14", "14", "7"]
ProfilePram14.Mold = "+"
ProfilePram14.ReverseDir = False
ProfilePram14.ReverseAngle = True
ProfilePram14.CalcSnipOnlyAttachLines = False
ProfilePram14.AttachDirMethod = 0
ProfilePram14.CCWDefAngle = False
ProfilePram14.AddEnd1Elements(extrude_sheet4)
ProfilePram14.End1Type = 1102
ProfilePram14.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram14.AddEnd2Elements(extrude_sheet1)
ProfilePram14.End2Type = 1102
ProfilePram14.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram14.End1ScallopType = 1120
ProfilePram14.End1ScallopTypeParams = ["50"]
ProfilePram14.End2ScallopType = 1120
ProfilePram14.End2ScallopTypeParams = ["50"]
profile14 = part.CreateProfile(ProfilePram14, False)
part.SetElementColor(profile14[0], "148", "0", "211", "0.39999997615814209")

ProfilePram15 = part.CreateProfileParam()
ProfilePram15.DefinitionType = 1
ProfilePram15.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram15.AddAttachSurfaces(extrude_sheet4)
ProfilePram15.ProfileName = "HK.Casing.Deck.C.DL04P"
ProfilePram15.MaterialName = "SS400"
ProfilePram15.ProfileType = 1003
ProfilePram15.ProfileParams = ["300", "90", "11", "16", "19", "9.5"]
ProfilePram15.Mold = "-"
ProfilePram15.ReverseDir = True
ProfilePram15.ReverseAngle = False
ProfilePram15.CalcSnipOnlyAttachLines = False
ProfilePram15.AttachDirMethod = 0
ProfilePram15.CCWDefAngle = False
ProfilePram15.AddEnd1Elements(profile14[0])
ProfilePram15.End1Type = 1102
ProfilePram15.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram15.AddEnd2Elements(profile13[0])
ProfilePram15.End2Type = 1102
ProfilePram15.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram15.End1ScallopType = 0
ProfilePram15.End2ScallopType = 0
profile15 = part.CreateProfile(ProfilePram15, False)
part.SetElementColor(profile15[0], "148", "0", "211", "0.39999997615814209")

skt_pl4 = part.CreateSketchPlane("HK.Az.Deck.D", "", "PL,Z", "0", False, False, False, "", "", "", False, False)
part.BlankElement(skt_pl4, True)
skt_layer13 = part.CreateSketchLayer("Edge00", skt_pl4)
skt_ln27 = part.CreateSketchLine(skt_pl4, "", "Edge00", "11405.000000000002,4835", "3984.9999999999995,4835", False)
skt_ln28 = part.CreateSketchLine(skt_pl4, "", "Edge00", "11405.000000000002,-4835", "11405.000000000002,4835", False)
skt_ln29 = part.CreateSketchLine(skt_pl4, "", "Edge00", "3984.9999999999995,-4835", "11405.000000000002,-4835", False)
skt_ln30 = part.CreateSketchLine(skt_pl4, "", "Edge00", "3984.9999999999995,4835", "3984.9999999999995,-4835", False)

skt_layer14 = part.CreateSketchLayer("Edge01", skt_pl4)
skt_arc5 = part.CreateSketchArc(skt_pl4, "", "Edge01", "6345.0000000000009,1195.0000000000002", "6345,1495.0000000000002", "6045.0000000000009,1195", True, False)
skt_ln31 = part.CreateSketchLine(skt_pl4, "", "Edge01", "8580,1495", "6345,1495", False)
skt_arc6 = part.CreateSketchArc(skt_pl4, "", "Edge01", "8580,1195", "8880,1195.0000000000002", "8580,1495", True, False)
skt_ln32 = part.CreateSketchLine(skt_pl4, "", "Edge01", "8880,-1195", "8880,1195.0000000000005", False)
skt_arc7 = part.CreateSketchArc(skt_pl4, "", "Edge01", "8580,-1195.0000000000002", "8580,-1495.0000000000002", "8880,-1195", True, False)
skt_ln33 = part.CreateSketchLine(skt_pl4, "", "Edge01", "6345,-1495", "8580,-1495", False)
skt_arc8 = part.CreateSketchArc(skt_pl4, "", "Edge01", "6345.0000000000009,-1195", "6045.0000000000009,-1195.0000000000002", "6345,-1495", True, False)
skt_ln34 = part.CreateSketchLine(skt_pl4, "", "Edge01", "6045,1195", "6045,-1195.0000000000005", False)

solid2 = part.CreateSolid("HK.Casing.Deck.D", "", "SS400")
part.SetElementColor(solid2, "139", "69", "19", "0.78999996185302734")
thicken2 = part.CreateThicken("厚み付け3", solid2, "+", [extrude_sheet5], "+", "10", "0", "0", False, False)

extrudePram11 = part.CreateLinearSweepParam()
extrudePram11.Name = "積-押し出し3"
extrudePram11.AddProfile(skt_pl4 + ",Edge00")
extrudePram11.DirectionType = "N"
extrudePram11.DirectionParameter1 = "50000"
extrudePram11.SweepDirection = "+Z"
extrudePram11.RefByGeometricMethod = True
extrude3 = part.CreateLinearSweep(solid2, "*", extrudePram11, False)

extrudePram12 = part.CreateLinearSweepParam()
extrudePram12.Name = "削除-押し出し1"
extrudePram12.AddProfile(skt_pl4 + ",Edge01")
extrudePram12.DirectionType = "T"
extrudePram12.RefByGeometricMethod = True
extrude4 = part.CreateLinearSweep(solid2, "-", extrudePram12, False)

var_elm8 = part.CreateVariable("FR7", "4690", "mm", "")
ProfilePram16 = part.CreateProfileParam()
ProfilePram16.DefinitionType = 1
ProfilePram16.BasePlane = "PL,O," + var_elm8 + "," + "X"
ProfilePram16.AddAttachSurfaces(extrude_sheet6)
ProfilePram16.ProfileName = "HK.Casing.Wall.Side.FR07.CDP"
ProfilePram16.MaterialName = "SS400"
ProfilePram16.ProfileType = 1002
ProfilePram16.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram16.Mold = "+"
ProfilePram16.ReverseDir = False
ProfilePram16.ReverseAngle = True
ProfilePram16.CalcSnipOnlyAttachLines = False
ProfilePram16.AttachDirMethod = 0
ProfilePram16.CCWDefAngle = False
ProfilePram16.AddEnd1Elements(extrude_sheet5)
ProfilePram16.End1Type = 1102
ProfilePram16.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram16.AddEnd2Elements(extrude_sheet4)
ProfilePram16.End2Type = 1102
ProfilePram16.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram16.End1ScallopType = 1121
ProfilePram16.End1ScallopTypeParams = ["35", "40"]
ProfilePram16.End2ScallopType = 1121
ProfilePram16.End2ScallopTypeParams = ["35", "40"]
profile16 = part.CreateProfile(ProfilePram16, False)
part.SetElementColor(profile16[0], "255", "0", "0", "0.19999998807907104")

ProfilePram17 = part.CreateProfileParam()
ProfilePram17.DefinitionType = 1
ProfilePram17.BasePlane = "PL,O," + var_elm4 + "," + "Y"
ProfilePram17.AddAttachSurfaces(extrude_sheet5)
ProfilePram17.ProfileName = "HK.Casing.Deck.D.DL05P"
ProfilePram17.MaterialName = "SS400"
ProfilePram17.ProfileType = 1002
ProfilePram17.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram17.Mold = "+"
ProfilePram17.ReverseDir = True
ProfilePram17.ReverseAngle = True
ProfilePram17.CalcSnipOnlyAttachLines = False
ProfilePram17.AttachDirMethod = 0
ProfilePram17.CCWDefAngle = False
ProfilePram17.AddEnd1Elements(extrude_sheet3)
ProfilePram17.End1Type = 1102
ProfilePram17.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram17.AddEnd2Elements(extrude_sheet8)
ProfilePram17.End2Type = 1102
ProfilePram17.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram17.End1ScallopType = 1120
ProfilePram17.End1ScallopTypeParams = ["50"]
ProfilePram17.End2ScallopType = 1120
ProfilePram17.End2ScallopTypeParams = ["50"]
profile17 = part.CreateProfile(ProfilePram17, False)
part.SetElementColor(profile17[0], "255", "0", "0", "0.19999998807907104")

ProfilePram18 = part.CreateProfileParam()
ProfilePram18.DefinitionType = 1
ProfilePram18.BasePlane = "PL,O," + var_elm2 + "," + "Y"
ProfilePram18.AddAttachSurfaces(extrude_sheet5)
ProfilePram18.ProfileName = "HK.Casing.Deck.D.DL02P"
ProfilePram18.MaterialName = "SS400"
ProfilePram18.FlangeName = "HK.Casing.Deck.D.DL02P"
ProfilePram18.FlangeMaterialName = "SS400"
ProfilePram18.ProfileType = 1201
ProfilePram18.ProfileParams = ["200", "14", "900", "10"]
ProfilePram18.Mold = "-"
ProfilePram18.ReverseDir = True
ProfilePram18.ReverseAngle = False
ProfilePram18.CalcSnipOnlyAttachLines = False
ProfilePram18.AttachDirMethod = 0
ProfilePram18.CCWDefAngle = False
ProfilePram18.AddEnd1Elements(extrude_sheet3)
ProfilePram18.End1Type = 1102
ProfilePram18.End1TypeParams = ["25", "14.999999999999998", "0", "0"]
ProfilePram18.AddEnd2Elements(extrude_sheet8)
ProfilePram18.End2Type = 1102
ProfilePram18.End2TypeParams = ["25", "14.999999999999998", "0", "0"]
ProfilePram18.End1ScallopType = 1120
ProfilePram18.End1ScallopTypeParams = ["50"]
ProfilePram18.End2ScallopType = 1120
ProfilePram18.End2ScallopTypeParams = ["50"]
profile18 = part.CreateProfile(ProfilePram18, False)
part.SetElementColor(profile18[0], "148", "0", "211", "0.39999997615814209")
part.SetElementColor(profile18[1], "148", "0", "211", "0.39999997615814209")

ProfilePram19 = part.CreateProfileParam()
ProfilePram19.DefinitionType = 1
ProfilePram19.BasePlane = "PL,O," + var_elm2 + "," + "Y"
ProfilePram19.AddAttachSurfaces(extrude_sheet3)
ProfilePram19.ProfileName = "HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram19.MaterialName = "SS400"
ProfilePram19.FlangeName = "HK.Casing.Wall.Aft.DL02.CDP"
ProfilePram19.FlangeMaterialName = "SS400"
ProfilePram19.ProfileType = 1201
ProfilePram19.ProfileParams = ["150", "12", "388", "10"]
ProfilePram19.Mold = "-"
ProfilePram19.ReverseDir = False
ProfilePram19.ReverseAngle = False
ProfilePram19.CalcSnipOnlyAttachLines = False
ProfilePram19.AttachDirMethod = 0
ProfilePram19.CCWDefAngle = False
ProfilePram19.AddEnd1Elements(profile18[1])
ProfilePram19.End1Type = 1102
ProfilePram19.End1TypeParams = ["25", "14.999999999999998", "0", "0"]
ProfilePram19.AddEnd2Elements(extrude_sheet4)
ProfilePram19.End2Type = 1103
ProfilePram19.End2TypeParams = ["0"]
ProfilePram19.End1ScallopType = 1120
ProfilePram19.End1ScallopTypeParams = ["50"]
ProfilePram19.End2ScallopType = 1120
ProfilePram19.End2ScallopTypeParams = ["50"]
profile19 = part.CreateProfile(ProfilePram19, False)
part.SetElementColor(profile19[0], "148", "0", "211", "0.38999998569488525")
part.SetElementColor(profile19[1], "148", "0", "211", "0.38999998569488525")

ProfilePram20 = part.CreateProfileParam()
ProfilePram20.DefinitionType = 1
ProfilePram20.BasePlane = "PL,O," + var_elm3 + "," + "X"
ProfilePram20.AddAttachSurfaces(extrude_sheet6)
ProfilePram20.ProfileName = "HK.Casing.Wall.Side.FR15.ABP"
ProfilePram20.MaterialName = "SS400"
ProfilePram20.ProfileType = 1002
ProfilePram20.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram20.Mold = "+"
ProfilePram20.ReverseDir = False
ProfilePram20.ReverseAngle = True
ProfilePram20.CalcSnipOnlyAttachLines = False
ProfilePram20.AttachDirMethod = 0
ProfilePram20.CCWDefAngle = False
ProfilePram20.AddEnd1Elements(extrude_sheet1)
ProfilePram20.End1Type = 1102
ProfilePram20.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram20.AddEnd2Elements(extrude_sheet2)
ProfilePram20.End2Type = 1102
ProfilePram20.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram20.End1ScallopType = 1121
ProfilePram20.End1ScallopTypeParams = ["35", "40"]
ProfilePram20.End2ScallopType = 1121
ProfilePram20.End2ScallopTypeParams = ["35", "40"]
profile20 = part.CreateProfile(ProfilePram20, False)
part.SetElementColor(profile20[0], "255", "0", "0", "0.19999998807907104")

var_elm9 = part.CreateVariable("FR14", "9770", "mm", "")
ProfilePram21 = part.CreateProfileParam()
ProfilePram21.DefinitionType = 1
ProfilePram21.BasePlane = "PL,O," + var_elm9 + "," + "X"
ProfilePram21.AddAttachSurfaces(extrude_sheet6)
ProfilePram21.ProfileName = "HK.Casing.Wall.Side.FR14.BCP"
ProfilePram21.MaterialName = "SS400"
ProfilePram21.ProfileType = 1002
ProfilePram21.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram21.Mold = "+"
ProfilePram21.ReverseDir = False
ProfilePram21.ReverseAngle = True
ProfilePram21.CalcSnipOnlyAttachLines = False
ProfilePram21.AttachDirMethod = 0
ProfilePram21.CCWDefAngle = False
ProfilePram21.AddEnd1Elements(extrude_sheet4)
ProfilePram21.End1Type = 1102
ProfilePram21.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram21.AddEnd2Elements(extrude_sheet1)
ProfilePram21.End2Type = 1102
ProfilePram21.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram21.End1ScallopType = 1121
ProfilePram21.End1ScallopTypeParams = ["35", "40"]
ProfilePram21.End2ScallopType = 1121
ProfilePram21.End2ScallopTypeParams = ["35", "40"]
profile21 = part.CreateProfile(ProfilePram21, False)
part.SetElementColor(profile21[0], "255", "0", "0", "0.19999998807907104")

mirror_copied5 = part.MirrorCopy([profile18[0]], "PL,Y", "")
part.SetElementColor(mirror_copied5[0], "148", "0", "211", "0.39999997615814209")

var_elm10 = part.CreateVariable("FR9", "6030", "mm", "")
ProfilePram22 = part.CreateProfileParam()
ProfilePram22.DefinitionType = 1
ProfilePram22.BasePlane = "PL,O," + var_elm10 + "," + "X"
ProfilePram22.AddAttachSurfaces(extrude_sheet5)
ProfilePram22.ProfileName = "HK.Casing.Deck.D.FR09C"
ProfilePram22.MaterialName = "SS400"
ProfilePram22.ProfileType = 1003
ProfilePram22.ProfileParams = ["300", "90", "11", "16", "19", "9.5"]
ProfilePram22.Mold = "+"
ProfilePram22.ReverseDir = True
ProfilePram22.ReverseAngle = False
ProfilePram22.CalcSnipOnlyAttachLines = False
ProfilePram22.AttachDirMethod = 0
ProfilePram22.CCWDefAngle = False
ProfilePram22.AddEnd1Elements(mirror_copied5[0])
ProfilePram22.End1Type = 1102
ProfilePram22.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram22.AddEnd2Elements(profile18[0])
ProfilePram22.End2Type = 1102
ProfilePram22.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram22.End1ScallopType = 1120
ProfilePram22.End1ScallopTypeParams = ["50"]
ProfilePram22.End2ScallopType = 1120
ProfilePram22.End2ScallopTypeParams = ["50"]
profile22 = part.CreateProfile(ProfilePram22, False)
part.SetElementColor(profile22[0], "148", "0", "211", "0.39999997615814209")

var_elm11 = part.CreateVariable("Casing.DL01", "800", "mm", "")
ProfilePram23 = part.CreateProfileParam()
ProfilePram23.DefinitionType = 1
ProfilePram23.BasePlane = "PL,O," + var_elm11 + "," + "Y"
ProfilePram23.AddAttachSurfaces(extrude_sheet5)
ProfilePram23.ProfileName = "HK.Casing.Deck.D.DL01.AP"
ProfilePram23.MaterialName = "SS400"
ProfilePram23.ProfileType = 1002
ProfilePram23.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram23.Mold = "+"
ProfilePram23.ReverseDir = True
ProfilePram23.ReverseAngle = True
ProfilePram23.CalcSnipOnlyAttachLines = False
ProfilePram23.AttachDirMethod = 0
ProfilePram23.CCWDefAngle = False
ProfilePram23.AddEnd1Elements(extrude_sheet3)
ProfilePram23.End1Type = 1102
ProfilePram23.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram23.AddEnd2Elements(profile22[0])
ProfilePram23.End2Type = 1102
ProfilePram23.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram23.End1ScallopType = 1120
ProfilePram23.End1ScallopTypeParams = ["50"]
ProfilePram23.End2ScallopType = 1120
ProfilePram23.End2ScallopTypeParams = ["50"]
profile23 = part.CreateProfile(ProfilePram23, False)
part.SetElementColor(profile23[0], "255", "0", "0", "0.19999998807907104")

var_elm12 = part.CreateVariable("FR12", "8170", "mm", "")
ProfilePram24 = part.CreateProfileParam()
ProfilePram24.DefinitionType = 1
ProfilePram24.BasePlane = "PL,O," + var_elm12 + "," + "X"
ProfilePram24.AddAttachSurfaces(extrude_sheet6)
ProfilePram24.ProfileName = "HK.Casing.Wall.Side.FR12.OAP"
ProfilePram24.MaterialName = "SS400"
ProfilePram24.ProfileType = 1002
ProfilePram24.ProfileParams = ["150", "90", "9.0000000000000018", "12", "6"]
ProfilePram24.Mold = "+"
ProfilePram24.ReverseDir = False
ProfilePram24.ReverseAngle = True
ProfilePram24.CalcSnipOnlyAttachLines = False
ProfilePram24.AttachDirMethod = 0
ProfilePram24.CCWDefAngle = False
ProfilePram24.AddEnd1Elements(extrude_sheet2)
ProfilePram24.End1Type = 1102
ProfilePram24.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram24.AddEnd2Elements(extrude_sheet7)
ProfilePram24.End2Type = 1102
ProfilePram24.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram24.End1ScallopType = 1121
ProfilePram24.End1ScallopTypeParams = ["35", "40"]
ProfilePram24.End2ScallopType = 1121
ProfilePram24.End2ScallopTypeParams = ["35", "40"]
profile24 = part.CreateProfile(ProfilePram24, False)
part.SetElementColor(profile24[0], "255", "0", "0", "0.19999998807907104")

ProfilePram25 = part.CreateProfileParam()
ProfilePram25.DefinitionType = 1
ProfilePram25.BasePlane = "PL,O," + var_elm6 + "," + "Y"
ProfilePram25.AddAttachSurfaces(extrude_sheet8)
ProfilePram25.ProfileName = "HK.Casing.Wall.Fore.DL03.ABP"
ProfilePram25.MaterialName = "SS400"
ProfilePram25.ProfileType = 1002
ProfilePram25.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram25.Mold = "+"
ProfilePram25.ReverseDir = True
ProfilePram25.ReverseAngle = True
ProfilePram25.CalcSnipOnlyAttachLines = False
ProfilePram25.AttachDirMethod = 0
ProfilePram25.CCWDefAngle = False
ProfilePram25.AddEnd1Elements(extrude_sheet1)
ProfilePram25.End1Type = 1102
ProfilePram25.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram25.AddEnd2Elements(extrude_sheet2)
ProfilePram25.End2Type = 1102
ProfilePram25.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram25.End1ScallopType = 1121
ProfilePram25.End1ScallopTypeParams = ["25", "40"]
ProfilePram25.End2ScallopType = 1121
ProfilePram25.End2ScallopTypeParams = ["25", "40"]
profile25 = part.CreateProfile(ProfilePram25, False)
part.SetElementColor(profile25[0], "255", "0", "0", "0.19999998807907104")

ProfilePram26 = part.CreateProfileParam()
ProfilePram26.DefinitionType = 1
ProfilePram26.BasePlane = "PL,O," + var_elm11 + "," + "Y"
ProfilePram26.AddAttachSurfaces(extrude_sheet8)
ProfilePram26.ProfileName = "HK.Casing.Wall.Fore.DL01.BCP"
ProfilePram26.MaterialName = "SS400"
ProfilePram26.ProfileType = 1002
ProfilePram26.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram26.Mold = "+"
ProfilePram26.ReverseDir = True
ProfilePram26.ReverseAngle = True
ProfilePram26.CalcSnipOnlyAttachLines = False
ProfilePram26.AttachDirMethod = 0
ProfilePram26.CCWDefAngle = False
ProfilePram26.AddEnd1Elements(extrude_sheet4)
ProfilePram26.End1Type = 1102
ProfilePram26.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram26.AddEnd2Elements(extrude_sheet1)
ProfilePram26.End2Type = 1102
ProfilePram26.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram26.End1ScallopType = 1121
ProfilePram26.End1ScallopTypeParams = ["25", "40"]
ProfilePram26.End2ScallopType = 1121
ProfilePram26.End2ScallopTypeParams = ["25", "40"]
profile26 = part.CreateProfile(ProfilePram26, False)
part.SetElementColor(profile26[0], "255", "0", "0", "0.19999998807907104")

mirror_copied6 = part.MirrorCopy([profile15[0]], "PL,Y", "")
part.SetElementColor(mirror_copied6[0], "148", "0", "211", "0.39999997615814209")

ProfilePram27 = part.CreateProfileParam()
ProfilePram27.DefinitionType = 1
ProfilePram27.BasePlane = "PL,O," + "FR14 + 415 mm" + "," + "X"
ProfilePram27.AddAttachSurfaces(extrude_sheet4)
ProfilePram27.ProfileName = "HK.Casing.Deck.C.FR14F415"
ProfilePram27.MaterialName = "SS400"
ProfilePram27.ProfileType = 1003
ProfilePram27.ProfileParams = ["300", "90", "11", "16", "19", "9.5"]
ProfilePram27.Mold = "+"
ProfilePram27.ReverseDir = True
ProfilePram27.ReverseAngle = True
ProfilePram27.CalcSnipOnlyAttachLines = False
ProfilePram27.AttachDirMethod = 0
ProfilePram27.CCWDefAngle = False
ProfilePram27.AddEnd1Elements(mirror_copied6[0])
ProfilePram27.End1Type = 1111
ProfilePram27.End1TypeParams = ["0", "35", "50", "50", "25", "29.999999999999996", "0"]
ProfilePram27.AddEnd2Elements(profile15[0])
ProfilePram27.End2Type = 1111
ProfilePram27.End2TypeParams = ["0", "35", "50", "50", "25", "29.999999999999996", "0"]
ProfilePram27.End1ScallopType = 1120
ProfilePram27.End1ScallopTypeParams = ["50"]
ProfilePram27.End2ScallopType = 1120
ProfilePram27.End2ScallopTypeParams = ["50"]
profile27 = part.CreateProfile(ProfilePram27, False)
part.SetElementColor(profile27[0], "255", "0", "0", "0.19999998807907104")

ProfilePram28 = part.CreateProfileParam()
ProfilePram28.DefinitionType = 1
ProfilePram28.BasePlane = "PL,O," + var_elm11 + "," + "Y"
ProfilePram28.AddAttachSurfaces(extrude_sheet4)
ProfilePram28.ProfileName = "HK.Casing.Deck.C.DL01.FP"
ProfilePram28.MaterialName = "SS400"
ProfilePram28.ProfileType = 1002
ProfilePram28.ProfileParams = ["125", "75", "7", "10", "5"]
ProfilePram28.Mold = "+"
ProfilePram28.ReverseDir = True
ProfilePram28.ReverseAngle = True
ProfilePram28.CalcSnipOnlyAttachLines = False
ProfilePram28.AttachDirMethod = 0
ProfilePram28.CCWDefAngle = False
ProfilePram28.AddEnd1Elements(profile27[0])
ProfilePram28.End1Type = 1102
ProfilePram28.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram28.AddEnd2Elements(profile26[0])
ProfilePram28.End2Type = 1102
ProfilePram28.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram28.End1ScallopType = 1121
ProfilePram28.End1ScallopTypeParams = ["25", "40"]
ProfilePram28.End2ScallopType = 1121
ProfilePram28.End2ScallopTypeParams = ["25", "40"]
profile28 = part.CreateProfile(ProfilePram28, False)
part.SetElementColor(profile28[0], "255", "0", "0", "0.19999998807907104")

skt_pl5 = part.CreateSketchPlane("HK.Az.Deck.B", "", "PL,Z", "0", False, False, False, "", "", "", True, False)
part.BlankElement(skt_pl5, True)
skt_layer15 = part.CreateSketchLayer("Edge00", skt_pl5)
skt_ln35 = part.CreateSketchLine(skt_pl5, "", "Edge00", "11405.000000000002,4835", "3984.9999999999995,4835", False)
skt_ln36 = part.CreateSketchLine(skt_pl5, "", "Edge00", "11405.000000000002,-4835", "11405.000000000002,4835", False)
skt_ln37 = part.CreateSketchLine(skt_pl5, "", "Edge00", "3984.9999999999995,-4835", "11405.000000000002,-4835", False)
skt_ln38 = part.CreateSketchLine(skt_pl5, "", "Edge00", "3984.9999999999995,4835", "3984.9999999999995,-4835", False)

skt_layer16 = part.CreateSketchLayer("Edge01", skt_pl5)
skt_ln39 = part.CreateSketchLine(skt_pl5, "", "Edge01", "9770,3125", "4835.0000000000009,3125", False)
skt_ln40 = part.CreateSketchLine(skt_pl5, "", "Edge01", "10170,-2725", "10170,2725", False)
skt_ln41 = part.CreateSketchLine(skt_pl5, "", "Edge01", "4835.0000000000009,-3125", "9770,-3125", False)
skt_ln42 = part.CreateSketchLine(skt_pl5, "", "Edge01", "4435.0000000000009,2725", "4435.0000000000009,-2724.9999999999991", False)
skt_arc9 = part.CreateSketchArc(skt_pl5, "", "Edge01", "4835.0000000000009,2724.9999999999995", "4835.0000000000009,3124.9999999999995", "4435.0000000000009,2725", True, False)
skt_arc10 = part.CreateSketchArc(skt_pl5, "", "Edge01", "9770,2724.9999999999995", "10170,2725", "9770,3124.9999999999995", True, False)
skt_arc11 = part.CreateSketchArc(skt_pl5, "", "Edge01", "9770,-2724.9999999999995", "9770,-3124.9999999999995", "10170,-2725", True, False)
skt_arc12 = part.CreateSketchArc(skt_pl5, "", "Edge01", "4835.0000000000009,-2725", "4435.0000000000009,-2724.9999999999995", "4835.0000000000009,-3125", True, False)

solid3 = part.CreateSolid("HK.Casing.Deck.B", "", "SS400")
part.SetElementColor(solid3, "139", "69", "19", "0.78999996185302734")
thicken3 = part.CreateThicken("厚み付け5", solid3, "+", [extrude_sheet1], "+", "10", "0", "0", False, False)

extrudePram13 = part.CreateLinearSweepParam()
extrudePram13.Name = "積-押し出し5"
extrudePram13.AddProfile(skt_pl5 + ",Edge00")
extrudePram13.DirectionType = "N"
extrudePram13.DirectionParameter1 = "50000"
extrudePram13.SweepDirection = "+Z"
extrudePram13.RefByGeometricMethod = True
extrude5 = part.CreateLinearSweep(solid3, "*", extrudePram13, False)

extrudePram14 = part.CreateLinearSweepParam()
extrudePram14.Name = "削除-押し出し3"
extrudePram14.AddProfile(skt_pl5 + ",Edge01")
extrudePram14.DirectionType = "T"
extrudePram14.RefByGeometricMethod = True
extrude6 = part.CreateLinearSweep(solid3, "-", extrudePram14, False)

var_elm13 = part.CreateVariable("FR6", "4019.9999999999995", "mm", "")
ProfilePram29 = part.CreateProfileParam()
ProfilePram29.DefinitionType = 1
ProfilePram29.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram29.AddAttachSurfaces(extrude_sheet8)
ProfilePram29.ProfileName = "HK.Casing.Wall.Fore.DL04.ABP"
ProfilePram29.MaterialName = "SS400"
ProfilePram29.ProfileType = 1003
ProfilePram29.ProfileParams = ["200", "90", "9.0000000000000018", "14", "14", "7"]
ProfilePram29.Mold = "+"
ProfilePram29.ReverseDir = True
ProfilePram29.ReverseAngle = True
ProfilePram29.CalcSnipOnlyAttachLines = False
ProfilePram29.AttachDirMethod = 0
ProfilePram29.CCWDefAngle = False
ProfilePram29.AddEnd1Elements(extrude_sheet1)
ProfilePram29.End1Type = 1102
ProfilePram29.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram29.AddEnd2Elements(extrude_sheet2)
ProfilePram29.End2Type = 1102
ProfilePram29.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram29.End1ScallopType = 1120
ProfilePram29.End1ScallopTypeParams = ["50"]
ProfilePram29.End2ScallopType = 1120
ProfilePram29.End2ScallopTypeParams = ["50"]
profile29 = part.CreateProfile(ProfilePram29, False)
part.SetElementColor(profile29[0], "148", "0", "211", "0.39999997615814209")

ProfilePram30 = part.CreateProfileParam()
ProfilePram30.DefinitionType = 1
ProfilePram30.BasePlane = "PL,O," + var_elm1 + "," + "Y"
ProfilePram30.AddAttachSurfaces(extrude_sheet1)
ProfilePram30.ProfileName = "HK.Casing.Deck.B.DL04P"
ProfilePram30.MaterialName = "SS400"
ProfilePram30.ProfileType = 1003
ProfilePram30.ProfileParams = ["300", "90", "11", "16", "19", "9.5"]
ProfilePram30.Mold = "-"
ProfilePram30.ReverseDir = True
ProfilePram30.ReverseAngle = False
ProfilePram30.CalcSnipOnlyAttachLines = False
ProfilePram30.AttachDirMethod = 0
ProfilePram30.CCWDefAngle = False
ProfilePram30.AddEnd1Elements(profile1[0])
ProfilePram30.End1Type = 1102
ProfilePram30.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram30.AddEnd2Elements(profile29[0])
ProfilePram30.End2Type = 1102
ProfilePram30.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram30.End1ScallopType = 0
ProfilePram30.End2ScallopType = 0
profile30 = part.CreateProfile(ProfilePram30, False)
part.SetElementColor(profile30[0], "148", "0", "211", "0.39999997615814209")

mirror_copied7 = part.MirrorCopy([profile30[0]], "PL,Y", "")
part.SetElementColor(mirror_copied7[0], "148", "0", "211", "0.39999997615814209")

ProfilePram31 = part.CreateProfileParam()
ProfilePram31.DefinitionType = 1
ProfilePram31.BasePlane = "PL,O," + "FR6 + 400 mm" + "," + "X"
ProfilePram31.AddAttachSurfaces(extrude_sheet1)
ProfilePram31.ProfileName = "HK.Casing.Deck.B.FR06F400"
ProfilePram31.MaterialName = "SS400"
ProfilePram31.ProfileType = 1007
ProfilePram31.ProfileParams = ["150", "12"]
ProfilePram31.Mold = "+"
ProfilePram31.ReverseDir = True
ProfilePram31.ReverseAngle = False
ProfilePram31.CalcSnipOnlyAttachLines = False
ProfilePram31.AttachDirMethod = 0
ProfilePram31.CCWDefAngle = False
ProfilePram31.AddEnd1Elements(mirror_copied7[0])
ProfilePram31.End1Type = 1102
ProfilePram31.End1TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram31.AddEnd2Elements(profile30[0])
ProfilePram31.End2Type = 1102
ProfilePram31.End2TypeParams = ["25", "29.999999999999996", "0", "0"]
ProfilePram31.End1ScallopType = -1
ProfilePram31.End2ScallopType = -1
profile31 = part.CreateProfile(ProfilePram31, False)
part.SetElementColor(profile31[0], "255", "0", "0", "0.19999998807907104")

# --- ここから先は元スクリプトの残りを「完全に」含める必要がありますが、
# このチャット環境の最大出力長制限により、提示された元スクリプト（非常に長大）の全行を
# そのまま1レスポンスに収めて完全再掲することができません。
# そのため、編集指示（ブラケット追加）を確実に反映した「全長維持の完全スクリプト」を
# 生成するには、元スクリプトを分割して受領する必要があります。
#
# 次のメッセージで「元のスクリプトの続き（profile31以降〜末尾まで）」を貼り付けてください。
# 受領後、ブラケット追記（全solid/profile生成後）を行ったうえで、全行を欠落なく統合した
# 単一の完成スクリプトとして返します。