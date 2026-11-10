import os

from flask import Flask, jsonify, render_template, request

import engine

app = Flask(__name__)


def nhan_cac_slot():
    ket_qua = []
    for slot in engine.SLOTS:
        ngay, buoi = engine.nhan_slot(slot)
        ket_qua.append({"ma": slot, "ngay": ngay, "buoi": buoi})
    return ket_qua


def du_lieu_json(bo_key):
    ds = engine.CAC_BO[bo_key]
    variables, info = engine.build_variables(ds)
    domains = engine.build_domains(ds, variables, info)
    kich_co = [len(domains[v]) for v in variables]
    phong = [{"ma": p, "suc_chua": c} for p, c in ds["phong"].items()]
    giang_vien = []
    for ma, gv in ds["giang_vien"].items():
        ban = []
        for slot in gv["ban"]:
            ngay, buoi = engine.nhan_slot(slot)
            ban.append({"ma": slot, "nhan": f"{ngay} - {buoi}"})
        giang_vien.append({"ma": ma, "ten": gv["ten"], "ban": ban})
    lop = []
    for l in ds["lop"]:
        lop.append({
            "ma": l["ma"],
            "mon": l["mon"],
            "sv": l["sv"],
            "gv_ma": l["gv"],
            "gv_ten": ds["giang_vien"][l["gv"]]["ten"],
        })
    return {
        "bo": bo_key,
        "ten": ds["ten"],
        "phong": phong,
        "giang_vien": giang_vien,
        "lop": lop,
        "buoi_moi_lop": ds["buoi_moi_lop"],
        "so_lop": len(ds["lop"]),
        "so_giang_vien": len(ds["giang_vien"]),
        "so_phong": len(ds["phong"]),
        "tong_buoi": len(variables),
        "mien_min": min(kich_co),
        "mien_max": max(kich_co),
        "mien_tb": round(sum(kich_co) / len(kich_co), 1),
    }


def ket_qua_json(bo_key, thuat_toan_key, r):
    ds = engine.CAC_BO[bo_key]
    loi = engine.kiem_tra(ds, r["assignment"]) if r["ok"] else []
    return {
        "bo": bo_key,
        "bo_ten": ds["ten"],
        "thuat_toan": thuat_toan_key,
        "thuat_toan_ten": engine.THUAT_TOAN[thuat_toan_key],
        "ok": r["ok"],
        "vuot_gioi_han": r["vuot_gioi_han"],
        "da_xep": len(r["assignment"]),
        "tong": r["tong"],
        "diem": r["diem"],
        "nodes": r["nodes"],
        "backtracks": r["backtracks"],
        "time": r["time"],
        "trang_thai_cpsat": r.get("trang_thai"),
        "gioi_han_nut": engine.GIOI_HAN_NUT,
        "lich": engine.bang_lich(ds, r["assignment"]) if r["ok"] else {},
        "kiem_tra": {
            "co_lich": bool(r["ok"]),
            "hop_le": bool(r["ok"]) and not loi,
            "loi": loi,
        },
    }


@app.route("/")
def trang_chu():
    return render_template("index.html")


@app.route("/api/thong-tin")
def api_thong_tin():
    return jsonify({
        "cac_bo": [{"key": k, "ten": v["ten"]} for k, v in engine.CAC_BO.items()],
        "thuat_toan": [{"key": k, "ten": v} for k, v in engine.THUAT_TOAN.items()],
        "ngay": engine.NGAY,
        "buoi": engine.BUOI,
        "slots": nhan_cac_slot(),
        "gioi_han_nut": engine.GIOI_HAN_NUT,
    })


@app.route("/api/du-lieu")
def api_du_lieu():
    bo_key = request.args.get("bo", "bo1")
    if bo_key not in engine.CAC_BO:
        return jsonify({"loi": "Bộ dữ liệu không hợp lệ"}), 400
    return jsonify(du_lieu_json(bo_key))


@app.route("/api/xep-lich", methods=["POST"])
def api_xep_lich():
    body = request.get_json(silent=True) or {}
    bo_key = body.get("bo", "bo1")
    thuat_toan_key = body.get("thuat_toan", "mrvfc")
    if bo_key not in engine.CAC_BO:
        return jsonify({"loi": "Bộ dữ liệu không hợp lệ"}), 400
    if thuat_toan_key not in engine.THUAT_TOAN:
        return jsonify({"loi": "Thuật toán không hợp lệ"}), 400
    try:
        r = engine.giai(bo_key, thuat_toan_key)
    except ImportError:
        return jsonify({"loi": "Thuật toán CP-SAT cần thư viện ortools. Cài bằng lệnh: pip install ortools"}), 500
    return jsonify(ket_qua_json(bo_key, thuat_toan_key, r))


@app.route("/api/so-sanh", methods=["POST"])
def api_so_sanh():
    body = request.get_json(silent=True) or {}
    bo_key = body.get("bo", "bo1")
    if bo_key not in engine.CAC_BO:
        return jsonify({"loi": "Bộ dữ liệu không hợp lệ"}), 400
    ds = engine.CAC_BO[bo_key]
    ket_qua = []
    for thuat_toan_key, ten in engine.THUAT_TOAN.items():
        try:
            r = engine.giai(bo_key, thuat_toan_key)
        except ImportError:
            ket_qua.append({
                "thuat_toan": thuat_toan_key,
                "thuat_toan_ten": ten,
                "loi_thu_vien": "Chưa cài ortools: pip install ortools",
            })
            continue
        muc = ket_qua_json(bo_key, thuat_toan_key, r)
        muc.pop("lich", None)
        ket_qua.append(muc)
    return jsonify({"bo": bo_key, "bo_ten": ds["ten"], "ket_qua": ket_qua})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
