import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("スケッチ2","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,-5.1232415479819116","220.36369998854195,-5.1232415479819116",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,-5.1232415479819116","220.36369998854195,208.37764962333941",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,208.37764962333941","27.002899867463931,208.37764962333941",False)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,208.37764962333941","27.002899867463938,-5.1232415479819107",False)
skt_arc1 = part.CreateSketchCircle(skt_pl1,"円1","デフォルト","123.683299928,101.627204037","50",True,True,False)
solid1 = part.CreateSolid("ソリッド1","","SS400")
part.SetElementColor(solid1,"225","225","225","0")
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.Name="押し出し1"
extrudePram1.AddProfile(skt_pl1)
extrudePram1.DirectionType="N"
extrudePram1.DirectionParameter1="10"
extrudePram1.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid1,"+",extrudePram1,False)
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.Name="押し出しカット1"
extrudePram2.AddProfile(skt_arc1)
extrudePram2.DirectionType="T"
extrudePram2.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"-",extrudePram2,False)

# ---- ここから四隅の直方体柱を追加 ----
# 元の板の外形座標（元スケッチの値を流用）
xL = 27.002899867463938
yB = -5.1232415479819116
xR = 220.36369998854195
yT = 208.37764962333941

# 柱パラメータ（必要に応じて変更）
pillar_size = 20.0   # 柱の一辺（正方形断面）
pillar_height = 40.0 # 柱の高さ（押し出し量）

# 柱1（左下）
skt_pl_p1 = part.CreateSketchPlane("柱スケッチ1","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_p1,True)
bl_x1, bl_y1 = xL, yB
bl_x2, bl_y2 = xL + pillar_size, yB + pillar_size
part.CreateSketchLine(skt_pl_p1,"","デフォルト",f"{bl_x1},{bl_y1}",f"{bl_x2},{bl_y1}",False)
part.CreateSketchLine(skt_pl_p1,"","デフォルト",f"{bl_x2},{bl_y1}",f"{bl_x2},{bl_y2}",False)
part.CreateSketchLine(skt_pl_p1,"","デフォルト",f"{bl_x2},{bl_y2}",f"{bl_x1},{bl_y2}",False)
part.CreateSketchLine(skt_pl_p1,"","デフォルト",f"{bl_x1},{bl_y2}",f"{bl_x1},{bl_y1}",False)
extrudePram_p1 = part.CreateLinearSweepParam()
extrudePram_p1.Name="柱1"
extrudePram_p1.AddProfile(skt_pl_p1)
extrudePram_p1.DirectionType="N"
extrudePram_p1.DirectionParameter1=str(pillar_height)
extrudePram_p1.RefByGeometricMethod=False
pillar1 = part.CreateLinearSweep(solid1,"+",extrudePram_p1,False)

# 柱2（右下）
skt_pl_p2 = part.CreateSketchPlane("柱スケッチ2","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_p2,True)
br_x1, br_y1 = xR - pillar_size, yB
br_x2, br_y2 = xR, yB + pillar_size
part.CreateSketchLine(skt_pl_p2,"","デフォルト",f"{br_x1},{br_y1}",f"{br_x2},{br_y1}",False)
part.CreateSketchLine(skt_pl_p2,"","デフォルト",f"{br_x2},{br_y1}",f"{br_x2},{br_y2}",False)
part.CreateSketchLine(skt_pl_p2,"","デフォルト",f"{br_x2},{br_y2}",f"{br_x1},{br_y2}",False)
part.CreateSketchLine(skt_pl_p2,"","デフォルト",f"{br_x1},{br_y2}",f"{br_x1},{br_y1}",False)
extrudePram_p2 = part.CreateLinearSweepParam()
extrudePram_p2.Name="柱2"
extrudePram_p2.AddProfile(skt_pl_p2)
extrudePram_p2.DirectionType="N"
extrudePram_p2.DirectionParameter1=str(pillar_height)
extrudePram_p2.RefByGeometricMethod=False
pillar2 = part.CreateLinearSweep(solid1,"+",extrudePram_p2,False)

# 柱3（左上）
skt_pl_p3 = part.CreateSketchPlane("柱スケッチ3","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_p3,True)
tl_x1, tl_y1 = xL, yT - pillar_size
tl_x2, tl_y2 = xL + pillar_size, yT
part.CreateSketchLine(skt_pl_p3,"","デフォルト",f"{tl_x1},{tl_y1}",f"{tl_x2},{tl_y1}",False)
part.CreateSketchLine(skt_pl_p3,"","デフォルト",f"{tl_x2},{tl_y1}",f"{tl_x2},{tl_y2}",False)
part.CreateSketchLine(skt_pl_p3,"","デフォルト",f"{tl_x2},{tl_y2}",f"{tl_x1},{tl_y2}",False)
part.CreateSketchLine(skt_pl_p3,"","デフォルト",f"{tl_x1},{tl_y2}",f"{tl_x1},{tl_y1}",False)
extrudePram_p3 = part.CreateLinearSweepParam()
extrudePram_p3.Name="柱3"
extrudePram_p3.AddProfile(skt_pl_p3)
extrudePram_p3.DirectionType="N"
extrudePram_p3.DirectionParameter1=str(pillar_height)
extrudePram_p3.RefByGeometricMethod=False
pillar3 = part.CreateLinearSweep(solid1,"+",extrudePram_p3,False)

# 柱4（右上）
skt_pl_p4 = part.CreateSketchPlane("柱スケッチ4","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_p4,True)
tr_x1, tr_y1 = xR - pillar_size, yT - pillar_size
tr_x2, tr_y2 = xR, yT
part.CreateSketchLine(skt_pl_p4,"","デフォルト",f"{tr_x1},{tr_y1}",f"{tr_x2},{tr_y1}",False)
part.CreateSketchLine(skt_pl_p4,"","デフォルト",f"{tr_x2},{tr_y1}",f"{tr_x2},{tr_y2}",False)
part.CreateSketchLine(skt_pl_p4,"","デフォルト",f"{tr_x2},{tr_y2}",f"{tr_x1},{tr_y2}",False)
part.CreateSketchLine(skt_pl_p4,"","デフォルト",f"{tr_x1},{tr_y2}",f"{tr_x1},{tr_y1}",False)
extrudePram_p4 = part.CreateLinearSweepParam()
extrudePram_p4.Name="柱4"
extrudePram_p4.AddProfile(skt_pl_p4)
extrudePram_p4.DirectionType="N"
extrudePram_p4.DirectionParameter1=str(pillar_height)
extrudePram_p4.RefByGeometricMethod=False
pillar4 = part.CreateLinearSweep(solid1,"+",extrudePram_p4,False)
# ---- ここまで ----