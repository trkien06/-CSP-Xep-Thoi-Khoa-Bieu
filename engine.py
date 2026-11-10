import time

SLOTS = ["T2S", "T2C", "T3S", "T3C", "T4S", "T4C", "T5S", "T5C", "T6S", "T6C"]
NGAY = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"]
BUOI = ["Sáng", "Chiều"]


def nhan_slot(slot):
    ngay = NGAY[int(slot[1]) - 2]
    buoi = "Sáng" if slot[2] == "S" else "Chiều"
    return ngay, buoi


BO_1 = {
    "ten": "Bộ 1 - Chuẩn (12 lớp, 5 giảng viên, 3 phòng, 24 buổi)",
    "phong": {"P101": 50, "P102": 60, "P201": 35},
    "giang_vien": {
        "GV01": {"ten": "Thầy An", "ban": ["T2C", "T5C"]},
        "GV02": {"ten": "Cô Bình", "ban": ["T4S"]},
        "GV03": {"ten": "Cô Chi", "ban": ["T6S"]},
        "GV04": {"ten": "Thầy Dũng", "ban": ["T6C"]},
        "GV05": {"ten": "Cô Hà", "ban": ["T3C"]},
    },
    "lop": [
        {"ma": "L01", "mon": "Trí tuệ nhân tạo", "sv": 45, "gv": "GV02"},
        {"ma": "L02", "mon": "Trí tuệ nhân tạo", "sv": 38, "gv": "GV05"},
        {"ma": "L03", "mon": "Cấu trúc dữ liệu", "sv": 50, "gv": "GV01"},
        {"ma": "L04", "mon": "Cơ sở dữ liệu", "sv": 30, "gv": "GV03"},
        {"ma": "L05", "mon": "Thiết kế Web", "sv": 42, "gv": "GV03"},
        {"ma": "L06", "mon": "Mạng máy tính", "sv": 35, "gv": "GV04"},
        {"ma": "L07", "mon": "Học máy", "sv": 40, "gv": "GV02"},
        {"ma": "L08", "mon": "Toán rời rạc", "sv": 55, "gv": "GV01"},
        {"ma": "L09", "mon": "Hệ điều hành", "sv": 48, "gv": "GV04"},
        {"ma": "L10", "mon": "An toàn thông tin", "sv": 33, "gv": "GV05"},
        {"ma": "L11", "mon": "Lập trình Python", "sv": 58, "gv": "GV03"},
        {"ma": "L12", "mon": "Toán rời rạc", "sv": 44, "gv": "GV01"},
    ],
    "buoi_moi_lop": 2,
}

BO_2 = {
    "ten": "Bộ 2 - Mở rộng (16 lớp, 8 giảng viên, 5 phòng, 48 buổi)",
    "phong": {"P101": 30, "P102": 40, "P201": 50, "P202": 60, "P301": 45},
    "giang_vien": {
        "GV01": {"ten": "Thầy An", "ban": ["T2C"]},
        "GV02": {"ten": "Cô Bình", "ban": ["T4S"]},
        "GV03": {"ten": "Cô Chi", "ban": ["T6S"]},
        "GV04": {"ten": "Thầy Dũng", "ban": ["T3C"]},
        "GV05": {"ten": "Cô Hà", "ban": ["T5S"]},
        "GV06": {"ten": "Thầy Long", "ban": ["T2S"]},
        "GV07": {"ten": "Cô Mai", "ban": ["T5C"]},
        "GV08": {"ten": "Thầy Nam", "ban": ["T3S"]},
    },
    "lop": [
        {"ma": "L01", "mon": "Trí tuệ nhân tạo", "sv": 26, "gv": "GV01"},
        {"ma": "L02", "mon": "Cấu trúc dữ liệu", "sv": 33, "gv": "GV02"},
        {"ma": "L03", "mon": "Cơ sở dữ liệu", "sv": 40, "gv": "GV03"},
        {"ma": "L04", "mon": "Thiết kế Web", "sv": 47, "gv": "GV04"},
        {"ma": "L05", "mon": "Mạng máy tính", "sv": 54, "gv": "GV05"},
        {"ma": "L06", "mon": "Học máy", "sv": 26, "gv": "GV06"},
        {"ma": "L07", "mon": "Toán rời rạc", "sv": 33, "gv": "GV07"},
        {"ma": "L08", "mon": "Hệ điều hành", "sv": 40, "gv": "GV08"},
        {"ma": "L09", "mon": "An toàn thông tin", "sv": 47, "gv": "GV01"},
        {"ma": "L10", "mon": "Lập trình Python", "sv": 54, "gv": "GV02"},
        {"ma": "L11", "mon": "Kiến trúc máy tính", "sv": 26, "gv": "GV03"},
        {"ma": "L12", "mon": "Xác suất thống kê", "sv": 33, "gv": "GV04"},
        {"ma": "L13", "mon": "Trí tuệ nhân tạo", "sv": 40, "gv": "GV05"},
        {"ma": "L14", "mon": "Cấu trúc dữ liệu", "sv": 47, "gv": "GV06"},
        {"ma": "L15", "mon": "Cơ sở dữ liệu", "sv": 54, "gv": "GV07"},
        {"ma": "L16", "mon": "Thiết kế Web", "sv": 26, "gv": "GV08"},
    ],
    "buoi_moi_lop": 3,
}

CAC_BO = {"bo1": BO_1, "bo2": BO_2}

THUAT_TOAN = {
    "thuan": "Backtracking thuần",
    "mrvfc": "Backtracking + MRV + Forward Checking",
    "cpsat": "OR-Tools CP-SAT (tối ưu)",
}


def build_variables(ds):
    variables = []
    info = {}
    for lop in ds["lop"]:
        for s in range(ds["buoi_moi_lop"]):
            v = (lop["ma"], s)
            variables.append(v)
            info[v] = lop
    return variables, info


def build_domains(ds, variables, info):
    domains = {}
    for v in variables:
        lop = info[v]
        ban = set(ds["giang_vien"][lop["gv"]]["ban"])
        vals = []
        for slot in SLOTS:
            if slot in ban:
                continue
            for room, cap in ds["phong"].items():
                if cap >= lop["sv"]:
                    vals.append((slot, room))
        domains[v] = vals
    return domains


def xung_dot(v1, val1, v2, val2, info):
    slot1, room1 = val1
    slot2, room2 = val2
    if slot1 != slot2:
        return False
    if info[v1]["gv"] == info[v2]["gv"]:
        return True
    if room1 == room2:
        return True
    if v1[0] == v2[0]:
        return True
    return False


class VuotGioiHan(Exception):
    pass


class Solver:
    def __init__(self, variables, info, domains, use_mrv=True, use_fc=True, node_limit=None):
        self.variables = variables
        self.info = info
        self.domains = {v: list(d) for v, d in domains.items()}
        self.use_mrv = use_mrv
        self.use_fc = use_fc
        self.node_limit = node_limit
        self.assignment = {}
        self.nodes = 0
        self.backtracks = 0

    def chon_bien(self):
        chua_gan = [v for v in self.variables if v not in self.assignment]
        if self.use_mrv:
            return min(chua_gan, key=lambda v: len(self.domains[v]))
        return chua_gan[0]

    def nhat_quan(self, v, val):
        for u, uval in self.assignment.items():
            if xung_dot(v, val, u, uval, self.info):
                return False
        return True

    def forward_check(self, v, val):
        bi_loai = []
        for u in self.variables:
            if u in self.assignment or u == v:
                continue
            con_lai = []
            for uval in self.domains[u]:
                if xung_dot(v, val, u, uval, self.info):
                    bi_loai.append((u, uval))
                else:
                    con_lai.append(uval)
            if not con_lai:
                for uu, uv in bi_loai:
                    self.domains[uu].append(uv)
                return None
            self.domains[u] = con_lai
        return bi_loai

    def khoi_phuc(self, bi_loai):
        for u, uval in bi_loai:
            self.domains[u].append(uval)

    def backtrack(self):
        self.nodes += 1
        if self.node_limit is not None and self.nodes > self.node_limit:
            raise VuotGioiHan()
        if len(self.assignment) == len(self.variables):
            return True
        v = self.chon_bien()
        for val in list(self.domains[v]):
            if not self.nhat_quan(v, val):
                continue
            self.assignment[v] = val
            bi_loai = self.forward_check(v, val) if self.use_fc else []
            if bi_loai is not None:
                if self.backtrack():
                    return True
                self.khoi_phuc(bi_loai)
            del self.assignment[v]
        self.backtracks += 1
        return False

    def giai(self):
        t0 = time.time()
        try:
            ok = self.backtrack()
        except VuotGioiHan:
            return False, time.time() - t0
        return ok, time.time() - t0


def diem_mem(assignment):
    return sum(1 for (slot, _) in assignment.values() if slot.endswith("S"))


def kiem_tra(ds, assignment):
    variables, info = build_variables(ds)
    domains = build_domains(ds, variables, info)
    loi = []
    if len(assignment) != len(variables):
        loi.append(f"Mới xếp {len(assignment)}/{len(variables)} buổi học")
    for v in variables:
        if v in assignment and assignment[v] not in domains[v]:
            loi.append(f"{v[0]} buổi {v[1] + 1}: giá trị {assignment[v]} ngoài miền (phòng không đủ chỗ hoặc giảng viên bận)")
    vals = [(v, assignment[v]) for v in variables if v in assignment]
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if xung_dot(vals[i][0], vals[i][1], vals[j][0], vals[j][1], info):
                loi.append(f"Xung đột giữa {vals[i][0][0]} và {vals[j][0][0]} tại {vals[i][1][0]}")
    return loi


def bang_lich(ds, assignment):
    _, info = build_variables(ds)
    lich = {slot: [] for slot in SLOTS}
    for (ma, s), (slot, room) in assignment.items():
        lop = info[(ma, s)]
        lich[slot].append({
            "phong": room, "ma": ma, "mon": lop["mon"],
            "gv": ds["giang_vien"][lop["gv"]]["ten"], "sv": lop["sv"],
        })
    for slot in lich:
        lich[slot].sort(key=lambda e: e["phong"])
    return lich


GIOI_HAN_NUT = 300000


def giai_backtracking(ds, use_mrv, use_fc, node_limit=GIOI_HAN_NUT):
    variables, info = build_variables(ds)
    domains = build_domains(ds, variables, info)
    solver = Solver(variables, info, domains, use_mrv, use_fc, node_limit=node_limit)
    ok, dt = solver.giai()
    vuot = (not ok) and solver.nodes > (node_limit or 0)
    return {
        "ok": ok,
        "vuot_gioi_han": vuot,
        "assignment": solver.assignment if ok else {},
        "nodes": solver.nodes,
        "backtracks": solver.backtracks,
        "time": dt,
        "diem": diem_mem(solver.assignment) if ok else 0,
        "tong": len(variables),
    }


def giai_cpsat(ds):
    from ortools.sat.python import cp_model
    variables, info = build_variables(ds)
    domains = build_domains(ds, variables, info)
    model = cp_model.CpModel()
    x = {}
    for v in variables:
        for val in domains[v]:
            x[(v, val)] = model.NewBoolVar(f"x_{v[0]}_{v[1]}_{val[0]}_{val[1]}")
        model.Add(sum(x[(v, val)] for val in domains[v]) == 1)
    for slot in SLOTS:
        gv_vars = {}
        room_vars = {}
        for v in variables:
            for val in domains[v]:
                if val[0] != slot:
                    continue
                gv_vars.setdefault(info[v]["gv"], []).append(x[(v, val)])
                room_vars.setdefault(val[1], []).append(x[(v, val)])
        for lst in gv_vars.values():
            model.Add(sum(lst) <= 1)
        for lst in room_vars.values():
            model.Add(sum(lst) <= 1)
    for lop in ds["lop"]:
        vs = [(lop["ma"], s) for s in range(ds["buoi_moi_lop"])]
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                for slot in SLOTS:
                    a = [x[(vs[i], val)] for val in domains[vs[i]] if val[0] == slot]
                    b = [x[(vs[j], val)] for val in domains[vs[j]] if val[0] == slot]
                    if a and b:
                        model.Add(sum(a) + sum(b) <= 1)
    model.Maximize(sum(x[(v, val)] for v in variables for val in domains[v] if val[0].endswith("S")))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    solver.parameters.num_search_workers = 8
    t0 = time.time()
    status = solver.Solve(model)
    dt = time.time() - t0
    assignment = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for v in variables:
            for val in domains[v]:
                if solver.Value(x[(v, val)]) == 1:
                    assignment[v] = val
    return {
        "ok": bool(assignment),
        "vuot_gioi_han": False,
        "assignment": assignment,
        "nodes": None,
        "backtracks": None,
        "time": dt,
        "diem": diem_mem(assignment) if assignment else 0,
        "tong": len(variables),
        "trang_thai": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
    }


def giai(bo_key, thuat_toan_key):
    ds = CAC_BO[bo_key]
    if thuat_toan_key == "thuan":
        return giai_backtracking(ds, False, False)
    if thuat_toan_key == "mrvfc":
        return giai_backtracking(ds, True, True)
    if thuat_toan_key == "cpsat":
        return giai_cpsat(ds)
    raise ValueError(thuat_toan_key)


def xuat_html(ds, ket_qua, thuat_toan_ten, duong_dan):
    lich = bang_lich(ds, ket_qua["assignment"])
    o = {}
    for slot, entries in lich.items():
        ngay, buoi = nhan_slot(slot)
        o[(ngay, buoi)] = entries
    dong = []
    for buoi in BUOI:
        o_html = []
        for ngay in NGAY:
            entries = o.get((ngay, buoi), [])
            if entries:
                noi_dung = "".join(
                    f'<div class="buoi-hoc"><b>{e["ma"]}</b> · {e["mon"]}<br>{e["phong"]} · {e["gv"]}</div>'
                    for e in entries)
            else:
                noi_dung = '<span class="trong">—</span>'
            o_html.append(f"<td>{noi_dung}</td>")
        dong.append(f'<tr><th class="cot-buoi">{buoi}</th>{"".join(o_html)}</tr>')
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Thời khóa biểu - {ds['ten']}</title>
<style>
body {{ font-family: "Times New Roman", serif; margin: 32px; color: #1a1a2e; }}
h1 {{ font-size: 22px; text-align: center; margin-bottom: 4px; }}
p.thong-tin {{ text-align: center; color: #444; margin-top: 0; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #666; padding: 8px; vertical-align: top; }}
th {{ background: #dbe4f0; }}
.cot-buoi {{ width: 60px; text-align: center; }}
.buoi-hoc {{ background: #eef4fb; border: 1px solid #b9cde8; border-radius: 6px; padding: 5px 7px; margin-bottom: 5px; font-size: 14px; }}
.trong {{ color: #999; }}
</style>
</head>
<body>
<h1>THỜI KHÓA BIỂU</h1>
<p class="thong-tin">{ds['ten']} · Thuật toán: {thuat_toan_ten} · Điểm ràng buộc mềm (buổi sáng): {ket_qua['diem']}/{ket_qua['tong']} · Thời gian giải: {ket_qua['time']:.4f} giây</p>
<table>
<tr><th></th>{''.join(f'<th>{n}</th>' for n in NGAY)}</tr>
{''.join(dong)}
</table>
</body>
</html>"""
    with open(duong_dan, "w", encoding="utf-8") as f:
        f.write(html)
    return duong_dan
