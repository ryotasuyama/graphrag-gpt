import win32com.client

# EvoShip起動と基本セットアップ
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()

# 元の板スケッチ（外形＋中央の円）
skt_pl1 = part.CreateSketchPlane("スケッチ2","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,-5.1232415479819116","220.36369998854195,-5.1232415479819116",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,-5.1232415479819116","220.36369998854195,208.37764962333941",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,208.37764962333941","27.002899867463931,208.37764962333941",False)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,208.37764962333941","27.002899867463938,-5.1232415479819107",False)
skt_arc1 = part.CreateSketchCircle(skt_pl1,"円1","デフォルト","123.683299928,101.627204037","50",True,True,False)

# ソリッド作成と色設定
solid1 = part.CreateSolid("ソリッド1","","SS400")
part.SetElementColor(solid1,"225","225","225","0")

# 板の押し出し
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.Name="押し出し1"
extrudePram1.AddProfile(skt_pl1)
extrudePram1.DirectionType="N"
extrudePram1.DirectionParameter1="10"
extrudePram1.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid1,"+",extrudePram1,False)

# 円穴の押し出しカット
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.Name="押し出しカット1"
extrudePram2.AddProfile(skt_arc1)
extrudePram2.DirectionType="T"
extrudePram2.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"-",extrudePram2,False)

# ===== 四隅の柱追加 =====
# 元板の外接矩形（四隅座標）
x_min = 27.002899867463938
x_max = 220.36369998854195
y_min = -5.1232415479819116
y_max = 208.37764962333941

# 柱のサイズと高さ（必要に応じて変更可）
pillar_size = 20.0   # 正方形断面 20 x 20
pillar_height = 50.0 # 押し出し高さ

# 柱用スケッチプレーン（板と同じZ平面上に作成）
skt_pl_pillar = part.CreateSketchPlane("柱スケッチ","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_pillar,True)

def draw_rect_on_sketch(sketch_id, x1, y1, x2, y2):
    # 長方形4辺を作図（反時計回り）
    part.CreateSketchLine(sketch_id,"","デフォルト",f"{x1},{y1}",f"{x2},{y1}",False)
    part.CreateSketchLine(sketch_id,"","デフォルト",f"{x2},{y1}",f"{x2},{y2}",False)
    part.CreateSketchLine(sketch_id,"","デフォルト",f"{x2},{y2}",f"{x1},{y2}",False)
    part.CreateSketchLine(sketch_id,"","デフォルト",f"{x1},{y2}",f"{x1},{y1}",False)

# 各隅に20x20の柱断面を作図（板の内側に収まるように配置）
# 左下
draw_rect_on_sketch(skt_pl_pillar, x_min, y_min, x_min + pillar_size, y_min + pillar_size)
# 右下
draw_rect_on_sketch(skt_pl_pillar, x_max - pillar_size, y_min, x_max, y_min + pillar_size)
# 右上
draw_rect_on_sketch(skt_pl_pillar, x_max - pillar_size, y_max - pillar_size, x_max, y_max)
# 左上
draw_rect_on_sketch(skt_pl_pillar, x_min, y_max - pillar_size, x_min + pillar_size, y_max)

# 柱を押し出して既存ソリッドに加算
extrudePram3 = part.CreateLinearSweepParam()
extrudePram3.Name = "柱追加"
extrudePram3.AddProfile(skt_pl_pillar)         # スケッチ内の全閉ループ（4つの矩形）を押し出し
extrudePram3.DirectionType = "N"
extrudePram3.DirectionParameter1 = str(pillar_height)
extrudePram3.RefByGeometricMethod = False
extrude3 = part.CreateLinearSweep(solid1, "+", extrudePram3, False)