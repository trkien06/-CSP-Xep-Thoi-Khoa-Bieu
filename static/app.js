let THONG_TIN = null;
let DU_LIEU_HIEN_TAI = null;

const $ = (id) => document.getElementById(id);

function soDep(n) {
  if (n === null || n === undefined) return "-";
  return n.toLocaleString("vi-VN");
}

function giayDep(t) {
  if (t === null || t === undefined) return "-";
  return t.toFixed(4).replace(".", ",") + "s";
}

function boKey() {
  return $("chon-bo").value;
}

function thuatToanKey() {
  const chon = document.querySelector('input[name="thuat-toan"]:checked');
  return chon ? chon.value : "mrvfc";
}

function datNutCho(cho) {
  ["nut-xep-lich", "nut-so-sanh", "nut-du-lieu"].forEach((id) => { $(id).disabled = cho; });
}

function hien(id) {
  $(id).classList.remove("an");
}

function an(id) {
  $(id).classList.add("an");
}

async function taiThongTin() {
  const res = await fetch("/api/thong-tin");
  THONG_TIN = await res.json();
  const chonBo = $("chon-bo");
  chonBo.innerHTML = "";
  THONG_TIN.cac_bo.forEach((b) => {
    const op = document.createElement("option");
    op.value = b.key;
    op.textContent = b.ten;
    chonBo.appendChild(op);
  });
  const khung = $("chon-thuat-toan");
  khung.innerHTML = "";
  THONG_TIN.thuat_toan.forEach((t, i) => {
    const lb = document.createElement("label");
    const rd = document.createElement("input");
    rd.type = "radio";
    rd.name = "thuat-toan";
    rd.value = t.key;
    if (t.key === "mrvfc") rd.checked = true;
    rd.addEventListener("change", danhDauThuatToan);
    lb.appendChild(rd);
    lb.appendChild(document.createTextNode(t.ten));
    khung.appendChild(lb);
  });
  danhDauThuatToan();
  capNhatTenBo();
}

function danhDauThuatToan() {
  document.querySelectorAll("#chon-thuat-toan label").forEach((lb) => {
    const rd = lb.querySelector("input");
    lb.classList.toggle("co-chon", rd.checked);
  });
}

function capNhatTenBo() {
  const b = THONG_TIN.cac_bo.find((x) => x.key === boKey());
  $("ten-bo").textContent = b ? b.ten : "";
}

function oThongKe(giaTri, nhan) {
  return `<div class="o-thong-ke"><span class="gia-tri">${giaTri}</span><span class="nhan">${nhan}</span></div>`;
}

function veKetQua(r) {
  const tt = $("trang-thai");
  tt.classList.remove("canh-bao");
  if (r.vuot_gioi_han) {
    tt.classList.add("canh-bao");
    tt.textContent = `${r.thuat_toan_ten}: ĐÃ DUYỆT ${soDep(r.nodes)} NÚT SAU ${r.time.toFixed(1).replace(".", ",")} GIÂY MÀ CHƯA TÌM ĐƯỢC LỊCH - chương trình tự dừng ở giới hạn ${soDep(r.gioi_han_nut)} nút. Với dữ liệu lớn, hãy dùng MRV + Forward Checking hoặc CP-SAT.`;
    an("muc-thong-ke");
    an("muc-luoi");
    return;
  }
  if (!r.ok) {
    tt.classList.add("canh-bao");
    tt.textContent = `${r.thuat_toan_ten}: KHÔNG tìm được lịch thỏa mãn.`;
    an("muc-thong-ke");
    an("muc-luoi");
    return;
  }
  tt.textContent = `Kết quả: ĐÃ XẾP ĐỦ ${r.tong} BUỔI · Thuật toán: ${r.thuat_toan_ten} · Thời gian: ${giayDep(r.time)}`;
  $("cac-o-thong-ke").innerHTML =
    oThongKe(`${r.da_xep}/${r.tong}`, "Buổi đã xếp") +
    oThongKe(`${r.diem}/${r.tong}`, "Điểm mềm (buổi sáng)") +
    oThongKe(soDep(r.nodes), "Nút duyệt") +
    oThongKe(soDep(r.backtracks), "Lần quay lui") +
    oThongKe(giayDep(r.time), "Thời gian giải") +
    oThongKe(r.trang_thai_cpsat || "Hoàn thành", "Trạng thái");
  const kl = $("ket-luan-kiem-tra");
  if (r.kiem_tra.hop_le) {
    kl.innerHTML = `<div class="hop-le dat">✓ Kiểm tra độc lập: ĐẠT - 0 vi phạm ràng buộc cứng (không trùng giảng viên, không trùng phòng, phòng đủ chỗ, đúng khung giờ bận)</div>`;
  } else {
    kl.innerHTML = `<div class="hop-le loi">Kiểm tra độc lập phát hiện lỗi: ${r.kiem_tra.loi.join("; ")}</div>`;
  }
  hien("muc-thong-ke");
  veLuoi(r);
}

function veLuoi(r) {
  const bang = $("bang-lich");
  const o = {};
  THONG_TIN.slots.forEach((s) => { o[`${s.ngay}|${s.buoi}`] = r.lich[s.ma] || []; });
  let html = "<thead><tr><th></th>";
  THONG_TIN.ngay.forEach((n) => { html += `<th>${n}</th>`; });
  html += "</tr></thead><tbody>";
  THONG_TIN.buoi.forEach((buoi) => {
    html += `<tr><th class="cot-buoi">${buoi}</th>`;
    THONG_TIN.ngay.forEach((ngay) => {
      const entries = o[`${ngay}|${buoi}`];
      if (!entries.length) {
        html += `<td><span class="o-trong">—</span></td>`;
      } else {
        html += "<td>" + entries.map((e) =>
          `<div class="the-buoi"><b>${e.ma} · ${e.mon}</b><br>${e.phong} · ${e.gv} · ${e.sv} SV</div>`
        ).join("") + "</td>";
      }
    });
    html += "</tr>";
  });
  html += "</tbody>";
  bang.innerHTML = html;
  $("ghi-chu-mo-hinh").textContent = DU_LIEU_HIEN_TAI && DU_LIEU_HIEN_TAI.bo === r.bo
    ? `Mô hình CSP của bộ này: ${DU_LIEU_HIEN_TAI.tong_buoi} biến (buổi học); kích thước miền giá trị: nhỏ nhất ${DU_LIEU_HIEN_TAI.mien_min}, lớn nhất ${DU_LIEU_HIEN_TAI.mien_max}, trung bình ${String(DU_LIEU_HIEN_TAI.mien_tb).replace(".", ",")} giá trị/biến.`
    : "";
  hien("muc-luoi");
}

async function xepLich() {
  datNutCho(true);
  const tt = $("trang-thai");
  tt.classList.remove("canh-bao");
  tt.textContent = "Đang xếp lịch... (Bộ 2 với Backtracking thuần có thể mất khoảng 15 giây trước khi dừng ở giới hạn nút)";
  try {
    const res = await fetch("/api/xep-lich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bo: boKey(), thuat_toan: thuatToanKey() }),
    });
    const r = await res.json();
    if (!res.ok) {
      tt.classList.add("canh-bao");
      tt.textContent = r.loi || "Có lỗi xảy ra.";
      return;
    }
    await taiDuLieu(false);
    veKetQua(r);
  } catch (e) {
    tt.classList.add("canh-bao");
    tt.textContent = "Không gọi được máy chủ. Hãy kiểm tra lại kết nối.";
  } finally {
    datNutCho(false);
  }
}

function dongSoSanh(m) {
  if (m.loi_thu_vien) {
    return `<tr><td>${m.thuat_toan_ten}</td><td colspan="7" class="nhan-loi">${m.loi_thu_vien}</td></tr>`;
  }
  let ketQua, lopKetQua;
  if (m.vuot_gioi_han) { ketQua = "Vượt giới hạn nút"; lopKetQua = "nhan-loi"; }
  else if (m.ok) { ketQua = "Đã xếp đủ"; lopKetQua = "nhan-dat"; }
  else { ketQua = "Không có lịch"; lopKetQua = "nhan-loi"; }
  const kiemTra = m.kiem_tra.co_lich
    ? (m.kiem_tra.hop_le ? '<span class="nhan-dat">ĐẠT</span>' : '<span class="nhan-loi">LỖI</span>')
    : "-";
  return `<tr>
    <td>${m.thuat_toan_ten}</td>
    <td class="${lopKetQua}">${ketQua}</td>
    <td>${m.da_xep}/${m.tong}</td>
    <td>${m.ok ? m.diem + "/" + m.tong : "-"}</td>
    <td>${m.vuot_gioi_han ? "&gt;" + soDep(m.gioi_han_nut) : soDep(m.nodes)}</td>
    <td>${soDep(m.backtracks)}</td>
    <td>${giayDep(m.time)}</td>
    <td>${kiemTra}</td>
  </tr>`;
}

async function soSanh() {
  datNutCho(true);
  const tt = $("trang-thai");
  tt.classList.remove("canh-bao");
  tt.textContent = "Đang chạy cả 3 thuật toán để so sánh... (có thể mất khoảng 15 giây vì Backtracking thuần trên bộ lớn)";
  try {
    const res = await fetch("/api/so-sanh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bo: boKey() }),
    });
    const r = await res.json();
    if (!res.ok) {
      tt.classList.add("canh-bao");
      tt.textContent = r.loi || "Có lỗi xảy ra.";
      return;
    }
    $("tieu-de-so-sanh").textContent = `So sánh 3 thuật toán - ${r.bo_ten}`;
    $("than-so-sanh").innerHTML = r.ket_qua.map(dongSoSanh).join("");
    hien("muc-so-sanh");
    tt.textContent = "Đã so sánh xong 3 thuật toán. Xem bảng bên dưới.";
  } catch (e) {
    tt.classList.add("canh-bao");
    tt.textContent = "Không gọi được máy chủ. Hãy kiểm tra lại kết nối.";
  } finally {
    datNutCho(false);
  }
}

async function taiDuLieu(hienThi) {
  const res = await fetch(`/api/du-lieu?bo=${boKey()}`);
  const d = await res.json();
  DU_LIEU_HIEN_TAI = d;
  $("tieu-de-du-lieu").textContent = `Dữ liệu đầu vào - ${d.ten}`;
  $("tom-tat-du-lieu").textContent = `${d.so_lop} lớp học phần × ${d.buoi_moi_lop} buổi/lớp = ${d.tong_buoi} buổi cần xếp · ${d.so_giang_vien} giảng viên · ${d.so_phong} phòng học · Mỗi buổi là một biến, miền giá trị là các cặp (khung giờ, phòng) khả thi: nhỏ nhất ${d.mien_min}, lớn nhất ${d.mien_max}, trung bình ${String(d.mien_tb).replace(".", ",")} giá trị/biến.`;
  $("than-phong").innerHTML = d.phong.map((p) => `<tr><td>${p.ma}</td><td>${p.suc_chua} chỗ</td></tr>`).join("");
  $("than-giang-vien").innerHTML = d.giang_vien.map((g) =>
    `<tr><td>${g.ma}</td><td>${g.ten}</td><td>${g.ban.length ? g.ban.map((b) => `${b.nhan} (${b.ma})`).join(", ") : "Không bận"}</td></tr>`
  ).join("");
  $("than-lop").innerHTML = d.lop.map((l) =>
    `<tr><td>${l.ma}</td><td>${l.mon}</td><td>${l.sv} SV</td><td>${l.gv_ten} (${l.gv_ma})</td></tr>`
  ).join("");
  if (hienThi) hien("muc-du-lieu");
}

document.addEventListener("DOMContentLoaded", async () => {
  await taiThongTin();
  await taiDuLieu(false);
  $("chon-bo").addEventListener("change", async () => {
    capNhatTenBo();
    an("muc-thong-ke");
    an("muc-luoi");
    an("muc-so-sanh");
    $("trang-thai").classList.remove("canh-bao");
    $("trang-thai").textContent = "Chưa xếp lịch. Chọn bộ dữ liệu và thuật toán rồi bấm Xếp lịch.";
    await taiDuLieu(!$("muc-du-lieu").classList.contains("an"));
  });
  $("nut-xep-lich").addEventListener("click", xepLich);
  $("nut-so-sanh").addEventListener("click", soSanh);
  $("nut-du-lieu").addEventListener("click", () => taiDuLieu(true));
});
