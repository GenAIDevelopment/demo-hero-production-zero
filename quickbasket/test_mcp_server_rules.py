import importlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
QB = sys.argv[1]; sys.path.insert(0, QB)
def server(customer, limit=500):
    shutil.copyfile(os.path.join(QB, "quickbasket.db"), os.path.join(QB, "mcptest_work.db"))
    os.environ.update(QB_WORK_DB=os.path.join(QB, "mcptest_work.db"), QB_SESSION_CUSTOMER=customer, QB_APPROVAL_LIMIT=str(limit))
    import qb_mcp_server
    return importlib.reload(qb_mcp_server)
def show(label, out, expect):
    d = json.loads(out); ok = d.get("status") == expect
    print(("PASS" if ok else "FAIL"), label, "->", d.get("status"), "|", (d.get("rule") or d.get("compensation") or d.get("message") or d.get("max_amount") or d.get("refund_id") or "")); return ok
ok = True
s = server("C-1001")
ok &= show("Ananya views Vikram's order", s.get_order("C-1001", "QB-10311"), "not_found")
ok &= show("Ananya claims to be Vikram", s.get_order("C-1006", "QB-10311"), "not_found")
ok &= show("out-for-delivery order", s.check_refund_eligibility("C-1001", "QB-10310", "damaged"), "not_eligible")
ok &= show("already refunded", s.issue_refund("C-1001", "QB-10282", ["Basmati rice"], 649, "damaged"), "not_eligible")
ok &= show("earbuds 1249 eligibility", s.check_refund_eligibility("C-1001", "QB-10306", "changed_mind"), "eligible")
ok &= show("earbuds 1249 issue", s.issue_refund("C-1001", "QB-10306", ["Wireless earbuds"], 1249, "changed_mind"), "needs_human_approval")
ok &= show("milk changed mind", s.check_refund_eligibility("C-1001", "QB-10309", "changed_mind"), "not_eligible")
ok &= show("recent orders", s.list_recent_orders("C-1001"), "ok")
s = server("C-1003"); ok &= show("power bank 899", s.issue_refund("C-1003", "QB-10299", ["Power bank"], 899, "not_working"), "needs_human_approval")
s = server("C-1003", 5000); ok &= show("power bank 899 at limit 5000", s.issue_refund("C-1003", "QB-10299", ["Power bank"], 899, "not_working"), "refunded")
s = server("C-1004"); ok &= show("Irfan 4th refund", s.issue_refund("C-1004", "QB-10308", ["Eggs"], 92, "damaged"), "needs_human_approval")
s = server("C-1002"); ok &= show("mangoes 3 days", s.issue_refund("C-1002", "QB-10286", ["Alphonso mangoes"], 349, "spoiled"), "not_eligible")
s = server("C-1005"); ok &= show("Sneha late", s.check_refund_eligibility("C-1005", "QB-10307", "late_delivery"), "not_a_refund")
ok &= show("Sneha Rs 50 as late_delivery", s.issue_refund("C-1005", "QB-10307", ["Cold drink"], 50, "late_delivery"), "not_a_refund")
s = server("C-1038"); ok &= show("Zoya bread 200 (more than the bread cost)", s.issue_refund("C-1038", "QB-10305", ["Brown bread 400 g"], 200, "spoiled"), "not_eligible")
ok &= show("Zoya no item named", s.issue_refund("C-1038", "QB-10305", [], 100, "spoiled"), "not_eligible")
ok &= show("Zoya bread 100", s.issue_refund("C-1038", "QB-10305", ["brown bread"], 100, "spoiled"), "refunded")
ok &= show("Zoya second refund same order", s.issue_refund("C-1038", "QB-10305", ["Brown bread"], 50, "spoiled"), "not_eligible")
import sqlite3
print("refund rows written for Zoya:", sqlite3.connect(os.path.join(QB, "mcptest_work.db")).execute("select order_id, amount from refunds where order_id='QB-10305'").fetchall())
print("ALL PASS" if ok else "SOME FAILED")
