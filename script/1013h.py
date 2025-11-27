import win32com.client

# EvoShip 起動と基本セットアップ
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()

# 元の板（外形スケッチと円）の作成
skt_pl1 = part.CreateSketchPlane("スケッチ2","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,-5.1232415479819116","220.36369998854195,-5.1232415479819116",False)
skt_ln2 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,-5.1232415479819116","220.36369998854195,208.37764962333941",False)
skt_ln3 = part.CreateSketchLine(skt_pl1,"","デフォルト","220.36369998854195,208.37764962333941","27.002899867463931,208.37764962333941",False)
skt_ln4 = part.CreateSketchLine(skt_pl1,"","デフォルト","27.002899867463938,208.37764962333941","27.002899867463938,-5.1232415479819107",False)
skt_arc1 = part.CreateSketchCircle(skt_pl1,"円1","デフォルト","123.683299928,101.627204037","50",True,True,False)

# ソリッドと押し出し（板）
solid1 = part.CreateSolid("ソリッド1","","SS400")
part.SetElementColor(solid1,"225","225","225","0")
extrudePram1 = part.CreateLinearSweepParam()
extrudePram1.Name="押し出し1"
extrudePram1.AddProfile(skt_pl1)
extrudePram1.DirectionType="N"
extrudePram1.DirectionParameter1="10"
extrudePram1.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid1,"+",extrudePram1,False)

# 円形カット（貫通）
extrudePram2 = part.CreateLinearSweepParam()
extrudePram2.Name="押し出しカット1"
extrudePram2.AddProfile(skt_arc1)
extrudePram2.DirectionType="T"
extrudePram2.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"-",extrudePram2,False)

# ここから追加：四隅に直方体の柱を追加
# 板の外形から四隅座標を定義
x_min = 27.002899867463938
x_max = 220.36369998854195
y_min = -5.1232415479819116
y_max = 208.37764962333941

pillar_size = 20.0     # 柱の一辺サイズ（平面上）
pillar_height = 50.0   # 柱の高さ（Z方向、板厚10より高く設定）

# 柱用スケッチプレーン（板と同じ基準面）を新規に作成
skt_pl_pillar = part.CreateSketchPlane("スケッチ柱","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl_pillar,True)
skt_layer_col = part.CreateSketchLayer("柱", skt_pl_pillar)

def draw_rect_on_layer(sketch_plane, layer_name, x1, y1, x2, y2):
    # (x1,y1) を左下、(x2,y2) を右上とする長方形を作図
    p1 = f"{x1},{y1}"
    p2 = f"{x2},{y1}"
    p3 = f"{x2},{y2}"
    p4 = f"{x1},{y2}"
    part.CreateSketchLine(sketch_plane,"",layer_name, p1, p2, False)
    part.CreateSketchLine(sketch_plane,"",layer_name, p2, p3, False)
    part.CreateSketchLine(sketch_plane,"",layer_name, p3, p4, False)
    part.CreateSketchLine(sketch_plane,"",layer_name, p4, p1, False)

# 四隅の柱（内側に pillar_size 分オフセットした直方体基面）を作図
# 左下
draw_rect_on_layer(skt_pl_pillar, "柱", x_min, y_min, x_min+pillar_size, y_min+pillar_size)
# 右下
draw_rect_on_layer(skt_pl_pillar, "柱", x_max-pillar_size, y_min, x_max, y_min+pillar_size)
# 右上
draw_rect_on_layer(skt_pl_pillar, "柱", x_max-pillar_size, y_max-pillar_size, x_max, y_max)
# 左上
draw_rect_on_layer(skt_pl_pillar, "柱", x_min, y_max-pillar_size, x_min+pillar_size, y_max)

# 柱を押し出し（加算）してソリッドに結合
extrudePram_col = part.CreateLinearSweepParam()
extrudePram_col.Name = "柱押し出し"
extrudePram_col.AddProfile(skt_pl_pillar + ",柱")  # 柱レイヤのみを押し出し対象に
extrudePram_col.DirectionType = "N"
extrudePram_col.DirectionParameter1 = str(pillar_height)
extrudePram_col.RefByGeometricMethod = False
extrude_col = part.CreateLinearSweep(solid1, "+", extrudePram_col, False)
# 必要に応じて色付け（任意）
# part.SetElementColor(extrude_col,"180","180","180","0")